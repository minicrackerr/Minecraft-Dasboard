from mcrcon import MCRcon
import json
import os
from functionality.launcher import Launcher
from functionality.constants import PROJECT_PATH, EXECUTABLE
import time

class Server:
    def __init__(self,name,ip,rcon_password,rcon_port=25575):
        self.name = name
        self.ip = ip
        self.rcon_password = rcon_password
        self.rcon_port = rcon_port
        self.launcher = Launcher(
                                check_cmd=["pgrep", "-f", "@user_jvm_args.txt"],
                                start_cmd=['screen', '-S', self.name, '-dm',
                                            'bash', '-c', f'cd {PROJECT_PATH}{self.name}/ && ./{EXECUTABLE}'])
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
            log_message = rcon.command(f'tellraw @a {{"text":"<Dashboard> {message}"}}')
            rcon.disconnect()
            print(log_message)
            #with open(f"{PROJECT_PATH}{self.name}/logs/latest.log", "a") as f:
            #    f.write(f'{time.strftime("[%H:%M]", time.localtime())} {log_message} \n')
        except Exception as e:
            print(f">>> | {e}")

    def get_chat_history(self):
        path = f"{PROJECT_PATH}{self.name}/logs/latest.log"
        with open(path, "r") as file:
            chat_history = new_message = ""
        for line in file:
            if not line.find("[Not Secure]") == -1:
                message = f'[{line[12:17]}] {line.replace("[Server thread/INFO] [net.minecraft.server.MinecraftServer/]: [Not Secure]", "").replace("[","<").replace("]",">")[27:]}'
                #\n each 50 chars
                BP = BREAKING_POINT = 52
                if len(message) > BP:
                    for i,length in enumerate(range(0,len(message),BP)):
                        if not length > len(message)-BP: new_message += message[i*BP:i*BP+BP]+"\n"
                        else: new_message += message[i*BP:i*BP+BP]
                    chat_history += new_message
                    new_message = ""
                else: chat_history += message
            if not line.find("joined the game") == -1:
                join_message = f"[{line[12:17]}] {line[88:]}"
                chat_history += join_message
            if not line.find("<Dashboard>") == -1:
                chat_history += line
            return chat_history

    # JSON INTERACTIONS
    def load(self):
        with open(f"data/server/{self.name}.json", "r") as f: data = json.load(f)
        return data

    def save(self,data):
        try: 
            with open(f"data/server/{self.name}.json", "w") as f: json.dump(data,f,indent=4)
        except FileNotFoundError:
            os.makedirs("data/server")
            self.save(data=data)

    def update_json(self):
        self.refresh()
        data = {
            "name": self.name,
            "ip": self.ip,
            "rcon_password": self.rcon_password,
            "rcon_port": self.rcon_port,
            "status": self.status,
            "players_online": self.players_online,
            "players_max": self.players_max,
            "players_list": self.players_list,
            "chat": self.chat}
        self.save(data=data)
