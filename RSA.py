from sympy.ntheory import factorint


def findPrivateKey(phi: int, e: int) -> int:
    for i in range(1, phi):
        if (e * i) % phi == 1:
            return i
    return -1


def findFactors(n: int) -> (int, int):
    """
    Nalazi proste faktore zadatog broja n. Vraca samo koji su to faktori, ako se vise puta pojavljuju nece biti navedeno
    """
    return factorint(n).keys()


def decipherRSA(inputFile: str, outputFile: str, n: int, e: int, d=None):
    """
    :param inputFile:sifrovani ulazni fajl sa porukom
    (Blok od po dva velika slova na primer: AB -> 65*256 + 66 u hex formatu)
    :param outputFile: izlazni fajl sa desifrovanom porukom
    :param n: javni kljuc kao modulator
    :param e: javni kljuc kao eksponent
    :param d: opcioni parametar koji je privatan kljuc, ako nije naveden funkcija pokusava da ga nadje
    :return:
    """
    if d is None:
        p, q = findFactors(n)
        phi = (p - 1) * (q - 1)
        d = findPrivateKey(phi, e)

    cypher = ""
    with open(inputFile, "r") as file:
        cypher = file.read()

    numChars = 0
    currString = ""
    with open(outputFile, "w") as file:
        for char in cypher:
            if char == '\n':
                continue
            numChars += 1
            currString += char
            if numChars == 4:
                value = int(currString, 16)  # iz hex vrednosti u int
                value = (value ** d) % n
                firstChar = chr(value // 256)
                secondChar = chr(value % 256)

                numChars = 0
                currString = ""

                try:
                    file.write(firstChar + secondChar)
                except UnicodeError as e:
                    print(str(ord(firstChar)) + " " + str(ord(secondChar)))


def cypherRSA(inputFile: str, outputFile: str, n: int, e: int):
    plaintext = ""
    with open(inputFile, "r") as file:
        plaintext = file.read()

    last = ""
    with open(outputFile, "w") as file:
        for char in plaintext:
            if last != "":
                value = ord(last) * 256 + ord(char)
                value = (value ** e) % n
                value = (hex(value)[2:]).zfill(4)  # da bi broj imao minimum 4 hex cifre

                file.write(value)

                last = ""
            else:
                last = char
