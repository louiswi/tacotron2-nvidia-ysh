import re

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

if __name__ == "__main__":
    print(expand_mobile_numbers("123213213 + 2 =2"))
    print(expand_mobile_numbers("12 + 2 =2"))