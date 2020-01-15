""" from https://github.com/keithito/tacotron """

'''
Cleaners are transformations that run over the input text at both training and eval time.

Cleaners can be selected by passing a comma-delimited list of cleaner names as the "cleaners"
hyperparameter. Some cleaners are English-specific. You'll typically want to use:
  1. "english_cleaners" for English text
  2. "transliteration_cleaners" for non-English text that can be transliterated to ASCII using
     the Unidecode library (https://pypi.python.org/pypi/Unidecode)
  3. "basic_cleaners" if you do not want to transliterate (in this case, you should also update
     the symbols in symbols.py to match your data).
'''
import emoji
import re
from unidecode import unidecode
from .numbers import normalize_numbers

# Regular expression matching whitespace:
_whitespace_re = re.compile(r'\s+')

# List of (regular expression, replacement) pairs for abbreviations:
_abbreviations_list = [
  ('mrs', 'misess'),
  ('mr', 'mister'),
  ('dr', 'doctor'),
  ('st', 'saint'),
  ('co', 'company'),
  ('jr', 'junior'),
  ('maj', 'major'),
  ('gen', 'general'),
  ('drs', 'doctors'),
  ('rev', 'reverend'),
  ('lt', 'lieutenant'),
  ('hon', 'honorable'),
  ('sgt', 'sergeant'),
  ('capt', 'captain'),
  ('esq', 'esquire'),
  ('ltd', 'limited'),
  ('col', 'colonel'),
  ('ft', 'fort'),
  ('Sen', 'senate')
]

_compute_marks_list = [
  (r'(\d)%', r'\1 percent'),
  (r'(\d)\s*\+\s*(\d)', r'\1 plus \2'),
  (r'(\d)\s*\+\s*(\d)', r'\1 minus \2'),
  (r'(\d)\s*/\s*(\d)', r'\1 slash \2'),
  (r'(\d)\s*=\s*(\d)', r'\1 equals \2'),
  (r'(\d)\s*\*\s*(\d)', r'\1 times \2'),

]

_single_word_list = [
  ('A', 'ai'), ('B', 'bee'), ('C','cee'), ('D','dee'), ('E','eee'), ('F', 'ef'), ('G', 'gee'),
  ('H', 'ech'), ('I', 'iee'), ('J','jje'), ('K', 'kay'), ('L', 'el'), ('M', 'emm'), ('N', 'en'),
  ('O', 'o'), ('P', 'pee'), ('Q', 'qeu'),
  ('R', 'ar'), ('S', 'aas'), ('T', 'tee'),
  ('U', 'you'), ('V', 'vee'), ('W', 'dabeyou'), ('X', 'eks'), ('Y', 'wi'), ('Z', 'zee'),
  ('.', '')
]

_single_word_dict = dict((k, v) for k, v in _single_word_list)

_single_word_re = re.compile('|'.join([k for k, v in _single_word_list]))

_single_word_ignore_case_re = re.compile('|'.join([k for k, v in _single_word_list]), flags=re.IGNORECASE)

# big abbreviation

_big_abbreviations_re = re.compile(r'\b[A-Z]*\b|\b(?:[A-Z]\.)+[A-Z]?\b') # first is no dot, second is with dot

# abbreviation

_abbreviations = [(re.compile(r'\b%s\.' % x[0], re.IGNORECASE), x[1]) for x in _abbreviations_list]

_abbreviations_dict = dict((item[0], item[1]) for item in _abbreviations_list)

_abbreviations_re = re.compile('|'.join([f"\\b{item}\\." for item in _abbreviations_dict.keys()]))


# compute marks

_compute_marks = [(re.compile(r'%s' % x[0]), r'%s' % x[1]) for x in _compute_marks_list]


# number
_zero_to_nine_list = \
  [('0', ' zero '),
  ('1', ' one '),
  ('2', ' two '),
  ('3', ' three '),
  ('4', ' four '),
  ('5', ' five '),
  ('6', ' six '),
  ('7', ' seven '),
  ('8', ' eight '),
  ('9', ' nine '),
]

_zero_to_nine_dict = dict((k, v) for k, v in _zero_to_nine_list)

_zero_to_nine_re = [(re.compile('%s' % x[0]), x[1]) for x in _zero_to_nine_list]

# numbers more than five digits will replace one by one
_mobile_number_re = re.compile(r'\d{5,}')

# emoji
_emoji_pattern = re.compile("["
                             u"\U0001F600-\U0001F64F"  # emoticons
                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            u"\U00002702-\U000027B0"
                             u"\U000024C2-\U0001F251"
                             "]+", flags=re.UNICODE)

# URl

def split_word_to_single_charactor(word):
  word = re.sub(_single_word_ignore_case_re, lambda match: ' ' + _single_word_dict[match.group().upper()] + ' ', word)
  return word

_url_re = re.compile(r"\b(https?://(?:[\w]+)(?:\.[\w\-]+)+)(?::\d*)?(?:/[^/ ]*)*\b", flags=re.IGNORECASE)

_url_replace_word_list = [
  ("/", " slash "),
  ("https", split_word_to_single_charactor('https')),
  ("http", split_word_to_single_charactor('http')),
  ('cn', split_word_to_single_charactor('cn')),
  ('www', split_word_to_single_charactor('www')),
  (':', ''),
  ('github', 'git hub'),
  ('gmail', 'gee mail'),
]

