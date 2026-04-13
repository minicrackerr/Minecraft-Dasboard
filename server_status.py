from mcrcon import MCRcon
import json
import os

class Server:
    def __init__(self,name,ip,rcon_password,rcon_port=25575):
        self.name = name
        self.ip = ip
        self.rcon_password = rcon_password
        self.rcon_port = rcon_port
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
        except Exception as e:
            print(f">>> | {e}")
            self.status = "Offline"
            self.players_online = self.players_max = 0
            self.players_list = ""

    # JSON INTERACTIONS
    def load(self):
        with open(f"data/server/{self.name}.json", "r") as f:
            data = json.load(f)
        return data

    def save(self,data):
        try:
            with open(f"data/server/{self.name}.json", "w") as f:
                json.dump(data,f,indent=4)
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
            "players_list": self.players_list}
        self.save(data=data)