from imports import *
log = setup("SPECIALTIES")

# Local imports
import obj

class AgentHash:
    def __init__(
            self,
            name: str,
            agent_hash: str,
            file_location: str) -> None:
        self.name = name
        self.hash = agent_hash
        self.location = file_location

class Specialties:
    class boxArt():
        def __init__(self, canvas: Image.Image, canvas_data: obj.Canvas, save_location: str) -> None:
            self.__canvas = canvas
            self.__canvas_data = canvas_data

            self.starting = True
            self.ending = True
            self.converting = False
            self.ini = False

        def start(self):
            for image in self.__canvas_data.images:
                # Placing the side cover (Just the same image moved over slightly.)
                res_image = image.image.resize((image.width, image.height), Image.Resampling.LANCZOS)
                self.__canvas.paste(res_image, (image.x + 35, image.y))

                # Placing the bottom of boxes
                drawing = ImageDraw.Draw(self.__canvas)
                box_coords = [image.x, image.y + image.height, image.x + image.width + 35, image.y + image.height + 27] # (x0, y0, x1, y1)

                # Getting most common colour
                res_image.thumbnail((200, 200))
                common_col_image = res_image.convert("RGB")

                pixels = list(common_col_image.getdata())
                # Filter out pure black and pure white pixels
                filtered_pixels = [pixel for pixel in pixels if pixel != (0, 0, 0) and pixel != (255, 255, 255)]

                pixel_count = Counter(filtered_pixels)

                most_common_rgb = pixel_count.most_common(1)[0][0]
                print(most_common_rgb)

                drawing.rectangle(box_coords, fill = most_common_rgb)
            
            return self.__canvas

        def end(self):
            box_notches = Image.open("data\\modules\\boxArt\\additional\\notches.png")
            box_notches = box_notches.convert("RGBA")
            self.__canvas.paste(box_notches, (0, 0), box_notches)

            return self.__canvas

    class agentIcons():
        def __init__(self,
                     canvas: Image.Image,
                     canvas_data: obj.Canvas,
                     save_location: str,
                     module_name: str) -> None:
            self.__canvas = canvas
            self.__canvas_data = canvas_data
            self.__save_location = save_location
            self.__module_name = module_name
            
            self.starting = False
            self.ending = False
            self.converting = True
            self.ini = True

            self.icons = Icons(
                self.__canvas,
                self.__canvas_data,
                self.__save_location,
                self.__module_name
            )

        def conversion(self) -> list[AgentHash]:
            return self.icons.conversion()
        
        def INI(self,
                agents: list[AgentHash],
                mod_name: str):

            return self.icons.INI(agents, mod_name)

    class battleIcons():
        def __init__(self,
                     canvas: Image.Image,
                     canvas_data: obj.Canvas,
                     save_location: str,
                     module_name: str) -> None:
            self.__canvas = canvas
            self.__canvas_data = canvas_data
            self.__save_location = save_location
            self.__module_name = module_name
            
            self.starting = False
            self.ending = False
            self.converting = True
            self.ini = True

            self.icons = Icons(
                self.__canvas,
                self.__canvas_data,
                self.__save_location,
                self.__module_name
            )

        def conversion(self) -> list[AgentHash]:
            return self.icons.conversion()
        
        def INI(self,
                agents: list[AgentHash],
                mod_name: str):

            return self.icons.INI(agents, mod_name)
    
    class chainIcons():
        def __init__(self,
                     canvas: Image.Image,
                     canvas_data: obj.Canvas,
                     save_location: str,
                     module_name: str) -> None:
            self.__canvas = canvas
            self.__canvas_data = canvas_data
            self.__save_location = save_location
            self.__module_name = module_name
            
            self.starting = False
            self.ending = False
            self.converting = True
            self.ini = True

            self.icons = Icons(
                self.__canvas,
                self.__canvas_data,
                self.__save_location,
                self.__module_name
            )

        def conversion(self) -> list[AgentHash]:
            return self.icons.conversion()
        
        def INI(self,
                agents: list[AgentHash],
                mod_name: str):

            return self.icons.INI(agents, mod_name)

class Icons:
    def __init__(self,
                 canvas: Image.Image,
                 canvas_data: obj.Canvas,
                 save_location: str,
                 module_name: str) -> None:
        self.__canvas = canvas
        self.__canvas_data = canvas_data
        self.__save_location = save_location
        self.__module_name = module_name

        self.data_path = f"data\\modules\\{self.__module_name}\\additional"
    
    def conversion(self) -> list[AgentHash]:
        # Getting hashes
        agents = []
        with open(f"{self.data_path}\\hashes.json") as file:
            hash_dict = json.load(file)

        # Applying the image mask
        mask = Image.open(f"{self.data_path}\\clipping_mask.png").convert("L")

        self.__canvas = Image.composite(self.__canvas, Image.new("RGBA", self.__canvas.size), mask)

        for image in self.__canvas_data.images:
            crop_area = (
                image.x,
                image.y,
                image.x + image.width,
                image.y + image.height
            )

            cropped_image = self.__canvas.crop(crop_area)

            cropped_image = ImageOps.flip(cropped_image)
            cropped_image = cropped_image.convert("RGBA")

            file_location = f"{self.__save_location}\\{image.name}.png"

            agents.append(AgentHash(
                name = image.name,
                agent_hash = hash_dict[image.name],
                file_location = file_location
            ))

            cropped_image.save(file_location)

        return agents

    def INI(self,
            agents: list[AgentHash],
            mod_name: str):

        ini = ""
        for agent in agents:
            ini += (
                f"; {agent.name}\n"
                f"[TextureOverride{agent.name}]\n"
                f"hash = {agent.hash}\n"
                f"this = Resource{agent.name}\n"
                f"[Resource{agent.name}]\n"
                f"filename = {agent.name}.png\n\n"
            )
        
        ini += (
            "; Mod Generated By N4GR\n"
            "; https://github.com/Vamptek\n"
            "; https://github.com/Vamptek/ZZZ-Mod-Generator"
        )

        with open(f"{self.__save_location}\\{mod_name}.ini", "w+") as file:
            file.writelines(ini)
        
        return ini