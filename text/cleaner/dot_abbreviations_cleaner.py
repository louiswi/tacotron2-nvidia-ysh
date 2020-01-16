import re

# List of (regular expression, replacement) pairs for abbreviations:
_dot_abbreviations_list = [
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
  ('sen', 'senate'),
  ('no', 'number'),
]

# abbreviation

_dot_abbreviations = [(re.compile(r'\b%s\.' % x[0], re.IGNORECASE), x[1]) for x in _dot_abbreviations_list]

_dot_abbreviations_dict = dict((item[0], item[1]) for item in _dot_abbreviations_list)

_dot_abbreviations_re = re.compile('|'.join([f"\\b{item}\\." for item in _dot_abbreviations_dict.keys()]), re.IGNORECASE)

def expand_dot_abbreviations_old(text):
  for regex, replacement in _dot_abbreviations:
    text = re.sub(regex, replacement, text)
  return text

def expand_dot_abbreviations(text):
  text = re.sub(_dot_abbreviations_re, lambda match: _dot_abbreviations_dict[match.group(0)[:-1].lower()] + " ", text)
  return text


if __name__ == "__main__":
    print(expand_dot_abbreviations("hello mr.stephen"))
    print(expand_dot_abbreviations("Asked if he had concerns the witness debate could get “messy,” Sen. John Thune (S.D.), the No. 2 Senate Republican, said “that’s the state of play.”"))