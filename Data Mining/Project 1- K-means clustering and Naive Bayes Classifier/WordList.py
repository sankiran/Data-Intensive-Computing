import string
def getList(text):
    text=text.lower()
    text=text.replace('.',' ')
    text=text.translate(None, '!@#$%^&*():;\"\'<>?,/')
    words=text.split()
    return words