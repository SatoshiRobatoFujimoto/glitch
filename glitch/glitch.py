#! usr/bin/python3
# -*- coding: utf-8 -*-

"""
Enjoy your glitch life!!
Replace: 任意の箇所のバイト列と 同サイズの任意のバイト列を入れ換える
Increase: 任意の箇所のバイト列と それより大きなサイズの任意のバイト列と入れ換える
Decrease: 任意の箇所のバイト列を 削除する
Swap: 任意の箇所のバイト列と 他の任意の箇所のバイト列を入れ換える
Changiling: 任意のバイト文字を 他の任意のバイト文字に置き換える
http://ucnv.org/openspace2013/map.html

Usage:
  glitch [-h] -i=<input> [-o=<output>] [-n=<times>] [maximum] [hard] [-m=<mode>]

Options:
  -h  show this
  -i=<input>  '*.jpg' file
  -o=<output>  '*.jpg' glitched file[default: ./glitched.jpg]
  -n=<times>  output files N times[default: 10]
  maximum  create 62 files
  hard  hard glitch
  -m=<mode> glitch mode, r: replace,
                         i: increase,
                         d: decreace,
                         s: swap,
                         c: changiling
                         [default: r]
"""


import base64
import random
import string
import docopt

class Glitch:
    def __init__(self):
        self.glitch_mode = {
            'r': self.replace,
            'i': self.increase,
            'd': self.decrease,
            's': self.swap,
            'c': self.changiling,
        }

    def glitch(self, infile, outfile='glitched.jpg', times=10, maximum=False, hard=False, mode='r'):
        mode, graphictext, times = self.prepare_glitchfile(infile, mode, times, maximum)
        self.factory(outfile, mode, graphictext, times, hard)

    def enjoyglitch(self):
        _ = ("".join(random.sample(s, len(s))) for s in ('njo', 'litc'))
        return "E" + next(_) + "y G" + next(_) + "h."

    def factory(self, outfile, mode, graphictext, times, hard):
        for i in range(times):
            name = 'hard' if hard else mode.__name__
            glitchfile = outfile.replace(".jpg", "{0}_{1}.jpg".format(i, name))
            with open(glitchfile, 'wb') as f:
                g = self.machine(mode, graphictext, hard)
                f.write(g)

    def prepare_glitchfile(self, infile, mode, times, maximum):
        mode = self.glitch_mode[mode]
        times = self.set_glitch_times(times, maximum)
        with open(infile, 'rb') as f:
            lines = [line for line in f]
            graphictext = list(map(base64.encodestring, lines))
        return (mode, graphictext, times)

    def machine(self, mode, graphictext, hard):
        if hard:
            for m in self.glitch_mode.values():
                graphictext = m(list(graphictext))
            gf = graphictext
        else:
            gf =  mode(graphictext)
        return b''.join(list(map(base64.decodestring, gf)))

    def set_glitch_times(self, times, maximum):
        if maximum:
            return len(string.ascii_letters + string.digits)
        return int(times)

    def alphanumeric(self):
        return bytes([ord(random.choice(list(string.ascii_letters + string.digits)))])

    def replace(self, infile):
        '''Replace: 任意の箇所のバイト列と 同サイズの任意のバイト列を入れ換える
        '''
        gf = infile[:]
        same_size_index = []
        while len(same_size_index) <= 1:
            index = random.randint(0,len(gf)-1)
            index_len = len(gf[index])
            same_size_index = [i for (i,g) in enumerate(gf) if len(g) == index_len]
        else:
            same_size_index = random.choice(same_size_index[:])
        gf[index], gf[same_size_index] = gf[same_size_index], gf[index]
        return gf

    def increase(self, infile):
        '''Increase: 任意の箇所のバイト列と それより大きなサイズの任意のバイト列と入れ換える
        '''
        gf = infile[:]
        index = gf.index(random.choice(gf))
        index_len = len(gf[index])
        large_size_index = random.choice([gf.index(g) for g in gf if len(g) > index_len])
        gf[index], gf[large_size_index] = gf[large_size_index], gf[index]
        return gf

    def decrease(self, infile):
        '''Decrease: 任意の箇所のバイト列を 削除する
        '''
        gf = infile[:]
        index = random.randint(0, len(gf)-1)
        gf = gf[:index] + gf[index+1:]
        return gf

    def swap(self, infile):
        '''Swap: 任意の箇所のバイト列と 他の任意の箇所のバイト列を入れ換える
        '''
        gf = infile[:]
        index = gf.index(random.choice(gf))
        another = gf.index(random.choice(gf))
        gf[index], gf[another] = gf[another], gf[index]
        return gf

    def changiling(self, infile):
        '''Changiling: 任意のバイト文字を 他の任意のバイト文字に置き換える
        '''
        gf = infile[:]
        baby, fetch = (self.alphanumeric() for _ in range(2))
        gf = [g.replace(baby, fetch) for g in gf]
        return gf


def main(*args):
    g = Glitch()
    g.glitch(*args)
    return g.enjoyglitch()

if __name__ == '__main__':
    args = docopt.docopt(__doc__, version=1.0)
    print(main(args["-i"], args["-o"], args["-n"], args["maximum"], args["hard"], args["-m"]))
