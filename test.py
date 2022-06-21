def addOne(filepath):
    newpath = ''
    i = 0
    substrings = filepath.split('.')
    for strg in substrings:
        newpath += strg
        if i == (len(substrings)-2):
            newpath += '(1).'
        i += 1
    return newpath


print(addOne('C:/dir/text.mov'))