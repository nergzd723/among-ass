import nclib
import threading
import sys
class Interface:
    def __init__(self, server, name, port):
        self.handle = nclib.Netcat((server, int(port)), verbose=False, echo_hex=True)
        # set name
        self.name = name
        self.communicate(name)
        self.listenerthread = threading.Thread(target=self.get)
        self.listenerthread.start()
        self.getlog = ""
        self.sendlog = ""
    def communicate(self, inp):
        self.handle.send(bytes(inp+'\n', 'ascii'))
        return self.handle.recv(timeout=0.1)
    def send(self, message):
        self.handle.send(bytes(message+'\n', 'ascii'))
        self.sendlog = self.sendlog+message+"\n"
    def get(self):
        while True:
            a = self.handle.recv(timeout=0.05).decode("ascii")
            if a != "" and a is not None:
                sys.stdout.write(a)
                self.getlog = self.getlog+a

class Player:
    def __init__(self, server, name, port, shortcutfile):
        self.interface = Interface(server, name, port)
        self.name = name
        self.macros = self.loadmacros(shortcutfile)
        self.commands = {"chartpath": self.chartpath, "whosawwho" : self.whosawwho}
        self.locations = ['weapons', 'cafe', 'cafeteria', 'o2', 'navigation', 'lower engine', 'medbay', 'admin', 'storage', 'comms', 'communications', 'reactor', 'upper engine', 'electrical', 'security']
    def loadmacros(self, shortcutfile):
        o = open(shortcutfile, "r")
        r = o.readlines()
        keys = []
        values = []
        for line in r:
            i = line.split(" ")
            keys.append(i[0])
            values.append(" ".join(i[1:]))
        return dict(zip(keys, values))
    def chartpath(self):
        a = self.interface.sendlog.split("\n")
        for message in a:
            if "go" in message or "cd" in message:
                if message[3:] in self.locations:
                    sys.stdout.write(message[3:])
                    sys.stdout.write("-->")
        sys.stdout.write('\n')
    def whosawwho(self):
        a = self.interface.sendlog.split("\n")
        for message in a:
            if "see" in message and "also" in message:
                print(message)
    def send(self, message):
        if message in self.macros:
            message = self.macros.get(message)
        if message in self.commands:
            return self.commands.get(message)()
        return self.interface.send(message)
if __name__ == "__main__":
    server = input("Enter server name ")
    name = input("Enter your nickname ")

    p = Player(server, name, "1234", "macros.txt")
    while True:
        p.send(input())