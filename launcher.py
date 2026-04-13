import subprocess
from mcstatus import JavaServer
import time

server = JavaServer.lookup("localhost:25565")

class Launcher():
    def __init__(self,check_cmd,start_cmd):
        self.check_cmd = check_cmd 
        self.start_cmd = start_cmd
    
    def check_instance(self):
        print(f">>> Checking Instance {self.start_cmd[2]}")
        subprocess.check_output(self.check_cmd, text=True)

    def start_instance(self):
        try:
            self.check_instance()
        except subprocess.CalledProcessError:
            try:
                subprocess.run(["screen", "-XS", self.start_cmd[2], "quit"], check=False)
                subprocess.run(self.start_cmd, check=True)
                print(f">>> Started Instance {self.start_cmd[2]}")
            except subprocess.CalledProcessError as e:
                print(f">>> Error with Instance {self.start_cmd[2]}\n{e}")

    def stop_instance(self):
        if self.start_cmd[2] == "ply":
            subprocess.run(["screen", "-XS", self.start_cmd[2], "quit"], check=False)
        elif self.start_cmd[2] == "mc":
            subprocess.run(["screen", "-S", "mc", "-X", "stuff","stop\r"], check=True)
            time.sleep(10)
            subprocess.run(["screen", "-XS", self.start_cmd[2], "quit"], check=False)

    def restart_instance(self):
        self.stop_instance()
        time.sleep(5)
        self.start_instance()


playit_launcher = Launcher(
    check_cmd=["pgrep", "-f", "playit-linux-amd64"],
    start_cmd=['screen', '-S', 'ply', '-dm',
                'bash', '-c', '/home/playit/playit-linux-amd64'])

homies_launcher = Launcher(
    check_cmd=["pgrep", "-f", "@user_jvm_args.txt"],
    start_cmd=['screen', '-S', 'homies', '-dm',
                'bash', '-c', 'cd /home/homies/ && ./run.sh'])

stoneblock_launcher = Launcher(
    check_cmd=["pgrep", "-f", "@user_jvm_args.txt"],
    start_cmd=['screen', '-S', 'stoneblock', '-dm',
                'bash', '-c', 'cd /home/stoneblock-4-8.1/ && ./run.sh'])