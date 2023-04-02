from random import sample


def caesarEncryption(plaintext: str, offset: int) -> str:
    """
    Cezarov algoritam koji pomera svaki karakter originalnog teksta za neki pomeraj unapred po engleskom alfabetu.\n
    :param plaintext: originalni tekst
    :param offset pomeraj u engleskom alfabetu
    :return: enkriptovani tekst.
    Sva velika slova postaju mala, svi razmaci se uklanjaju i dozvoljeni su samo brojevi a-z&&A-Z
    """
    newString = []
    plaintext = plaintext.lower()
    for char in plaintext:
        if char.isalpha():
            newString.append(chr((ord(char) - ord('a') + offset) % 26 + ord('a')))
    return ''.join(newString)


def monoalphabeticEncryption(plaintext: str, key=None) -> tuple[str, str]:
    """
    Monoalfabetski algoritam preslikava svaki karakter originalnog teksta za ASCII vrednost permutacije alfabeta\n
    :param plaintext: originalni tekst
    :param key: opciono neka permutacija alfabeta, kao string
    :return: tuple(enkriptovani tekst, ascii permutacija)
    Sva velika slova postaju mala, svi razmaci se uklanjaju i dozvoljeni su samo brojevi a-z&&A-Z
    """
    if key is None:
        key = [chr(c) for c in range(ord('a'), ord('z') + 1)]
        key = sample(key, 26)
    newString = []
    plaintext = plaintext.lower()
    for i in range(len(plaintext)):
        if plaintext[i].isalpha():
            plaintextVal = ord(plaintext[i]) - ord('a')
            newString.append(key[plaintextVal])  # preslikavanje
    return ''.join(newString), ''.join(key)


def _createPlayfairEntry(plaintext: str, equalChars: tuple[chr, chr]) -> list[tuple[chr, chr]]:
    """
    Od plaintexta, pravi lowercase, alphabet listu parnjaka. Nealfabetski karakteri se preskacu
    Specijalni slucajevi:
    1. Neparna velicina: paranjak postaje (plaintext[-1], x)
    2. Parnjaci su isti kaakteri: pravimo dva parnjaka (x, char) i (char, x)\n
    :param plaintext: originalni tekst
    :param equalChars: par karaktera koji se preslikavaju u isti(prvi karakter)
    :return: Lista parnjaka koju dalje obradjuje playfair algoritam
    """
    last = ''
    result = []
    plaintext = plaintext.lower()
    plaintext = plaintext.replace(equalChars[1], equalChars[0])  # preslikavamo drugi karakter u prvi
    for i in range(len(plaintext)):
        if not plaintext[i].isalpha():
            continue
        if last == '':
            if i == len(plaintext) - 1:  # neparna velicina
                result.append((plaintext[i], 'x'))
            else:
                last = plaintext[i]
        else:
            if plaintext[i] == last:  # parnjaci isti karakteri
                result.append((last, 'x'))
                result.append(('x', plaintext[i]))
            else:
                result.append((last, plaintext[i]))
            last = ''  # resetujemo last da bi znali da smo na pocetku parnjaka
    return result


def _charPosition(matrix: list[list[chr]], char: chr) -> tuple[int, int]:
    """
    :param matrix: matrica karaktera
    :param char: karakter ciju poziciju trazimo
    :return: tuple reda i kolone pozicije karaktera
    """
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j
    return 0, 0  # greska


def _printMatrix(matrix: list[list[chr]]):
    """Ispisuje prozivoljnu matricu"""
    for row in matrix:
        for elem in row:
            print(elem, end=" ")
        print()


