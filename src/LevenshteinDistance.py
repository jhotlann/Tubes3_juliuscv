def LevenshteinDistance(source:str, target:str):
    m = len(source)
    n = len(target)

    matrix = [[0 for _ in range(m + 1)] for _ in range(n + 1)]

    for i in range(1, m + 1):
        matrix[0][i] = i
    
    for i in range(1, n + 1):
        matrix[i][0] = i

    for j in range(1, n + 1):
        for i in range(1, m + 1):
            if source[i-1].lower() == target[j-1].lower():
                cost = 0

            else:
                cost = 1

            matrix[j][i] = min(matrix[j-1][i] + 1, matrix[j][i-1] + 1, matrix[j-1][i-1] + cost)
            
    return matrix[n][m]

if __name__ == "__main__":
    res = LevenshteinDistance("Benyam", "Ephrem")
    print("Jarak = ", res)