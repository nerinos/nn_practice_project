import random
import json
import os
import sys


test_sentence = 'o oo ooo oooo ooooo oooooo'
form_iter = 0


class Iterate_:
    form_iter = 0

    def next_(self):
        self.form_iter += 1

    def print(self):
        print(self.form_iter)


class Iterate:
    length = 0
    iterate = 0
    current = 1
    max = 100

    def __init__(self, length):
        print('[', end='')
        self.length = length
        self.iterate = 0
        self.current = 1
        self.max = 100

    def next_(self):
        self.iterate += 1
        if self.iterate >= round((self.current * (self.length - 1)) / self.max):
            self.current += 1
            print('=', end='')
        if self.iterate >= self.length:
            print('=]')
            return True
        return False


common_mistakes = [['then', 'than'], ['lose', 'loose'], ['their', 'there', 'they are'], ['to', 'too'], ['your', 'you are'],
                   ['which', 'who', 'that', 'what'], ['since', 'for'], ['work', 'job'], ['am', 'is', 'are'], ['in', 'at', 'on'],
                   ['a', 'an', 'the'], ['as', 'like'], ['gone', 'went'], ['watch', 'look', 'see'], ['among', 'between']]


def common_find(source, target):
    for i in range(len(source)):
        for j in range(len(source[i])):
            if source[i][j] == target:
                return i
    return -1


# shuffle words in sentence
# takes sentence='str' and probe_a as chance to swap words
def word_shuffling(sentence, probe_a):
    word_list = sentence.split()

    if len(word_list) <= 3:
        return sentence

    trash_swap = [round(1000 * probe_a), 1000]

    for i in range(len(word_list)):
        random.seed()
        if random.randint(0, trash_swap[1]) <= trash_swap[0] and len(word_list) > 3:
            rand = random.randint(-1, 1)
            if i + rand >= len(word_list) - 1 or i + rand < 0:
                rand *= -1
            word_list[i], word_list[i + rand] = word_list[i + rand], word_list[i]

    # print('\n', sentence, '\n', [' '.join(word_list)][0], '\n')
    return [' '.join(word_list)][0]


# changes word's form in given sentence
# takes probe_a as chance to change word
# and mistakes_list as list of common_mistakes
def word_form_changer(sentence, probe_a, mistakes_list):
    word_list = sentence.split()

    trash_change = [round(1000 * probe_a), 1000]

    for i in range(len(word_list)):
        random.seed()
        position = common_find(mistakes_list, word_list[i])
        if position != -1 and random.randint(0, trash_change[1]) <= trash_change[0]:
            word_list[i] = mistakes_list[position][random.randint(0, len(mistakes_list[position]) - 1)]
    return [' '.join(word_list)][0]


# shuffle letter in each word of given sentence
# takes probe_a as chance to swap letters for each word
def letter_shuffling(sentence, probe_a):
    word_list = sentence.split()
    trash_swap = [round(1000 * probe_a), 1000]

    result = []
    for word in word_list:
        random.seed()
        res = word
        if random.randint(0, trash_swap[1]) <= trash_swap[0] and len(word) > 2:
            rand = random.randint(0, len(word)-2)
            res = word[:rand] + word[rand+1] + word[rand] + word[rand+2:]
        result.append(res)

    # print('\n', sentence, '\n', [' '.join(result)][0], '\n')
    return [' '.join(result)][0]


# finds letter for given letter, basing on letter_map
# takes char and dict
def generate(source_letter, letter_map):
    try:
        list_ = letter_map[source_letter] + source_letter
    except KeyError:
        return source_letter
    random.seed()
    rand = random.randint(0, len(list_))

    # for deleting letter
    if rand == len(list_):
        return ''
    return list_[rand]


# creating noise in given sentence (add, replace, delete)
# takes probe_a as chance to do smth with letter probe_b as chance to add instead replace
# gives new sentence as result
def sentence_letter_noise(sentence, probe_a, probe_b, space_delete=False):
    sentence = sentence.lower()
    keyboard_map = {'q': 'wsa', 'w': 'edsaq', 'e': 'rfdsw', 'r': 'tgfde', 't': 'yhgfr', 'y': 'ujhgt', 'u': 'ikjhy', 'i': 'olkju', 'o': 'plki', 'p': 'lo',
                    'a': 'qwsxz', 's': 'wedxza', 'd': 'rfcxse', 'f': 'rtgvcd', 'g': 'tyhbvf', 'h': 'yujnbg', 'j': 'uikmnh', 'k': 'iolmj', 'l': 'kop',
                    'z': 'asx', 'x': 'zsdc', 'c': 'xdfv', 'v': 'cfgb', 'b': 'vghn', 'n': 'bhjm', 'm': 'njk'}

    trash_letter = [round(1000*probe_a), 1000]
    trash_add = [round(1000*probe_b), 1000]

    result_ = ''
    for i in range(len(sentence)):
        if sentence[i] == ' ':
            if space_delete and random.randint(0, trash_letter[1]) <= trash_letter[0]:
                continue
            else:
                result_ += ' '
                continue
        if random.randint(0, trash_letter[1]) <= trash_letter[0]:
            temp_1 = random.randint(0, trash_add[1])
            generated = generate(sentence[i], keyboard_map)

            if temp_1 <= trash_add[0]:
                if temp_1 % 2 == 0:
                    result_ += sentence[i] + generated
                else:
                    result_ += generated + sentence[i]
            else:
                result_ += generated

        else:
            result_ += sentence[i]

    return result_


