import os
import random


class GameLogic:
    def __init__(self):
        self.board = [[0 for _ in range(4)] for _ in range(4)]
        self.score = 0
        self.bestScore = 0
        # 载入最高得分
        try:
            with open('bestScore.ini', mode='r', encoding='utf-8') as f:
                self.bestScore = int(f.read())
        except:
            with open("bestScore.ini", mode='w', encoding='utf-8') as f:
                f.write(r'0')
                print('创建成功')
        self.init_tiles()

    def init_tiles(self):
        for _ in range(2):
            self.add_random_tile(self.board)

    def move_up(self):
        new_board = [[0 for _ in range(4)] for _ in range(4)]
        for j in range(4):
            temp_list = []
            for i in range(4):
                if self.board[i][j] != 0:
                    temp_list.append(self.board[i][j])
            new_list = self.merge_tiles(temp_list)
            for i in range(len(new_list)):
                new_board[i][j] = new_list[i]
        return new_board

    def move_down(self):
        new_board = [[0 for _ in range(4)] for _ in range(4)]
        for j in range(4):
            temp_list = []
            for i in range(3, -1, -1):
                if self.board[i][j] != 0:
                    temp_list.append(self.board[i][j])
            new_list = self.merge_tiles(temp_list)
            for i in range(len(new_list)):
                new_board[3 - i][j] = new_list[i]
        return new_board

    def move_left(self):
        new_board = [[0 for _ in range(4)] for _ in range(4)]
        for i in range(4):
            temp_list = []
            for j in range(4):
                if self.board[i][j] != 0:
                    temp_list.append(self.board[i][j])
            new_list = self.merge_tiles(temp_list)
            for j in range(len(new_list)):
                new_board[i][j] = new_list[j]
        return new_board

    def move_right(self):
        new_board = [[0 for _ in range(4)] for _ in range(4)]
        for i in range(4):
            temp_list = []
            for j in range(3, -1, -1):
                if self.board[i][j] != 0:
                    temp_list.append(self.board[i][j])
            new_list = self.merge_tiles(temp_list)
            for j in range(len(new_list)):
                new_board[i][3 - j] = new_list[j]
        return new_board

    def merge_tiles(self, tiles):
        merged_tiles = []
        i = 0
        while i < len(tiles):
            if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
                merged_value = tiles[i] * 2
                self.score += tiles[i] * 2
                merged_tiles.append(merged_value)
                i += 2
            else:
                merged_tiles.append(tiles[i])
                i += 1
        return merged_tiles

    def is_game_over(self):
        cur_score = self.score
        for direction in [self.move_up, self.move_down, self.move_left, self.move_right]:
            new_board = direction()
            if new_board != self.board:
                self.score = cur_score
                return False
        return True

    def has_won(self):
        for row in self.board:
            for tile in row:
                if tile == 2048:
                    return True
        return False

    @staticmethod
    def add_random_tile(board):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
        if empty_cells:
            row, col = random.choice(empty_cells)
            board[row][col] = 2 if random.random() < 0.9 else 4
