from functionality.constants import Config_Constants as CC
import os
import json

def create_json(data):
    try: 
        with open(f"data/config/{data['name']}.json", "w", encoding="utf-8") as f: json.dump(data,f,indent=4,ensure_ascii=False)
    except FileNotFoundError:
        os.makedirs("data/config")
        create_json(data=data)


def get_server_data():
    requirements = {"name":"","ip":CC.IP,"modpack":"","version":"","modpack_download":CC.MODPACK_DOWNLOAD,
                    "world_download":CC.WORLD_DOWNLOAD,"rcon_password":CC.RCON_PASSWORD,"rcon_port":CC.RCON_PORT}
    for requirement in requirements:
        if requirements[requirement] == "":
            requirements[requirement] = input(f"{requirement} | ")
        else:
            user_input = input(f"{requirement} ({requirements[requirement]})| ")
            if not user_input == "":
                requirements[requirement] = user_input
    create_json(data=requirements)

get_server_data()