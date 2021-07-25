import asyncio
from datetime import datetime

#
# Connection
# A state machine representing a user.
#

class Connection(object):

    def __init__(self):
        self.send_queue = asyncio.Queue()
        self.last_seen = datetime.utcnow()

    # add the event to the queue
    async def queue_event(self, event):
        await self.send_queue.put(event)
