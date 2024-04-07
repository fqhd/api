import chess
import chess.polyglot
import re
from tqdm import tqdm
import pickle

chess_positions = {}

def remove_move_numbers(input_string):
    pattern = r'\d+\. '

    output_string = re.sub(pattern, '', input_string)

    return output_string

with open('openings.pgn') as f:
    games = f.read().split('\n')
    for game in tqdm(games):
        game = remove_move_numbers(game)
        moves = game.split(' ')[:-1]
        if "eval" in game:
            continue
        board = chess.Board()
        for move in moves:
            hsh = chess.polyglot.zobrist_hash(board)
            if hsh in chess_positions:
                chess_positions[hsh].append(move)
            else:
                chess_positions[hsh] = [move]
            board.push_san(move)

keys_to_remove = [key for key, value in chess_positions.items() if len(value) < 4]
for key in keys_to_remove:
    del chess_positions[key]

print(chess_positions)

with open('opening_book.bin', 'wb') as f:
    pickle.dump(chess_positions, f)

print('Opening book saved successfully')