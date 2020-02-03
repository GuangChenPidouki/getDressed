from getDressed import *
import unittest

class TestGetDress(unittest.TestCase):
    def initDressHandler(self, h):
        d_hat = DressType(1, "hat")
        d_pants = DressType(2, "pants")
        d_shirts = DressType(3, "shirts")
        d_shoes = DressType(4, "shoes")
        d_socks = DressType(5, "socks")
        d_leave = DressType(6, "leave")

        Rules.dependOn(d_shoes, d_socks)
        Rules.dependOn(d_shoes, d_pants)
        Rules.dependOn(d_hat, d_shirts)

        Rules.required(d_pants)
        Rules.required(d_shirts)
        Rules.required(d_shoes)
        Rules.required(d_socks)

        h.addDressType(d_hat)
        h.addDressType(d_pants)
        h.addDressType(d_shirts)
        h.addDressType(d_shoes)
        h.addDressType(d_socks)
        h.addDressType(d_leave)

    def test_leave_with_6(self):
        h = DressHandler()
        self.initDressHandler(h)
        self.assertEqual(h.runCommand("5 2 3 4"), "socks, pants, shirts, shoes, leave")
    
    def test_leave_without_6(self):
        h = DressHandler()
        self.initDressHandler(h)
        self.assertEqual(h.runCommand("5 2 3 4 6"), "socks, pants, shirts, shoes, leave")

    def test_not_fully_required_with_6(self):
        h = DressHandler()
        self.initDressHandler(h)
        self.assertEqual(h.runCommand("5 2 3 6"), "socks, pants, shirts, fail")

    def test_not_fully_required_without_6(self):
        h = DressHandler()
        self.initDressHandler(h)
        self.assertEqual(h.runCommand("5 2 3"), "socks, pants, shirts, fail")
    
    def test_not_meet_dependency_with_6(self):
        h = DressHandler()
        self.initDressHandler(h)
        self.assertEqual(h.runCommand("5 3 4 2 6"), "socks, shirts, fail")

    def test_not_meet_dependency_without_6(self):
        h = DressHandler()
        self.initDressHandler(h)
        self.assertEqual(h.runCommand("5 3 4 2"), "socks, shirts, fail")

    def test_no_such_number(self):
        h = DressHandler()
        self.initDressHandler(h)
        self.assertEqual(h.runCommand("5 3 8"), "socks, shirts, fail")

    def test_invalid_input(self):
        h = DressHandler()
        self.initDressHandler(h)
        self.assertEqual(h.runCommand("5 3 haha"), "socks, shirts, fail")

    def test_empty(self):
        h = DressHandler()
        self.initDressHandler(h)
        self.assertEqual(h.runCommand(""), "fail")

    def test_not_init(self):
        h = DressHandler()
        #self.initDressHandler(h)
        self.assertEqual(h.runCommand("5 2 3 4"), "fail")

def main():
    unittest.main()

if __name__ == "__main__":
    main()
