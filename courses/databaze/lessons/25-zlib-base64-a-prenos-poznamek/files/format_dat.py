MAX_TEXT = 65536  # Počet bajtů UTF-8, nikoli počet znaků.
MAX_BALICEK = 100000
PREFIX = 'z1:'

def text_utf8(text):
    if not isinstance(text,str):
        raise ValueError('Předávejte text.')
    try:
        data = text.encode('utf-8')
    except UnicodeError:
        raise ValueError('Text musí být platný UTF-8.') from None
    if len(data)>MAX_TEXT:
        raise ValueError('Text překračuje 65536 bajtů UTF-8.')
    return data
