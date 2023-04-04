# url = 'https://krazydad.com/play/suguru/?kind=8x8&volumeNumber=5&bookNumber=10&puzzleNumber=8'

import suguru

class SuguruKrazy(suguru.Suguru):
    def __init__(self, puzzle):
        super().__init__()
        inStr, fillS = puzzle['puzz'].split(';')
        givens = SuguruKrazy.__decodeGivens(inStr)
        self.width = int(puzzle['width'])
        self.height = int(puzzle['height'])
        assert len(fillS) == len(givens) == self.width * self.height
        line = []
        for x in range(len(fillS)):
            i = x//self.width
            j = x%self.width
            fill = fillS[x]
            c = suguru.Cell(i, j, block=fill)
            if givens[x] != '.':
                c.marks = {int(givens[x])}
            self.blocks[fill].append(c)
            line.append(c)
            if len(line) == self.width:
                self.grid.append(line)
                line = []
        self._Suguru__set_marks()

    @classmethod
    def __decodeGivens(cls, inStr):
        out = []
        
        for c in inStr:
            if c == '.':
                out.append('.')
            elif 'a' <= c <= 'z':
                reps = 1 + ord(c) - ord('a')
                out.append('.'*reps)
            elif '0' <= c <= '9':
                out.append(c)
            else:
                raise Exception(f'Invalid char "{c}" in "{inStr}"')
        return ''.join(out)

    def krazy_solved_str(self):
        s = []
        for line in self.grid:
            for cell in line:
                if cell.solved():
                    s.append(str(next(iter(cell.marks))))
                else:
                    s.append('.')
        return ''.join(s)

def main(puzzle):
    s = SuguruKrazy(puzzle)

    print(s)
    print(s.get_solved_count())
    print()

    for i in range(1, 15):
        s.solve_step()
        print(s)
        print(i, ':', s.get_solved_count())
        if s.is_solved():
            break
        print()
    
    assert(s.krazy_solved_str() == puzzle['solved'])

puzzle_data1 = {"puzz":"5b4c4b3d1m1b4c4i1j53d2;ABCCDDEEACCDDEEEAACDFFFFGAHHIFJJGHHIIJJKGHIILJKKGGMLLLLNMMMMNNNN","width":8,"height":8, \
    "solved":"5154315432325231141434525232513141414242353235131215124545324312","ptitle":"KD_Suguru_8x8_V5-B10-P8"}
puzzle_data2 = {"puzz":"b5i2g1g5b12f2e2a5j4w1g13c3c3d3a5k2a3c4a2i4e3g;AABBCCDEEFFFFGGHAABBCDDEEFIIJJHHAKBCCDDELLIIJHKKKKMNNOOLLLIJHPPQQMMNNOORSSJTTPPQQMMNUORRSSVTTPQWXXUUURYYSVVTZZWWXXUaabYYcVVZZdWWXaaebbYccccZddddaeeebb",\
    "solved":"515135254531212343421313145354512134245232121235425131414543412313252323212254525414151454131343252342313454521434515425323145251323134145231432414252","height":10,"width":15,"ptitle":"KD_Suguru_15x10_V1-B1-P1"}

if __name__ == '__main__':
    main(puzzle_data2)
