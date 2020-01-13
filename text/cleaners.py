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
import emojis
import re
from unidecode import unidecode
from .numbers import normalize_numbers

# Regular expression matching whitespace:
_whitespace_re = re.compile(r'\s+')

# List of (regular expression, replacement) pairs for abbreviations:
_abbreviations = [(re.compile('\\b%s\\.' % x[0], re.IGNORECASE), x[1]) for x in [
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
]]

_compute_marks = [(re.compile('%s' % x[0], re.IGNORECASE), x[1]) for x in [
  ('(\d)%', '\1 percent'),
  ('(\d)\s*\+\s*(\d)', '\1 plus \2'),
  ('(\d)\s*\+\s*(\d)', '\1 minus \2'),
  ('(\d)\s*/\s*(\d)', '\1 slash \2'),
  ('(\d)\s*=\s*(\d)', '\1 equals \2'),
  ('(\d)\s*\*\s*(\d)', '\1 times \2'),

]]

_zero_to_nine_re = [(re.compile('%s' % x[0]), x[1]) for x in [
  ('0', ' zero '),
  ('1', ' one '),
  ('2', ' two '),
  ('3', ' three '),
  ('4', ' four '),
  ('5', ' five '),
  ('6', ' six '),
  ('7', ' seven '),
  ('8', ' eight '),
  ('9', ' nine '),
]]

_emoji_pattern = re.compile("["
                             u"\U0001F600-\U0001F64F"  # emoticons
                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            u"\U00002702-\U000027B0"
                             u"\U000024C2-\U0001F251"
                             "]+", flags=re.UNICODE)

# numbers more than five digits will replace one by one
_mobile_number_re = re.compile(r'\d{5,}')

def dealwith_emoji(string, mode="decode"):
  mode_choices = ['decode', 'remove']
  if mode not in mode_choices:
    raise ValueError("Invalid mode type. Expected one of: %s" % mode_choices)

  if mode == "decode": # decode with emojis package
    return emojis.decode(string)
  else: # remove with pattern
    return re.sub(_emoji_pattern, r'', string)

def expand_abbreviations(text):
  for regex, replacement in _abbreviations:
    text = re.sub(regex, replacement, text)
  return text

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

def expand_mobile_numbers(text):
  while True:
    item = re.search(_mobile_number_re, text)
    if item is None:
      break
    mobile_text = item.group()
    for regex, replacement in _zero_to_nine_re:
      mobile_text = re.sub(regex, replacement, mobile_text)
    text = text[:item.start()] + " " + mobile_text + " " + text[item.end():]
  return text

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
  text = lowercase(text)
  text = expand_compute_marks(text)
  text = expand_mobile_numbers(text)
  text = expand_numbers(text)
  text = expand_abbreviations(text)
  text = collapse_whitespace(text)
  text = add_end_punctuation(text)
  return text