def playfairEncryption(plaintext: str, key: str, equalChars=None) -> str:
    """
    Playfair algoritam radi sa 5x5 matricom u sledecim koracima:
    Prvi korak: Upisujemo kljuc u matricu karakter po karakter tako da ne ponavljamo nijedno slovo
    Drugi korak: Prepisujemo ostatak alfabeta, ali pritom preskacemo slova koja se vec pojavljuju.
    Posto engleski alfabet ima 26 slova, potrebno je dva karaktera preslikati u jedan\n
    :param plaintext: originalni tekst
    :param key: kljuc
    :param equalChars: Karakteri koji se preslikavaju u jedan(prvi), podrazumevano (i, j)
    :return: Enkriptovani tekst
    Sva velika slova postaju mala, svi razmaci se uklanjaju i dozvoljeni su samo brojevi a-z&&A-Z
    """
    if equalChars is None:
        equalChars = ('i', 'j')
    matrix = [[''] * 5 for i in range(5)]  # 5x5 matrica
    charAdded = [False for i in range(26)]  # provera da li je karakter dodat
    row, col = 0, 0
    for char in key:  # PRVI KORAK
        if char == equalChars[1]:
            char = equalChars[0]  # mapiramo drugi karakter u prvi
        alphabetValue = ord(char) - ord('a')
        if not charAdded[alphabetValue]:
            charAdded[alphabetValue] = True
            matrix[row][col] = char
            col = (col + 1) % 5
            if col == 0:
                row += 1
    for i in range(26):  # DRUGI KORAK
        alphabetChar = chr(ord('a') + i)
        if alphabetChar == equalChars[1]:
            continue  # preskacemo iteraciju jer mapiramo drugi karakter kao prvi
        if not charAdded[i]:
            charAdded[i] = True
            matrix[row][col] = alphabetChar
            col = (col + 1) % 5
            if col == 0:
                row += 1
    plaintext = _createPlayfairEntry(plaintext, equalChars)  # list[tuple[chr, chr]]
    result = []
    for pair in plaintext:
        rowFirst, colFirst = _charPosition(matrix, pair[0])
        rowSecond, colSecond = _charPosition(matrix, pair[1])
        if rowFirst == rowSecond:  # isti red
            colFirst = (colFirst + 1) % 5
            colSecond = (colSecond + 1) % 5
        elif colFirst == colSecond:  # ista kolona
            rowFirst = (rowFirst + 1) % 5
            rowSecond = (rowSecond + 1) % 5
        else:  # razliciti red i kolona
            colFirst, colSecond = colSecond, colFirst  # menjamo mesta kolonama
        result.append(matrix[rowFirst][colFirst])
        result.append(matrix[rowSecond][colSecond])

    return ''.join(result)


def rowTranspositionEncryption(plaintext: str, numberOfCols: int, key=None) -> tuple[str, str]:
    """
    Row Transposition upisuje redom originalni tekst u matricu, sa zadatim brojem kolona. U slucaju da se ne moze
    popuniti ceo red, dodaje se znak x. Onda se na osnovu kljuca koji je jedna permutacija brojeva od 1..numberOfCols
    bira kojim ce redom biti ispisan tekst(na primer kolona 1 i key[0] = 3, to znaci da ce kolona 1 ici treca)\n
    :param key: opciono permutacija brojeva u obliku stringa, duzina i brojevi treba da budu od 1..numberOfCols
    :param plaintext: originalni tekst
    :param numberOfCols: broj kolona u transpozicionoj matrici
    :return:
    """
    if key is None:
        key = ''.join(str(i) for i in sample(range(1, numberOfCols + 1), numberOfCols))  # permutacija brojeva od 0..numberOfCols-1

    plaintext = ''.join([c.lower() for c in plaintext if c != ' '])  # uklanjamo razmake, ostali znaci dozvoljeni
    if numberOfCols > len(plaintext) or len(key) != numberOfCols:
        return "", ""  # greska
    numberOfRows = len(plaintext) // numberOfCols
    if len(plaintext) % numberOfCols != 0:
        numberOfRows += 1
    matrix = [['']*numberOfCols for i in range(numberOfRows)]
    curr = 0
    for i in range(numberOfRows):  # pravljenje matrice
        for j in range(numberOfCols):
            if curr >= len(plaintext):
                matrix[i][j] = 'x'  # ako nema vise originalnog teksta dodajemo x za dopunu
            else:
                matrix[i][j] = plaintext[curr]
            curr += 1
    cypher = []
    for j in range(1, numberOfCols + 1):  # kljuc indeksiran od 1
        nextIndex = key.index(str(j))  # nadjemo na kojem se indeksu se nalazi i, ta kolona se sledeca ubacuje
        for i in range(numberOfRows):
            cypher.append(matrix[i][nextIndex])
    return ''.join(cypher), key


if __name__ == '__main__':
    text = "Napadamo u podne ako ne bude vetra"
    res = caesarEncryption(text, 3)
    print(res)
    textKey = "qwertzuiopasdfghjklyxcvbnm"
    res = monoalphabeticEncryption(text, textKey)
    print(res)
    res = playfairEncryption(text, "vetrobran")
    print(res)
    res = rowTranspositionEncryption("That's what she said", 4, "3142")
    print(res)
    res = rowTranspositionEncryption(res[0], 4, "3142")  # dupla transpozicija
    print(res)
