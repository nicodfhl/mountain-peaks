"""
Near-to integration tests for the API that interacts with a database isolated from Prod database:
- Dedicated memory SQL database,
- Override the injection of the nominal session by using the "Session = Depends(db)" mechanism
- test all the endpoints with various tests
"""
import pytest
from typing import Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import Session

from mountain_peaks.backend.main import app
from mountain_peaks.backend.db.create import Base, get_db, get_session
from mountain_peaks.backend.app.crud_ops import add_a_peak, delete_a_peak, get_a_peak_by_id

from mountain_peaks.backend.db.models import DBPeak
from mountain_peaks.backend.app.schemas import PeakCreate

# Setup the TestClient
test_client = TestClient(app)

# Use the in-memory SQLite database option for testing a pretty small db
TEST_DATABASE_URL = "sqlite:///:memory:"
# create the test_engine app
test_engine = create_engine(
    TEST_DATABASE_URL,
    # options which will be passed directly to the DBAPI's connect method
    # => no "check_same_thread" to avoid inconsistencies while writing tests
    connect_args={
        "check_same_thread": False,
    },
    # create a connection pool instance using the connection parameters given in the URL
    # => "StaticPool" t oalways connect the same in memory db
    poolclass=StaticPool,
)


# Dependency to override the get_db dependency in the main app
def override_get_db():
    # this function will replace original get_db function (potentially linked to PROD db)
    # Construct a new session based on test_engine
    test_db = get_session(engine=test_engine)()
    try:
        yield test_db
    finally:
        test_db.close()


# overide the original get_db function with the current test function
app.dependency_overrides[get_db] = override_get_db


def setup() -> None:
    # Make sure that tables are created in the test database (no startup on event here)
    Base.create_all_tables(engine=test_engine)


def teardown() -> None:
    # Because we no longer need to keep test data, drop the tables in the test database
    Base.metadata.drop_all(bind=test_engine)


def compare_peaks(out_data, in_data, peak_id=None):
    if peak_id:
        assert "pid" in out_data
        assert out_data["pid"] == int(peak_id)
    assert out_data["name"] == in_data["name"]
    assert out_data["height"] == int(in_data["height"])
    assert out_data["latitude"] == in_data["latitude"]
    assert out_data["longitude"] == in_data["longitude"]
    return True


def test_endpoint_1_root():
    resp = test_client.get("/")
    assert resp.status_code == 200
    assert resp.json().startswith("Welcome to Mountain Peaks application")


def test_endpoint_2_add_peak():
    # Create a peak and check if the response is ok
    in_data = {
        "name": "Test Peak",
        "height": 1234,
        "latitude": 0.0,
        "longitude": 60.0,
    }
    resp_1 = test_client.post("/peaks/", json=in_data)
    assert resp_1.status_code == 200, resp_1.text
    compare_peaks(out_data=resp_1.json(), in_data=in_data)
    resp_2 = test_client.get("/peaks/")
    assert resp_2.status_code == 200, resp_2.text
    out_data = resp_2.json()
    assert len(out_data) == 1
    compare_peaks(out_data=out_data[0], in_data=in_data)
    # try to add the same peak, and check it failss
    resp_bis = test_client.post("/peaks/", json=in_data)
    assert resp_bis.status_code == 400, resp_bis.text


def test_endpoint_3_read_peak():
    in_data = {
        "name": "Test Peak 2",
        "height": 2587.0,
        "latitude": -60,
        "longitude": 189.0,
    }
    # Create a peak
    resp = test_client.post("/peaks/", json=in_data)
    assert resp.status_code == 200, resp.text
    peak_id = resp.json()["pid"]
    # and check if we can get it
    resp = test_client.get(f"/peaks/{peak_id}")
    assert resp.status_code == 200, resp.text
    compare_peaks(out_data=resp.json(), in_data=in_data, peak_id=peak_id)
    # check a none existing peak item
    ko_resp = test_client.get("/peaks/9999")
    assert ko_resp.status_code == 404, ko_resp.text
    # check a inconsisten peak item
    ko_resp = test_client.get("/peaks/NOT_A_GOOD_INFO")
    assert ko_resp.status_code == 422, ko_resp.text
    assert ko_resp.reason_phrase == 'Unprocessable Entity'


def test_endpoint_4_update_peak():
    peak_id = 1
    up_data = {
        "name": "Updated Peak 1",
        "height": 999,
        "latitude": +60,
        "longitude": -189.0,
    }
    resp = test_client.put(f"/peaks/{peak_id}", json=up_data)
    assert resp.status_code == 200, resp.text
    compare_peaks(out_data=resp.json(), in_data=up_data, peak_id=peak_id)


def test_endpoint_5_delete_peak():
    peak_id = 1
    ok_resp = test_client.get(f"/peaks/{peak_id}")
    del_resp = test_client.delete(f"/peaks/{peak_id}")
    assert del_resp.status_code == 200, del_resp.text
    compare_peaks(out_data=del_resp.json(), in_data=ok_resp.json(), peak_id=peak_id)
    # Try to get the deleted peak
    ko_resp = test_client.get(f"/peaks/{peak_id}")
    assert ko_resp.status_code == 404, ko_resp.text


@pytest.fixture
def session() -> Generator[Session, None, None]:
    # Same utility than setup and teardown but in a single method
    # 1. create the tables in the test database
    Base.create_all_tables(engine=test_engine)
    db_session = get_session(engine=test_engine)()
    # 2. create some peak items in the test db
    db_item = DBPeak(pid=123, name='Peak 123', height=1230, latitude=12.3, longitude=-123.)
    db_session.add(db_item)
    db_session.commit()

    # activate the session
    yield db_session

    # finally close the db and drop the tables of the test db
    db_session.close()
    Base.metadata.drop_all(bind=test_engine)


def test_operation_2_add_peak(session: Session) -> None:
    # Create a new peak and check if the response is ok
    peak = add_a_peak(session=session,
                      peak=PeakCreate(
                          name="Test Peak 4321",
                          height=4321,
                          latitude=-43.21,
                          longitude=4.321))
    assert peak.name == "Test Peak 4321"
    assert peak.height == 4321
    assert peak.latitude == -43.21
    assert peak.longitude == 4.321


def test_operation_5_delete_peak(session: Session) -> None:
    # Add a peak
    peak = add_a_peak(session=session,
                      peak=PeakCreate(
                          name="Test Peak 4321",
                          height=4321,
                          latitude=-43.21,
                          longitude=4.321))
    # save the pid
    peak_id = peak.pid
    # Try to get the deleted peak
    del_peak = delete_a_peak(session=session, peak_id=peak.pid)
    assert del_peak.pid == peak_id
    assert del_peak.name == "Test Peak 4321"
    assert del_peak.height == 4321
    assert del_peak.latitude == -43.21
    assert del_peak.longitude == 4.321
    # try to get the deleted peak again
    with pytest.raises(Exception):
        get_a_peak_by_id(session=session, info=peak_id)
