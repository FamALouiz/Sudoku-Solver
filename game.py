import pygame as py
import sys
import sudokuSolver as ss
import time
import random


py.init()

# Setting width and height of canvas and colors
(width, height) = (520, 600)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Starting display
screen = py.display.set_mode((width, height))
py.display.set_caption("Sudoku Game!")
screen.fill(white)

# Setting variables
input_rectangles = []
random_puzzle = random.randint(1, 19810)
puzzle = []

# Displaying board
py.display.flip()
font = py.font.Font("freesansbold.ttf", 16)


def main():
    generateRandomPuzzle()
    board = []
    r = []

    solution = None
    button = None
    running = True
    total_rectangles = drawCanvas()
    button = makeButtons(button)
    current_focus = None
    removed = printProblem()
    counter = 0
    for row in puzzle:
        for number in row:
            r.append(number)
            if len(r) == 9:
                board.append(r)
                r = []
            total_rectangles[counter][1] = number
            counter += 1

    check(board, solution, total_rectangles)

    while running:
        current_focus, board = checkEvents(
            current_focus, button, board, removed, solution, total_rectangles
        )


def drawCanvas():

    # Draws the background
    py.draw.rect(screen, black, py.Rect(60, 60, 10, 400))
    py.draw.rect(screen, black, py.Rect(60, 460, 400, 10))
    py.draw.rect(screen, black, py.Rect(60, 60, 400, 10))
    py.draw.rect(screen, black, py.Rect(460, 60, 10, 410))

    for i in range(1, 3):

        # Draws the lines
        py.draw.rect(screen, black, py.Rect(60 + 135 * i, 60, 3, 400))
        py.draw.rect(screen, black, py.Rect(60, 60 + 135 * i, 400, 3))

    for i in range(1, 9):

        # Draws the cells
        py.draw.rect(screen, black, py.Rect(60 + 45 * i, 60, 1, 400))
        py.draw.rect(screen, black, py.Rect(60, 60 + 45 * i, 400, 1))

    # Adding input recognition to the cells
    for i in range(9):
        for j in range(9):
            input_rectangles.append(
                [py.Rect(65 + 45 * j, 65 + 45 * i, 45, 45), ".", i, j]
            )

    text = font.render("Sudoku Game", True, black, white)

    # Outputting the title
    textX = 520 / 2 - 45
    textY = 35

    screen.blit(text, (textX, textY))
    py.display.flip()

    return input_rectangles.copy()


def checkEvents(focus, button, board, removed, solution, total_rectangles):

    # Checking if a wrong number was written
    check(board, solution, total_rectangles)

    if board == puzzle:
        py.draw.rect(screen, black, py.Rect(250, 250, 250, 250))
        text = font.render("You won!!", True, white)
        screen.blit(text, (260, 260))
        time.sleep(10)
        print("Quitting...")
        return False, False

    # Event log
    for event in py.event.get():

        # Quitting
        if event.type == py.QUIT:
            running = False
            sys.exit()

        if event.type == py.MOUSEBUTTONDOWN:

            # Checking if the solution button has been clicked
            if button.collidepoint(event.pos):
                solution = ss.solveSudoku(puzzle)
                printSolution(solution, removed)

            # Checking if any cell has been clicked
            for rect in input_rectangles:
                if rect[0].collidepoint(event.pos):
                    focus = rect[0]

        # Checking what number has been written
        if event.type == py.KEYDOWN:

            # If backspace then delete what is in the cell
            if event.key == py.K_BACKSPACE:
                for rect in input_rectangles:
                    if rect[0] == focus:
                        rect[1] = "."
            else:
                try:

                    # If a digit then input it
                    int(event.unicode)
                    for rect in input_rectangles:
                        if rect[0] == focus:
                            rect[1] = event.unicode

                # If letter
                except:
                    print(focus, "That is not an int!")

            # Updating the board with the new number
            updateBoard(total_rectangles, board)
            printNumbers()

    return focus, board


def printNumbers():
    for rect in input_rectangles:
        (x, y) = (rect[0].x + 15, rect[0].y + 15)

        # Checking which box was clicked and writing number
        if not rect[1] == ".":
            text = font.render(rect[1], True, black, white)
            screen.blit(text, (x, y))

        # If back space then deleting the written number if written
        else:
            text = font.render("   ", True, white, white)
            screen.blit(text, (x, y))

    py.display.flip()


def updateBoard(total, board):

    # Updating current board in memory with any additions
    row = 0
    col = 0
    for rect in total:
        if col == 9:
            row += 1
            col = 0

        board[row][col] = rect[1]
        col += 1


def makeButtons(button):

    # Making the solution button
    button = py.draw.rect(screen, black, py.Rect(195, 520, 70, 30))
    text = font.render("Solve!", True, white)
    screen.blit(text, (205, 530))

    # Returning their coordinates
    return button


def printProblem():
    col = 0
    row = 0
    remove = []

    # Printing the numbers that were generated
    for rect in input_rectangles:
        (x, y) = (rect[0].x + 15, rect[0].y + 15)

        # If "." was generated then output an empty cell
        if not puzzle[row][col] == ".":
            text = font.render(puzzle[row][col], True, black, white)
            remove.append(rect)
        else:
            text = font.render("", True, black, white)

        col += 1

        if col == 9:
            row += 1
            col = 0
        screen.blit(text, (x, y))

    py.display.flip()

    # Checking the cells that were given in the puzzle so players can't edit those cells
    for item in remove:
        input_rectangles.remove(item)
    return remove


def printSolution(solution, removed):
    col = 0
    row = 0
    (startingx, startingy) = (60 + 20, 60 + 20)

    # Prints the numbers on screen from the solution found
    for rowIndex in range(9):
        for colIndex in range(9):
            text = font.render(solution[rowIndex][colIndex], True, black, white)

            screen.blit(text, (startingx + 45 * colIndex, startingy + 45 * rowIndex))

            py.display.flip()
            time.sleep(0.02)


def generateRandomPuzzle():

    # Going through the file and randomly selecting a puzzle
    with open("puzzles.txt", "r") as file:
        row = []
        for position, line in enumerate(file):
            if position == random_puzzle:

                # Forming the puzzle into the acceptable formate
                for i in range(81):
                    row.append(str(line[i]))
                    if len(row) == 9:
                        puzzle.append(row)
                        row = []


def check(board, solution, total):
    index = 0

    # Checking if there is a previous solution found if not find it
    if solution == None:
        solution = ss.solveSudoku(puzzle)

    # Looping over ever cell checking if it is correct
    for rowIndex in range(9):
        for colIndex in range(9):
            if (
                not board[rowIndex][colIndex] == "."
                and not board[rowIndex][colIndex] == solution[rowIndex][colIndex]
            ):
                (x, y) = (total[index][0].x + 15, total[index][0].y + 15)

                # Changing the color of the text to red if it is incorrect
                text = font.render(board[rowIndex][colIndex], True, red, white)
                screen.blit(text, (x, y))
                py.display.flip()

            index += 1


if __name__ == "__main__":
    main()
