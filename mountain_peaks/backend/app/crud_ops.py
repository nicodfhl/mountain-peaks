from typing import List

from sqlalchemy import select, and_, delete
from sqlalchemy.orm import Session

from ..db.models import DBPeak
from .schemas import (
    BBox as BBoxORM,
    Peak as PeakORM,
    PeakCreate as PeakCreateORM,
    PeakUpdate as PeakUpdateORM,
    PeakAttr as PeakAttrORM,
)


def get_all_peaks(session: Session) -> List[DBPeak]:
    return session.execute(select(DBPeak)).scalars().all()


def get_a_peak_by_id(session: Session, pid: int) -> DBPeak:
    # peak's id given
    select_peaks = select(DBPeak).where(DBPeak.pid == pid)
    peak_item = session.execute(select_peaks).scalar_one_or_none()
    if peak_item is None:
        raise PeakNotFoundException
    return peak_item


def find_peaks_into_bbox(session: Session, bbox: BBoxORM) -> List[DBPeak]:
    # left-bottom-right-top given
    select_peaks = select(DBPeak).where(and_(bbox.latitude_min <= DBPeak.latitude,
                                             DBPeak.latitude <= bbox.latitude_max,
                                             bbox.longitude_min <= DBPeak.longitude,
                                             DBPeak.longitude <= bbox.longitude_max))
    return session.execute(select_peaks).scalars().all()


def find_peaks_by_attr(session: Session, attr: PeakAttrORM) -> List[DBPeak]:
    attr_d = attr.model_dump()
    if len(attr_d) == 0:
        raise BadFormatEntryException
    if p_name := attr_d.get("name"):
        # peak's name given
        select_peaks = select(DBPeak).where(DBPeak.name == p_name)
        # no peaks should have the same name
        req_by_name = session.execute(select_peaks).scalar_one_or_none()
        peak_items = [req_by_name] if req_by_name is not None else []
    else:
        # peak's height given,
        # find it with a tolerance of 1 meter
        p_height = float(attr_d["height"])
        select_peaks = select(DBPeak).where(
            and_(
                p_height + 1.0 >= DBPeak.height,
                p_height - 1.0 <= DBPeak.height,
            )
        )
        # some peaks can have the same height
        peak_items = session.execute(select_peaks).scalars().all()
    if len(peak_items) == 0:
        raise PeakNotFoundException
    return peak_items


def check_peak_exists(session: Session, peak_data: PeakCreateORM) -> None:
    # check if a peak has the same name in db
    # if same name, raise an exception
    attr_d = {}
    for k, v in peak_data.model_dump().items():
        if k in ["name", "height"]:
            attr_d[k] = v
    try:
        return find_peaks_by_attr(session=session, attr=PeakAttrORM(**attr_d))[0]
    except PeakNotFoundException:
        # the peak elment does not exist yet
        return False


def add_a_peak(session: Session, peak: PeakCreateORM) -> PeakORM:
    db_peak = DBPeak(**peak.model_dump())
    # peak_model = DBPeak.model_validate(peak)  # AVEC SQLModel
    session.add(db_peak)
    session.commit()
    session.refresh(db_peak)
    return PeakORM(**db_peak.__dict__)


def update_a_peak(session: Session, peak_id: int, peak_data: PeakUpdateORM) -> PeakORM:
    peak_item = get_a_peak_by_id(session=session, pid=peak_id)
    # .model_dump() returns a dictionary of the model's fields and values
    for k, v in peak_data.model_dump().items():
        if v is not None:
            setattr(peak_item, k, v)
    session.commit()
    session.refresh(peak_item)
    return PeakORM(**peak_item.__dict__)


def delete_a_peak(session: Session, peak_id: int) -> PeakORM:
    peak_item = get_a_peak_by_id(session=session, pid=peak_id)
    session.execute(delete(DBPeak).where(DBPeak.pid == peak_id))
    session.commit()
    return PeakORM(**peak_item.__dict__)


def error_message(message):
    return {"error": message}


class PeakNotFoundException(Exception):
    pass


class BadFormatEntryException(Exception):
    pass
