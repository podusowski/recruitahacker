#!/usr/bin/env python3

import sys
from itertools import cycle, combinations_with_replacement, product
from functools import reduce
import string
import requests

from vigenere import decrypt


s = 'Ccoheal ieu w qwu tcb'.lower()


class Dictionary:
    def __init__(self, filename, lengths):
        with open(filename, 'r') as f:
            all_words = f.read().split()
            words = {w.lower() for w in all_words if len(w) in lengths}
            self.words = words

            print('{} words for lengths {} taken from {} words loaded from {}'.format(len(words), lengths, len(all_words), filename))

            prefixes = {word[:length] for word in words for length in range(1, len(word))}
            self.prefixes = prefixes

            print('prefixes: {}'.format(len(self.prefixes)))

    def is_prefix_of_a_word(self, s):
        if len(s) == 0:
            return True

        return s in self.prefixes

    def is_a_word(self, s):
        return s in self.words

    def are_all_words(self, strings):
        if not strings:
            return False

        return all(self.is_a_word(s) for s in strings)

    def are_any_words(self, strings):
        if not strings:
            return False

        return any(self.is_a_word(s) for s in strings)


dictionary = Dictionary('/usr/share/dict/american-english', {len(w) for w in s.split()})

def check_online(key):
    if key == '':
        return False

    status_code = None

    while not status_code or status_code == 504:
        url = 'http://www.recruitahacker.net/Puzzle/Mid'
        status_code = requests.get(url, params={'key': key}).status_code
        print('key: {} server: {}                               '.format(key, status_code))

    return status_code != 403


def test_prefix_of_a_valid_word():
    assert dictionary.is_prefix_of_a_word('the')
    assert dictionary.is_prefix_of_a_word('t')
    assert dictionary.is_prefix_of_a_word('')
    assert not dictionary.is_prefix_of_a_word('legan')


def test_is_any_string_a_word():
    assert not dictionary.are_all_words(['banana']) # invalid length
    assert not dictionary.are_all_words(['legan', 'banana']) # invalid word and length
    assert not dictionary.are_all_words(['legan']) # invalid word
    assert not dictionary.are_all_words(['legan', 'zyszkiew']) # invalid words

    assert dictionary.are_all_words(['the'])
    assert dictionary.are_all_words(['two'])
    assert dictionary.are_all_words(['two', 'the'])


def need_to_go_deeper(decrypted, key_length):
    if decrypted == '':
        return True

    valid = decrypted[:key_length]
    words = valid.split()
    return dictionary.is_prefix_of_a_word(words[0])


def test_need_to_go_deeper():
    assert need_to_go_deeper('', 0)
    assert need_to_go_deeper('', 1)

    assert need_to_go_deeper('t', 1)
    assert need_to_go_deeper('th', 2)
    assert need_to_go_deeper('the', 3)

    assert need_to_go_deeper('th', 10)
    assert need_to_go_deeper('the', 10)
    assert need_to_go_deeper('the legan', 20)

    assert need_to_go_deeper('the', 1)

    assert need_to_go_deeper('legan', 1)
    assert need_to_go_deeper('legan the', 1)
    assert not need_to_go_deeper('żyszkiew', 6)
    assert not need_to_go_deeper('legan', 10)

    assert not need_to_go_deeper('legan the zyszkiew', 20)
    assert not need_to_go_deeper('legan zyszkiew', 7)


def test_crap():
    '''
    bih -> buhgwtk axt o jvm mbt -> False
    '''

    assert not dictionary.is_prefix_of_a_word('buh')


i = 0


def process_key(key=''):
    global i
    i += 1

    if i % 1000 == 0:
        print('{}    '.format(key), end='\r')
        sys.stdout.flush()

    if len(key) > len(s):
        #print("longer than {}".format(key))
        return

    decrypted = decrypt(key, s)

    if dictionary.are_all_words(decrypted.split()):
        print("got candidate: {} {}".format(key, decrypted))
        if check_online(key):
            print("legan! {} {}".format(key, decrypted))
            sys.exit(0)

    deeper = need_to_go_deeper(decrypted, len(key))
    print('{} -> {} -> {}'.format(key, decrypted, deeper))

    if need_to_go_deeper(decrypted, len(key)):
    #if dictionary.is_prefix_of_a_word(decrypted[:len(key)]):
        for k in string.ascii_lowercase:
            process_key(''.join([key, k]))


if __name__ == "__main__":
    process_key()
