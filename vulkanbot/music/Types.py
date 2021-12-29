from enum import Enum


class Provider(Enum):
    """Store Enum Types of the Providers"""
    Spotify = "Spotify"
    Spotify_Playlist = "Spotify Playlist"
    YouTube = "YouTube"
    Name = 'Track Name'
    Unknown = "Unknown"


class Playlist_Types(Enum):
    Spotify_Playlist = "Spotify Playlist"
    YouTube_Playlist = "YouTube Playlist"
    Unknown = "Unknown"


class Origins(Enum):
    Default = "Default"
    Playlist = "Playlist"
