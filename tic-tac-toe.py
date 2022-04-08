import random
from copy import copy, deepcopy


def main():
    command = 'none'
    while command != 'exit':
        command, x_player, y_player = menu()
        if command.lower() == 'exit':
            return
        elif command.lower() == 'start':
            game_routine(x_player, y_player)


def game_routine(x_player, y_player):
    board = [[' ' for x in range(3)] for y in range(0, 9, 3)]

    game_active = True
    turn = 0
    # start game routine:
    draw_board(board)
    # check if there is a winner or if board is full
    # if game over, print who won
    while game_active:
        winner = check_game_state(board)
        if winner:
            print(f'{winner} wins')
            game_active = False
            continue
        if turn == 9:
            print('Draw')
            game_active = False
            continue
        # if even X and Os, ask for X
        player_turn = 'X' if turn % 2 == 0 else 'O'
        # ask for move, checking if valid and making move
        if player_turn == 'X':
            if x_player.lower() == 'easy':
                board = easy_computer_move(board, player_turn)
            elif x_player.lower() == 'user':
                board = next_player_move(board, player_turn)
            elif x_player.lower() == 'medium':
                board = medium_computer_move(board, player_turn)
            elif x_player.lower() == 'hard':
                board = hard_computer_move(board, player_turn)
        else:
            if y_player.lower() == 'easy':
                board = easy_computer_move(board, player_turn)
            elif y_player.lower() == 'user':
                board = next_player_move(board, player_turn)
            elif y_player.lower() == 'medium':
                board = medium_computer_move(board, player_turn)
            elif y_player.lower() == 'hard':
                board = hard_computer_move(board, player_turn)

        turn += 1
        # draw board and recheck if winner

        draw_board(board)


def menu():
    valid_players = ('user', 'easy', 'medium', 'hard')
    valid_menu_items = ('start', 'end')
    option_valid = False
    bad_input_message = 'Bad parameters!'
    while not option_valid:
        player_input = input('Input command: ')
        if player_input.split()[0].lower() == 'exit':
            return ('exit', 'player', 'player')
        if len(player_input.split()) != 3:
            print(bad_input_message)
            continue
        command, x_player, y_player = player_input.split()
        if command.lower() not in valid_menu_items:
            print(bad_input_message)
            continue
        if x_player.lower() not in valid_players or y_player not in valid_players:
            print(bad_input_message)
            continue
        return command, x_player, y_player

def minimax(board, turn, ai):
    result = {}

    vacant_spots = avail_spots(board)
    human_turn = 'X' if turn == 'O' else 'O'

    # base case
    # check if there's a winner a return corresponding score
    winner = check_game_state(board)
    if winner == turn:
        result['score'] = 10
        return result
    elif winner == human_turn:
        result['score'] = -10
        return result
    elif len(vacant_spots) == 0:
        result['score'] = 0
        return result

    # dictionary to hold possible moves and their scores
    moves = {}

    # loop through available spots
    for row, column in vacant_spots:
        board[row][column] = turn if ai else human_turn

        #if currently ai, run minimax as human and vice versa
        if ai:
            new_result = minimax(board, turn, False)
        else:
            new_result = minimax(board, turn, True)

        #assign the resulting score the current move we're iterating over
        moves[(row, column)] = new_result['score']

        #reset the spot to empty
        board[row][column] = ' '

    # find which moves best suits the ai or player

    if ai:
        best_score = -1000
        for move, score in moves.items():
            if score > best_score:
                best_score = score
                best_move = move
    else:
        best_score = 1000
        for move, score in moves.items():
            if score < best_score:
                best_score = score
                best_move = move

    result['best_move'] = best_move
    result['score'] = best_score
    return result


def avail_spots(board):
    vacant_spots = []
    for row in range(3):
        for column in range(3):
            if board[row][column] == ' ':
                vacant_spots.append((row, column))
    return vacant_spots



def easy_computer_move(board, turn):
    print('Making move level "easy"')
    valid_move = False
    while not valid_move:
        valid_move = True
        x = random.randint(0, 2)
        y = random.randint(0, 2)
        if (board[x][y] != ' '):
            valid_move = False
            continue
        else:
            board[x][y] = turn
            return board


def medium_computer_move(board, turn):
    print('Making move level "medium"')

    #check to see if computer can win with move and, if so, win
    for x in range(3):
        for y in range(3):
            if (board[x][y] == ' '):
                new_board = deepcopy(board)
                new_board[x][y] = turn
                if check_game_state(new_board) == turn:
                    return new_board

    #check if it can prevent user from winning with a move
    other_player = 'X' if turn == 'O' else 'O'
    for x in range(3):
        for y in range(3):
            if (board[x][y] == ' '):
                new_board = deepcopy(board)
                new_board[x][y] = other_player
                if check_game_state(new_board) == other_player:
                    board[x][y] = turn
                    return board

    #make random move
    valid_move = False
    while not valid_move:
        valid_move = True
        x = random.randint(0, 2)
        y = random.randint(0, 2)
        if (board[x][y] != ' '):
            valid_move = False
            continue
        else:
            board[x][y] = turn
            return board

def hard_computer_move(board, turn):
    print('Making move level "hard"')
    row, column = minimax(board, turn, True)['best_move']
    board[row][column] = turn
    return board



def next_player_move(board, turn):
    move = ''
    valid_move = False
    while not valid_move:
        valid_move = True
        move = input('Enter the coordinates: ')
        if (len(move.split()) != 2 or not move.split()[0].isdigit() or not move.split()[1].isdigit()):
            print("You should enter numbers!")
            valid_move = False
            continue
        else:
            x = int(move.split()[0])
            y = int(move.split()[1])
        if (x < 1 or x > 3 or y < 1 or y > 3):
            print('Coordinates should be from 1 to 3!')
            valid_move = False
            continue
        # check if spot is vacant
        if (board[x - 1][y - 1] != ' '):
            print('This cell is occupied! Choose another one!')
            valid_move = False
            continue
        else:
            board[x - 1][y - 1] = turn
            return board


def draw_board(board):
    print('---------')
    for row in board:
        print('|', end=' ')
        for column in row:
            print(column, end=' ')
        print('|')
    print('---------')


def check_game_state(board):
    winner = ''
    for x in range(3):
        if board[x][0] != ' ' and board[x][0] == board[x][1] and board[x][0] == board[x][2]:
            winner = board[x][0]
    for y in range(3):
        if board[0][y] != ' ' and board[0][y] == board[1][y] and board[0][y] == board[2][y]:
            winner = board[0][y]
    if board[0][0] != ' ' and board[0][0] == board[1][1] and board[0][0] == board[2][2]:
        winner = board[0][0]
    if board[0][2] != ' ' and board[0][2] == board[1][1] and board[0][2] == board[2][0]:
        winner = board[0][2]
    return winner


def initial_state_is_valid(s: str) -> bool:
    valid_chars = ['X', 'O', '_']
    if len(s) != 9:
        return False
    for letter in s:
        if letter not in valid_chars:
            print(letter)
            return False
    return True


if __name__ == '__main__':
    main()
    #print(bool(''))
