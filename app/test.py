from models.domain.artist import Artist
from models.domain.album import Album

if __name__ == "__main__":
    artist = Artist(
        external_urls={"g": "H"},
        href="Hello",
        id="Hello",
        name="Hello",
        type="Hello",
        uri="Hello",
    )
    print(artist)

    album = Album(album_type="type", artists=[artist])
