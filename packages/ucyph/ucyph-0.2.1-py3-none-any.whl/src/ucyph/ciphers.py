# ---- Ciphers ----

# OG Caesar - shift of 3
def caesar(text: str, encode: bool, *args) -> str:
    """
    The Caesar cipher is one of the earliest known and simplest ciphers. It is a type of substitution cipher in which
    each letter in the plaintext is 'shifted' a certain number of places down the alphabet. For example, with a shift
    of 3, A would be replaced by D, B would become E, and so on.
    :param text: The string to be encoded/decoded
    :param encode: Whether to encode or decode the string
    :return: The encoded/decoded string
    """
    text = text.lower()
    az = 'abcdefghijklmnopqrstuvwxyz'
    new = ''
    if encode:
        for i in text:
            if i.isalpha():
                new += az[(az.index(i) + 3) % 26]
            else:
                new += i
    else:
        for i in text:
            if i.isalpha():
                if az.index(i) < 3:
                    new += az[26 - (abs(az.index(i) - 3) % 26)]
                else:
                    new += az[az.index(i) - 3]
            else:
                new += i
    return new


# ROT-47
def rot47(text: str, *args) -> str:
    """
    ROT-47 is a derivative of ROT-13 which, in addition to scrambling the basic letters, also treats numbers and
    common symbols. ROT-47 is frequently used to obfuscate plaintext in online forums such as Usenet to hide
    spoilers, punchlines, and puzzle solutions from the casual glance.
    :param text: The string to be encoded/decoded
    :return: The encoded/decoded string
    """
    key = '!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
    words = text.split(' ')
    final = []

    for word in words:
        crypted = []
        for letter in word:
            crypted.append(key[(key.index(letter) + 47) % 94])
        final.append(''.join(crypted))

    return ' '.join(final)


# ROT-13
def rot13(text: str, *args) -> str:
    """
    ROT-13 ("rotate by 13 places", sometimes hyphenated ROT-13) is a simple letter substitution cipher that replaces a
    letter with the 13th letter after it, in the alphabet. ROT13 is a special case of the Caesar cipher which was
    developed in ancient Rome.
    :param text: The string to be encoded/decoded
    :return: The encoded/decoded string
    """
    az = 'abcdefghijklmnopqrstuvwxyz'
    decrypted = ''
    for i in text:
        if i.isalpha():
            if i.islower():
                if az.index(i) < 13:
                    decrypted += az[az.index(i) + 13]
                elif az.index(i) >= 13:
                    decrypted += (az[(az.index(i) + 13) % 13])
            else:
                if az.upper().index(i) < 13:
                    decrypted += az.upper()[az.upper().index(i) + 13]
                elif az.upper().index(i) >= 13:
                    decrypted += az.upper()[(az.upper().index(i) + 13) % 13]
        else:
            decrypted += i
    return decrypted


# Vigenere
def vigenere(text: str, encode: bool, key: str) -> str:
    """
    The Vigenère cipher is a method of encrypting alphabetic text by using a series of interwoven Caesar ciphers,
    based on the letters of a keyword. It was invented in 1553 by Giovan Battista Bellaso, and is thus
    also known as the Bellaso cipher. While the cipher is easy to understand and implement, for three centuries
    it resisted all attempts to break it; this earned it the description le chiffre indéchiffrable (French for
    'the indecipherable cipher').
    :param text: The string to be encoded/decoded
    :param key: The key to be used for the cipher
    :param encode: Whether to encode or decode the string
    :return: The encoded/decoded string
    """
    text = text.lower()
    key = key.lower()
    alph = 'abcdefghijklmnopqrstuvwxyz'
    key_repeat = []
    encoded = ''

    if encode:
        for position, value in enumerate(text):
            key_repeat.append(key[position % len(key)])

            if value in alph:
                alph_position = alph.index(value)
                key_position = alph.index(key_repeat[position])
                encoded += alph[(alph_position + key_position) % len(alph)]
            else:
                encoded += value

        return encoded

    else:
        for position, value in enumerate(text):
            key_repeat.append(key[position % len(key)])

            if value in alph:
                alph_position = alph.index(value)
                key_position = alph.index(key_repeat[position])
                if alph_position >= key_position:
                    encoded += alph[abs(alph_position - key_position) % len(alph)]
                else:
                    encoded += alph[len(alph) - abs(alph_position - key_position)]
            else:
                encoded += value
        return encoded


