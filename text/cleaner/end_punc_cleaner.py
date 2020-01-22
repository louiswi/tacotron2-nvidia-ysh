import re

# big abbreviation
_punc_list = [
('!', 'exclamation mark'),
('"', 'quote'),
('#', 'hash'),
('$', 'dollar'),
('%', 'percent'),
('&', 'and'),
("'", 'single quote'),
('(', 'opening parentheses'),
(')', 'closing parentheses'),
('*', 'asterisk'),
('+', 'plus'),
(',', 'comma'),
('-', 'dash'),
('.', 'dot'),
('/', 'slash'),
(':', 'colon'),
(';', 'semi-colon'),
('<', 'less than'),
('=', 'equals'),
('>', 'greater than'),
('?', 'question mark'),
('@', 'at'),
('[', 'opening square brackets'),
('\\', 'back slash'),
(']', 'closing square brackets'),
('^', 'mark'),
('_', 'underscore'),
('`', 'apostrophe'),
('{', 'opening brackets'),
('|', 'mark'),
('}', 'closing brackets'),
('~', 'mark'),
]

_punc_dict = dict((k, v) for k, v in _punc_list)

_punc_re = re.compile('|'.join([k for k, v in _punc_dict]))

def add_end_punctuation(text):
  # if nothing in the text, just add stop mark
  if text == '':
    return 'Empty Text. Please Check.'
  return re.sub('([^\.\,\?\:\;])$', r'\1.', text)

def handle_all_punctuation(text):
  # if all is punctuation
  if not re.match(r'.*[a-zA-Z0-9].*', text):
    return text = re.sub(_punc_re,
                lambda match: _punc_dict[match],
                text)
  return text
