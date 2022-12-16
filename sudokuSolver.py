import time


def generatePossibleNumbers(row, col, board):
    possibleNumbers = set()

    # Setting the numbers
    for index in range(1, 10):
        possibleNumbers.add(str(index))

    # Checking the row
    for colIndex in range(9):
        if board[row][colIndex] in possibleNumbers:
            possibleNumbers.remove(board[row][colIndex])

    # Checking the column
    for rowIndex in range(9):
        if board[rowIndex][col] in possibleNumbers:
            possibleNumbers.remove(board[rowIndex][col])

    # Checking the box
    for rowIndex in range(row // 3 * 3, row // 3 * 3 + 3):
        for colIndex in range(col // 3 * 3, col // 3 * 3 + 3):
            if board[rowIndex][colIndex] in possibleNumbers:
                possibleNumbers.remove(board[rowIndex][colIndex])

    return possibleNumbers


def solveSudoku(board):

    # Looping over cells
    for rowIndex in range(9):
        for colIndex in range(9):
            if board[rowIndex][colIndex] == ".":

                # Generating their possible numbers
                possibleNumbers = generatePossibleNumbers(rowIndex, colIndex, board)
                for number in possibleNumbers:
                    board[rowIndex][colIndex] = number

                    for row in board:
                        print(row)
                    time.sleep(0.1)

                    # Creating possible tree if possible then return final answer
                    if solveSudoku(board):
                        return board

                    # Replace the number with '.' if the number doesn't fit
                    board[rowIndex][colIndex] = "."
                return False
    return board
