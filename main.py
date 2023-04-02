from random import sample


def caesarEncription(plaintext: str, offset: int) -> str:
    """
    Cezarov algoritam koji pomera svaki karakter originalnog teksta za neki pomeraj unapred po engleskom alfabetu.
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


def monoalphabeticEncription(plaintext: str, key=None) -> tuple[str, str]:
    """
    Monoalfabetski algoritam preslikava svaki karakter originalnog teksta za ASCII vrednost permutacije alfabeta
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
    2. Parnjaci su isti kaakteri: pravimo dva parnjaka (x, char) i (char, x)
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


def playfairEncription(plaintext: str, key: str, equalChars=None) -> str:
    """
    Playfair algoritam radi sa 5x5 matricom u sledecim koracima:
    Prvi korak: Upisujemo kljuc u matricu karakter po karakter tako da ne ponavljamo nijedno slovo
    Drugi korak: Prepisujemo ostatak alfabeta, ali pritom preskacemo slova koja se vec pojavljuju.
    Posto engleski alfabet ima 26 slova, potrebno je dva karaktera preslikati u jedan
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


if __name__ == '__main__':
    text = "Napadamo u podne ako ne bude vetra"
    res = caesarEncription(text, 3)
    print(res)
    textKey = "qwertzuiopasdfghjklyxcvbnm"
    res = monoalphabeticEncription(text, textKey)
    print(res)
    res = playfairEncription(text, "vetrobran")
    print(res)
