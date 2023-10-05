import re

def censor(text, censor_words):
    censor_words = set([word.lower() for word in censor_words])
    text_words = re.findall(r'\w+', text.lower())
    censored_text = text

    for word in text_words:
        if word in censor_words:
            censored_word = '*' * len(word)
            censored_text = re.sub(r'\b' + re.escape(word) + r'\b', censored_word, censored_text, flags=re.IGNORECASE)

    return censored_text

def check(text, censor_words):
    text_words = re.findall(r'\w+', text.lower())

    for word in text_words:
        if word in censor_words:
            return True

    return False
