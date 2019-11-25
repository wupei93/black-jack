from abc import abstractmethod

from player import BasePlayer, BotPlayer
from poker import Pile


class Game:
    _pile = Pile()
    _players = []

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
        print('{}加入了游戏！'.format(player))


class ConsoleGame(Game):

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
        self.add_player(BasePlayer(player_name))
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

        print('游戏开始！')
        game_continue = True
        while game_continue:
            self.show_result()
            game_continue = input('继续游戏请输入(y)') in ['y', 'Y', '']

        print('good bye!')