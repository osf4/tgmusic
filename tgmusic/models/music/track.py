from pydantic import BaseModel


class Track(BaseModel):
    id: str

    title: str
    artist: str


    def __str__(self):
        return f'{self.artist} - {self.title}'