from collections import defaultdict

class Cell():
    def __init__(self, i, j, block) -> None:
        self.i = i
        self.j = j
        self.block = block
        self.marks = None

    def solved(self) -> bool:
        return self.marks and len(self.marks) == 1

    def __repr__(self) -> str:
        return f'({self.i}, {self.j}, {self.block}, {self.marks})'

    def __hash__(self) -> int:
        return hash((self.i, self.j))

class Suguru():
    def __init__(self):
        self.blocks = defaultdict(list[Cell])
        self.grid = [] #2D array
        self.width = None
        self.height = None

    def parseFile(self, fname):
        with open(fname, 'r') as f:
            for i, line in enumerate(f.read().splitlines()):
                cells = []
                for j in range(len(line)//2):
                    val, block = line[2*j:2*j+2]
                    c = Cell(i, j, block)
                    if val != ' ':
                        c.marks = {int(val)}
                    self.blocks[block].append(c)
                    cells.append(c)
                self.grid.append(cells)
            self.height = i + 1
            self.width = j + 1
        self.__set_marks()

    def __set_marks(self):
        for block in self.blocks.values():
            for cell in block:
                if not cell.marks:
                    cell.marks = set(range(1, len(block) +1))

    def get_cell(self, i, j) -> Cell: #Just for type info
        return self.grid[i][j]

    def is_solved(self):
        return all(c.solved() for line in self.grid for c in line)

    def get_solved_count(self):
        return sum(c.solved() for line in self.grid for c in line)

    def print_progress(self):
        pass

    def solve_step(self):
        self.__propagate_block()
        self.__propagate_solved_to_neighbors()
        self.__pairs_in_block()
        self.__block_single_pos()
        self.__propagate_marks()

    def __propagate_block(self):
        # In a block, propagate solved cells to others
        for block in self.blocks.values():
            solved = set()
            for cell in block:
                if cell.solved():
                    solved |= cell.marks
            for cell in block:
                if not cell.solved():
                    cell.marks -= solved

    def __neighbors(self, cell:Cell) -> list[Cell]:
        neighbors = []
        for i, j in [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]:
            i += cell.i
            j += cell.j
            if (0 <= i < self.height) and (0<= j < self.width):
                neighbors.append(self.grid[i][j])
        return neighbors 

    def __propagate_solved_to_neighbors(self):
        # Remove solved cell value from neighbor cells 
        for line in self.grid:
            for cell in line:
                if cell.solved():
                    for n in self.__neighbors(cell):
                        n.marks -= cell.marks

    def __pairs_in_block(self):
        # Within a block, if there is a pair or triple that have the same marks, they are linked
        # Remove those marks from other cells in the block
        for block in self.blocks.values():
            d = defaultdict(int)
            for cell in block:
                d[frozenset(cell.marks)] += 1
            for marks, count in d.items():
                if count > 1 and len(marks) == count:
                    for cell in block:
                        if not cell.solved() and cell.marks != marks:
                            cell.marks -= marks
    
    def __block_single_pos(self):
        # If a value is only possible in one place in a block, then set it
        for block in self.blocks.values():
            val_cells = defaultdict(list)
            for cell in block:
                for val in cell.marks:
                    val_cells[val].append(cell)
            for val, cells in val_cells.items():
                if len(cells) == 1 and not cells[0].solved():
                    cells[0].marks = {val}

    def __propagate_marks(self):
        # If cells in a block have a mark 
        for block in self.blocks.values():
            unsolved = set()
            for c in block:
                if not c.solved():
                    unsolved |= c.marks
            for val in unsolved:
                cells_with_val = set(c for c in block if val in c.marks)
                if len(cells_with_val):
                    #See if cells have common neighbors:
                    neighbors = [set(self.__neighbors(c)) for c in cells_with_val]
                    common = set.intersection(*neighbors)
                    for cell in common:
                        if val in cell.marks:
                            cell.marks -= {val}

    def __repr__(self) -> str:
        grid = []
        for i in range(self.height):
            line = []
            for j in range(self.width):
                c = self.get_cell(i, j)
                marks = "".join(map(str, sorted(c.marks)))
                line.append(f'{c.block}:{marks.ljust(5)}')
            grid.append(' '.join(line))
        return '\n'.join(grid)

def main():
    s = Suguru()
    fname = '6x6.txt'

    s.parseFile(fname)
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

if __name__ == '__main__':
    main()