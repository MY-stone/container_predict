character_list = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10, 'B': 12,
                  'C': 13, 'D': 14, 'E': 15, 'F': 16, 'G': 17, 'H': 18, 'I': 19, 'J': 20, 'K': 21, 'L': 23, 'M': 24,
                  'N': 25, 'O': 26, 'P': 27, 'Q': 28, 'R': 29, 'S': 30, 'T': 31, 'U': 32, 'V': 34, 'W': 35, 'X': 36,
                  'Y': 37, 'Z': 38}


def container_check(str_11):
    list_num = []
    for i in range(11):
        list_num.append(character_list[str_11[i]])
    sum_pow = 0
    for i in range(10):
        sum_pow += list_num[i] * (2 ** i)
    last_num = sum_pow % 11
    if last_num == 10:
        last_num = 0
    if last_num == list_num[10]:
        return True
    else:
        return False

