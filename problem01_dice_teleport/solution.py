import sys
from collections import deque

def main():
    N_str = sys.stdin.readline()
    N = int(N_str)
    
    # マス番号とインデックスを合わせるため、先頭にダミー要素を追加
    A = [0] + list(map(int, sys.stdin.readline().split()))
    
    # Nを超えたマスはゴールなので、探索範囲はNまでで十分
    MAX_POS = N + 1
    # dist[マス][フェーズ]
    # フェーズ0: 次にサイコロを振る状態
    # フェーズ1: マスの数字に従うか選べる状態
    inf = float('inf')
    dist = [[inf] * 2 for _ in range(MAX_POS)]
    
    # dequeを使用してBFS
    q_curr = deque()
    
    # 初期状態: マス0、フェーズ0(サイコロを振る)、コスト0
    dist[0][0] = 0
    q_curr.append((0, 0))
    
    rolls = 0
    while q_curr:
        # --- このターン(rolls)で到達可能な全状態をコスト0移動で洗い出す ---
        q_zero_cost = deque(q_curr)
        visited_in_level = set(q_curr)
        
        while q_zero_cost:
            pos, phase = q_zero_cost.popleft()
            
            cost = dist[pos][phase]
            if phase == 1:  # 「マスに従うか選ぶ」フェーズからのみコスト0移動が可能
                # 選択肢1: 進まない -> フェーズ0へ
                if cost < dist[pos][0]:
                    dist[pos][0] = cost
                    if (pos, 0) not in visited_in_level:
                        q_zero_cost.append((pos, 0))
                        visited_in_level.add((pos, 0))
                
                # 選択肢2: 進む -> フェーズ1のまま
                if 1 <= pos < N:
                    next_pos = pos + A[pos]
                    if next_pos >= N:  # ゴールに到達
                        if cost < dist[N][1]:
                            dist[N][1] = cost
                    elif cost < dist[next_pos][1]:
                        dist[next_pos][1] = cost
                        if (next_pos, 1) not in visited_in_level:
                            q_zero_cost.append((next_pos, 1))
                            visited_in_level.add((next_pos, 1))
        
        # --- 次のターン(rolls+1)の状態を計算する ---
        q_next = deque()
        
        # 現状のターンで到達した全ての状態からサイコロを振る
        for pos, phase in visited_in_level:
            # 「サイコロを振る」フェーズからのみコスト1移動が可能
            if dist[pos][0] == rolls:
                for roll in range(1, 7):
                    next_pos = pos + roll
                    
                    if next_pos >= N:  # ゴールに到達
                        if rolls + 1 < dist[N][0]:
                            dist[N][0] = rolls + 1
                        continue
                    
                    if rolls + 1 < dist[next_pos][1]:
                        dist[next_pos][1] = rolls + 1
                        q_next.append((next_pos, 1))
        
        # 状態を更新して次のループへ
        q_curr = q_next
        rolls += 1
        
        # 早期終了: ゴールに到達した場合
        if dist[N][0] != inf or dist[N][1] != inf:
            break
    
    # Nに到達する最小コストを取得
    result = min(dist[N])
    if result == inf:
        print(-1)
    else:
        print(result)

if __name__ == '__main__':
    main()