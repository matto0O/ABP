from jellyfish import jaro_winkler_similarity as jws


def addNamesToDatabase(fList, sList, cursor):
    array = []

    for team in sList:
        b = findBestMatch(team, fList, 0.85 - len(team) * 0.015)
        array.append([team, b])
        if b is not None:
            fList.remove(b)

    for left in fList:
        insertIntoEmpty(left, array)

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS teams(ID smallint(4) AUTO_INCREMENT PRIMARY KEY , sts VARCHAR(20) NOT NULL UNIQUE , fortuna VARCHAR(20) NOT NULL UNIQUE )")

    for elem in array:
        cursor.execute("INSERT IGNORE INTO teams (sts, fortuna) VALUES (%s, %s)",(elem[0],elem[1]))


def findBestMatch(s, xs, threshold):
    best = None
    bestVal = threshold
    for a in xs:
        split_a = a.split(' ')
        split_s = s.split(' ')
        if len(split_a) > 1:
            for sa in split_a:
                if len(sa) < 4 - ("." in sa):
                    continue
                else:
                    v = jws(s, sa)
                    if v > bestVal:
                        bestVal = v
                        best = a
        if len(split_s) > 1:
            for ss in split_s:
                if len(ss) < 4 - ("." in ss):
                    continue
                else:
                    v = jws(a, ss)
                    if v > bestVal:
                        bestVal = v
                        best = a
        v = jws(s, a)
        if v > bestVal:
            bestVal = v
            best = a
    return best


def insertIntoEmpty(s, csFull):
    cs = sorted(filter(lambda elem: elem[1] is None, csFull), key=(lambda string: len(string)))
    upperS = ""
    bestMatch = None
    bestMatchVal = 0
    for char in s:
        if char.isupper():
            upperS += char
    for c in cs:
        upperC = ""
        for char in c[0]:
            if char.isupper():
                upperC += char
        u = jws(upperS, upperC)
        if u > bestMatchVal:
            bestMatchVal = u
            bestMatch = c
    if bestMatch is not None:
        csFull[csFull.index(bestMatch)] = [bestMatch[0], s]
    else:
        cs1 = list(filter(lambda elem: elem[1] is None, csFull))
        cs2 = []
        for z in cs1:
            cs2.append(z[0])
        o = findBestMatch(s, cs2, 0)
        csFull[csFull.index([o, None])] = [o, s]

