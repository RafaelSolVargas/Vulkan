from enum import Enum


class Provider(str, Enum):
    Spotify = 'Spotify'
    Deezer = 'Deezer'
    YouTube = 'YouTube'
    Name = 'Track Name'
    Unknown = 'Unknown'
