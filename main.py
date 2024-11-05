import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QIcon

from gameUI2048 import Ui_Form
from logic import GameLogic


class GameGUI(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.prompted = False
        self.game_logic = GameLogic()
        self.tile_labels = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('2048 Game')
        self.setWindowIcon(QIcon('logo.jpg'))

        # 重新开始按钮
        self.new_game_btn.clicked.connect(self.restart_game)

        for i in range(4):
            row_labels = []
            for j in range(4):
                tile_label = QLabel()
                tile_label.setFont(QFont('Arial', 30, QFont.Bold))
                tile_label.setAlignment(Qt.AlignCenter)
                tile_label.setFixedSize(100, 100)
                self.gridLayout.addWidget(tile_label, i, j)
                row_labels.append(tile_label)
                self.set_tile_color(tile_label, self.game_logic.board[i][j])
            self.tile_labels.append(row_labels)

        self.update_board()

    def update_board(self):
        for i in range(4):
            for j in range(4):
                value = self.game_logic.board[i][j]
                tile_label = self.tile_labels[i][j]
                tile_label.setText(str(value) if value > 0 else '')
                self.set_tile_color(tile_label, value)
        self.score_label.setText(f'{self.game_logic.score}')
        self.best_score_label.setText(f'{self.game_logic.bestScore}')
        if self.game_logic.is_game_over():
            QMessageBox.information(
                self,
                'Game Over',
                'There are no more possible moves.')
        elif self.game_logic.has_won():
            if self.prompted:
                return
            QMessageBox.information(
                self,
                'Congratulations',
                'You have reached 2048! You won!')
            self.prompted = True

    @staticmethod
    def set_tile_color(tile_label, value):
        color_dict = {
            0: QColor("#ccc0b3"),
            2: QColor("#eee4da"),
            4: QColor("#ede0c8"),
            8: QColor("#f2b179"),
            16: QColor("#f59563"),
            32: QColor("#f67c5f"),
            64: QColor("#f65e3b"),
            128: QColor("#edcf72"),
            256: QColor("#edbb45"),
            512: QColor("#eda529"),
            1024: QColor("#ed8e1a"),
            2048: QColor("#e5550c")
        }
        if value in color_dict:
            tile_label.setStyleSheet(
                f"background-color: {color_dict[value].name()}; "
                f"color: {'#776e65' if value < 16 else 'white'}; "
                "border-radius: 5px;")
        else:
            tile_label.setStyleSheet(
                f"background-color: red; color: white; border-radius: 5px;")

    def restart_game(self):
        if self.game_logic.bestScore < self.game_logic.score:
            self.game_logic.bestScore = self.game_logic.score
            # 保存最高得分
            with open("bestScore.ini", "w") as f:
                f.write(str(self.game_logic.bestScore))
        self.game_logic = GameLogic()
        self.update_board()

    def keyPressEvent(self, event):
        """overwrite event"""
        if event.key() == Qt.Key_Up:
            new_board = self.game_logic.move_up()
        elif event.key() == Qt.Key_Down:
            new_board = self.game_logic.move_down()
        elif event.key() == Qt.Key_Left:
            new_board = self.game_logic.move_left()
        elif event.key() == Qt.Key_Right:
            new_board = self.game_logic.move_right()
        else:
            return

        if self.game_logic.board != new_board:
            self.game_logic.add_random_tile(new_board)
            self.game_logic.board = new_board
            self.update_board()

    def closeEvent(self, e):
        # 保存最高得分
        if self.game_logic.bestScore < self.game_logic.score:
            with open("bestScore.ini", "w") as f:
                f.write(str(self.game_logic.score))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = GameGUI()
    game.show()
    sys.exit(app.exec_())
