"""Interprets text as words, sentences, and paragraphs

This script takes a string and separates it into sentences based on certain punctuation
and allows sentences to be iterated through and indexed using magic methods
"""

from sentences import Sentence

SENTENCE_DELIMITERS = {'.', '?', '!'}


def list_combine(text: list):
    """this function combines a list of lists into one list

    :param text: list of lists to be flattened into one
    :return: single list containing all original elements
    """
    return [  # formatted to show nested for loops
        e
        for elem in text
        for e in elem
    ]


def parse_sentences(text: str, delimiters):
    """This function takes an input string and splits it into sentences
    at certain delimiters and appends the delimiter back onto each sentence
    Below is an example of what this function produces.
    First, it turns each character in a sentence to an element in a list, with each list being a sentence
    After joining, each list becomes a sentence string in the list
        Example input: (note tandem '!!') 'Hello!! How are you? I am well. Bye.'

        Generated before return:
        ['H', 'e', 'l', 'l', 'o', '!']
        ['!']
        [' ', 'H', 'o', 'w', ' ', 'a', 'r', 'e', ' ', 'y', 'o', 'u', '?']
        [' ', 'I', ' ', 'a', 'm', ' ', 'w', 'e', 'l', 'l', '.']
        [' ', 'B', 'y', 'e', '.']
        []

        Generated after return:
        Hello!
        How are you?
        I am well.
        Bye.


    :param text: input string to be separated into sentences
    :param delimiters: set of certain characters to use when splitting sentences (set allows for dealing with tandems)
    :return: list of sentences with correct punctuation
    """
    sentence_list = [[]]
    for char in text:
        if char in delimiters:
            sentence_list[-1].append(char)  # places delimiter punctuation back at end of sentence
            sentence_list.append([])
        else:
            sentence_list[-1].append(char)  # each letter in sentence gets added to list in list

    # if statement at end of comprehension deals with extra elements created from tandem punctuation
    return [''.join(sentence).strip() for sentence in sentence_list if len(sentence) > 1]


class Paragraph:
    """Creates paragraph object from string

    Attributes: text - original text input, sentences - text split into sentences to be processed,
    pointer for __iter__
    Methods: constructor generates list of sentence objects to be processed, __len__ gets # of sentences
    __str__ returns the original string, __iter__ and __next__ allow for loop processing of sentences
    __getitem__ allows index calls on paragraph
    """
    def __init__(self, text):
        """sets up text and separates it into sentence objects, also sets up pointer for __iter__"""
        self.full_text = text
        self.pointer = 0
        parsed_sentences = parse_sentences(self.full_text, SENTENCE_DELIMITERS)
        self.sentences = list_combine([Sentence(elem).split() for elem in parsed_sentences])

    def __len__(self):
        """gets number of sentences in sentences list"""
        return len(self.sentences)

    def __str__(self):
        """returns original text"""
        return self.full_text

    def __iter__(self):
        """sets up pointer for starting point for __next__"""
        self.pointer = 0
        return self

    def __next__(self):
        """iterates through sentences in sentence list"""
        if self.pointer >= len(self.sentences):
            raise StopIteration
        self.pointer += 1
        return self.sentences[self.pointer - 1]

    def __getitem__(self, index):
        """allows for calls to indexes of sentences list"""
        if index < -len(self.sentences) or index > len(self.sentences) - 1:
            return None
        return self.sentences[index]


if __name__ == '__main__':
    small_test = Paragraph('Hello! How are you?? I am well. Bye.')
    for s in small_test.sentences:
        print(s)

    print(f'\n-----------------------------------------\n')

    test_par = """Many an argument did he have with the curate of his village (a learned man, and a graduate of 
    Siguenza) as to which had been the better knight, Palmerin of England or Amadis of Gaul. Master Nicholas, 
    the village barber, however, used to say that neither of them came up to the Knight of Phœbus, and that if there 
    was any that could compare with him it was Don Galaor, the brother of Amadis of Gaul, because he had a spirit 
    that was equal to every occasion, and was no finikin knight, nor lachrymose like his brother, while in the matter 
    of valour he was not a whit behind him. In short, he became so absorbed in his books that he spent his nights 
    from sunset to sunrise, and his days from dawn to dark, poring over them; and what with little sleep and much 
    reading his brains got so dry that he lost his wits. His fancy grew full of what he used to read about in his 
    books, enchantments, quarrels, battles, challenges, wounds, wooings, loves, agonies, and all sorts of impossible 
    nonsense; and it so possessed his mind that the whole fabric of invention and fancy he read of was true, 
    that to him no history in the world had more reality in it. He used to say the Cid Ruy Diaz was a very good 
    knight, but that he was not to be compared with the Knight of the Burning Sword who with one back-stroke cut in 
    half two fierce and monstrous giants. He thought more of Bernardo del Carpio because at Roncesvalles he slew 
    Roland in spite of enchantments, availing himself of the artifice of Hercules when he strangled Antæus the son of 
    Terra in his arms. He approved highly of the giant Morgante, because, although of the giant breed which is always 
    arrogant and ill-conditioned, he alone was affable and well-bred. But above all he admired Reinaldos of 
    Montalban, especially when he saw him sallying forth from his castle and robbing everyone he met, and when beyond 
    the seas he stole that image of Mahomet which, as his history says, was entirely of gold. To have a bout of 
    kicking at that traitor of a Ganelon he would have given his housekeeper, and his niece into the bargain. """

    par_check = Paragraph(test_par)
    total_words = sum([len(item) for item in par_check])

    print(f'There are {len(par_check)} sentences in the paragraph.')
    print(f'There are {total_words} words in the paragraph.')
    print('\nThe first word for each sentence is as follows:')

    for num, item in enumerate(par_check, start=1):
        print(f'Sentence {num}) {item[0]}')

    print(f'\n-----------------------------------------\n')

    for s in parse_sentences('Hello!! How are you? I am well. Bye.', SENTENCE_DELIMITERS):
        print(s)
