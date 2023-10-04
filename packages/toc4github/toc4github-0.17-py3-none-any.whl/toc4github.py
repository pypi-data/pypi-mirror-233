#!/usr/bin/env python3
"""
To generate TOC for Markdown file, especially for README.md of Github.

Author:   xinlin-z
Github:   https://github.com/xinlin-z/toc4github
Blog:     https://cs.pynote.net
License:  MIT
"""
import sys
import re
import argparse
from functools import singledispatch
from typing import Iterable


MAX_HEAD_LEVEL = 6


def _make_toc(lines: Iterable[str]) -> tuple[int,str]:
    toc = ''
    pos = -1
    skip = 0
    pattern_head = re.compile(r'\s*(#+)\s(.*)')
    pattern_syn = re.compile(r'([~*_]{1,2})(.*)\1')
    for i,line in enumerate(lines):
        # skip empty line
        if(line:=line.strip()) == '':
            continue
        # skip block started with 4 space
        if line.startswith(' '*4):
            continue
        # skip ``` block
        if line.startswith('```'):
            skip = abs(skip-1)
        if skip:
            continue
        # try to find placeholder {toc} and skip
        if line.strip().lower() == '{toc}':
            pos = i
            continue
        # line search and make toc
        if strs:=re.match(pattern_head,line):
            g1 = strs.group(1)
            if (g1n:=len(g1)) > MAX_HEAD_LEVEL:
                continue
            g2 = strs.group(2).strip()
            # remove markdown syntax elements ~*_
            while a:=re.search(pattern_syn,g2):
                g2 = g2[:a.start()] + a.group(2) + g2[a.end():]
            # space to -
            g2 = re.sub(r'\s', '-', g2)
            # squeeze other chars
            r = re.sub(r'[^-\w]', '', g2)
            # join
            toc += ''.join((' '*(g1n-1)*4, '* ',
                           '[',strs.group(2).strip(),'](#', r,')'))+'\n'
    else:
        if skip:
            raise ValueError('``` block is open.')
    # remove extra leading spaces,
    # for the case that head line is not started by level 1.
    if toc != '':
        lines = toc.split('\n')
        if rem:=re.match(r'(\s*)',lines[0]):
            rmn = len(rem.group(1))
            toc = ''.join(h[rmn:]+'\n' for h in lines if h!='')
    return pos, toc


@singledispatch
def make_toc(lines: Iterable[str]|str) -> str:
    """Return the TOC contents."""
    return _make_toc(lines)[1]


@make_toc.register
def _(strlines: str) -> str:
    return _make_toc(strlines.split('\n'))[1]


_VER = 'toc4github V0.17 by xinlin-z'\
       ' (https://github.com/xinlin-z/toc4github)'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-V', '--version', action='version', version=_VER)
    parser.add_argument('-d','--dryrun', action='store_true',
                        help='do not write input file, only show TOC')
    parser.add_argument('-t','--title',
                        help='add a customized title')
    parser.add_argument('markdown_file',
                        help='the input markdown file, like README.md')
    args = parser.parse_args()

    try:
        # open and read
        with open(args.markdown_file) as f:
            lines = f.readlines()
        # make toc
        pos, toc = _make_toc(lines)
        # if add title
        toc = ('# '+args.title.strip()+'\n\n' if args.title else '') + toc
        # if dryrun
        if args.dryrun:
            print(toc, end='')
            sys.exit(0)
        # if no {toc} found
        if pos == -1:
            raise ValueError('No {toc} placeholder found!')
        # insert toc
        lines[pos] = toc
        # write back
        with open(args.markdown_file,'w') as f:
            f.write(''.join(lines))
    except Exception as e:
        print('Err:', str(e))
        sys.exit(1)


