import random
import json
import os

test_sentence = 'o oo ooo oooo ooooo oooooo'


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


# shuffle letter in each word of given sentence
# takes probe_a as chanse to swap letters for each word
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
def sentence_noise(sentence, probe_a, probe_b, space_delete=False):
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
def create_dataset(file_name, multiplier, max_spaces):
    data = []
    sentences = parse_(file_name)
    for sen in sentences:
        if sen.count(' ') <= max_spaces:
            for i in range(multiplier):
                data_1 = [[sen, sentence_noise(sen, 0.01, 0.1)], [sen, sentence_noise(sen, 0.3, 0.3)], [sen, sentence_noise(sen, 0.01, 0.5)], [sen, sentence_noise(sen, 0.2, 0.5)],
                          [sen, word_shuffling(sen, 0.2)], [sen, word_shuffling(sen, 0.3)], [sen, word_shuffling(sentence_noise(sen, 0.01, 0.1), 0.2)], [sen, word_shuffling(sentence_noise(sen, 0.2, 0.5), 0.2)],
                          [sen, letter_shuffling(sen, 0.2)], [sen, letter_shuffling(sen, 0.5)]]
                for temp_ in data_1:
                    if temp_[0] != temp_[1] and temp_[0].count(' ') <= max_spaces:
                        data.append(temp_)
    print('\nfile: ', file_name)
    print('dataset size: ', len(data))
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
def parse_(file_name):
    f = open(file_name, 'r')
    line_temp = ''
    sentences = []
    for line in f.readlines():
        dot_pos = [line_temp.find(str_) for str_ in """.?![]()"'"""]

        if dot_pos != [-1]*len(dot_pos):
            min_ = find_min(dot_pos)
            sentences.append(line_temp[0:min_].lower().strip(' '))
            line_temp = line_temp[min_+1:]
            continue
        if line != '\n':
            line_temp += line.replace("\\\'94", '').replace("\\\'93", '').replace("\\\'92", '').replace("\\\'91", '').replace("\\", ' ').replace("\n", ' ').replace('--', ' ').replace('   ', '').replace('  ', ' ').replace('  ', ' ')

    return sentences


# main function
# uses all files in path "book" for dataset creating
# takes max_spaces as permissible value of words in one sentence
# and multiplier as one of coefficient to increase number of samples
def books_to_dataset(max_spaces, multiplier):
    books = os.listdir('books')
    data_ = []
    for book in books:
        data_ += create_dataset('books/' + book, multiplier, max_spaces)
    print('whole dataset size: ', len(data_))
    with open("dataset_shuffle_v2.json", "w") as write_file:
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


books_to_dataset(40, 2)

