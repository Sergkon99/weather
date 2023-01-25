def transliteration(text):
    cyrillic = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    latin = 'a|b|v|g|d|e|e|zh|z|i|i|k|l|m|n|o|p|r|s|t|u|f|kh|tc|ch|sh|shch||y||e|iu|ia'.split('|')
    trantab = {k: v for k, v in zip(cyrillic, latin)}
    newtext = ''
    for ch in text:
        casefunc = str.capitalize if ch.isupper() else str.lower
        newtext += casefunc(trantab.get(ch.lower(), ch))
    return newtext
