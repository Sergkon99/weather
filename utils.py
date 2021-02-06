def transliteration(text):
    cyrillic = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    latin = 'a|b|v|g|d|e|e|zh|z|i|i|k|l|m|n|o|p|r|s|t|u|f|kh|tc|ch|sh|shch||y||e|iu|ia'.split('|')
    trantab = {k: v for k, v in zip(cyrillic, latin)}
    newtext = ''
    for ch in text:
        casefunc = str.capitalize if ch.isupper() else str.lower
        newtext += casefunc(trantab.get(ch.lower(), ch))
    return newtext


import collections

c = collections.Counter((w['description'],) for w in [
    {
        "id": 804,
        "main": "Clouds",
        "description": "пасмурно",
        "icon": "04n"
    },
    {
        "id": 804,
        "main": "Clouds",
        "description": "пасмурно",
        "icon": "04n"
    }
]).most_common(1)[0]

c = collections.Counter().most_common(1)
# print(c)

# with open("input.txt") as fin, \
#         open("output.txt", "w", encoding='utf8') as fout:
#     for data in sorted(fin.readlines()):
#         lastName, firstName, _, score = data.split()
#         fout.write(f'{lastName} {firstName} {score}\n')


class A:
    n = 1


class B(A):
    def __init__(self):
        self.n = 2

    def get(self):
        print(super().n)
        print(self.n)


class C(A):
    def __init__(self):
        self.n = 3

    def get(self):
        print(super().n)
        print(self.n)

a = A()
b = B()
c = C()

b.get()
c.get()
