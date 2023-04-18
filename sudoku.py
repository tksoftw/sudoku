import time
import os

""" Copyright (C) tksoftw - All Rights Reserved
    Unauthorized copying of this file, via any medium is strictly prohibited
    Proprietary and confidential
    Written by tksoftw <https://github.com/tksoftw>, August 2022
"""

board1 = [["5","3",".",".","7",".",".",".","."],
        ["6",".",".","1","9","5",".",".","."],
        [".","9","8",".",".",".",".","6","."],
        ["8",".",".",".","6",".",".",".","3"],
        ["4",".",".","8",".","3",".",".","1"],
        ["7",".",".",".","2",".",".",".","6"],
        [".","6",".",".",".",".","2","8","."],
        [".",".",".","4","1","9",".",".","5"],
        [".",".",".",".","8",".",".","7","9"]]

board2 = [[".",".","9","7","4","8",".",".","."],
        ["7",".",".",".",".",".",".",".","."],
        [".","2",".","1",".","9",".",".","."],
        [".",".","7",".",".",".","2","4","."],
        [".","6","4",".","1",".","5","9","."],
        [".","9","8",".",".",".","3",".","."],
        [".",".",".","8",".","3",".","2","."],
        [".",".",".",".",".",".",".",".","6"],
        [".",".",".","2","7","5","9",".","."]]

board3 = [[".", ".", ".",   ".", "." ,".",  ".",".","."],
          [".", ".", ".",   ".", "." ,"3",  ".","5","8"],
          [".", ".", "1",   ".", "2" ,".",  ".",".","."],

          [".", ".", ".",   "5", "." ,"7",  ".",".","."],
          [".", ".", "4",   ".", "." ,".",  "1",".","."],
          [".", "9", ".",   ".", "." ,".",  ".",".","."],

          ["5", ".", ".",   ".", "." ,".",  ".","7","3"],
          [".", ".", "2",   ".", "1" ,".",  ".",".","6"],
          [".", ".", ".",   ".", "4" ,".",  ".",".","9"]]



board4 = [[".", ".", ".",   ".", "." ,".",  ".",".","1"],
          [".", ".", ".",   ".", "." ,".",  ".","2","3"],
          [".", ".", "4",   ".", "." ,".",  ".",".","."],

          [".", ".", ".",   "1", "." ,".",  ".",".","."],
          [".", ".", ".",   ".", "3" ,".",  "6",".","."],
          [".", ".", "7",   ".", "." ,".",  "5","8","."],

          [".", ".", ".",   ".", "6" ,"7",  ".",".","."],
          [".", "1", ".",   ".", "." ,"4",  ".",".","."],
          ["5", "2", ".",   ".", "." ,".",  ".",".","."]]


board5 = [[".", ".", ".",   "8", "." ,"1",  ".",".","."],
          [".", ".", ".",   ".", "." ,".",  ".","4","3"],
          ["5", ".", ".",   ".", "." ,".",  ".",".","."],

          [".", ".", ".",   ".", "7" ,".",  "8",".","."],
          [".", ".", ".",   ".", "." ,".",  "1",".","."],
          [".", "2", ".",   ".", "3" ,".",  ".",".","."],

          ["6", ".", ".",   ".", "." ,".",  ".","7","5"],
          [".", ".", "3",   "4", "." ,".",  ".",".","."],
          [".", ".", ".",   "2", "." ,".",  "6",".","."]]

board6 = [[".", ".", "5",   "3", "." ,".",  ".",".","."],
          ["8", ".", ".",   ".", "." ,".",  ".","2","."],
          [".", "7", ".",   ".", "1" ,".",  "5",".","."],

          ["4", ".", ".",   ".", "." ,"5",  "3",".","."],
          [".", "1", ".",   ".", "7" ,".",  ".",".","6"],
          [".", ".", "3",   "2", "." ,".",  ".","8","."],

          [".", "6", ".",   "5", "." ,".",  ".",".","9"],
          [".", ".", "4",   ".", "." ,".",  ".","3","."],
          [".", ".", ".",   ".", "." ,"9",  "7",".","."]]

board6a = [["8", ".", ".",   ".", "." ,".",  ".",".","."],
          [".", ".", "3",   "6", "." ,".",  ".",".","."],
          [".", "7", ".",   ".", "9" ,".",  "2",".","."],

          [".", "5", ".",   ".", "." ,"7",  ".",".","."],
          [".", ".", ".",   ".", "4" ,"5",  "7",".","."],
          [".", ".", ".",   "1", "." ,".",  ".","3","."],

          [".", ".", "1",   ".", "." ,".",  ".","6","8"],
          [".", ".", "8",   "5", "." ,".",  ".","1","."],
          [".", "9", ".",   ".", "." ,".",  "4",".","."]]

