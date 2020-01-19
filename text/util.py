import re

def split_long_text(long_text):
    split_marks = r'\.\?\!'
    text_list = re.findall(r'.{1,100}(?:[\.\?\!]|$)|.{1,100}(?:[,]|$)|.{1,100}(?:\s+|$)', long_text)
    return text_list

def split_long_text_old(long_text):
    return re.findall(r'.{1,100}(?:\s+|$)', long_text)

if __name__ == "__main__":
    text = "We are doing our best to transform our services into smart ones. In 2019, we conducted more than 350 corrective measures to develop our services, and these procedures covered 13 service channels, distributed among the seven service centres, smart applications, 47 metro stations,11 Tram stations and 17 bus stops."
    print(split_long_text(text))
    print(split_long_text_old(text))
