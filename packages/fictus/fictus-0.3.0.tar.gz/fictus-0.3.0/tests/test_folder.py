import unittest

from fictus.fictusnode import Folder


class MyTestCase(unittest.TestCase):
    def test_parent(self):
        a = Folder("a", None)
        b = Folder("b", a)
        a.children.append(b)
        self.assertEqual(
            a,
            b.parent,
        )
        self.assertEqual(None, a.parent)


if __name__ == "__main__":
    unittest.main()
