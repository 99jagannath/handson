def longestPalindrome( s: str):
    n = len(s)
    if n <= 1:
        return s
    p = s[::-1]
    dp = [[0]*n] * n
    print(dp)
    for i in range(n):
        for j in range(n):
            if i ==0 or j ==0:
                dp[i][j] = 1 if s[i] == p[j] else 0
            elif s[i] == p[j]:

                dp[i][j] = dp[i-1][j-1] + 1
            else:

                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
            print( dp[i][j], end=" ")
        print('\n')

    print(dp)


longestPalindrome("cbbd")