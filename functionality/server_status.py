from mcrcon import MCRcon
import json
import os
from functionality.launcher import Launcher
from functionality.constants import Paths_Constants as PC

class Server:
    def __init__(self,data):
        self.name = data["name"]
        self.ip = data["ip"]
        self.rcon_password = data["rcon_password"]
        self.rcon_port = int(data["rcon_port"])
        self.modpack = data["modpack"]
        self.version = data["version"]
        self.modpack_download = data["modpack_download"]
        self.world_download = data["world_download"]
        self.screenshots = [pic for pic in os.listdir(f"server/{self.name}/screenshots")]
        self.launcher = Launcher(
                                check_cmd=["pgrep", "-f", "@user_jvm_args.txt"],
                                start_cmd=['screen', '-S', self.name, '-dm',
                                            'bash', '-c', f'cd {PC.PROJECT_PATH}{self.name}/ && ./{PC.EXECUTABLE}'])
        self.refresh()

    def refresh(self):
        try:
            rcon = MCRcon(self.ip, self.rcon_password, self.rcon_port)
            rcon.connect()
            command_list = rcon.command("list")
            rcon.disconnect()

            SLICER_MIDDLE = command_list.rfind("of a max of")
            SLICER_END = command_list.rfind("players online")

            self.status = "Online"
            self.players_online = command_list[10:SLICER_MIDDLE-1]
            self.players_max = command_list[SLICER_MIDDLE+12:SLICER_END-1]
            self.players_list = command_list[SLICER_END+16:]
            self.chat = self.get_chat_history()
            while self.chat.count("\n") > 32:
                self.chat = self.chat[self.chat.find("\n")+1:]
            self.screenshots = [pic for pic in os.listdir(f"server/{self.name}/screenshots")]
        except Exception as e:
            print(f">>> | {e}")
            self.status = "Offline"
            self.players_online = self.players_max = 0
            self.players_list = ""
            self.chat = "No one here"

    def send_message(self,message):
        try:
            rcon = MCRcon(self.ip, self.rcon_password, self.rcon_port)
            rcon.connect()
            rcon.command(f'say {message}')
            rcon.disconnect()
        except Exception as e:
            print(f">>> | {e}")

    def get_chat_history(self):
        path = f"{PC.PROJECT_PATH}{self.name}/logs/latest.log"
        with open(path, "r") as file:
            chat_history = new_message = ""
            for line in file:
                if not line.find("[Not Secure]") == -1:
                    beginning_location = line.find("[Not Secure]")+13
                    message = f'{line.replace("[","<").replace("]",">").replace("<Rcon>","<Dashboard>")[beginning_location:]}'
                    #\n each BP (BREAKING_POINT) chars
                    BP = 52
                    if len(message) > BP:
                        for i,length in enumerate(range(0,len(message),BP)):
                            if not length > len(message)-BP: new_message += message[i*BP:i*BP+BP]+"\n"
                            else: new_message += message[i*BP:i*BP+BP]
                        chat_history += new_message
                        new_message = ""
                    else: chat_history += message
                if not line.find("joined the game") == -1:
                    beginning_location = line.find("[net.minecraft.server.MinecraftServer/]:")+41
                    join_message = f"{line[beginning_location:]}"
                    chat_history += join_message
                if not line.find("left the game") == -1:
                    beginning_location = line.find("[net.minecraft.server.MinecraftServer/]:")+41
                    join_message = f"{line[beginning_location:]}"
                    chat_history += join_message
            return chat_history

    # JSON INTERACTIONS
    def load(self):
        with open(f"server/{self.name}/config.json", "r", encoding="utf-8") as f: data = json.load(f)
        return data

    def save(self,data):
        try: 
            with open(f"server/{self.name}/config.json", "w", encoding="utf-8") as f: json.dump(data,f,indent=4,ensure_ascii=False)
        except FileNotFoundError:
            os.makedirs(f"server/{self.name}")
            self.save(data=data)

    def create_json(self):
        data = {
            "name": self.name,
            "ip": self.ip,
            "rcon_password": self.rcon_password,
            "rcon_port": self.rcon_port,
            "modpack": self.modpack,
            "version": self.version,
            "modpack_download": self.modpack_download,
            "world_download": self.world_download}
        self.save(data=data)