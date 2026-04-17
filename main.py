from flask import Flask, render_template, request, redirect
from functionality.launcher import Launcher
from functionality.server_status import Server
import secret

playit_launcher = Launcher(
    check_cmd=["pgrep", "-f", "playit-linux-amd64"],
    start_cmd=['screen', '-S', 'ply', '-dm',
                'bash', '-c', '/home/playit/playit-linux-amd64'])



app = Flask(__name__)
server = Server(name=secret.name,ip=secret.ip,rcon_password=secret.rcon_password)

async def run_flask():
    app.run(debug=False, host="0.0.0.0",port=80)

@app.route('/', methods=['POST','GET'])
def index():
    server.update_json()
    return render_template("index.html",server=server)

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
    return redirect("/")

@app.route("/command_submitted", methods=["POST"])
def command_submitted():
    text_input = request.form.get("command")
    server.send_message(text_input)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0",port=80)