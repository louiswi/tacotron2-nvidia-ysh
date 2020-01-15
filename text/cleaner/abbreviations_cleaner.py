import re

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

# abbreviation

_abbreviations = [(re.compile(r'\b%s\.' % x[0], re.IGNORECASE), x[1]) for x in _abbreviations_list]

_abbreviations_dict = dict((item[0], item[1]) for item in _abbreviations_list)

_abbreviations_re = re.compile('|'.join([f"\\b{item}\\." for item in _abbreviations_dict.keys()]))

def expand_abbreviations_old(text):
  for regex, replacement in _abbreviations:
    text = re.sub(regex, replacement, text)
  return text

def expand_abbreviations(text):
  text = re.sub(_abbreviations_re, lambda match: _abbreviations_dict[match.group(0)[:-1]]+" ", text)
  return text


if __name__ == "__main__":
    print(expand_abbreviations("hello mr.stephen"))