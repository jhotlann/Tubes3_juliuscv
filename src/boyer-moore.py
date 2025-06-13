from string import ascii_lowercase

def boyer_moore(text: str, pattern: str):
    p = len(pattern)
    t = len(text)

    if t < p:
        return -1
    last_occurrence = {}

    for i in range(26):
        last_occurrence[ascii_lowercase[i]] = -1
    
    for i in range(len(pattern)):
        last_occurrence[pattern[i]] = i
        

    i = p - 1
    j = p - 1
    while True:
        while j >= 0 and i < t: 
            if pattern[j] == text[i]:
                if (j == 0):
                    return i
                else:
                    j -= 1
                    i -= 1
            else:
                i += p - min(last_occurrence[text[i]] + 1, j)
                j = p - 1
        return -1

if __name__ == "__main__":
    text =  "bbacabbadcabacabaababb"
    pattern = "abacab"
    res = boyer_moore(text=text, pattern=pattern)
    print("i: ", res)
