
import asyncio
from datetime import datetime, timedelta

from cards.connection import Connection

#
# Game
# Class responsable for the game implementation
#

class Game(object):

    def __init__(self):
        self.input_queue = asyncio.Queue()
        self.connections = {}

    # get a connection for a user, creating one if needed
    def get_connection(self, userid):
        if not userid in self.connections.keys():
            self.connections[userid] = Connection()

        return self.connections[userid]

    # execute the heartbeat every 200ms
    async def heartbeat(self):
        while True:
            await self.do_heartbeat()
            await asyncio.sleep(0.1)

    # send a ping to all connections, and age off old connections
    async def do_heartbeat(self):
        # get a list of connections to age off
        deadline = datetime.utcnow() - timedelta(seconds=3)
        old = [key for key, value in self.connections.items() if value.last_seen < deadline]

        # remove those keys
        for key in old:
            print(f"removing connection for user: {key}")
            del self.connections[key]

        # ping all connections left
        for connection in self.connections.values():
            await connection.queue_event({"type": "ping"})

    # add the input from our data to the queue
    async def add_input(self, userid, data):
        await self.input_queue.put({"userid": userid, "event": data})

    # handle the input queue appropriately
    async def process_input(self):
        while True:
            data = await self.input_queue.get()
            connection = self.connections[data["userid"]]
            connection.last_seen = datetime.utcnow()
            print(data)
