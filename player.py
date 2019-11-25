import random
import string

from poker import Pile


class BasePlayer:
    name = 'unknown'
    _cards = []

    def __init__(self, name, token=1000):
        self.name = name
        self.token = token

    def __str__(self):
        return self.name

    def get_card(self, pile: Pile):
        c = pile.get_card()
        self._cards.append(c)

    # 按照规则，第一张牌不展示
    def show_cards(self):
        for i in range(1, len(self._cards)):
            print(self._cards[i])

    def show_all_cards(self):
        for card in self._cards:
            print(card)

    def drop_cards(self):
        self._cards = []

    def add_token(self, delta_token):
        self.token += delta_token


# 电脑玩家
class BotPlayer(BasePlayer):
    _name_no = 0

    def __init__(self):
        BotPlayer._name_no += 1
        super().__init__('Bot_{}'.format(BotPlayer._name_no))
