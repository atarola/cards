import os
from quart import Quart, render_template, websocket

app = Quart(__name__)

#
# root url
#

@app.route("/")
async def root():
    return await render_template("index.html")

#
# websocket handler
#

@app.websocket("/ws")
async def ws():
    while True:
        await websocket.send("hello")
        await websocket.send_json({"hello": "world"})

#
# application entrypoint
#

if __name__ == "__main__":
    app.run()