board6b = [["8", "5", ".",   ".", "." ,"2",  "4",".","."],
          ["7", "2", ".",   ".", "." ,".",  ".",".","9"],
          [".", ".", "4",   ".", "." ,".",  ".",".","."],

          [".", ".", ".",   "1", "." ,"7",  ".",".","2"],
          ["3", ".", "5",   ".", "." ,".",  "9",".","."],
          [".", "4", ".",   ".", "." ,".",  ".",".","."],

          [".", ".", ".",   ".", "8" ,".",  ".","7","."],
          [".", "1", "7",   ".", "." ,".",  ".",".","."],
          [".", ".", ".",   ".", "3" ,"6",  ".","4","."]]

board6c = [[".", ".", ".",   ".", "." ,"5",  ".","8","."],
          [".", ".", ".",   "6", "." ,"1",  ".","4","3"],
          [".", ".", ".",   ".", "." ,".",  ".",".","."],

          [".", "1", ".",   "5", "." ,".",  ".",".","."],
          [".", ".", ".",   "1", "." ,"6",  ".",".","."],
          ["3", ".", ".",   ".", "." ,".",  ".",".","5"],

          ["5", "3", ".",   ".", "." ,".",  ".","6","1"],
          [".", ".", ".",   ".", "." ,".",  ".",".","4"],
          [".", ".", ".",   ".", "." ,".",  ".",".","."]]

board7 = [[".", ".", ".",   ".", "." ,".",  ".",".","."],
          [".", ".", ".",   ".", "." ,"3",  ".","8","5"],
          [".", ".", "1",   ".", "2" ,".",  ".",".","."],

          [".", ".", ".",   "5", "." ,"7",  ".",".","."],
          [".", ".", "4",   ".", "." ,".",  "1",".","."],
          [".", "9", ".",   ".", "." ,".",  ".",".","."],

          ["5", ".", ".",   ".", "." ,".",  ".","7","3"],
          [".", ".", "2",   ".", "1" ,".",  ".",".","."],
          [".", ".", ".",   ".", "4" ,".",  ".",".","9"]]

board8 = [[".", ".", ".",   ".", "." ,".",  ".",".","."],
          [".", ".", ".",   ".", "." ,".",  ".",".","."],
          [".", ".", ".",   ".", "." ,".",  ".",".","."],

          [".", ".", ".",   ".", "." ,".",  ".",".","."],
          [".", ".", ".",   ".", "." ,".",  ".",".","."],
          [".", ".", ".",   ".", "." ,".",  ".",".","."],

          [".", ".", ".",   ".", "." ,".",  ".",".","."],
          [".", ".", ".",   ".", "." ,".",  ".",".","."],
          [".", ".", ".",   ".", "." ,".",  ".",".","."]]


def boardToStr(board):
    result = ''
    for row in board:
        for v in row:
            result += str(v)
    return result

def strToBoard(strBoard):
    result = []
    for i, v in enumerate(strBoard):
        if i % 9 == 0:
            result.append([])
        result[-1].append(v)
    return result

def solved(board):
    return sum(v != '.' for row in board for v in row) == 81

def getPossibles(board):
    possibles = [[[] for x in range(9)] for _ in range(9)]
    get_box_num = lambda r, c: c//3+(r//3)*3
    get_box_ind = lambda r, c: c%3+(r%3)*3

    board_swapped = [[] for _ in range(9)]
    board_boxes = [[] for _ in range(9)]
    for x in range(81):
        i, j = divmod(x, 9)
        board_swapped[i].append(board[j][i])
        board_boxes[i].append(board[get_box_num(i, j)][get_box_ind(i, j)])

    for i, row in enumerate(possibles):
        for j, col in enumerate(row):
            if board[i][j] != '.':
                col.extend({board[i][j]})
                continue
            full_possibles = set(str(n) for n in range(1, 10))
            col.extend(full_possibles.difference(set(board[i] + board_swapped[j] + board_boxes[get_box_num(i, j)])))

    return possibles

def getMinPossibles(possibles):
    currentMin, (currentMinRow, currentMinCol) = 9, (0, 0)
    for i, row in enumerate(possibles):
        for j, col in enumerate(row):
            if len(col) >= 2 and len(col) < currentMin:
                currentMin, (currentMinRow, currentMinCol) = len(possibles[i][j]), (i, j)
    return (currentMinRow, currentMinCol)

