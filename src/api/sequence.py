def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def window(lst, size):
    for i in range(len(lst) - size + 1):
        yield lst[i:i + size]
