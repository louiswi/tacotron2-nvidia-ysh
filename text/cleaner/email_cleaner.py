import re
from text.cleaner.hard_word_cleaner import expand_hard_word

# email
_email_replace_word_list = [
    ('.', ' dot '),
    ('@', ' at ')
]

_email_re = re.compile(r'[\.\w]+@\w+?(?:\.\w+)+', flags=re.IGNORECASE)

def expand_email(text):
  return re.sub(_email_re, lambda match: deal_with_email(match.group()), text)

def deal_with_email(email):
    for k, v in _email_replace_word_list:
        email = email.replace(k, v)
    return email

if __name__ == "__main__":
    print(expand_email("www.dasd@dasdas"))
    print(expand_email("dasdsa@dsad.com"))
    print(expand_email("da-dfsdfsd@dsadas.com.dsad"))
