#!/usr/bin/env python3

import sys
import requests
import codecs
import string
# from unittest.mock import patch, mock_open
# import io

import vigenere
import utils


s = 'Ccoheal ieu w qwu tcb'.lower()
#s = 'Ccoheal ieuw qwu tcb'.lower()


from dictionary import Dictionary, PrincetonDictionary


#dictionary = Dictionary('/usr/share/dict/american-english', {len(w) for w in s.split() if len(w) > 1})
dictionary = Dictionary('dictionary.txt', {len(w) for w in s.split()})


with open('blacklist.txt', 'r') as blacklist_file:
    blacklist = {word.strip().lower() for word in blacklist_file}


def check_online(key):
    if key == '':
        return False

    if key in blacklist:
        return False

    status_code = None

    while not status_code or status_code == 504:
        url = 'http://www.recruitahacker.net/Puzzle/Mid'
        status_code = requests.get(url, params={'key': key}).status_code
        print('key: {} ({}) server: {}                               '.format(key, len(key), status_code))

    key_valid = status_code != 403
    if not key_valid:
        with open('blacklist.txt', 'a+') as blacklist_file:
            blacklist_file.write(key+'\n')
            blacklist.add(key)
    return key_valid


#@patch('builtins.open', return_value=io.StringIO("legan\n"))
#def test_blacklist_check(file_mock):
#    class Response:
#        pass
#    with patch("requests.get") as p:
#        response = Response()
#        response.status_code = 505
#        p.return_value = response
#        assert not check_online('legan')

#@patch('builtins.open', return_value=io.StringIO("dupa\n"))
#def test_blacklist_check(file_mock):
#    class Response:
#        pass
#    with patch("requests.get") as p:
#        response = Response()
#        response.status_code = 403
#        p.return_value = response
#        assert not check_online('legan')
#        assert 'legan' in file_mock.getvalue()

def test_prefix_of_a_valid_word():
    assert dictionary.is_prefix_of_a_word('the')
    assert dictionary.is_prefix_of_a_word('t')
    assert dictionary.is_prefix_of_a_word('')
    assert not dictionary.is_prefix_of_a_word('legan')


def test_are_all_words():
    assert not dictionary.are_all_words(['banana']) # invalid length
    assert not dictionary.are_all_words(['legan', 'banana']) # invalid word and length
    assert not dictionary.are_all_words(['legan']) # invalid word
    assert not dictionary.are_all_words(['legan', 'zyszkiew']) # invalid words

    assert dictionary.are_all_words(['the'])
    assert dictionary.are_all_words(['two'])
    assert dictionary.are_all_words(['two', 'the'])


def trim_decrypted(s, key_length):
    if len(s) < key_length:
        return s, ''.join([c for c in s if c != ' '])

    result = []
    without_spaces = []
    for c in s:
        if key_length:
            if c != ' ':
                key_length -= 1
                without_spaces += c
            result += c

    return ''.join(result), ''.join(without_spaces)


def test_trim_decrypted():
    assert 'qw', 'qw' == trim_decrypted('qw', 2)
    assert 'q', 'q' == trim_decrypted('qw', 1)
    assert 'q w', 'qw' == trim_decrypted('q w', 2)
    assert 'q', 'q' == trim_decrypted('q w', 1)
    assert ('', '') == trim_decrypted('', 0)

    assert 'abc def', 'abcdef' == trim_decrypted('abc def', 7)
    assert 'abc def', 'abcdef' == trim_decrypted('abc def', 6)
    assert 'abc de', 'abcde' == trim_decrypted('abc def', 5)


#@utils.log_nth_call(10000)
def need_to_go_deeper(decrypted, key_length):
    if decrypted == '':
        return True

    all_without_spaces = ''.join([c for c in decrypted if c != ' '])
    trimmed, without_spaces = trim_decrypted(decrypted, key_length)

    if key_length == len(all_without_spaces):
        return False

    words = trimmed.split()
    last = words[-1]
    all_but_last = words[:-1]

    if key_length == len(all_without_spaces):
        last_ok = dictionary.is_a_word(last)
    else:
        last_ok = dictionary.is_prefix_of_a_word(last)

    return last_ok and all(dictionary.is_a_word(word) for word in all_but_last)


def test_need_to_go_deeper():
    return
    assert need_to_go_deeper('', 0)
    assert need_to_go_deeper('', 1)

    assert need_to_go_deeper('t', 1)
    assert not need_to_go_deeper('th', 2)
    assert not need_to_go_deeper('the', 3)

    assert need_to_go_deeper('the l', 4)
    assert not need_to_go_deeper('the l', 10)
    assert not need_to_go_deeper('the legan', 20)

    assert need_to_go_deeper('the th', 4)
    assert need_to_go_deeper('the the', 4)
    assert not need_to_go_deeper('the the legan', 20)

    assert not need_to_go_deeper('the th the', 10)
    assert not need_to_go_deeper('the th the', 6)

    assert need_to_go_deeper('the th', 5)

    assert not need_to_go_deeper('the ż t', 5)
    assert not need_to_go_deeper('the ż t', 6)


def test_crap():
    '''
    bih -> buhgwtk axt o jvm mbt -> False
    '''

    assert not dictionary.is_prefix_of_a_word('buh')


princeton_dictionary = PrincetonDictionary()


@utils.log_nth_call(100000)
def process_key(key='', max_key_length=20):
    decrypted = vigenere.decrypt(key, s)

    phrase = decrypted.split()

    if dictionary.are_all_words(phrase) and princeton_dictionary.words_make_sense_as_whole(phrase):
        print('key: "{}" message: "{}"'.format(key, decrypted))
        if check_online(key):
            print("legan! {} {}".format(key, decrypted))
            sys.exit(0)

    if len(key) < max_key_length and need_to_go_deeper(decrypted, len(key)):
        for k in string.ascii_lowercase:
            process_key(''.join([key, k]), max_key_length)


if __name__ == "__main__":
    for i in range(3, 20):
        process_key('', i)
