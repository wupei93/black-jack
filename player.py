import random
import string
from abc import abstractmethod

from poker import Pile, ConsoleCard, Card, ConsoleCardBack


class BasePlayer:

    def __init__(self, name, token=1000):
        self.name = 'unknown'
        self._cards = []
        self.name = name
        self.token = token

    def __str__(self):
        return self.name

    def get_card(self, pile: Pile):
        c = pile.get_card()
        self._cards.append(c)

    def show_cards(self):
        cards = []
        c = self._cards[0]
        # 按照规则，第一张牌不展示
        if self.is_bot():
            cards.append(ConsoleCardBack())
        else:
            cards.append(self._cards[0])
        for i in range(1, len(self._cards)):
            cards.append(self._cards[i])
        self._show_cards(cards)

    def show_all_cards(self):
        self._show_cards(self._cards)

    def drop_cards(self):
        self._cards = []

    def add_token(self, delta_token):
        self.token += delta_token

    @abstractmethod
    def _show_cards(self, cards):
        pass

    def is_bot(self):
        return False

    def get_point(self):
        _card = Card()
        for card in self._cards:
            _card += card
        return _card.score

    @abstractmethod
    def need_card(self):
        pass

    def is_black_jack(self):
        _card_nums = []
        for c in self._cards:
            _card_nums.append(c.num)
        return len(self._cards) == 2 \
               and ('A' == _card_nums[0] and _card_nums[1] in ['10', 'J', 'Q', 'K']) \
               or ('A' == _card_nums[1] and _card_nums[0] in ['10', 'J', 'Q', 'K'])


class ConsolePlayer(BasePlayer):

    def need_card(self):
        return input('要牌(y)') in ['y', 'Y', '']

    def _show_cards(self, cards):
        s = ''
        for i in range(6):
            for c in cards:
                s += str(c).split('\n')[i]
            s += '\n'
        print(s)


# 电脑玩家
class BotPlayer(ConsolePlayer):
    _name_no = 0

    def __init__(self):
        BotPlayer._name_no += 1
        super().__init__('Bot_{}'.format(BotPlayer._name_no))
        self.risk_appetite = random.random()

    def is_bot(self):
        return True

    def need_card(self):
        """
        1. 手牌小于15点时要牌
        2. 手牌大于18点时不要牌
        3. 15点到18点以self.risk_appetite的概率要牌
        :return:
        """
        if self.get_point() > 18:
            return False
        if self.get_point() < 15:
            return True
        return random.random() < self.risk_appetite
