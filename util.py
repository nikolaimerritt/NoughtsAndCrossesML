def before(superstring, bit):
    return superstring.split(bit)[0]

def after(superstring, bit):
    return superstring.split(bit)[1]

def between(superstring, firstBit, secondBit):
    return after(before(superstring, secondBit), firstBit)