# creates data for dataset with taken file_name of text file
# takes multiplier as one of coefficient to increase number of samples
# and max_spaces as permissible value of words in one sentence
def create_dataset(file_name, multiplier, max_spaces, limit):
    data = []
    sentences = parse_(file_name, limit)
    iterat = Iterate(len(sentences))

    for sen in sentences:
        if sen.count(' ') <= max_spaces:
            for i in range(multiplier):
                # data_1 = [[sen, sentence_letter_noise(sen, 0.01, 0.1)], [sen, sentence_letter_noise(sen, 0.3, 0.3)], [sen, sentence_letter_noise(sen, 0.01, 0.5)], [sen, sentence_letter_noise(sen, 0.2, 0.5)],
                #           [sen, word_shuffling(sen, 0.2)], [sen, word_shuffling(sen, 0.3)], [sen, word_shuffling(sentence_letter_noise(sen, 0.01, 0.1), 0.2)], [sen, word_shuffling(sentence_letter_noise(sen, 0.2, 0.5), 0.2)],
                #           [sen, letter_shuffling(sen, 0.2)], [sen, letter_shuffling(sen, 0.5)],
                #           [sen, word_form_changer(sen, 0.5, common_mistakes)], [sen, word_form_changer(sen, 0.9, common_mistakes)]]
                data_1 = [[sen, letter_shuffling(sentence_letter_noise(word_shuffling(word_form_changer(sen, 0.2, common_mistakes), 0.1), 0.1, 0.2), 0.1)],
                          [sen, letter_shuffling(sentence_letter_noise(word_shuffling(word_form_changer(sen, 0.1, common_mistakes), 0.08), 0.08, 0.3), 0.05)]]
                for temp_ in data_1:
                    if temp_[0] != temp_[1] and temp_[0].count(' ') <= max_spaces:
                        data.append(temp_)
        if iterat.next_():
            break

    print('file: ', file_name)
    print('dataset size: ', len(data), '\n')
    return data


# just find minimum without excluding values = -1
def find_min(list_):
    min_ = 10000
    for obj in list_:
        if obj != -1 and obj < min_:
            min_ = obj
    return min_


# parser
# changes data to more comfortable operations
def parse_(file_name, limit):
    if file_name[0:4] == 'wiki':
        f = open(file_name, 'r', encoding='utf-8')
    else:
        f = open(file_name, 'r')

    lines = f.readlines()
    line_temp = ''
    sentences = []
    iterat = Iterate(round(len(lines) * limit))

    for line in lines:

        dot_pos = [line_temp.find(str_) for str_ in """.?![]("""]
        if iterat.next_():
            return sentences

        if dot_pos != [-1]*len(dot_pos):
            min_ = find_min(dot_pos)
            sentences.append(line_temp[0:min_].lower().strip(' '))
            line_temp = line_temp[min_+1:]
            continue
        if line != '\n' and line.find('\\u') == -1:
            line_temp += line.replace("\\\'94", '').replace("\\\'93", '').replace("\\\'92", '').replace("\\\'91", '').\
                replace("\\", ' ').replace("\n", ' ').replace('--', ' ').replace('=', '').replace('@.@', '').\
                replace('@,@', '').replace('@-@', '').replace('   ', '').replace('  ', ' ').replace('  ', ' ').replace('\'s', 's')

    return sentences


# main function
# uses all files in path "book" for dataset creating
# takes max_spaces as permissible value of words in one sentence
# and multiplier as one of coefficient to increase number of samples
def books_to_dataset(max_spaces, multiplier, limit):
    books = os.listdir('books')
    data_ = []
    for book in books:
        data_ += create_dataset('books/' + book, multiplier, max_spaces, limit)
    print('whole dataset size: ', len(data_))
    with open("dataset_shuffle_v3.json", "w") as write_file:
        json.dump(data_, write_file)


# calculating maximum number of word in sentence from dataset
def count_max():
    with open("dataset_books_99.json", "r") as read_file:
        data = json.load(read_file)
        max_ = 0
        counter = 0
        for temp in data:
            temp_count = temp[0].count(' ')
            if temp_count <= 2:
                counter += 1
            if max_ < temp_count:
                max_ = temp_count
                print(max_, '\n', temp[0], '\n\n')
        print(max_)
        print(counter)


# deletes all sentences having more than n words
def clean_dataset(n):
    result = []
    with open("dataset_shuffle.json", "r") as read_file:
        data = json.load(read_file)
        for temp in data:
            if temp[0].count(' ') <= n:
                result.append(temp)

    print('result dataset size: ', len(result))
    with open("dataset_books_"+str(n)+".json", "w") as write_file:
        json.dump(result, write_file)


# creates dataset based on wikipedia_103
def wiki_parser(max_spaces, multiplier, limit):
    wiki = os.listdir('wiki')
    data_ = []
    for article in wiki:
        data_ += create_dataset('wiki/' + article, multiplier, max_spaces, limit)
    print('whole dataset size: ', len(data_))
    with open("wiki_shuffle_v2.json", "w") as write_file:
        json.dump(data_, write_file)


# shuffles data between wiki and book
# and concatenate it in one dataset
def dataset_shuffle():
    with open("wiki_shuffle_v2.json", "r") as read_file_w:
        data_wiki = json.load(read_file_w)

    with open("dataset_shuffle_v2.json") as read_file_b:
        data_books = json.load(read_file_b)

    data = []
    data.extend(data_wiki)
    data.extend(data_books)
    random.shuffle(data)
    data = data[1:1200000]
    with open("wiki_books_shuffle.json", "w") as write_file:
        json.dump(data, write_file)


# checking sizes of dataset
# with open("wiki_books_shuffle.json") as read_file:
#     data = json.load(read_file)
#     print(len(data))

books_to_dataset(40, 1, 0.2)
print(form_iter)