from typing import List

def compute_lps(pattern: str) -> List[int]:
        lps = [0] * len(pattern)
        length = 0
        i = 1
        
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

def kmp_search(pattern: str, text: str) -> int:
    lps = compute_lps(pattern)
    indices = []
    i = j = 0

    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        
        if j == len(pattern):
            indices.append(i - j)
            j = lps[j - 1]
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    # Mengembalikan daftar indeks semua kemunculan pola dalam teks.
    # return indices 

    return len(indices)  # Mengembalikan jumlah kemunculan pola dalam teks.

