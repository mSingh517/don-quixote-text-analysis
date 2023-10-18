"""Interprets text as paragraphs, sentences and words.

This script takes a chapter from the book Don Quixote de la Mancha and
analyzes it to separate it in paragraphs and sentences. It provides
some basic functionality to reformat and characterize the structure of
the text.
"""

from paragraphs import Paragraph
import urllib.request
import ssl  # library to handle security in IP

INVALID_CHARS = {'_', '\u201c', '\u201d'}


def preprocess(para):
    """removes certain characters from utf-8 text file by
    including all characters in input except for invalids in
    a list. commented code below shows original slower, attempt

    :param para: paragraph input
    :return: all elements of paragraph list joined together
    """
    para_list = []
    for c in para:
        if c in INVALID_CHARS:
            continue  # skips over invalid characters
        elif c == '\u2014':
            para_list.append(' ')  # adds ' ' for every occurrence of '-'
        else:
            para_list.append(c)  # adds character from input to list if it isn't invalid
    return ''.join(para_list)
    # return para.replace('\u2014', ' ').replace('_', '').replace('\u201c', '').replace('\u201d', '')


def chapter_summary(output, paragraphs):
    """Writes first and last sentence of each paragraph to output file,
    creating a "summary" of the paragraph

    :param output: file to be written to
    :param paragraphs: object to get each paragraph from
    :return: file output
    """
    for i, para in enumerate(paragraphs):
        hidden = f'--|--  Paragraph {i + 1}: {len(para)} hidden sentences  --|--'
        output.write(f'{para[0]}\n')
        output.write(f'{"":>15}{hidden}')
        output.write(f'\n{para[-1]}\n\n')


url = "https://www.gutenberg.org/cache/epub/996/pg996.txt"
# Modifying some settings urllib.request will use.
ctx = ssl.create_default_context()
ctx.check_hostname = False  # Disables hostname checks.
ctx.verify_mode = ssl.CERT_NONE  # Disables certificate checks.
file = urllib.request.urlopen(url, context=ctx)
input_file = file.read().decode('utf-8-sig')

# stripping twice to get rid of invisible characters
lines_in_file = [line.strip() for line in input_file.strip().split('\n')]

# storing markers in text for beginning and end of first chapter
chapter_marker = lines_in_file.index('p007.jpg (150K)')
chapter_end = lines_in_file.index('p007b.jpg (61K)')
chapter_start = lines_in_file.index('Full Size', chapter_marker) + 1
chapter = lines_in_file[chapter_start:chapter_end]

# similar method to preprocess function, except at each empty line it adds empty list to list of lists
# otherwise, it adds each paragraph to the end of the list
chapter_list = [[]]
for elem in chapter:
    if elem == '':
        chapter_list.append([])
    else:
        chapter_list[-1].append(elem)

# this creates single string, removes invalid chars, and creates Paragraph objects
# for each paragraph and removes empty lists from chapter_list
paragraphs = [Paragraph(preprocess(' '.join(paragraph))) for paragraph in chapter_list if paragraph]

# storing analysis outputs for display
num_sentences = sum([len(p) for p in paragraphs])
num_words = sum([len(s) for p in paragraphs for s in p])
he_sentences = sum([1 for p in paragraphs for s in p if 'he' in s])  # number of occurrences of "he"
mancha_sentences = sum([1 for p in paragraphs for s in p if 'mancha' in s])  # number of occurrences of "mancha"


o_file = 'manchaOutput.txt'
output = open(o_file, mode='w')

output.write(f'Analysis of the chapter:'
             f'\nThe total number of paragraphs is {len(paragraphs)}.'
             f'\nThe total number of sentences is {num_sentences}.'
             f'\nThe total number of words is {num_words}.'
             f'\nThe average number of words per sentence is {num_words / num_sentences:.2f}'
             f'\nThe average number of sentences per paragraph is {num_sentences / len(paragraphs):.2f}'
             f'\nThe total number of sentences with query "he" is {he_sentences}.'
             f'\nThe total number of sentences with query "mancha" is {mancha_sentences}.')

output.write('\n\nA "summary" of the chapter follows:\n')
chapter_summary(output, paragraphs)

output.close()
