from abc import abstractmethod, ABC

from black_jack_utils import message
from player import BasePlayer, BotPlayer, ConsolePlayer
from poker import Pile, ConsolePile


class Game:
    __slots__ = ['_pile']
    _players = []
    # 庄家位置
    _banker_index = 0

    @abstractmethod
    def start_game(self):
        """
        游戏开始，由基类实现控制逻辑
        :return:
        """
        pass

    @abstractmethod
    def round_begin(self):
        """
        新一轮开始
        :return:
        """
        pass

    @abstractmethod
    def round_stop(self):
        """
        一轮游戏结束， 需进行结算并踢出输光筹码的玩家
        :return:
        """
        pass

    def add_player(self, player: BasePlayer):
        self._players.append(player)
        self.add_player_tips(player)

    @abstractmethod
    def add_player_tips(self, player):
        pass

    def get_winner(self):
        winner = self._players[0]
        for player in self._players:
            if winner.get_point() > 21 or winner.get_point() <= player.get_point() <= 21:
                # 点数同样的情况下black jack最大，其次是庄家
                if winner.get_point() == player.get_point() \
                        and (winner.is_black_jack()
                             or (self._banker_index == self._players.index(winner)
                                 and not player.is_black_jack())):
                    continue
                winner = player
        return winner

class ConsoleGame(Game, ABC):
    _pile = ConsolePile()

    def add_player_tips(self, player):
        print('{}加入了游戏！'.format(player))

    def show_result(self):
        for player in self._players:
            print('''
             ___________________________________________
            |       name                 |      token   |
            ++++++++++++++++++++++++++++++++++++++++++++
            |       {}           |     {:4d}         |
            |____________________________|______________|
            '''.format(player.name.ljust(8, ' '), player.token))

    def start_game(self):
        player_name = ''
        while not 0 < len(player_name) <= 8:
            player_name = input('请输入您的名字（1-8字符）：')
        self.add_player(ConsolePlayer(player_name))
        bot_num = -1
        while not 0 <= bot_num <= 5:
            try:
                bot_num = int(input('请输入电脑玩家数目（1-5）：'))
            except ValueError:
                print('请输入数字！')
                bot_num = -1
            else:
                if not 0 <= bot_num <= 5:
                    print('输入数目不符合条件')

        for i in range(bot_num):
            self.add_player(BotPlayer())

        message('游戏开始！')
        game_continue = True
        _player_num = len(self._players)
        while game_continue:
            print('计分板')
            self.show_result()
            self._banker_index %= _player_num
            message('庄家是：{}'.format(self._players[self._banker_index]))
            # 发牌
            for player in self._players[self._banker_index : _player_num+self._banker_index]:
                message('{}拿牌>>>'.format(player))
                player.get_card(self._pile)
                player.get_card(self._pile)
                player.show_cards()
            # 加注、要牌
            for player in self._players[self._banker_index : _player_num+self._banker_index]:
                _need_card = True
                while _need_card:
                    _need_card = player.need_card()
                    message('{}{}要牌'.format(player, '' if _need_card else '不'))
                    if _need_card:
                        player.get_card(self._pile)
                        player.show_cards()
                        if player.get_point() >= 21:
                            continue
            winner = self.get_winner()
            message('{}获胜！'.format(winner))
            # 亮牌
            for player in self._players[self._banker_index: _player_num + self._banker_index]:
                print(player)
                player.show_all_cards()
            game_continue = input('继续游戏请输入(y)') in ['y', 'Y', '']
            self._banker_index += 1

        print('good bye!')

