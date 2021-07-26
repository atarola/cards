
import asyncio
from datetime import datetime, timedelta

from cards.game import Game

#
# ConnectionPool
# Handles all of the communications between the game simulation and the world.
#

class ConnectionPool(object):

    def __init__(self):
        self.game = Game()
        self.input_queue = asyncio.Queue()
        self.connections = {}

    # get a connection for a user, creating one if needed
    def get_connection(self, userid):
        if not userid in self.connections.keys():
            self.connections[userid] = Connection()
            self.game.add_player(userid)

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
            self.game.remove_player(key)

        # setup our heartbeats
        self.game.heartbeat()

        # ping all connections left
        for connection in self.connections.values():
            await connection.queue_event({"type": "status", "data": self.game.to_dict()})

    # add the input from our data to the queue
    async def add_input(self, userid, data):
        await self.input_queue.put({"userid": userid, "event": data})

    # handle the input queue appropriately
    async def process_input(self):
        while True:
            data = await self.input_queue.get()

            # mark the user as being seen
            connection = self.get_connection(data["userid"])
            connection.last_seen = datetime.utcnow()

            # pass the event along
            self.game.handle_input(data)

#
# Connection
# a wrapper around the user's send queue with some metadata attached.
#

class Connection(object):

    def __init__(self):
        self.send_queue = asyncio.Queue()
        self.last_seen = datetime.utcnow()

    # add the event to the queue
    async def queue_event(self, event):
        await self.send_queue.put(event)
