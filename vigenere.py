from itertools import cycle


ALPHA = 'abcdefghijklmnopqrstuvwxyz'


def decrypt(key, ciphertext):
    words = ciphertext.lower().split()

    def decrypt_char(key_char, cipher_char):
        total = ALPHA.index(cipher_char) - ALPHA.index(key_char)
        return ALPHA[total % 26]

    key_iter = iter(cycle(key.lower()))

    def decrypt_word(word):
        return ''.join(decrypt_char(next(key_iter), c) for c in word)

    return ' '.join(decrypt_word(word) for word in words).strip()


def test_decrypt():
    assert "zizhbgw" == decrypt(key="dupa", ciphertext="Ccoheal")
    assert "zizhbgw iba h qta ecy" == decrypt(key="dupa", ciphertext="Ccoheal ieu w qwu tcb")
    assert "" == decrypt(key="", ciphertext="Ccoheal ieu w qwu tcb")
