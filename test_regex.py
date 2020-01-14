import re
import time

table = [
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
]

d = dict((item[0], item[1]) for item in table)

_zero_to_nine_re = [(re.compile('%s' % x[0]), x[1]) for x in table]

_group_regex = re.compile("|".join([item[0] for item in table]))

def expand_zero_to_nine(text):
  for regex, replacement in _zero_to_nine_re:
    text = re.sub(regex, replacement, text)
  return text

def expand_zero_to_nine2(text):

  text = re.sub(_group_regex, lambda match: d[match.group(0)], text)
  return text

if __name__ == "__main__":
  repeat_times = 10

  t1 = time.time()
  for _ in range(repeat_times):
    expand_zero_to_nine("i have a 1 dasd 0 fdgfd2 fdgdf5 2 + 3213 dsad 3215 123")
  t11 = time.time() - t1
  print(t11)

  t2 = time.time()
  for _ in range(repeat_times):
    expand_zero_to_nine2("i have a 1 dasd 0 fdgfd2 fdgdf5 2 + 3213 dsad 3215 123")

  t22 = time.time() - t2
  print(t22)

  print(t11/t22)
