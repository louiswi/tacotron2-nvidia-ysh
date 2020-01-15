import re
from text.cleaner.big_abbreviations_cleaner import split_word_to_single_charactor

_url_re = re.compile(r"\b(https?://(?:[\w]+)(?:\.[\w\-]+)+)(?::\d*)?(?:/[^/ ]*)*\b", flags=re.IGNORECASE)

_url_replace_word_list = [
  ("/", " slash "),
  ("https", split_word_to_single_charactor('https')),
  ("http", split_word_to_single_charactor('http')),
  ('cn', split_word_to_single_charactor('cn')),
  ('www', split_word_to_single_charactor('www')),
  (':', ''),
  ('github', 'git hub'),
  ('gmail', 'gee mail'),
]

_url_replace_word_dict = dict((k, v) for k, v in _url_replace_word_list)

_url_replace_word_re = re.compile("|".join([k for k,v in _url_replace_word_list]), flags=re.IGNORECASE)

def expand_url(text):

  return re.sub(_url_re, lambda match: deal_with_main_url(match.group()), text)

def deal_with_main_url(url):
  prefix = url.split('//')[0]
  main_name = '//'.join(url.split('//')[1:]).split('/')[0]
  main_url = prefix + '//' + main_name
  main_url = re.sub(r'\.', ' dot ', main_url)
  return re.sub(_url_replace_word_re, lambda match: _url_replace_word_dict[match.group().lower()], main_url)

if __name__ == "__main__":
    print(expand_url("https://unicode.org/emoji/charts/full-emoji-list.html"))
    print(expand_url("i come from U.A.E."))
    print(expand_url("https://www.google.com/search?q=python+regex+dynamic+group&oq=python+regex+dynamic+group&aqs=chrome..69i57.8625j0j7&sourceid=chrome&ie=UTF-8"))
    print(expand_url("https://stackoverflow.com/questions/7866128/python-split-without-removing-the-delimiter"))