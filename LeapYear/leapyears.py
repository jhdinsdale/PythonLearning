def leapyear(y):
    if (y % 100 != 0) and (y % 4 == 0) or (y % 400 == 0):
        print "%s is a leap year" % y
    else:
        print "%s is not a leap year" % y

def inputyear():
    ly = 0
    while len(str(ly)) != 4:
        print "Input a year with four digits e.g. 1984"
        ly = raw_input("which year do you want check for leapiness?  ")
    return ly

if __name__ == '__main__':
    year = inputyear()
    try:
        year = int(year)
        leapyear(year)
    except ValueError:
        print "That's not even a number Silly"
