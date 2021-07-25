import os
import json
import uuid
import asyncio
from quart import Quart, render_template, websocket, request, make_response
from werkzeug import http

from cards.game import Game

#
# Card API
#

app = Quart(__name__)
game = None

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

    async def do_send():
        connection = game.get_connection(userid)
        while True:
            data = await connection.send_queue.get()
            await websocket.send_json(data)

    async def do_receive():
        connection = game.get_connection(userid)
        while True:
            data = await websocket.receive()
            await game.add_input(userid, json.loads(data))

    send = asyncio.create_task(do_send())
    recieve = asyncio.create_task(do_receive())

    await asyncio.gather(send, recieve)

#
# runs the app
#

@app.before_first_request
async def lifespan():
    global game

    game = Game()
    asyncio.create_task(game.process_input())
    asyncio.create_task(game.heartbeat())

#
# application entrypoint
#

if __name__ == "__main__":
    app.run()
