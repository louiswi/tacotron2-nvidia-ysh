import re

# big abbreviation
_single_word_list = [
  ('A', 'ai'), ('B', 'bee'), ('C','cee'), ('D','dee'), ('E','eee'), ('F', 'ef'), ('G', 'gee'),
  ('H', 'ech'), ('I', 'eye'), ('J','jje'), ('K', 'kay'), ('L', 'el'), ('M', 'emm'), ('N', 'en'),
  ('O', 'oo'), ('P', 'pee'), ('Q', 'qeu'),
  ('R', 'ar'), ('S', 'aas'), ('T', 'tee'),
  ('U', 'you'), ('V', 'vee'), ('W', 'dabeyou'), ('X', 'eks'), ('Y', 'wi'), ('Z', 'zee'),
  ('.', ''), 
  ('0', 'zero'), ('1', 'one'), ('2', 'two'), ('3', 'three'), ('4', 'four'), ('5', 'five'),
  ('6', 'six'), ('7', 'seven'), ('8', 'eight'), ('9', 'nine')
]

_single_word_dict = dict((k, v) for k, v in _single_word_list)

_single_word_re = re.compile('|'.join([k for k, v in _single_word_list]))

_single_word_ignore_case_re = re.compile('|'.join([k for k, v in _single_word_list]), flags=re.IGNORECASE)

_big_abbreviations_re = re.compile(r'\b(?:[A-Za-z]\.)+[A-Za-z]?\b') # first is no dot, second is with dot

def split_word_to_single_charactor(word):
  word = re.sub(_single_word_ignore_case_re, lambda match: ' ' + _single_word_dict[match.group().upper()] + ' ', word)
  return word

def expand_big_abbreviations(text):
  return re.sub(_big_abbreviations_re,
                lambda match: ' '.join([split_word_to_single_charactor(single_word) for single_word in match.group()]),
                text)

if __name__ == "__main__":
    print(expand_big_abbreviations("i come from u.e.a it is a good place"))
    print(expand_big_abbreviations("i come from U.A.E it is a good place"))
    print(expand_big_abbreviations("i come from .u.e.a it is a good place"))
    print(expand_big_abbreviations("i come from u.e.a. it is a good place"))
    print(expand_big_abbreviations("i come from .u.e.a. it is a good place"))
    print(expand_big_abbreviations("i come from su.e.a. it is a good place"))
    print(expand_big_abbreviations("i come from ..u.e.a. it is a good place"))

