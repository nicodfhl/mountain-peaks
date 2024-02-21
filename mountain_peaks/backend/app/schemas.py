from pydantic import BaseModel, Field


class PeakAttr(BaseModel):
    # at least one of these attributes have to be given
    name: str = Field(description="name of the peak")
    height: int = Field(gt=0, description="height of the peak")

    class Config:
        from_attributes = True


class Coords(BaseModel):
    latitude: float = Field(..., ge=-90.0, le=+90.0, description="latitude coord")
    longitude: float = Field(..., ge=-180.0, le=+180.0, description="longitude coord")


class Peak(BaseModel):
    pid: int = Field(..., gt=0, description="ID number of the peak, autoincremented")
    name: str = Field(..., description="name of the peak")
    height: int = Field(..., gt=0, description="height of the peak")
    latitude: float = Field(..., description="latitude coordinate of the peak")
    longitude: float = Field(..., description="longitude coordinate of the peak")

    class Config:
        from_attributes = True


class PeakCreate(BaseModel):
    name: str = Field(..., description="name of the peak")
    height: int = Field(..., gt=0, description="height of the peak")
    latitude: float = Field(..., description="latitude coordinate of the peak")
    longitude: float = Field(..., description="longitude coordinate of the peak")

    class Config:
        from_attributes = True


class PeakUpdate(BaseModel):
    # at least one of these attributes have to be given
    name: str = Field(description="name of the peak")
    height: int = Field(gt=0, description="height of the peak")
    latitude: float = Field(description="latitude coordinate of the peak")
    longitude: float = Field(description="longitude coordinate of the peak")

    class Config:
        from_attributes = True


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
