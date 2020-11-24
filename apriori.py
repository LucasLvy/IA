def apriori(transaction, n):
    items = []
    countList = []
    for i in range(0, len(transaction)):
        for j in range(0, len(transaction[i])):
            if not items.__contains__(transaction[i][j]):
                items.append([transaction[i][j]])
    while len(countList) != -1:
        items = list(map(list, set(map(frozenset, items))))
        for i in range(0, len(items)):
            countList.append(count(transaction, items[i]))
        useless = mini(countList, n)
        items = nextStep(items, useless)
        if len(items) == 1:
            break
        countList = []
        items = mergeLists(items)
        #print(items)
    return items


def mergeLists(list1):
    newList = []
    for j in range(0, len(list1)):
        for i in range(j + 1, len(list1)):
            newList.append(list(set(list1[j] + list1[i])))
    return newList


def mini(list, n):
    x = []
    for i in range(0, len(list)):
        if list[i] < n:
            x.append(i)
    x.sort(reverse=True)
    return x


def nextStep(list, useless):
    for i in range(0, len(useless)):
        list.pop(useless[i])
    return list


def count(list, target):
    counter = 0
    for i in range(0, len(list)):
        if all(elem in list[i] for elem in target):
            counter += 1
    return counter


if __name__ == "__main__":
    print(apriori([[1, 2, 5], [1, 3, 5], [1, 2], [1, 2, 3, 4, 5], [1, 2, 4, 5], [2, 3, 5], [1, 5]], 3))
