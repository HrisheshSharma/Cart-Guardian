from pydantic import BaseModel

class Report(BaseModel):
    websiteURL: str
    patternType: str = None
    status: str
    pattern: str = None