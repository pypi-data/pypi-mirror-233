import unittest
from toc4github import make_toc
import os
import subprocess


def cmd(cmd, shell=False):
    """execute a cmd without shell, return exitcode"""
    proc = subprocess.run(cmd if shell else cmd.split(),
                          shell=shell,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    assert proc.returncode == 0
    return proc.returncode


raw = """\
{toc}

# Test
## header
### head 3
#### head 4
##### head 5
###### head 6
####### not a head 7

# _abc
# a & b & c
# a       c
# a ( c )
# a(c)
# a.,.,!@#$%^&*().,.7

# *italic 12345*
# **bold 12345**
# _italic2 12345_
# __bold2 12345__
# ~cross out~
# ~~cross out 2~~
# **~bold cross out~**
# __~~blod cross out 2~~__
"""
cooked = ('* [Test](#Test)\n'
          '    * [header](#header)\n'
          '        * [head 3](#head-3)\n'
          '            * [head 4](#head-4)\n'
          '                * [head 5](#head-5)\n'
          '                    * [head 6](#head-6)\n'
          '* [_abc](#_abc)\n'
          '* [a & b & c](#a--b--c)\n'
          '* [a       c](#a-------c)\n'
          '* [a ( c )](#a--c-)\n'
          '* [a(c)](#ac)\n'
          '* [a.,.,!@#$%^&*().,.7](#a7)\n'
          '* [*italic 12345*](#italic-12345)\n'
          '* [**bold 12345**](#bold-12345)\n'
          '* [_italic2 12345_](#italic2-12345)\n'
          '* [__bold2 12345__](#bold2-12345)\n'
          '* [~cross out~](#cross-out)\n'
          '* [~~cross out 2~~](#cross-out-2)\n'
          '* [**~bold cross out~**](#bold-cross-out)\n'
          '* [__~~blod cross out 2~~__](#blod-cross-out-2)\n')


class test_make_toc(unittest.TestCase):

    def test_make_toc_1(self):
        toc = make_toc(raw)
        self.assertEqual(toc, cooked)
        toc = make_toc(raw.split('\n'))
        self.assertEqual(toc, cooked)

    def test_make_toc_2(self):
        fn = '__toc4github_test2.txt'
        with open(fn,'w') as f:
            f.write(raw)
        cmd('python3 toc4github.py %s' % fn)
        with open(fn) as f:
            cont = f.read()
        self.assertEqual(cont, cooked+raw[6:])
        os.remove(fn)

    def test_make_toc_21(self):
        fn = '__toc4github_test21.txt'
        with open(fn,'w') as f:
            f.write(raw)
        cmd('python3 toc4github.py --title "The Contents" %s' % fn, True)
        with open(fn) as f:
            cont = f.read()
        os.remove(fn)
        self.assertEqual(cont, '# The Contents\n\n'+cooked+raw[6:])

    def test_make_toc_3(self):
        raw = """
        ```
        123456
        """
        self.assertRaises(ValueError, make_toc, raw)

    def test_make_toc_4(self):
        s = "# 中文效果"
        self.assertEqual('* ['+s[2:]+'](#'+s[2:]+')\n', make_toc(s))
        s = "## 中文效果"
        self.assertEqual('* ['+s[3:]+'](#'+s[3:]+')\n', make_toc(s))
        s = "# 中EN混Mix"
        self.assertEqual('* ['+s[2:]+'](#'+s[2:]+')\n', make_toc(s))
        s = "### 中EN混Mix"
        self.assertEqual('* ['+s[4:]+'](#'+s[4:]+')\n', make_toc(s))

    def test_make_toc_5(self):
        s = '#abcde'
        self.assertEqual(make_toc(s), '')
        s = '#  abcde'
        self.assertEqual(make_toc(s), '* [abcde](#abcde)\n')
        s = ' #abcde'
        self.assertEqual(make_toc(s), '')
        s = '  #  abcde'
        self.assertEqual(make_toc(s), '* [abcde](#abcde)\n')


if __name__ == '__main__':
    unittest.main()

