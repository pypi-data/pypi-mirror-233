#!/usr/bin/python3
import json
import socket
from typing import Dict


class BosMiner:
    def __init__(self, miner_host):
        self.miner_host = miner_host

    def call_command(self, command, parameters: Dict = None):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.miner_host, 4028))
        command = {
            "command": command,
        }
        if parameters:
            command.update(parameters)
        command = json.dumps(command) + "\n"
        command = bytes(command, "ascii")
        s.send(command)
        data = s.recv(2048)
        while True:
            page = s.recv(2048)
            if not page:
                break
            data += page
        s.close()
        response = json.loads(data.decode("ascii").rstrip("\x00"))
        del s
        return response

    def asccount(self):
        return self.call_command("asccount")

    def asc(self, N: int):
        return self.call_command("asc", {"parameter": N})

    def config(self):
        return self.call_command("config")

    def devs(self):
        return self.call_command("devs")

    def devdetails(self):
        return self.call_command("devdetails")

    def pools(self):
        return self.call_command("pools")

    def summary(self):
        return self.call_command("summary")

    def stats(self):
        return self.call_command("stats")

    def version(self):
        return self.call_command("version")

    def estats(self):
        return self.call_command("estats")

    def coin(self):
        return self.call_command("coin")

    def check(self):
        return self.call_command("check")

    def lcd(self):
        return self.call_command("lcd")

    def switchpool(self, N: int):
        return self.call_command("switchpool", {"parameter": N})

    def enablepool(self, N: int):
        return self.call_command("enablepool", {"parameter": N})

    def disablepool(self, N: int):
        return self.call_command("disablepool", {"parameter": N})

    def addpool(self, URL: str, USR: str, PASS: str):
        return self.call_command("addpool", {"parameter": f"{URL},{USR},{PASS}"})

    def removepool(self, N: int):
        return self.call_command("removepool", {"parameter": N})

    def fans(self):
        return self.call_command("fans")

    def tempctrl(self):
        return self.call_command("tempctrl")

    def temps(self):
        return self.call_command("temps")

    def tunerstatus(self):
        return self.call_command("tunerstatus")

    def pause(self):
        return self.call_command("pause")

    def resume(self):
        return self.call_command("resume")