def removeFromPossibles(possibles, row, col, val):
    get_box_num = lambda r, c: c//3+(r//3)*3
    # Row, col and box possibles excluding given point
    local_row_possibles = possibles[row][:col] + possibles[row][col+1:]
    local_col_possibles = [row[col] for row in (possibles[:row] + possibles[row+1:])]
    local_box_possibles = [possibles[get_box_num(row, k)][k%3+(col//3)*3] for k in range(9) if (row, col) != (get_box_num(row, k), k%3+(col//3)*3)]
    
    # Remove val from all local possibles excluding (row, col)
    for possibles_list in (local_row_possibles, local_col_possibles, local_box_possibles):
        for current_possibles in possibles_list:
            if val in current_possibles:
                current_possibles.remove(val)

def eliminationReduce(board):
    possibles = getPossibles(board)
    solvedCount = 1
    while solvedCount > 0:
        solvedCount = 0
        for i, row in enumerate(possibles):
            for j, col in enumerate(row):
                if len(col) == 0:
                    return None
                elif len(col) == 1 and board[i][j] == '.':
                    board[i][j] = col[0]
                    removeFromPossibles(possibles, i, j, col[0])
                    solvedCount += 1
    return board

def createPossibleBoards(board, possibles, minPossiblesTile):
    strBoards = []
    
    mpRow, mpCol = minPossiblesTile
    for p in possibles[mpRow][mpCol]:
        board[mpRow][mpCol] = p
        strBoards.append(boardToStr(board))

    return strBoards

def guessNewBoards(board):
    newBoardStrs = []

    currentPossibles = getPossibles(board)
    minPossiblesTile = getMinPossibles(currentPossibles)
    validPossibleBoardStrs = createPossibleBoards(board, currentPossibles, minPossiblesTile)
    newBoardStrs.extend(validPossibleBoardStrs)
    return newBoardStrs

def greedyBestDepthFirst(start):
    queue = [boardToStr(start)]
    while len(queue) > 0:
        current = queue.pop()
        board = strToBoard(current)
        reduced = eliminationReduce(board)
        if reduced is None:
            continue
        elif solved(reduced):
            return reduced
        else:
            # Make guesses
            bestGuessBoardStrs = guessNewBoards(reduced)
            # Add guesses to queue
            queue.extend(bestGuessBoardStrs)
    return None

def print_board(board):
    for row in board:
        print(' '.join(row))

def print_possibles(possibles):
    print('='*(9*3+9*2+8*3))
    # Assuming 9x9 sudoku grid
    for row in possibles:
        row_str = ''
        for i in range(3):
            for values in row:
                for j in range(i*3+1, i*3+4):
                    if str(j) in values:
                        row_str += str(j)
                    else:
                        row_str += '.'
                    row_str += ' ' if j != i*3+3 else '\t'
            row_str += '\n'
        print(row_str)
    print('='*69)

def validBoard(br):
    get_box_num = lambda r, c: c//3+(r//3)*3
    get_box_ind = lambda r, c: c%3+(r%3)*3

    rv = []
    bx = []
    for i in range(9):
        rv.append([])
        bx.append([])
        for j in range(9):
            rv[i].append(br[j][i])
            bx[i].append(br[get_box_num(i, j)][get_box_ind(i, j)])
    
    return not any((br[i][j] != '.' and (br[i].count(br[i][j]) > 1  or rv[j].count(br[i][j]) > 1 or bx[get_box_num(i, j)].count(br[i][j]) > 1) ) for i in range(9) for j in range(9))


class Grid:
    def __init__(self):
        self.dim = 9
        #self.grid = [['.']*dim for _ in range(dim)]
        #self.viewable_grid = [["."]*dim for _ in range(dim)]

        self.viewable_grid = board6b
        self.grid = greedyBestDepthFirst(self.viewable_grid)

        self.hints = { (i,j):v for i, row in enumerate(self.viewable_grid) for j, v in enumerate(row) if v.isdigit()}

    def boardToStr(self, boardArr):
        resultStr = ''
        for row in boardArr:
            for v in row:
                resultStr += v
        return resultStr

    def boardFromStr(self, boardStr):
        resultArr = []
        for i, v in enumerate(boardStr):
            if i % self.dim == 0:
                resultArr.append([])
            resultArr[-1].append(v)
        return resultArr

    def is_hint(self, i, j):
        return (i,j) in self.hints

    def is_solved(self, i, j):
        return self.boardToStr(self.viewable_grid) == self.boardToStr(self.grid)

    def guess_number(self, i, j, n: str):
        if self.is_hint(i,j):
            return
        self.viewable_grid[i][j] = n

    def remove_guess(self, i, j):
        if self.viewable_grid[i][j] == '.':
            return
        self.guess_number(i,j, '.')
    
    def print(self):
        for row in self.viewable_grid:
            print(' '.join(row))

    def play_game(self):
        while True:
            self.print()
            choice = input('Would you like to make a guess (G) or remove a guess (R)? ').lower()
            row = int(input('Enter the row of the guess: '))-1
            col = int(input('Enter the col of the guess: '))-1
            if choice == 'g':
                num = input('Enter number to guess: ')
                self.guess_number(row,col,num)
            else:
                self.remove_guess(row,col)

if __name__ == '__main__':
    g = Grid()
    g.print()
    for i in range(g.dim):
        for j in range(g.dim):
            g.guess_number(i,j,str(1))
    g.print()
    for i in range(g.dim):
        for j in range(g.dim):
            g.remove_guess(i,j)
    g.print()
    #g.play_game()

#    b = board6b
#    print('='*10,'initial','='*10)
#    print_board(b)
#    os.system('pause')
#    t1_start = time.perf_counter()
#    solved = greedyBestDepthFirst(b)
#    t1_stop = time.perf_counter()
#    print('='*10,'solved','='*10)
#    print_board(solved)
#    print('Valid Solution?', validBoard(solved))
#    print('Elapsed time in seconds:', t1_stop-t1_start)
