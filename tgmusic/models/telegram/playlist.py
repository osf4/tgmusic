from pydantic import BaseModel
from tgmusic.models.music.track import Track


class Playlist(BaseModel):
    query_message_id: int 

    raw_query: str

    title: str
    tracks: list[Track]

    total_count: int
    offset: int = 0

    
    def update(self, new_tracks: list[Track]):
        self.tracks = new_tracks


    def move_back(self, step: int = 10) -> bool:
        if self.offset - step < 0:
            return False
        
        self.offset -= step
        return True


    def move_next(self, step: int = 10) -> bool:
        if self.offset + step > self.total_count:
            return False

        self.offset += step
        return True
    

    def is_same_playlist(self, playlist_id: int) -> bool:
        return self.query_message_id == playlist_id