def add_one(number):
    return number + 1

def get_highest_elem_freq(inList):
    elem_max_freq = 0
    dic = dict()
    for elem in inList:
        if elem in dic:
            dic[elem] += 1
            if dic[elem] > elem_max_freq:
                elem_max_freq = dic[elem]
        else:
            dic[elem] = 1
    
    return elem_max_freq