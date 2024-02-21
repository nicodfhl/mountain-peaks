from os import environ
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from .db.create import Base, get_db
from .app.crud_ops import (
    get_all_peaks,
    get_a_peak_by_id,
    find_peaks_into_bbox,
    find_peaks_by_attr,
    check_peak_exists,
    add_a_peak,
    update_a_peak,
    delete_a_peak,
    error_message,
    PeakNotFoundException,
    BadFormatEntryException
)
from .app.schemas import (
    Peak as PeakORM,
    PeakCreate as PeakCreateORM,
    PeakUpdate as PeakUpdateORM,
    PeakAttr as PeakAttrORM,
    BBox as BBoxORM
)

app = FastAPI()


@app.get("/")
def root():
    return "Welcome to Mountain Peaks application v0.2"


@app.on_event("startup")
async def startup():
    # First of all, set a specific env var to make sure the original db
    # will be used only here, and not for testing
    environ["AUTHORIZE_PROD_DB_TABLES_CREATION"] = "YES"
    Base.create_all_tables()


@app.get("/peaks", response_model=List[PeakORM])
def get_all_mountain_peaks(db: Session = Depends(get_db)) -> List[PeakORM]:
    # "db: Session = Depends(get_db)" is the dependency injection mechanism proposed by FastAPI
    # to inject the session into each endpoint instead of being created each time
    # It will allow to test endpoints by using another db than the "PROD" db
    return get_all_peaks(session=db)


@app.get("/peaks/{peak_id}")
def get_a_mountain_peak_by_id(peak_id: int, db: Session = Depends(get_db)) -> PeakORM:
    try:
        return get_a_peak_by_id(session=db, pid=peak_id)
    except PeakNotFoundException:
        raise HTTPException(
            404,
            detail=error_message(f"No peak found with the id: {peak_id}"),
        )


@app.post("/peaks", response_model=PeakORM)
def add_a_mountain_peak(peak: PeakCreateORM, db: Session = Depends(get_db)) -> PeakORM:
    if peak_in_db := check_peak_exists(session=db, peak_data=peak):
        raise HTTPException(
            400,
            detail=error_message(f"This peak info already exists: {peak_in_db.pid}"),
        )
    else:
        return add_a_peak(db, peak)


@app.put("/peaks/{peak_id}", response_model=PeakORM)
def update_a_mountain_peak(
    peak_id: int, peak_data: PeakUpdateORM, db: Session = Depends(get_db)
) -> PeakORM:
    try:
        return update_a_peak(session=db, peak_id=peak_id, peak_data=peak_data)
    except PeakNotFoundException:
        raise HTTPException(
            404,
            detail=error_message(f"No peak found with the id: {peak_id}"),
        )


@app.delete("/peaks/{peak_id}")
def delete_a_mountain_peak(peak_id: int, db: Session = Depends(get_db)) -> PeakORM:
    try:
        peak_to_del = delete_a_peak(session=db, peak_id=peak_id)
        return peak_to_del
    except PeakNotFoundException:
        raise HTTPException(
            404,
            detail=error_message(f"No peak found with the id: {peak_id}"),
        )


@app.post("/get_peaks_from_attr", response_model=PeakAttrORM)
def get_mountain_peak_by_attribute(from_attr: PeakAttrORM, db: Session = Depends(get_db)) -> List[PeakORM]:
    try:
        return find_peaks_by_attr(session=db, attr=from_attr)
    except PeakNotFoundException:
        raise HTTPException(
            404,
            detail=error_message(f"No peak found with the attribute: {from_attr}"),
        )


@app.post("/get_peaks_inside_bbox", response_model=BBoxORM)
def get_mountain_peaks_by_bbox(inside_bbox: BBoxORM, db: Session = Depends(get_db)) -> List[PeakORM]:
    try:
        return find_peaks_into_bbox(session=db, bbox=inside_bbox)
    except PeakNotFoundException:
        raise HTTPException(
            404,
            detail=error_message(f"No peak found in the bbox: {inside_bbox}"),
        )
    except BadFormatEntryException:
        entry_ex = '{"name": "Everest"} or {"height": 4808}'
        raise HTTPException(
            422,
            detail=error_message(f'Wrong entry bad format. {entry_ex} was expected'),
        )
