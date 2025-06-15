from string import printable

def boyer_moore(text: str, pattern: str):
    # start
    p = len(pattern)
    t = len(text)

    if t < p:
        return -1
    last_occurrence = {}
    
    for i in range(len(printable)):
        last_occurrence[printable[i]] = -1
    
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
                i += p - min(last_occurrence.get(text[i], -1) + 1, j)
                j = p - 1
        return -1
    
def boyer_moore_search(text: str, pattern:str):
    i = 0
    last = 0
    result = []

    while i < len(text) - len(pattern):
        temp = (boyer_moore(text[i:], pattern))
        if temp == -1:
            break
        else:
            last = i
            result.append(temp + last)
            i = temp + len(pattern) + last

    return result

if __name__ == "__main__":
    text =  "saya suka python python dan pyrthonpythonp"
    pattern = "python"
    res = boyer_moore_search(text=text, pattern=pattern)
    # print("i: ", res)
    print(res)
