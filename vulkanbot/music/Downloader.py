class Downloader():
    """Download music source from Youtube with a music name"""

    def __init__(self) -> None:
        pass

    def download(self, track_name: str) -> str:
        if type(track_name) != str:
            return

    def download_many(self, track_list: list) -> list:
        if type(track_list) != list:
            return
