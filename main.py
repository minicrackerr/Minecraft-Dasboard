from functionality.launcher import Launcher
from functionality.server_status import Server
from functionality.constants import Paths_Constants as PC
import os
import json
import flask

playit_launcher = Launcher(
    check_cmd=["pgrep", "-f", "playit-linux-amd64"],
    start_cmd=['screen', '-S', 'ply', '-dm',
                'bash', '-c', PC.PLAYIT_PATH])

app = flask.Flask(__name__)

server_list = {}

for file in os.listdir("data/config/"):
    with open(f"data/config/{file}", "r", encoding="utf-8") as f: data = json.load(f)
    server_list[data["name"]] = Server(data=data)

### MAIN-PAGE

@app.route('/', methods=['POST','GET'])
def main_page():
    return flask.render_template("main_page.html",server_list=server_list)


@app.route('/<request>', methods=['POST','GET'])
def index(request):
    if request in server_list:
        server = server_list[request]
        server.refresh()
        return flask.render_template("dashboard_page.html",server=server)
    if request in [server_list[x].name+"_gallery" for x in server_list]: #trigger gallery
        server = server_list[request[:-8]]
        return flask.render_template("dashboard_page.html",server=server)
    if request in [server_list[x].name+"_controls_triggered" for x in server_list]: #trigger buttons
        server = server_list[request[:-19]]
        button_value = flask.request.form.get("controls")
        if button_value == "start":
            playit_launcher.start_instance()
            server.launcher.start_instance()
        elif button_value == "stop":
            playit_launcher.stop_instance()
            server.launcher.stop_instance()
        elif button_value == "restart":
            playit_launcher.restart_instance()
            server.launcher.restart_instance()
        return flask.redirect(f"/{server.name}")
    if request in [server_list[x].name+"_command_submitted" for x in server_list]: #trigger command subbmitted
        server = server_list[request[:-18]]
        text_input = flask.request.form.get("command")
        server.send_message(text_input)
        return flask.redirect(f"/{server.name}")
    else:
        return "Not Found", 404


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0",port=80)