_url_replace_word_dict = dict((k, v) for k, v in _url_replace_word_list)

_url_replace_word_re = re.compile("|".join([k for k,v in _url_replace_word_list]), flags=re.IGNORECASE)


# email

_email_re = re.compile(r'[\.\w]+@\w+?(?:\.\w+)+', flags=re.IGNORECASE)

def dealwith_emoji(string, mode="decode"):
  mode_choices = ['decode', 'remove']
  if mode not in mode_choices:
    raise ValueError("Invalid mode type. Expected one of: %s" % mode_choices)

  if mode == "decode": # decode with emojis package
    return emoji.demojize(string)
  else: # remove with pattern
    return re.sub(_emoji_pattern, r'', string)

def expand_email(text):
  return re.sub(_email_re, lambda match: deal_with_email(match.group()), text)

def deal_with_email(text):
  text = text.replace('@', ' at ').replace('.', ' dot ')
  return re.sub(_url_replace_word_re, lambda match: _url_replace_word_dict[match.group().lower()], text)

def expand_url(text):

  return re.sub(_url_re, lambda match: deal_with_main_url(match.group()), text)

def deal_with_main_url(url):
  prefix = url.split('//')[0]
  main_name = '//'.join(url.split('//')[1:]).split('/')[0]
  main_url = prefix + '//' + main_name
  main_url = re.sub(r'\.', ' dot ', main_url)
  return re.sub(_url_replace_word_re, lambda match: _url_replace_word_dict[match.group().lower()], main_url)


def expand_big_abbreviations(text):
  return re.sub(_big_abbreviations_re,
                lambda match: ' '.join([_single_word_dict[single_word] for single_word in match.group()]),
                text)

def expand_abbreviations_old(text):
  for regex, replacement in _abbreviations:
    text = re.sub(regex, replacement, text)
  return text

def expand_abbreviations(text):
  text = re.sub(_abbreviations_re, lambda match: _abbreviations_dict[match.group(0)[:-1]]+" ", text)
  return text

# can not do as expand abbreviation use one regex to group multi regexs
def expand_compute_marks(text):
  for regex, replacement in _compute_marks:
    text = re.sub(regex, replacement, text)
  return text

def add_end_punctuation(text):
  # if nothing in the text, just add stop mark
  if text == '':
    return 'Empty Text. Please Check.'
  return re.sub('([^\.\,\?\:\;])$', r'\1.', text)

def expand_numbers(text):
  return normalize_numbers(text)

def expand_mobile_numbers_old(text):
  while True:
    item = re.search(_mobile_number_re, text)
    if item is None:
      break
    mobile_text = item.group()
    for regex, replacement in _zero_to_nine_re:
      mobile_text = re.sub(regex, replacement, mobile_text)
    text = text[:item.start()] + " " + mobile_text + " " + text[item.end():]
  return text

def expand_mobile_numbers(text):
  return re.sub(_mobile_number_re, lambda match: ' '.join([_zero_to_nine_dict[item] for item in match.group(0)]), text)

def lowercase(text):
  return text.lower()

def collapse_whitespace(text):
  return re.sub(_whitespace_re, ' ', text).strip()


def convert_to_ascii(text):
  return unidecode(text)


def basic_cleaners(text):
  '''Basic pipeline that lowercases and collapses whitespace without transliteration.'''
  text = lowercase(text)
  text = collapse_whitespace(text)
  return text


def transliteration_cleaners(text):
  '''Pipeline for non-English text that transliterates to ASCII.'''
  text = convert_to_ascii(text)
  text = lowercase(text)
  text = collapse_whitespace(text)
  return text


def english_cleaners(text):
  '''Pipeline for English text, including number and abbreviation expansion.'''
  text = convert_to_ascii(text)
  text = lowercase(text)
  text = expand_numbers(text)
  text = expand_abbreviations(text)
  text = collapse_whitespace(text)
  return text

def english_punctuation_cleaners(text):
  '''Pipeline for English text, including number and abbreviation and punctuation_expansion.'''
  text = convert_to_ascii(text)
  text = lowercase(text)
  text = expand_numbers(text)
  text = expand_abbreviations(text)
  text = expand_compute_marks(text)
  text = collapse_whitespace(text)
  text = add_end_punctuation(text)
  return text

def english_punctuation_emoji_cleaners(text):
  '''Pipeline for English text, including number, abbreviation and punctuation_expansion. and dealwith emoji'''
  text = dealwith_emoji(text)
  text = convert_to_ascii(text)
  text = lowercase(text)
  text = expand_numbers(text)
  text = expand_abbreviations(text)
  text = expand_compute_marks(text)
  text = collapse_whitespace(text)
  text = add_end_punctuation(text)
  return text

def enhanced_english_cleaners(text):
  '''Pipeline for English text, including number, abbreviation and punctuation_expansion. and dealwith emoji'''
  text = dealwith_emoji(text)
  text = convert_to_ascii(text)
  text = expand_email(text)
  text = expand_url(text) # expand url before big_abbreviation, cause url may contains big_abbreviation
  text = expand_big_abbreviations(text)
  text = lowercase(text)
  text = expand_compute_marks(text)
  text = expand_mobile_numbers(text)
  text = expand_numbers(text)
  text = expand_abbreviations(text)
  text = collapse_whitespace(text)
  text = add_end_punctuation(text)
  return text