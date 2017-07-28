from itertools import cycle, islice


ALPHA = 'abcdefghijklmnopqrstuvwxyz'


def decrypt(key, ciphertext):
    words = ciphertext.lower().split()

    def decrypt_char(key_char, cipher_char):
        total = _alpha_index(cipher_char) - _alpha_index(key_char)
        return ALPHA[total % 26]

    key_iter = iter(cycle(key.lower()))

    def decrypt_word(word):
        return ''.join(decrypt_char(next(key_iter), c) for c in word)

    return ' '.join(decrypt_word(word) for word in words).strip()


def test_decrypt():
    assert "zizhbgw" == decrypt(key="dupa", ciphertext="Ccoheal")
    assert "zizhbgw iba h qta ecy" == decrypt(key="dupa", ciphertext="Ccoheal ieu w qwu tcb")
    assert "" == decrypt(key="", ciphertext="Ccoheal ieu w qwu tcb")


def _drop_whitespace_and_make_list(s):
    return [c for c in s if c != ' ']


def _alpha_index(c):
    return ord(c) - 97


def find_obvious_key(encrypted, decrypted):
    encrypted = _drop_whitespace_and_make_list(encrypted)
    decrypted = _drop_whitespace_and_make_list(decrypted)

    def key_char(enc, dec):
        diff = _alpha_index(enc) - _alpha_index(dec)
        return ALPHA[diff % 26]

    obvious_key = [key_char(e, d) for e, d in zip(encrypted, decrypted)]

    return ''.join(obvious_key)


def test_find_obvious_key():
    encrypted = 'ccoheal ieu w qwu tcb'
    decrypted = 'zizhbgw iba h qta ecy'

    key = find_obvious_key(decrypted=decrypted, encrypted=encrypted)

    assert decrypted == decrypt(key=key, ciphertext=encrypted)


def reduce_key(s):
    def check(candidate):
        part = ''.join(islice(cycle(candidate), len(s)))
        return part == s

    for i in range(1, len(s)):
        candidate = s[:i]
        if check(candidate):
            return candidate

    return s


def test_reduce_key():
    assert 'abc' == reduce_key('abcabcabc')
    assert 'abc' == reduce_key('abcabc')
    assert 'abc' == reduce_key('abcab')
    assert 'abc' == reduce_key('abca')
    assert 'abc' == reduce_key('abc')


def find_shortest_key(encrypted, decrypted):
    return reduce_key(find_obvious_key(encrypted, decrypted))


def test_find_shortest_key():
    assert 'dupa' == find_shortest_key("ccoheal ieu w qwu tcb", "zizhbgw iba h qta ecy")
