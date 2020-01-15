import re
from text.cleaner.url_cleaner import _url_replace_word_re, _url_replace_word_dict

# email

_email_re = re.compile(r'[\.\w]+@\w+?(?:\.\w+)+', flags=re.IGNORECASE)



def expand_email(text):
  return re.sub(_email_re, lambda match: deal_with_email(match.group()), text)

def deal_with_email(text):
  text = text.replace('@', ' at ').replace('.', ' dot ')
  return re.sub(_url_replace_word_re, lambda match: _url_replace_word_dict[match.group().lower()], text)


if __name__ == "__main__":
    print(expand_email("dasd@dasdas"))
    print(expand_email("dasdsa@dsad.com"))
    print(expand_email("da-dfsdfsd@dsadas.com.dsad"))
