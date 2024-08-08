from sql import sql
import obj

### IMAGES
class images:
    def __init__(self) -> None:
        sq = sql()

        self.side_panel = obj.image(sq.get("images", "name = 'side_panel'"))
        self.upload_button = obj.button(up = sq.get("images", "name = 'upload_up'"), down = sq.get("images", "name = 'upload_down'"))

        sq.close()