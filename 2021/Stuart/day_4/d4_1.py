from collections import OrderedDict

def read_input(path):
    with open(path) as f:
        numbers = f.readline().strip().split(',')
        numbers = list(map(int, numbers))

        boards = []
        while f.readline() != '':
            board = OrderedDict()
            for i in range(5):
                line = f.readline().strip().split(' ')
                board.update({int(num):False for num in line if num != ''})

            boards.append(board)
        
        return numbers, boards


def check_complete(board):
    for i in range(5):
        # Horizontal rows
        if all(list(board.values())[i*5:(i+1)*5]):
            return True

        # Vertical rows
        if all(list(board.values())[i::5]):
            return True

    return False


def calc_score(board, number):
    unmarked = sum([k for k,v in board.items() if not v])
    return unmarked * number


def find_first_board(numbers, boards):

    for number in numbers:
        for board in boards:
            if number in board:
                board[number] = True
                if check_complete(board):
                    return calc_score(board, number)

def find_last_board(numbers, boards):

    for number in numbers:
        remaining = []
        for board in boards:
            if number in board:
                board[number] = True
                if not check_complete(board):
                    remaining.append(board)
                elif len(boards) == 1:
                    return calc_score(board, number)
            else:
                remaining.append(board)

        boards = remaining


numbers, boards = read_input('d4_1_in.txt')
first_score = find_first_board(numbers, boards)
last_score = find_last_board(numbers, boards)

print(f"First board: {first_score}")
print(f"Last board: {last_score}")
