<<<<<<< HEAD
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys, os


def lister(root):
    for (thisdir, subshere, fileshere) in os.walk(root):
        print('[' + thisdir + ']')
        for fname in fileshere:
            path = os.path.join(thisdir, fname)
            print(path)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    lister(sys.argv[1])

=======
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys, os


def lister(root):
    for (thisdir, subshere, fileshere) in os.walk(root):
        print('[' + thisdir + ']')
        for fname in fileshere:
            path = os.path.join(thisdir, fname)
            print(path)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    lister(sys.argv[1])

>>>>>>> 8ab1643e980ddcf1acddf86f8f7e0f275ba6a2d6
