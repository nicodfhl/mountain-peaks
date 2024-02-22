from typing import Optional
from pydantic import BaseModel, Field, model_validator


class Peak(BaseModel):
    pid: int = Field(gt=0, description="ID number of the peak, autoincremented")
    name: str = Field(description="name of the peak")
    height: int = Field(gt=0, description="height of the peak")
    latitude: float = Field(description="latitude coordinate of the peak")
    longitude: float = Field(description="longitude coordinate of the peak")

    class Config:
        from_attributes = True


class PeakCreate(BaseModel):
    name: str = Field(description="name of the peak")
    height: int = Field(gt=0, description="height of the peak")
    latitude: float = Field(description="latitude coordinate of the peak")
    longitude: float = Field(description="longitude coordinate of the peak")

    class Config:
        from_attributes = True


class PeakUpdate(BaseModel):
    # at least one of these attributes have to be given
    name: Optional[str] = Field(None, omit_default=True, description="name of the peak")
    height: Optional[int] = Field(None, omit_default=True, gt=0, description="height of the peak")
    latitude: Optional[float] = Field(None, omit_default=True, description="latitude coordinate of the peak")
    longitude: Optional[float] = Field(None, omit_default=True, description="longitude coordinate of the peak")

    class Config:
        from_attributes = True


class PeakAttr(BaseModel):
    # at least one of these attributes have to be given
    name: Optional[str] = Field(None, omit_default=True, description="name of the peak")
    height: Optional[int] = Field(None, omit_default=True, gt=0, description="height of the peak")

    class Config:
        from_attributes = True


class Coords(BaseModel):
    latitude: float = Field(ge=-90.0, le=+90.0, description="latitude coord")
    longitude: float = Field(ge=-180.0, le=+180.0, description="longitude coord")


class BBox(BaseModel):
    """Bounding Box system, in degrees
           ___4.top__<
           |           |
    1.left v           | 3.right
           |_2.bottom__^
    """

    latitude_min: float = Field(
        ...,
        ge=-90.0,
        lt=+90.0,
        description="left or min horizontal coordinate, degrees unit",
    )
    longitude_min: float = Field(
        ...,
        ge=-180.0,
        lt=+180.0,
        description="bottom or min vertical coordinate, degrees unit",
    )
    latitude_max: float = Field(
        ...,
        gt=-90.0,
        le=+90.0,
        description="right or max horizontal coordinate, degrees unit",
    )
    longitude_max: float = Field(
        ...,
        gt=-180.0,
        le=+180.0,
        description="top or max vertical coordinate, degrees unit",
    )

    class Config:
        from_attributes = True

    @model_validator(mode="after")
    def check_min_lower_than_max(self) -> "BBox":
        if self.latitude_max < self.latitude_min:
            raise ValueError("latitude_max shall be greater than latitude_min")
        if self.longitude_max < self.longitude_min:
            raise ValueError("longitude_max shall be greater than longitude_min")
        return self
