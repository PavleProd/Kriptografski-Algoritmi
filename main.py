from random import sample


def cezarovAlgoritam(plaintext: str, offset: int) -> str:
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


def monoalfabetskiAlgoritam(plaintext: str, cypher=None) -> tuple[str, str]:
    """
    Monoalfabetski algoritam preslikava svaki karakter originalnog teksta za ASCII vrednost permutacije alfabeta
    :param plaintext: originalni tekst
    :param cypher: opciono neka permutacija alfabeta, kao string
    :return: tuple(enkriptovani tekst, ascii permutacija)
    Sva velika slova postaju mala, svi razmaci se uklanjaju i dozvoljeni su samo brojevi a-z&&A-Z
    """
    if cypher is None:
        cypher = [chr(c) for c in range(ord('a'), ord('z') + 1)]
        cypher = sample(cypher, 26)
    newString = []
    plaintext = plaintext.lower()
    for i in range(len(plaintext)):
        if plaintext[i].isalpha():
            plaintextVal = ord(plaintext[i]) - ord('a')
            newString.append(cypher[plaintextVal])  # preslikavanje
    return ''.join(newString), ''.join(cypher)


if __name__ == '__main__':
    text = "Napadamo u podne ako ne bude vetra"
    res = cezarovAlgoritam(text, 3)
    print(res)
    textCypher = "qwertzuiopasdfghjklyxcvbnm"
    res = monoalfabetskiAlgoritam(text, textCypher)
    print(res)

