from pydantic import BaseModel
from .playlist import Playlist


class UserState(BaseModel):
    last_playlist: Playlist