#!/usr/bin/env python3

from itertools import product, islice
import vigenere
from crack5 import Dictionary
import crack5
import utils


s = 'Ccoheal ieu w qwu tcb'.lower()
dictionary = Dictionary('dictionary.txt', {len(w) for w in s.split()})


def words(length):
    return [w for w in dictionary.words if len(w) == length]


l = [words(len(w)) for w in s.split()]


@utils.log_nth_call(10000)
def check_key(key):
    decrypted = ''.join(x)
    key = vigenere.find_shortest_key(s, decrypted)

    if len(key) != 15:
        return

    print('{} {}'.format(decrypted, key))

    if crack5.check_online(key):
        print("legan! {}".format(key))


for x in product(*l):
    decrypted = ''.join(x)
    key = vigenere.find_shortest_key(s, decrypted)

    check_key(key)
