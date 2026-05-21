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

for server in os.listdir("server"):
    with open(f"server/{server}/config.json", "r", encoding="utf-8") as f: data = json.load(f)
    server_list[data["name"]] = Server(data=data)

### MAIN-PAGE

@app.route('/', methods=['POST','GET'])
def main_page():
    return flask.render_template("main_page.html",server_list=server_list)

@app.route('/server/<server_name>')
def server_dashboard(server_name):
    if server_name not in server_list: flask.abort(404)
    server = server_list[server_name]
    server.refresh()
    return flask.render_template("dashboard_page.html",server=server)

@app.route('/server/<server_name>/gallery')
def server_gallery(server_name):
    if server_name not in server_list: flask.abort(404)
    server = server_list[server_name]
    server.refresh()
    return flask.render_template("gallery_page.html",server=server)

@app.route('/server/<server_name>/statistics')
def server_statistics(server_name):
    if server_name not in server_list: flask.abort(404)
    server = server_list[server_name]
    server.refresh()
    return flask.render_template("gallery_page.html",server=server)

@app.route('/server/<server_name>/controlls/<value>', methods=['POST','GET'])
def server_controlls(server_name, value):
    if server_name not in server_list: flask.abort(404)
    server = server_list[server_name]
    if value == "start":
        playit_launcher.start_instance()
        server.launcher.start_instance()
    elif value == "stop":
        playit_launcher.stop_instance()
        server.launcher.stop_instance()
    elif value == "restart":
        playit_launcher.restart_instance()
        server.launcher.restart_instance()
    elif value == "message":
        text_input = flask.request.form.get("message")
        server.send_message(text_input)
    return flask.redirect(f"/server/{server_name}")

### FILE ACCESS

@app.route('/server/<server_name>/modpack_download')
def return_modpack_download(server_name):
    modpack_path = f"server/{server_list[server_name].name}/"
    return flask.send_from_directory(modpack_path, "modpack_download.zip")

@app.route('/server/<server_name>/world_download')
def return_world_download(server_name):
    world_path = f"server/{server_list[server_name].name}/"
    return flask.send_from_directory(world_path, "world_download.zip")

@app.route('/server/<server_name>/screenshots/<filename>')
def return_screenshot(server_name, filename):
    screenshots_path = f"server/{server_list[server_name].name}/screenshots"
    return flask.send_from_directory(screenshots_path, filename)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0",port=80)