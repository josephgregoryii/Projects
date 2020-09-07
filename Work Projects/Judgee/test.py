def r(elems):
    new_list = []
    for i in range(len(elems)):
        new_list.append(elems[len(elems)-i-1])

    return new_list

print(r([1,2,3,4]))
