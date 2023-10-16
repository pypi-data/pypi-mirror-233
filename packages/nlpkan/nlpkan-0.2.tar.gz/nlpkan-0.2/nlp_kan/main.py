import re

def contains_only_kannada(word):
    try:
        word = word.encode('utf-8').decode('utf-8')
        kannada_pattern = re.compile(r'^[\u0C80-\u0CFF\s]+$')
        return kannada_pattern.match(word) is not None
    except Exception as e:
        print(e)
        return False

def remove_non_kannada_characters(word):
    try:
        cleaned_word = re.sub(r'[^\u0C80-\u0CFF\s]+', '', word)
        return cleaned_word
    except Exception as e:
        print(e)
        return ""

def remove_special_characters(text):
    try:
        text = text.encode('utf-8').decode('utf-8')
        cleaned_text = re.sub(r'[^\w\s\u0C80-\u0CFF]+', '', text)
        return cleaned_text
    except Exception as e:
        print(e)
        return ""

def is_kannada_words(text):
    try:
        words = text.strip().split()
        return all( contains_only_kannada(word)  for word in words )
    except Exception as e:
        print(e)
        return False

if "__main__" == __name__:
    pass