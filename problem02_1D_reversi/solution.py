import sys
from collections import deque

def main():
    initial_board_str = sys.stdin.readline().strip()
    moves_str = sys.stdin.readline().strip()
    
    
    # 1. 初期盤面をブロック単位に圧縮してdequeに格納
    board_blocks = deque()
    
    if initial_board_str:
        current_char = initial_board_str[0]
        current_count = 1
        for i in range(1, len(initial_board_str)):
            if initial_board_str[i] == current_char:
                current_count += 1
            else:
                board_blocks.append([current_char, current_count])
                current_char = initial_board_str[i]
                current_count = 1
        board_blocks.append([current_char, current_count])
    
    # 2. 棋譜を1手ずつ処理
    for i, move in enumerate(moves_str):
        turn_number = i + 1
        stone_to_place = 'b' if turn_number % 2 == 1 else 'w'
        
        if move == 'L':
            # --- 左端に石を置く ---
            if not board_blocks:  # 盤面が空の場合
                board_blocks.append([stone_to_place, 1])
                continue
            
            leftmost_block = board_blocks[0]
            if leftmost_block[0] == stone_to_place:
                # 同じ色なので単純にカウントを増やす
                leftmost_block[1] += 1
            else:
                # 異なる色
                if len(board_blocks) > 1 and board_blocks[1][0] == stone_to_place:
                    # 反転・マージ処理
                    flipped_count = leftmost_block[1]
                    board_blocks.popleft()  # 左端ブロックを削除
                    board_blocks[0][1] += flipped_count + 1  # 新しい左端ブロックに統合
                else:
                    # 新しいブロックを左端に追加
                    board_blocks.appendleft([stone_to_place, 1])
                    
        elif move == 'R':
            # --- 右端に石を置く ---
            if not board_blocks:  # 盤面が空の場合
                board_blocks.append([stone_to_place, 1])
                continue
            
            rightmost_block = board_blocks[-1]
            if rightmost_block[0] == stone_to_place:
                # 同じ色なので単純にカウントを増やす
                rightmost_block[1] += 1
            else:
                # 異なる色
                if len(board_blocks) > 1 and board_blocks[-2][0] == stone_to_place:
                    # 反転・マージ処理
                    flipped_count = rightmost_block[1]
                    board_blocks.pop()  # 右端ブロックを削除
                    board_blocks[-1][1] += flipped_count + 1  # 新しい右端ブロックに統合
                else:
                    # 新しいブロックを右端に追加
                    board_blocks.append([stone_to_place, 1])
    
    # 3. 最終結果の集計
    black_stones = 0
    white_stones = 0
    
    for color, count in board_blocks:
        if color == 'b':
            black_stones += count
        else:
            white_stones += count
    
    print(f"{black_stones} {white_stones}")

if __name__ == '__main__':
    main()