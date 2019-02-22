from check50 import *

class Crack(Checks):
    @check()
    def exists(self):
        """crack.c exists."""
        self.require("crack.c")

    @check("exists")
    def compiles(self):
        """crack.c compiles."""
        self.spawn("clang -std=c11 -o crack crack.c -lcs50 -lcrypt -lm").exit(0)

    @check("compiles")
    def cracks_andi(self):
        """cracks andi's password: 50.jPgLzVirkc"""
        self.spawn("./crack 50.jPgLzVirkc").stdout("hi", timeout=5).exit(0)

    @check("compiles")
    def cracks_jason(self):
        """cracks jason's password: 50YHuxoCN9Jkc"""
        self.spawn("./crack 50YHuxoCN9Jkc").stdout("JH", timeout=5).exit(0)

    @check("compiles")
    def cracks_mzlatkova(self):
        """cracks mzlatkova's password: 50CPlMDLT06yY"""
        self.spawn("./crack 50CPlMDLT06yY").stdout("ha", timeout=5).exit(0)

    @check("compiles")
    def cracks_summer(self):
        """cracks summer's password: 50C6B0oz0HWzo"""
        self.spawn("./crack 50C6B0oz0HWzo").stdout("FTW", timeout=5).exit(0)

    @check("compiles")
    def cracks_stelios(self):
        """cracks stelios's password: 50nq4RV/NVU0I"""
        self.spawn("./crack 50nq4RV/NVU0I").stdout("ABC", timeout=5).exit(0)

    @check("compiles")
    def cracks_zamyla(self):
        """cracks zamyla's password: 50i2t3sOSAZtk"""
        self.spawn("./crack 50i2t3sOSAZtk").stdout("lol", timeout=5).exit(0)
