import sql

### IMAGES
class images:
    def __init__(self) -> None:
        sq = sql.sql()

        self.magazine = image(sq.get("images", "name = magazine_thumbnail"))

        sq.close()

class image:
    def __init__(self, image_bytes: bytes) -> None:
        pass