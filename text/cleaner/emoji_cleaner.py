import re
import emoji

# emoji
_emoji_pattern = re.compile("["
u"\U0001F600-\U0001F64F"  # emoticons
u"\U0001F300-\U0001F5FF"  # symbols & pictographs
u"\U0001F680-\U0001F6FF"  # transport & map symbols
u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
u"\U00002702-\U000027B0"
u"\U000024C2-\U0001F251"
"]+", flags=re.UNICODE)

def expand_emoji(string, mode="decode"):
  mode_choices = ['decode', 'remove']
  if mode not in mode_choices:
    raise ValueError("Invalid mode type. Expected one of: %s" % mode_choices)

  if mode == "decode": # decode with emojis package
    return emoji.demojize(string)
  else: # remove with pattern
    return re.sub(_emoji_pattern, r'', string)

if __name__ == "__main__":
    print(expand_emoji("1🇰🇪 + 🇮🇸1 =2"))
    print(expand_emoji("1 + 😀 =2"))