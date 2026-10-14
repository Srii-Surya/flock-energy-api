from pydantic import BaseModel, ConfigDict


class Meter(BaseModel):
    model_config = ConfigDict(extra="ignore")

    meterId: str
    serialNo: str | None = None
    make: str | None = None
    phaseType: str | None = None
    installStatus: str | None = None
    dtCode: str | None = None


class MeterSearchResponse(BaseModel):
    data: list[Meter]