# Playfair
def playfair(text: str, encode: bool, key: str) -> str:
    """
    The Playfair cipher is a digraph substitution cipher that was invented in 1854 by Charles Wheatstone,
    but named after Lord Playfair who heavily promoted its use.
    This cipher was used by the British during the Boer War and World War I and the Australians during World War II.

    :param text: The string to be encoded/decoded
    :param key: The key to be used for the cipher
    :param encode: Whether to encode or decode the string
    :return: The encoded/decoded string
    """
    AZ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    diagram = []
    row = []

    # -----Diagram-----

    # Clean text and Convert key to upper + no space
    text = ''.join(char if char.isalpha() or char == ' ' else '' for char in text)
    key = key.upper()
    key = key.replace(' ', '')

    # Create beginning of diagram using key
    for letter in key:
        if letter == 'J': letter = 'I'

        if len(row) < 5 and letter in AZ:
            row.append(letter)
            AZ = AZ.replace(letter, '')
        elif letter in AZ:
            diagram.append(row)
            row = []
            row.append(letter)
            AZ = AZ.replace(letter, '')

    # Fill in rest of diagram using remaining AZ
    for letter in AZ:
        if letter == 'J': letter = 'I'

        if len(row) < 5 and letter in AZ:
            row.append(letter)
            AZ = AZ.replace(letter, '')
        elif letter in AZ:
            diagram.append(row)
            row = []
            row.append(letter)
            AZ = AZ.replace(letter, '')
    # Append last row to diagram
    diagram.append(row)

    # -----Format Text-----

    # Convert text to upper + no space
    text = text.upper()
    text = text.replace(' ', '')

    # Split text into pairs
    # If pair is two of the same letter,
    # Add 'X' between them
    pair = []
    plain_text = []
    for letter in text:
        if len(pair) == 1:
            if pair[0] == letter:
                pair.append('X')
                plain_text.append(pair)
                pair = [letter]
            else:
                pair.append(letter)
                plain_text.append(pair)
                pair = []
        else:
            pair.append(letter)
    # Check if there is a leftover letter in pair.
    # If so, add 'X' and append to plain_text
    if len(pair) == 1:
        pair.append('X')
        plain_text.append(pair)

    # -----Encode-----
    encoded = []
    for pair in plain_text:
        coord_a = []
        coord_b = []
        for row in diagram:
            if pair[0] in row:
                coord_a.append(diagram.index(row))
                coord_a.append(diagram[diagram.index(row)].index(pair[0]))
            if pair[1] in row:
                coord_b.append(diagram.index(row))
                coord_b.append(diagram[diagram.index(row)].index(pair[1]))
        # Rule 1: If they are on same row, add/sub 1 from row
        if coord_a[0] == coord_b[0]:
            if encode:
                encoded.append(diagram[coord_a[0]][(coord_a[1] + 1) % 5])
                encoded.append(diagram[coord_b[0]][(coord_b[1] + 1) % 5])
            else:
                # is the col index 0?
                if coord_a[1] == 0:
                    encoded.append(diagram[coord_a[0]][4])
                else:
                    encoded.append(diagram[coord_a[0]][coord_a[1] - 1])
                if coord_b[1] == 0:
                    encoded.append(diagram[coord_b[0]][4])
                else:
                    encoded.append(diagram[coord_b[0]][coord_b[1] - 1])
        # Rule 2: If they are on the same col, add/sub 1 from col
        elif coord_a[1] == coord_b[1]:
            if encode:
                encoded.append(diagram[(coord_a[0] + 1) % 5][coord_a[1]])
                encoded.append(diagram[(coord_b[0] + 1) % 5][coord_b[1]])
            else:
                # is the row index 0?
                if coord_a[0] == 0:
                    encoded.append(diagram[4][coord_a[1]])
                else:
                    encoded.append(diagram[coord_a[0] - 1][coord_a[1]])
                if coord_b[0] == 0:
                    encoded.append(diagram[4][coord_b[1]])
                else:
                    encoded.append(diagram[coord_b[0] - 1][coord_b[1]])
        # Rule 3: Make square and grab opposite corner on same row
        else:
            encoded.append(diagram[coord_a[0]][coord_b[1]])
            encoded.append(diagram[coord_b[0]][coord_a[1]])

    return ''.join(encoded)
