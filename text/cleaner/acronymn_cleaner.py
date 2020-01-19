import re
import time
import string
from pathlib import Path
import os
from mylogger import logger
from text.cleaner.big_abbreviations_cleaner import split_word_to_single_charactor
import uuid


def _load_dict_from_file():
    current_dir = Path(__file__).resolve().parent
    t1 = time.time()
    acronymn_list = []
    print(os.getcwd())
    with open(current_dir / 'wikipedia-acronyms-simple.json', 'r') as f:
        while True:
            text = f.readline()
            if text == '':
                break
            acronymn_list.append(text.strip())

    logger.debug(f'load acronymn dict use time {time.time() - t1}')
    return acronymn_list


_acronymn_list = _load_dict_from_file()

_acronymn_set = set(_acronymn_list)

_acronymn_re = re.compile('|'.join(_acronymn_set))


def expand_acronymn_old(text):
    return_text_list = []
    for word in re.split(rf'([{string.punctuation}\s])', text): # use () to keep seperator
        if word in _acronymn_set:
            return_text_list.append(split_word_to_single_charactor(word))
        else:
            return_text_list.append(word)
    return ' '.join(return_text_list)

def expand_acronymn(text):
    # use () to keep seperator, do not split by ' cause this is usually a word
    seperate_marks = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\s'
    return ''.join([split_word_to_single_charactor(word) if word in _acronymn_set else word
                    for word in re.split(rf'([{seperate_marks}])', text)])

def remove_from_set(acronymn_set, text):
    f = open('checked_saved.txt', 'r')
    saved_set = set()
    while True:
        word = f.readline()
        if word == '':
            break
        saved_set.add(word.strip())
    f.close()

    f = open('checked_saved.txt', 'a')

    stop = False
    word_set = set()
    for word in re.split(rf'[{string.punctuation}\s]', text):
        word_set.add(word)

    for word in word_set:
        if len(word) == 1:
            continue
        if word not in saved_set and word in acronymn_set:
            print(f'[FIND ACRONYMN]: {word}')
            while True:
                k = input('do you want this word read as one word, that is modify the file? press Y or N: ')

                if k == 'y':
                    acronymn_set.remove(word)
                    break
                elif k == 'n':
                    f.write(f'{word}\n')
                    break
                elif k == 'exit':
                    stop = True
                    break
                else:
                    continue

        if stop == True:
            f.close()
            return acronymn_set, True

    f.close()
    return acronymn_set, False

def save_set(acronymn_set):
    with open(f"{uuid.uuid1()}.txt", "w") as f:
        for word in acronymn_set:
            f.write(f'{word}\n')

def optimize_dict():
    acronymn_set = _acronymn_set
    ori_len = len(acronymn_set)
    while True:
        text = input("================================== please input remove text:    ")

        if text == 'exit':
            save_set(acronymn_set)
            print(f'ori_len {ori_len}, current len {len(acronymn_set)}, removed {ori_len - len(acronymn_set)}')
            break

        acronymn_set, stopped = remove_from_set(acronymn_set, text.upper())

        if stopped:
            save_set(acronymn_set)
            print(f'ori_len {ori_len}, current len {len(acronymn_set)}, removed {ori_len - len(acronymn_set)}')
            break

if __name__ == "__main__":
    times = 10000

    t2 = time.time()
    for _ in range(times):
        if 'UAE' in _acronymn_set:
            a = 1
    print(time.time() - t2)

    t3 = time.time()
    for _ in range(times):
        if 'UAE' in _acronymn_list:
            a = 1
    print(time.time() - t3)


    t3 = time.time()
    for _ in range(times):
        if re.match(_acronymn_re, 'UAE'):
            a = 1
    print(time.time() - t3)

    t4 = time.time()
    print(expand_acronymn("Xi's ability to control dissent far outweighs Putin's, however. Since reaching the top of the Communist Party, Xi has tightened internal discipline, using an anti-corruption campaign to root out bad actors and -- critics say -- go after potential challengers. He also has a colossal propaganda apparatus to rally support around him in times of challenge, and faces no opposition outside of the CCP, nor even the chance that such a figure could arise without a radical transformation in the way China operates".upper()))
    print(time.time() - t4)

    t5 = time.time()
    for _ in range(times):
        expand_acronymn("you're my friend".upper())
    print(time.time() - t5)

    t6 = time.time()
    for _ in range(times):
        expand_acronymn_old("you're my friend".upper())
    print(time.time() - t6)
