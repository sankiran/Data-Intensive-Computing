import string
def getList(text):
    words = text.lower().translate(string.maketrans("", ""), string.punctuation).split()
    return words