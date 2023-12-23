from secrets import choice

from string import ascii_letters


def generate_code(length=8):
    rstr = ''
    for i in range(length):
        rstr += choice(ascii_letters)

    print(rstr)
    return rstr