## Cards

A simple multiplayer card game.

### Running the Game

The game is packaged as a docker container, and can be simply run in docker:

    git clone git@github.com:atarola/cards.git
    cd cards
    git checkout card_game
    docker build -t cards:latest .
    docker run --rm -p 5000:5000 cards:latest

Once started, point your browser to http://localhost:5000
