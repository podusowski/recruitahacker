import codecs


class Dictionary:
    def __init__(self, filename, lengths=None):
        with codecs.open(filename, encoding='utf-8') as f:
            all_words = f.read().split()

            def correct_length(word):
                if lengths is not None:
                    return len(word) in lengths
                return True

            words = {w.lower() for w in all_words if correct_length(w) and not "'" in w}

            words.add("arcyber")
            words.add("hacking")
            words.add("hackers")
            words.add("vinegar")
            words.add("america")
            words.add("i")
            words.add("a")
            #words.add("u")

            self.words = words

            print('{} words for lengths {} taken from {} words loaded from {}'.format(len(words), lengths, len(all_words), filename))

            prefixes = {word[:length] for word in words for length in range(1, len(word) + 1)}
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

    def mostly_words(self, strings):
        if not strings:
            return False

        return all(self.is_a_word(s) for s in strings if len(s) > 3)


def test_dictionary():
    dictionary = Dictionary('american-english')

    assert dictionary.is_a_word('hacker')
    assert not dictionary.is_a_word('legan')

    assert dictionary.is_prefix_of_a_word('hac') # hacker
    assert dictionary.is_prefix_of_a_word('hacker')


def test_length_limited_dictionary():
    dictionary = Dictionary('american-english', lengths=[3, 6])

    assert dictionary.is_a_word('hacker')
    assert dictionary.is_a_word('the')

    assert not dictionary.is_a_word('haemoglobin')
