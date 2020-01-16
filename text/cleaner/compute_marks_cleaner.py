import re

_compute_marks_list = [
  (r'(\d)%', r'\1 percent'),
  (r'(\d)\s*\+\s*(\d)', r'\1 plus \2'),
  (r'(\d)\s*\+\s*(\d)', r'\1 minus \2'),
  (r'(\d)\s*/\s*(\d)', r'\1 slash \2'),
  (r'(\d)\s*=\s*(\d)', r'\1 equals \2'),
  (r'(\d)\s*\*\s*(\d)', r'\1 times \2'),
]

# compute marks

_compute_marks = [(re.compile(r'%s' % x[0]), r'%s' % x[1]) for x in _compute_marks_list]

# can not do as expand abbreviation use one regex to group multi regexs
def expand_compute_marks(text):
  for regex, replacement in _compute_marks:
    text = re.sub(regex, replacement, text)
  return text



if __name__ == "__main__":
    print(expand_compute_marks("1 + 1 =2"))
    print(expand_compute_marks("1 + 1dasd =2"))