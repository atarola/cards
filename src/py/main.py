import asyncio
import json
import os
import uuid
from quart import Quart, render_template, websocket, request, make_response
from werkzeug import http

from cards.connection_pool import ConnectionPool

#
# Card API
#

app = Quart(__name__)
connections = None

#
# root url
#

@app.route("/")
async def root():
    # make sure an id cookie exists, this will track the user throughout
    userid = request.cookies.get('userid')
    if userid is None:
        userid = str(uuid.uuid4())

    # setup and pass out the response
    resp = await make_response(await render_template('index.html'))
    resp.set_cookie('userid', userid)
    return resp

#
# websocket handler
#

@app.websocket("/ws")
async def ws():
    # get the userid for this connection from the cookies
    cookies = http.parse_cookie(websocket.headers["cookie"])
    userid = cookies.get("userid")

    # async process to handle sending to the client via the websocket
    async def do_send():
        connection = connections.get_connection(userid)
        while True:
            data = await connection.send_queue.get()
            await websocket.send_json(data)

    # async process to handle data coming in from the websocket
    async def do_receive():
        while True:
            data = await websocket.receive()
            await connections.add_input(userid, json.loads(data))

    # run both the send and recieve channel
    send = asyncio.create_task(do_send())
    recieve = asyncio.create_task(do_receive())
    await asyncio.gather(send, recieve)

#
# runs the app
#

@app.before_first_request
async def lifespan():
    global connections

    connections = ConnectionPool()
    asyncio.create_task(connections.process_input())
    asyncio.create_task(connections.heartbeat())

#
# application entrypoint
#

if __name__ == "__main__":
    app.run()
