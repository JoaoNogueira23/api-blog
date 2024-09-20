from datetime import datetime, date
from pydantic import BaseModel
from datetime import datetime

class PostSchemaOut(BaseModel):
    postId: str
    rawText: str
    publishedDate: datetime
    ingestionDate: datetime
    author: str
    userId: str
    title: str
    subTitle: str
    imgUrlPost: str

    class Config:
        orm_mode = True

