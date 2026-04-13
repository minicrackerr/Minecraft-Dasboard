from flask import Flask, render_template, request, redirect
from launcher import homies_launcher,playit_launcher
from server_status import Server
import secret

minecraft_launcher = homies_launcher

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
        minecraft_launcher.start_instance()
    elif button_value == "stop":
        playit_launcher.stop_instance()
        minecraft_launcher.stop_instance()
    elif button_value == "restart":
        playit_launcher.restart_instance()
        minecraft_launcher.restart_instance()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0",port=80)