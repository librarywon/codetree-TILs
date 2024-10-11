import sys
from collections import deque

input = sys.stdin.readline

N, m, k = map(int,input().split())
graph = [list(map(int,input().split())) for _ in range(N)]
teams = []
# 동 북 서 남
di = [0,-1,0,1]
dj = [1,0,-1,0]

answer = 0

balli, ballj = 0, 0

def make_team(si,sj):

    Q = deque()
    Q.append([si,sj])
    cnt = -1
    graph[si][sj] = cnt

    while True:
        cnt -=1
        for i in range(4):
            ni = si + di[i]
            nj = sj + dj[i]

            if ni <0 or ni > N-1 or nj<0 or nj > N-1:
                continue

            if graph[ni][nj] ==2 :
                Q.append([ni,nj])
                graph[ni][nj] = cnt
                si, sj = ni, nj
                break
            elif graph[ni][nj] ==3 and len(Q) >= 2 :
                Q.append([ni, nj])
                graph[ni][nj] = cnt
                return Q

for i in range(N):
    for j in range(N):
        # 1을 찾으면 팀을 형성한다.
        if graph[i][j] == 1:
            teams.append(make_team(i,j))
round_cnt = 0

for round in range(k):

    # 팀 이동
    for team in teams:
        headi,headj = team[0]

        for i in range(4):
            ni = headi + di[i]
            nj = headj + dj[i]

            if ni < 0 or ni > N - 1 or nj < 0 or nj > N - 1:
                continue

            if graph[ni][nj] == 4:
                team.appendleft([ni,nj])
                taili, tailj = team.pop()
                graph[taili][tailj] = 4
                break

            if graph[ni][nj] == -len(team):
                team.appendleft([ni, nj])
                team.pop()
                break

        new_index = -1
        for i, j in team:
            graph[i][j] = new_index
            new_index -= 1

    if round_cnt == 4*N:
        round_cnt = 0

    # 공 발사
    if round_cnt == 0:
        balli, ballj,direction = 0,0,0
    elif round_cnt == N:
        balli, ballj, direction = N-1, 0, 1
    elif round_cnt == 2*N:
        balli, ballj, direction = N-1, N-1, 2
    elif round_cnt == 3*N:
        balli, ballj, direction = 0, N-1, 3

    for move in range(N):
        ni = balli + move*di[direction]
        nj = ballj + move*dj[direction]

        if graph[ni][nj] < 0:
            answer+= pow(graph[ni][nj],2)
            for team in teams:
                if [ni,nj] in team:
                    team.reverse()
                    new_index = -1
                    for i, j in team:
                        graph[i][j] = new_index
                        new_index -= 1
                    break
            break
    round_cnt +=1

    if direction == 0:
        balli +=1
    elif direction == 1:
        ballj +=1
    elif direction == 2:
        balli -=1
    elif direction == 3:
        ballj -=1

print(answer)