from flask import Flask, render_template, request, redirect
from functionality.launcher import Launcher
from functionality.server_status import Server
import os
import json

playit_launcher = Launcher(
    check_cmd=["pgrep", "-f", "playit-linux-amd64"],
    start_cmd=['screen', '-S', 'ply', '-dm',
                'bash', '-c', '/home/playit/playit-linux-amd64'])

app = Flask(__name__)

server_list = {}

for file in os.listdir("data/server/"):
    with open(f"data/server/{file}", "r", encoding="utf-8") as f: data = json.load(f)
    server_list[data["name"]] = Server(data=data)

server = server_list["Homies"]

### MAIN-PAGE

@app.route('/', methods=['POST','GET'])
def main_page():
    return render_template("main_page.html",server_list=server_list)


@app.route('/<request>', methods=['POST','GET'])
def index(request):
    if request in server_list:
        server = server_list[request]
        server.refresh()
        return render_template("dashboard_page.html",server=server)
    if request in [server_list[x].name+"_gallery" for x in server_list]:
        server = server_list[request[:-8]]
        return render_template("dashboard_page.html",server=server)
    else:
        return "Not Found", 404

@app.route("/controls_triggered", methods=["POST"])
def controls_triggered():
    button_value = request.form.get("controls")
    if button_value == "start":
        playit_launcher.start_instance()
        server.launcher.start_instance()
    elif button_value == "stop":
        playit_launcher.stop_instance()
        server.launcher.stop_instance()
    elif button_value == "restart":
        playit_launcher.restart_instance()
        server.launcher.restart_instance()
    return redirect(f"/{server_list[server].name}")

@app.route("/command_submitted", methods=["POST"])
def command_submitted():
    text_input = request.form.get("command")
    # print(request.headers.get())
    server.send_message(text_input)
    return redirect(f"/{server_list[server].name}")

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0",port=80)