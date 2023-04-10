
import suguru


class SuguruKrazy(suguru.Suguru):
    def __init__(self, puzzle) -> None:
        super().__init__()
        inStr, fillS = puzzle["puzz"].split(";")
        givens = SuguruKrazy.__decodeGivens(inStr)
        self.width = int(puzzle["width"])
        self.height = int(puzzle["height"])
        assert len(fillS) == len(givens) == self.width * self.height
        line = []
        for x in range(len(fillS)):
            i = x//self.width
            j = x%self.width
            fill = fillS[x]
            c = suguru.Cell(i, j, block=fill)
            if givens[x] != ".":
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
            if c == ".":
                out.append(".")
            elif "a" <= c <= "z":
                reps = 1 + ord(c) - ord("a")
                out.append("."*reps)
            elif "0" <= c <= "9":
                out.append(c)
            else:
                raise Exception(f'Invalid char "{c}" in "{inStr}"')
        return "".join(out)

    def krazy_solved_str(self):
        s = []
        for line in self.grid:
            for cell in line:
                if cell.solved():
                    s.append(str(next(iter(cell.marks))))
                else:
                    s.append(".")
        return "".join(s)

def main(puzzle):
    s = SuguruKrazy(puzzle)

    print(s)
    print(s.get_solved_count())
    print()

    for i in range(1, 15):
        s.solve_step()
        print(s)
        print(i, ":", s.get_solved_count())
        if s.is_solved():
            break
        print()

    assert(s.krazy_solved_str() == puzzle["solved"])


puzzles = [

 {"puzz":"5b4c4b3d1m1b4c4i1j53d2;ABCCDDEEACCDDEEEAACDFFFFGAHHIFJJGHHIIJJKGHIILJKKGGMLLLLNMMMMNNNN","width":8,"height":8, \
    "solved":"5154315432325231141434525232513141414242353235131215124545324312","ptitle":"KD_Suguru_8x8_V5-B10-P8"},

 {"puzz":"b5i2g1g5b12f2e2a5j4w1g13c3c3d3a5k2a3c4a2i4e3g;AABBCCDEEFFFFGGHAABBCDDEEFIIJJHHAKBCCDDELLIIJHKKKKMNNOOLLLIJHPPQQMMNNOORSSJTTPPQQMMNUORRSSVTTPQWXXUUURYYSVVTZZWWXXUaabYYcVVZZdWWXaaebbYccccZddddaeeebb",\
    "solved":"515135254531212343421313145354512134245232121235425131414543412313252323212254525414151454131343252342313454521434515425323145251323134145231432414252",\
        "height":10,"width":15,"ptitle":"KD_Suguru_15x10_V1-B1-P1"},

 {"puzz":"a4d4a3e66a3a4e6a5h562e3b5a2i15d6b5b1a26c63f5g5j26a4c1b24a5a43m2b3b54b1b23;AAAAABBCCCDDDDEAFFGGGBCCDDHHEEIIFGGBBCJJJJHEEIFFGKBLLMNNHHOEIFPQKKRRMMNHOOSIPPQQKKRMNNTTOSPPUUQKRRMNVVTWSPXXUQQRYYYVTTWSXXUUZZYYaYVTWWSXXUZZZZaaaVVWWS","branches":0,\
    "solved":"245132423454326613241315162545324656562431323165321213654641524156545121326465634312345615313151264163234265424315324152432616262453641215324541314123",\
    "height":10,"width":15,"ptitle":"KD_Suguru_15x10n6_V1-B1-P1"},

    {"puzz":"5a63d6a43b5g41c2a44a2b3g5b1a4d34a6a2a5l1b4d3e2a415a4h5a3a4f3d6g45a5a4c3b2a2b262c5;ABCCCCCDDDEFFFFABBCGGHDDIEEFFJAABBBGHHDIIEEEJKAALGGMHHHIIIJJKKLLLNMMOOPPQJJRKKKLNNMMPPSQQQRTTTTUNNNPVSSQQRWTXTUYZZZVVSSSRWWXXXYYZZZVVVaRRWWWXXYYYaaaaa","branches":0,\
        "solved":"546325136543415215414241326264432363152513153216425263426426532314152153515641652343421264152431615153513241562323626264563431454514131341252612623645",\
        "height":10,"width":15,"ptitle":"KD_Suguru_15x10n6_V1-B1-P2"},
]



if __name__ == "__main__":
    for puzzle in puzzles:
        main(puzzle)
        print("---")
