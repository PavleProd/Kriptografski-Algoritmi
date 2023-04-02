def cezarovAlgoritam(plaintext : str, offset : int) -> str:
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


if __name__ == '__main__':
    res = cezarovAlgoritam("Napadamo u podne ako ne bude vetra", 3)
    print(res)

