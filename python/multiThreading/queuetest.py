def solution(board):
    # Implement your solution here
    n, m = len(board), len(board[0])
    ans = 0
    if n == 0 or m == 0:
        return 0

    dp = [[[0,0]]* m for i in range(n)]

    if board[0][0] == '.':
        dp[0][0] = [0, 0]
    elif board[0][0] == 'A':
        dp[0][0] = [1, 0]
    else:
        dp[0][0] = [0, 1]

    for j in range(1, m):
        if board[0][j] == 'A':
            dp[0][j] = [dp[0][j-1][0] + 1, dp[0][j-1][1]]
        elif board[0][j] == 'B':
            dp[0][j] = [dp[0][j-1][0], dp[0][j-1][1] + 1]

        else:
            dp[0][j] = [dp[0][j-1][0], dp[0][j-1][1]]

    for i in range(1, n):
        if board[i][0] == 'A':
            dp[i][0] = [dp[i-1][0][0] + 1, dp[i-1][0][1]]
        elif board[i][0] == 'B':
            dp[i][0] = [dp[i-1][0][0], dp[i-1][0][1] + 1]

        else:
            dp[i][0] = [dp[i-1][0][0], dp[i-1][0][1]]
    print(dp)
    for i in range(n):
        for j in range(m):
            if i != 0 and j != 0:
                dp[i][j][0] = dp[i-1][j][0] + dp[i][j-1][0]
                dp[i][j][1] =  dp[i-1][j][1] + dp[i][j-1][1]
                print(dp[i][j],i, j)
                if board[i][j] == 'A':
                    dp[i][j][0] += 1
                elif board[i][0] == 'B':
                    dp[i][j][1] += 1
                print(dp[i][j],i, j)
            if dp[i][j][0] == dp[i][j][1]:
                    ans += 1

    print(dp)
    return ans


grid = [['A', 'B', '.'], ['B', '.', '.'], ['.', '.', 'A']]

print(solution(grid))