from quart import Quart, render_template, websocket


app = Quart(__name__)

#
# static file handler
#

@app.route("/")
async def hello():
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
