import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        mines = set()
        if self.count == len(self.cells):
            for cell in self.cells:
                mines.add(cell)
     
        return mines
        
        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        safes = set()
        if self.count == 0:
            for cell in self.cells:
                safes.add(cell)
        return safes


        raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        contains = cell in self.cells
        if contains:
            self.cells.remove(cell)
            if self.count > 0:
                self.count = self.count -1    
       
        return
        raise NotImplementedError
        

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        contains = cell in self.cells
        if contains:
            self.cells.remove(cell)
        
        return
       
        raise NotImplementedError


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()
         
        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.update(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

       

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.update(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
        

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """


        #1) mark the cell as a move that has been made
        #2) mark the cell as safe

        self.moves_made.add(cell)
               
       
        for sentence in self.knowledge:
            sentence.mark_safe(cell) 
            if len(sentence.cells) == 0:   
                if sentence in self.knowledge:
                        self.knowledge.remove(sentence)

        
        
        
        #3) add a new sentence to the AI's knowledge base
        #       based on the value of `cell` and `count`
        #built new sentence , we check neighbours  
        a = cell[0]
        b = cell[1]
        new_sentence_cells =  set()

        for i in range(a-1,a+2):
            if (i >= 0 and i <= 7):
                for j in range(b-1,b+2):
                    if (j >= 0 and j <= 7):
                        # cell(i,j) test if used or mine
                        if (i,j) not in self.moves_made:
                            new_sentence_cells.add((i,j))

        #add to knowledge                     
        if len(new_sentence_cells) > 0 and count >= 0:
            new_know = Sentence(new_sentence_cells,count)
            self.knowledge.append(new_know)
        
        #mark as safe in each sentence and adding new possible known mines and known safes
        for sentence in self.knowledge:
            sentence.mark_safe((a,b))
            self.mines.update(sentence.known_mines())
            self.safes.update(sentence.known_safes())
            self.safes.difference_update(self.moves_made)
        
        #clean known mines:
        for sentence in self.knowledge:
            for mine in self.mines:
                sentence.mark_mine(mine)
                

        #clean known safe cells:
        for sentence in self.knowledge:
            for safe in self.safes:
                sentence.mark_safe(safe)
                
        #clean empty clauses:
        for sentence in self.knowledge:
            if len(sentence.cells) == 0:
                self.knowledge.remove(sentence)

        #5 - last step inference, create new rules: 
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                    if sentence1 != sentence2:
                        if sentence1.cells.issubset(sentence2.cells):
                            newsentence = Sentence(sentence2.cells - sentence1.cells, sentence2.count - sentence1.count)
                            if newsentence not in self.knowledge:
                                 self.knowledge.append(newsentence)
        
        return
        raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
 
        for cell in self.safes:
            if cell not in self.moves_made and cell not in self.mines:
                return cell
        
        return

        raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        import random
        a = random.randint(0,7)
        b = random.randint(0,7)

        count = 0
        for i in range(a, a+8):
            for j in range(b, b+8):
                x1 = i % 7
                y1 = j % 7
                if (x1,y1) not in self.moves_made:
                        if (x1,y1) not in self.mines:
                            return (x1,y1)

        return
        
        raise NotImplementedError
