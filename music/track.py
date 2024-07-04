from dataclasses import dataclass

@dataclass(kw_only=True)
class Track:
    id: str
    artist: str
    title: str

    def __str__(self):
        return f'{self.artist} - {self.title}'