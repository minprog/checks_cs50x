import re

from check50 import *

class Sentimental(Checks):

    ### HELLO ###

    @check()
    def exists_hello(self):
        """hello.py exists."""
        self.require("hello.py")

    @check("exists_hello")
    def prints_hello(self):
        """prints "hello, world\\n" """
        expected = "[Hh]ello, world!?\n"
        actual = self.spawn("python3 hello.py").stdout()
        if not re.match(expected, actual):
            err = Error(Mismatch("hello, world\n", actual))
            if re.match(expected[:-1], actual):
                err.helpers = "Did you forget a newline (\"\\n\") at the end of your string?"
            raise err

    ### MARIO MORE ###

    @check()
    def exists_mario(self):
        """mario.py exists."""
        self.require("mario.py")
        self.add("1.txt", "2.txt", "23.txt")

    @check("exists_mario")
    def test_reject_negative(self):
        """rejects a height of -1"""
        self.spawn("python3 mario.py").stdin("-1").reject()

    @check("exists_mario")
    def test0(self):
        """handles a height of 0 correctly"""
        self.spawn("python3 mario.py").stdin("0").stdout(EOF).exit(0)

    @check("exists_mario")
    def test1(self):
        """handles a height of 1 correctly"""
        out = self.spawn("python3 mario.py").stdin("1").stdout()
        correct = File("1.txt").read()
        check_pyramid(out, correct)

    @check("exists_mario")
    def test2(self):
        """handles a height of 2 correctly"""
        out = self.spawn("python3 mario.py").stdin("2").stdout()
        correct = File("2.txt").read()
        check_pyramid(out, correct)

    @check("exists_mario")
    def test23(self):
        """handles a height of 23 correctly"""
        out = self.spawn("python3 mario.py").stdin("23").stdout()
        correct = File("23.txt").read()
        check_pyramid(out, correct)

    @check("exists_mario")
    def test24(self):
        """rejects a height of 24, and then accepts a height of 2"""
        self.spawn("python3 mario.py").stdin("24").reject()\
            .stdin("2").stdout(File("2.txt")).exit(0)

    @check("exists_mario")
    def test_reject_foo(self):
        """rejects a non-numeric height of "foo" """
        self.spawn("python3 mario.py").stdin("foo").reject()

    @check("exists_mario")
    def test_reject_empty(self):
        """rejects a non-numeric height of "" """
        self.spawn("python3 mario.py").stdin("").reject()

    ### CASH ###

    @check()
    def exists_cash(self):
        """cash.py exists"""
        self.require("cash.py")

    @check("exists_cash")
    def test041(self):
        """input of 0.41 yields output of 4"""
        self.spawn("python3 cash.py").stdin("0.41").stdout(coins(4), "4\n").exit(0)

    @check("exists_cash")
    def test001(self):
        """input of 0.01 yields output of 1"""
        self.spawn("python3 cash.py").stdin("0.01").stdout(coins(1), "1\n").exit(0)

    @check("exists_cash")
    def test015(self):
        """input of 0.15 yields output of 2"""
        self.spawn("python3 cash.py").stdin("0.15").stdout(coins(2), "2\n").exit(0)

    @check("exists_cash")
    def test160(self):
        """input of 1.6 yields output of 7"""
        self.spawn("python3 cash.py").stdin("1.6").stdout(coins(7), "7\n").exit(0)

    @check("exists_cash")
    def test230(self):
        """input of 23 yields output of 92"""
        self.spawn("python3 cash.py").stdin("23").stdout(coins(92), "92\n").exit(0)

    @check("exists_cash")
    def test420(self):
        """input of 4.2 yields output of 18"""
        expected = "18\n"
        actual = self.spawn("python3 cash.py").stdin("4.2").stdout()
        if not re.search(coins(18), actual):
            err = Error(Mismatch(expected, actual))
            if re.search(coins(22), actual):
                err.helpers = "Did you forget to round your input to the nearest cent?"
            raise err

    @check("exists_cash")
    def test_cash_reject_negative(self):
        """rejects a negative input like -.1"""
        self.spawn("python3 cash.py").stdin("-1").reject()

    @check("exists_cash")
    def test_cash_reject_foo(self):
        """rejects a non-numeric input of "foo" """
        self.spawn("python3 cash.py").stdin("foo").reject()

    @check("exists_cash")
    def test_cash_reject_empty(self):
        """rejects a non-numeric input of "" """
        self.spawn("python3 cash.py").stdin("").reject()

    ### VIGENERE ###

    @check()
    def exists_vigenere(self):
        """vigenere.py exists."""
        self.require("vigenere.py")

    @check("exists_vigenere")
    def aa(self):
        """encrypts "a" as "a" using "a" as keyword"""
        self.spawn("python3 vigenere.py a").stdin("a").stdout("ciphertext:\s*a\n", "ciphertext: a\n").exit(0)

    @check("exists_vigenere")
    def bazbarfoo_caqgon(self):
        """encrypts "barfoo" as "caqgon" using "baz" as keyword"""
        self.spawn("python3 vigenere.py baz").stdin("barfoo").stdout("ciphertext:\s*caqgon\n", "ciphertext: caqgon\n").exit(0)

    @check("exists_vigenere")
    def mixedBaZBARFOO(self):
        """encrypts "BaRFoo" as "CaQGon" using "BaZ" as keyword"""
        self.spawn("python3 vigenere.py BaZ").stdin("BaRFoo").stdout("ciphertext:\s*CaQGon\n", "ciphertext: CaQGon\n").exit(0)

    @check("exists_vigenere")
    def allcapsBAZBARFOO(self):
        """encrypts "BARFOO" as "CAQGON" using "BAZ" as keyword"""
        self.spawn("python3 vigenere.py BAZ").stdin("BARFOO").stdout("ciphertext:\s*CAQGON\n", "ciphertext: CAQGON\n").exit(0)

    @check("exists_vigenere")
    def bazworld(self):
        """encrypts "world!$?" as "xoqmd!$?" using "baz" as keyword"""
        self.spawn("python3 vigenere.py baz").stdin("world!$?").stdout("ciphertext:\s*xoqmd!\$\?\n", "ciphertext: xoqmd!$?\n").exit(0)

    @check("exists_vigenere")
    def withspaces(self):
        """encrypts "hello, world!" as "iekmo, vprke!" using "baz" as keyword"""
        self.spawn("python vigenere.py baz").stdin("hello, world!").stdout("ciphertext:\s*iekmo, vprke!\n", "ciphertext: iekmo, vprke!\n").exit(0)
    
    @check("exists_vigenere")
    def noarg(self):
        """handles lack of argv[1]"""
        self.spawn("python3 vigenere.py").exit(1)

    @check("exists_vigenere")
    def toomanyargs(self):
        """handles argc > 2"""
        self.spawn("python3 vigenere.py 1 2 3").exit(1)

    @check("exists_vigenere")
    def reject(self):
        """rejects "Hax0r2" as keyword"""
        self.spawn("python3 vigenere.py Hax0r2").exit(1)


def coins(num):
    return r"(^|[^\d]){}(?!\d)".format(num)


def check_pyramid(output, correct):
    if output == correct:
        return

    output = output.split("\n")
    correct = correct.split("\n")

    err = Error(Mismatch(correct, output))
    # check if pyramids are the same height and only differ by trailing whitespace
    if len(output) == len(correct) and all(ol.rstrip() == cl for ol, cl in zip(output, correct)):
        err.helpers = "Did you add too much trailing whitespace to the end of your pyramid?"
    elif len(output) == len(correct) and all(ol[1:] == cl for ol, cl in zip(output, correct)):
        err.helpers = "Are you printing an additional character at the beginning of each line?"
    raise err
