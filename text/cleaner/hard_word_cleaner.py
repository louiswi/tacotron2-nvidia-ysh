import re
from text.cleaner.big_abbreviations_cleaner import split_word_to_single_charactor

# all the words will be replaced in anywhere of the sentence
_hard_word_list = [
    ("https", split_word_to_single_charactor('https')),
    ("http", split_word_to_single_charactor('http')),
    ('cn', split_word_to_single_charactor('cn')),
    ('www', split_word_to_single_charactor('www')),
    ('github', 'git hub'),
    ('gmail', 'gee mail'),
    ('u', 'you'),
    ("ur", 'your'),
    ("thx", 'thanks'),
    ("email", 'eee mail'),
    ('ahmed', 'aha med'),
    ('zayed', 'zaah yeed'),
    ('china', 'chiina'),
    ('ipad', 'ii pad'),
    ('ure', 'you are'),
    ('youre', 'you are'),
    ("re", 'are'),
    ("dubai", 'du buy'),
    ("ok", 'okay'),
    ("aka", 'ai kay ai.'),
    ("ai", 'artificial intelligence'),
    ("pls", "please"),
    ("restaurant", "resdrungt"),
    ("beta", "baita"),
    ("island", "eyeland"),
    ("tiger", "tiigger"),
]

_hard_word_dict = dict((k, v) for k, v in _hard_word_list)

_hard_word_re = re.compile("|".join([f'\\b{k}\\b' for k,v in _hard_word_list]), flags=re.IGNORECASE)

def expand_hard_word(text):
    return re.sub(_hard_word_re, lambda match: _hard_word_dict[match.group().lower()], text)

if __name__ == "__main__":
    print(expand_hard_word("http://dsad.dsad"))
    print(expand_hard_word("i come from UAE."))
    print(expand_hard_word("i come from U.A.E."))
    print(expand_hard_word("I.M come from UA.E."))
