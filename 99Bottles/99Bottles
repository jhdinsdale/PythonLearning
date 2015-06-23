def xbottles(x):
    while x > 0:
        bottles = "bottles" if x != 1 else "bottle"
        print "%s %s of beer on the wall" %(x, bottles)
        print "%s %s of beer" %(x, bottles)
        print "You take one down pass it around."
        x = (x - 1)
        print "%s %s of beer on the wall" %(x, "bottles" if x != 1 else "bottle")
    else:
        print "No more bottles of beer on the wall"

if __name__ == "__main__":
    n = raw_input("How many Bottles? ")
    try:
        n = int(n)
        xbottles(n)
    except ValueError:
        print "That's not a number Silly"
