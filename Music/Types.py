from enum import Enum


class Provider(str, Enum):
    Spotify = 'Spotify'
    Yandex = 'Yandex Music'
    Deezer = 'Deezer'
    YouTube = 'YouTube'
    Name = 'Track Name'
    Unknown = 'Unknown'
