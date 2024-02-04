from pydantic import BaseModel

class PageData(BaseModel):
    pageUrl: str
    pageTitle: str
    pageData: str