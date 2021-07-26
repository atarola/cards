
import copy
import itertools
from datetime import datetime, timedelta

from cards.deck import Deck, Card

#
# Game
# class responsible for the game simulation.
#

class Game(object):

    def __init__(self):
        self.actions = []
        self.players = set()
        self.tableu = None

    def heartbeat(self):
        action = self.get_action()
        action.heartbeat()

    def handle_input(self, data):
        action = self.get_action()
        action.handle_input(data)

    def get_action(self):
        # if there are no players, then there is no need to do anything
        if len(self.players) == 0:
            self.actions = []
            return BaseAction(self)

        # if we have no actions, create the new set
        if len(self.actions) == 0:
            self.create_actions()

        return self.actions[0]

    def create_actions(self):
        self.actions = [
            SetupAction(self),
            DealAction(self),
            VerifyAction(self),
            SleepAction(self)
        ]

    def pop(self):
        self.actions.pop(0)

    def add_player(self, userid):
        self.players.add(userid)

    def remove_player(self, userid):
        self.players.remove(userid)
        if self.tableu is not None:
            self.tableu.verified.add(userid)

    def to_dict(self):
        output = {
            "state": type(self.get_action()).__name__,
            "tableu": None
        }

        if self.tableu != None:
            output["tableu"] = self.tableu.to_dict()

        return output


class Tableu(object):

    def __init__(self, game):
        self.to_deal = len(game.players) * 2 + 2
        self.players = list(game.players)
        self.verified = set()
        self.winners = set()
        self.cards = [Card(None, None) for _ in range(self.to_deal)]
        self.idx = 0

    def add_card(self, card):
        if self.full():
            return

        self.cards[self.idx] = card
        self.idx = self.idx + 1

    def full(self):
        return self.idx >= self.to_deal

    def to_dict(self):
        output = {}
        cards = copy.copy(self.cards)

        # get the cards for each player
        for user in self.players:
            output[user] = self.user_to_dict(user, [cards.pop(0), cards.pop(0)])

        # get the cards for the dealer
        output["dealer"] = self.user_to_dict("dealer", cards)
        return output

    def user_to_dict(self, userid, cards):
        return {
            "cards": [c.to_dict() for c in cards],
            "verified": (userid in self.verified),
            "value": sum([c.to_value() for c in cards])
        }


class BaseAction(object):

    def __init__(self, game):
        self.game = game

    def heartbeat(self):
        pass

    def handle_input(self, data):
        pass


class SetupAction(BaseAction):

    def heartbeat(self):
        self.game.tableu = Tableu(self.game)
        self.game.pop()


class DealAction(BaseAction):

    def __init__(self, game):
        super().__init__(game)
        self.deck = Deck()
        self.ctr = 0

    def heartbeat(self):
        tableu = self.game.tableu

        # give a bit of breathing room to dealing
        self.ctr = self.ctr + 1
        if (self.ctr % 2) != 0:
            return

        card = self.deck.deal()
        tableu.add_card(card)

        if tableu.full():
            self.game.pop()


class VerifyAction(BaseAction):

    def heartbeat(self):
        if len(self.game.tableu.players) == len(self.game.tableu.verified):
            self.game.pop()

    def handle_input(self, data):
        if data['event']['type'] == "verified":
            self.game.tableu.verified.add(data['userid'])


class SleepAction(BaseAction):

    def __init__(self, game):
        super().__init__(game)
        self.start = datetime.utcnow()

    def heartbeat(self):
        if self.game.tableu != None:
            self.game.tableu = None

        if self.start < datetime.utcnow() - timedelta(seconds=1):
            self.game.pop()
