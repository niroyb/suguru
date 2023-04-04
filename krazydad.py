# url = 'https://krazydad.com/play/suguru/?kind=8x8&volumeNumber=5&bookNumber=10&puzzleNumber=8'
# pRec = {"puzzle_data":{"puzz":"5b4c4b3d1m1b4c4i1j53d2;ABCCDDEEACCDDEEEAACDFFFFGAHHIFJJGHHIIJJKGHIILJKKGGMLLLLNMMMMNNNN","branches":0,"width":8,"height":8,
# "solved":"5154315432325231141434525232513141414242353235131215124545324312","ptitle":"KD_Suguru_8x8_V5-B10-P8"},"puzzle_id":"KD_Suguru_8x8_V5-B10-P8",

import suguru

class SuguruKrazy(suguru.Suguru):
    def __init__(self):
        super().__init__()

    def parsePuzz(self, puzz):
        inStr, fillS = puzz.split(';')
        givens = SuguruKrazy.__decodeGivens(inStr)
        self.width = self.height = 8
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

def main():
    s = SuguruKrazy()
    s.parsePuzz('5b4c4b3d1m1b4c4i1j53d2;ABCCDDEEACCDDEEEAACDFFFFGAHHIFJJGHHIIJJKGHIILJKKGGMLLLLNMMMMNNNN')

    print(s)
    print(s.get_solved_count())
    print()

    for _ in range(10):
        s.solve_step()
        print(s)
        print(s.get_solved_count())
        if s.is_solved():
            break
        print()
    
    assert(s.krazy_solved_str() == '5154315432325231141434525232513141414242353235131215124545324312')

if __name__ == '__main__':
    main()
