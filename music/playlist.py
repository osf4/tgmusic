from dataclasses import dataclass
from enum import Enum
from .track import Track

default_page_size = 10

class TrackNotFound(Exception):
    pass

class PageAction(str, Enum):
    next = 'next'
    prev = 'prev'

@dataclass(init = False, kw_only = True)
class Playlist:
    """
    Playlist describes current playlist
    """
    id: str

    name: str
    count: int
    offset: int
    tracks: list[Track]

    page: int
    total_pages: int

    def __init__(self, *, id:str, name: str, count: int, tracks: list[Track]):
        self.id = id
        
        self.name = name
        self.count = count
        self.offset = 0
        self.tracks = tracks
        
        self.page = 1
        self.total_pages = Playlist.__count_pages(count, default_page_size)

    def id_equals(self, id: str) -> bool:
        return self.id == id

    def get_track_by_id(self, id: str) -> Track:
        for track in self.tracks:
            if track.id == id:
                return track
        
        raise TrackNotFound

    def change_page(self, action: PageAction) -> bool:
        match action:
            case PageAction.prev:
                if self.page - 1 >= 1: # self.page can't be < 1
                    self.page -= 1
                    self.offset -= default_page_size
                    
                    return True
                
            case PageAction.next:
                if self.page + 1 <= self.total_pages: # self.page can't be > self.total_pages
                    self.page += 1
                    self.offset += default_page_size
                    
                    return True
                
        return False
    
    def __count_pages(count: int, page_size: int) -> int:
        """
        Returns how many pages you get if divide 'count' by 'page_size'.
        For example, for 'count' == 100 and 'page_size' == 10 - you get 10 pages.

        If there are any extra tracks (101, 112), it returns one additonal page (11 for 'count' == 101, 12 for 'count' == 112)
        """
        pages, extra_tracks = divmod(count, page_size)
        return pages if extra_tracks == 0 else pages + 1