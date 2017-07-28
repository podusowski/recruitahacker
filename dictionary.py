import codecs


class Dictionary:
    def __init__(self, filename, lengths):
        with codecs.open(filename, encoding='utf-8') as f:
            all_words = f.read().split()
            #words = {w.lower() for w in all_words if len(w) in lengths and w.lower() == w and not "'" in w}
            words = {w.lower() for w in all_words if len(w) in lengths and not "'" in w}

            words.add("arcyber")
            words.add("hacking")
            words.add("hackers")
            words.add("vinegar")
            words.add("america")
            #words.add("i")
            #words.add("a")
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
