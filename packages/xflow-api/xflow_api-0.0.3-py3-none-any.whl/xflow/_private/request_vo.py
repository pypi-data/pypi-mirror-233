from pydantic import BaseModel


class ExportComponent(BaseModel):
    PRJ_ID: str
    REG_ID: str
    CMPNT_NM: str
    CMPNT_TYPE_CD: str
    CMPNT_IN: dict[str, str]
    CMPNT_OUT: list[str]
    CMPNT_SCRIPT: str
    CMPNT_DESC: str

    class Config:
        extra = 'forbid'
