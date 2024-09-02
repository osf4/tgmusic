from pydantic import BaseModel


class TrackDetails(BaseModel):
    id: str
    
    title: str
    artist: str
    
    url: str
    thumbnail_url: str | None