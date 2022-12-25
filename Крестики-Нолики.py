from tkinter import *
#TODO Понять что такое окно!

root = Tk()

#   Constants
CANVAS_SIZE = 600
FIGURE_SIZE = 200
RATIO = CANVAS_SIZE // FIGURE_SIZE
BG_COLOR = "black"
EMPTY = None


#   Players setup
X = "player 1"
O = "player 2"
FIRST_PLAYER = X
SECOND_PLAYER = O

class Board(Tk):
    def __init__(self, start_player):
        super().__init__()
        self.canvas = Canvas(height=CANVAS_SIZE, width=CANVAS_SIZE, bg=BG_COLOR)
        self.canvas.pack()  #подключение виджета к полю
        self.figure_size = FIGURE_SIZE
        self.current_player = start_player
        self.canvas.bind("<Button-1>", self.click_event)
        self.board = [
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]
        ]

    def change_player(self):
        if self.current_player == X:
            self.current_player = O
        else:
            self.current_player = X


    def build_grid(self, grid_color):
        x = CANVAS_SIZE // RATIO
        y1 = 0
        y2 = CANVAS_SIZE
        for _ in range(2):
            self.canvas.create_line(x, y1, x, y2, fill=grid_color)
            self.canvas.create_line(y1, x, y2, x, fill=grid_color)
            x += CANVAS_SIZE // RATIO

    def render_cross(self, posX, posY):
        f_size = self.figure_size
        retreat = f_size/10
        self.canvas.create_line(posX + retreat, posY + retreat, posX + f_size - retreat, posY + f_size - retreat, fill="red", width=5)
        self.canvas.create_line(posX + retreat, posY - retreat + f_size, posX - retreat + f_size, posY + retreat, fill="red", width=5)

    def check_win(self, board, player):
        #победа по вертикали
        for l in board:
            b = l.count(player)
            if b == len(l):
                return True

        #по горизонту
        win_line = [player]*len(board)
        for l in range(len(board)):
            current_board = []
            for i in range(len(board)):
                current_board.append(board[i][l])
            if current_board == win_line:
                return True

        #по диагонали
        current_board = []
        for i in range(len(board)):
            current_board.append(board[i][i])
            if current_board == win_line:
                return True

        current_board = []
        for i in range(len(board)):
            current_board.append(board[i][len(board)-i-1])
        if current_board == win_line:
            return True
        else:
            current_board = []

        return False

    def show_winner(self, player):
        win_line = [player] * len(self.board)
        counter = 0
        #по вертикали
        for l in self.board:
            counter += 1
            b = l.count(player)
            if b == len(l):
                self.canvas.create_line((counter-1)*FIGURE_SIZE + FIGURE_SIZE/2, 0, (counter-1)*FIGURE_SIZE + FIGURE_SIZE/2, RATIO * FIGURE_SIZE, fill="IndianRed2" if player == X else "DodgerBlue2", width=5)


        #по горизонтали(верхний левый угол - нижний правый)
        current_board = []
        for i in range(len(self.board)):
            current_board.append(self.board[i][i])
            if current_board == win_line:
                self.canvas.create_line(0, 0, CANVAS_SIZE, CANVAS_SIZE, fill="IndianRed2" if player == X else "DodgerBlue2", width=5)

        #по горизонтали(верхний правый угол - нижний левый угол)
        current_board = []
        for i in range(len(self.board)):
            current_board.append(self.board[i][len(self.board) - i - 1])
        if current_board == win_line:
            self.canvas.create_line(CANVAS_SIZE, 0, 0, CANVAS_SIZE, fill="IndianRed2" if player == X else "DodgerBlue2", width=5)

        #по горизонту
        counter = 0
        for l in range(len(self.board)):
            current_board = []
            counter += 1
            for i in range(len(self.board)):
                current_board.append(self.board[i][l])
            if current_board == win_line:
                self.canvas.create_line(0, (counter - 1)*FIGURE_SIZE+FIGURE_SIZE/2, CANVAS_SIZE, (counter - 1)*FIGURE_SIZE+FIGURE_SIZE/2, fill="IndianRed2" if player == X else "DodgerBlue2", width=5)

    def check_draw(self, board):
        for i in board:
            for k in range(len(board)):
                if i[k] == EMPTY:
                    return False
        return True

    def render_circle(self, posX, posY):
        """5 - отступ от сетки поля, чтобы лучше смотелось"""
        f_size = self.figure_size - 10
        self.canvas.create_oval(posX + 10, posY + 10, posX + f_size, posY + f_size, width=5, outline="blue")

    def update_board(self, x, y, ):
        c_player = self.current_player
        self.board[x][y] = c_player
        if self.check_win(self.board, c_player):
            self.winner(c_player)
            #self.show_winner(c_player)
        elif self.check_draw(self.board):
            self.winner()

    def make_move(self, x, y):
        position = {}
        current_player = self.current_player
        for i in range(CANVAS_SIZE // FIGURE_SIZE):
            position[i] = i*200
        if self.board[x][y] == EMPTY:
            if current_player == X:
                self.render_cross(position[x], position[y])
            elif current_player == O:
                self.render_circle(position[x], position[y])
            self.update_board(x, y)
            self.change_player()

    def winner(self, player=None):
        """Окошко, показывающее кто победил\проиграл"""
        center = CANVAS_SIZE // 2
        if player:
            text = f"Winner: {player}"
            self.show_winner(player)
        else:
            text = "Draw"
        self.canvas.create_text(center, center, text=text, fill="green", font="Arial 50")
        self.canvas.unbind("<Button-1>")

    def click_event(self, event):
        """Передача координат курсора"""
        #player move
        x_coord = event.x // FIGURE_SIZE
        y_coord = event.y // FIGURE_SIZE
        if x_coord >= 3:
            x_coord -= 1
        if y_coord >= 3:
            y_coord -= 1
        self.make_move(x_coord, y_coord)


game_v1 = Board(start_player = FIRST_PLAYER)
game_v1.build_grid("green")

#TESTING


#Run the game
game_v1.mainloop()
