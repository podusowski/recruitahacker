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


class PrincetonDictionary:
    def __init__(self):
        self.adjectives = set(self._load('princeton-wordnet/index.adj'))
        self.nouns = set(self._load('princeton-wordnet/index.noun'))
        self.adverbs = set(self._load('princeton-wordnet/index.adv'))
        self.verbs = set(self._load('princeton-wordnet/index.verb'))

    def _load(self, filename):
        ret = []
        with open(filename, 'r') as f:
            for line in f:
                word = line.split()[0]
                ret.append(word)
        return ret

    def word_classes(self, word):
        ret = set()
        if word in self.adjectives:
            ret.add('adjective')
        if word in self.nouns:
            ret.add('noun')
        if word in self.adverbs:
            ret.add('adverb')
        if word in self.verbs:
            ret.add('verb')
        return ret

    def words_make_sense_as_whole(self, words):

        duplicated_words = len(set(words)) != len(words)

        def make_sense(first, second):
            if first == second:
                return False

            first_classes = self.word_classes(first)
            second_classes = self.word_classes(second)

            various_classes = len(first_classes) > 1 or len(second_classes) > 1

            return various_classes or first_classes != second_classes

        return not duplicated_words and all(make_sense(first, second) for first, second in _pairs(words))



def test_princeton_dictionary():
    dictionary = PrincetonDictionary()

    assert {'adjective'} == dictionary.word_classes('awesome')
    assert {'noun'} == dictionary.word_classes('computer')
    assert {'adverb'} == dictionary.word_classes('repeatedly')
    assert {'verb'} == dictionary.word_classes('eat')

    assert {'noun', 'verb'} == dictionary.word_classes('hack')
    assert {'noun', 'verb'} == dictionary.word_classes('rub')

    assert {'noun'} == dictionary.word_classes('disease')
    assert {'noun', 'verb'} == dictionary.word_classes('gun')


def _pairs(a):
    return zip(a, a[1:])


def test_pairs():
    assert [(1, 2), (2, 3)] == list(_pairs([1, 2, 3]))


def test_words_make_sense_as_whole():
    dictionary = PrincetonDictionary()

    assert dictionary.words_make_sense_as_whole(['hacking', 'computer'])
    assert dictionary.words_make_sense_as_whole(['hack', 'rub'])
    assert not dictionary.words_make_sense_as_whole(['hack', 'hack'])
    assert not dictionary.words_make_sense_as_whole(['computer', 'computer'])

    assert not dictionary.words_make_sense_as_whole(['hack', 'rub', 'hack'])

