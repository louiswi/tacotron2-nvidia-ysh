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
from text.cleaner import *

# Regular expression matching whitespace:
_whitespace_re = re.compile(r'\s+')

def add_end_punctuation(text):
  # if nothing in the text, just add stop mark
  if text == '':
    return 'Empty Text. Please Check.'
  return re.sub('([^\.\,\?\:\;])$', r'\1.', text)

def expand_numbers(text):
  return normalize_numbers(text)

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

def enhanced_english_cleaners(text):
  '''Pipeline for English text, including number, abbreviation and punctuation_expansion. and dealwith emoji'''
  text = expand_emoji(text)
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