"""Interprets text as words and sentences

This script takes a string and separates it into a list of words. It allows for len calls, indexing
and for loops on the list. It allows for 'in' to be called on the list. It also splits sentences at ';'
"""

import string

punctuation = ['?', '!', '.']


def format_text(text):
    """Formats sentences when they are split by ;
    (capitalizes first letter of each sentence and adds '.' to the end)

    :param text: input string to be formatted
    :return: grammatically correct string
    """
    new_text = text[0].upper() + text[1:]
    if text[-1] not in punctuation:
        new_text += '.'
    return new_text


class Sentence:
    """Turns a string into a sentence object

    Attributes: original text - original string, words - list of words froms string, pointer - set up for __iter__
    methods: constructor separates string into words, sets up pointer, get_word_list is getter for list of words
    __len__ returns length of sentence, __str__ returns the original string
    __iter__ and __next__ allow for looping over words in sentence, __getitem__ allows indexes to be called on sentence
    contains() allows for 'in' functionality (check if word is in sentence), reset_iterator puts pointer back to 0
    split() splits sentences at ';'
    """
    def __init__(self, text):
        """converts input text into a list of words, sets pointer at 0"""
        self.original_text = text
        self.words = [w.strip(string.punctuation).lower() for w in text.strip(',.?!()').split(' ')]
        self.pointer = 0

    def get_word_list(self):
        """returns list of words"""
        return self.words

    def __len__(self):
        """returns length of sentence"""
        return len(self.words)

    def __str__(self):
        """returns original text input"""
        return self.original_text

    def __iter__(self):
        """sets up pointer for starting point for __next__"""
        self.pointer = 0
        return self

    def __next__(self):
        """iterates through words in sentence"""
        if self.pointer >= len(self.words):
            raise StopIteration
        self.pointer += 1
        return self.words[self.pointer - 1]

    def __getitem__(self, index):
        """allows for calls to indexes of words list"""
        if index < -len(self.words) or index > len(self.words) - 1:
            raise IndexError('Index out of range')
        return self.words[index]

    def __contains__(self, item):
        """allows for 'in' to be used on list of words"""
        return item.lower() in self.words

    def reset_iterator(self):
        """resets iterator to 0"""
        self.pointer = 0

    def split(self):
        """returns formatted list of sentences split by ';' or list containing one sentence if no ';' present"""
        return [self] if ';' not in self.original_text \
            else [Sentence(format_text(sentence.strip())) for sentence in self.original_text.split(';')]


if __name__ == '__main__':
    tests = [
        ("In a village of La Mancha, the name of which I have no desire to call to mind, there lived not long since"
         " one of those gentlemen that keep a lance in the lance-rack, an old buckler, a lean hack, and a greyhound"
         " for coursing."),
        ("This, however, is of but little importance to our tale; it will be enough not to stray a hair’s breadth from"
         " the truth in the telling of it.")]

    sentence_1 = Sentence(tests[0])
    mancha_count = sum([1 for word in sentence_1 if word == 'mancha'])
    sentence_2 = Sentence(tests[1])

    print(f'First test:\nThere are {len(sentence_1)} words in the sentence.')
    print(f'Number of times the word "mancha" shows up in the sentence: {mancha_count}')

    print(f'\nSecond test with semicolon sentence:')
    print(f'Original sentence: {sentence_2}')
    print(f'\nHere is the second test sentence split into two sentences:')
    for s in sentence_2.split():
        print(s)
