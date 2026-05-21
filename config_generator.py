from functionality.constants import Config_Constants as CC
import os
import json

def create_json(data):
    try: 
        with open(f"server/{data['name']}/config.json", "w", encoding="utf-8") as f: json.dump(data,f,indent=4,ensure_ascii=False)
    except FileNotFoundError:
        os.makedirs(f"server/{data['name']}")
        create_json(data=data)
    make_folder_tree()

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

def make_folder_tree():
    folders = ["screenshots"]
    try:
        for server in os.listdir("server"):
            for folder in folders:
                if not os.path.isdir(f"server/{server}/{folder}"): 
                    os.makedirs(f"server/{server}/{folder}")
    except FileNotFoundError: os.makedirs(f"server")


user_input = input("New Project (1) | Update Folder Tree (2) | ")
match user_input:
    case "1":
        get_server_data()
    case "2":
        make_folder_tree()