import json
import sys
import numpy as np
from random import shuffle, random, sample, randint
from copy import deepcopy
from math import exp
from json import JSONEncoder

# *** you can change everything except the name of the class, the act function and the problem_data ***
class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

class AI:
    # ^^^ DO NOT change the name of the class ***

    def __init__(self, data=None, initial_values=None):
       
        if data is None:
             #Paste input file location here ****
             f = open ('C:\\Users\Hassan\Desktop\data.json', "r")
             dataa = json.loads(f.read())
             data1 = dataa["sudoku"]
             arr = []
             for i in range(9):
              data2 = json.dumps(data1[i])
              data2 = eval(data2)
              arr = arr + data2
              "print(arr)"
             data3 = eval(str(arr))
             self.data = np.array(data3)
             "print(self.data)"  
        else:
            self.data = data
    
        if initial_values is None:
            self.initial_values = np.arange(81)[self.data > 0]
        else:
            self.initial_values = initial_values
            
    def fill_randomly(self):
        for num in range(9):
            block_index = self.block_index(num)
            block = self.data[block_index]
            zero_value = [ind for i,ind in enumerate(block_index) if block[i] == 0]
            fill = [i for i in range(1,10) if i not in block]
            shuffle(fill)
            for ind, value in zip(zero_value, fill):
                self.data[ind] = value
            
    def block_index(self, k, ignore_initial=False):
        offset_r = (k // 3) * 3
        offset_c = (k % 3)  * 3
        index = [offset_c + (j%3) + 9*(offset_r + (j//3)) for j in range(9)]
        if ignore_initial:
            index = list(filter(lambda x:x not in self.initial_values, index))
        return index
        
    def column_index(self, i, type="data index"):
        if type=="data index":
            column = i % 9
        elif type=="column index":
            column = i
        index = [column + 9 * j for j in range(9)]
        return index
        
    def row_index(self, i, type="data index"):
        if type=="data index":
            row = i // 9
        elif type=="row index":
            row = i
        index = [j + 9*row for j in range(9)]
        return index

    def view_results(self):
        def notzero(s):
            if s < 0 or s > 0: return str(s)
            if s == 0: return "0"
            
        results = np.array([self.data[self.row_index(j, type="row index")] for j in range(9)])
        numpyData = {"sudoku": results}
        #Paste empty JSON file location here ****
        with open("C:\\Users\Hassan\Desktop\sudoku.json", "w") as write_file:
          json.dump(numpyData, write_file, cls=NumpyArrayEncoder)
        
        
    def evaluation_points(self):

        points = 0
        for row in range(9):
            points -= len(set(self.data[self.row_index(row, type="row index")]))
        for col in range(9):
            points -= len(set(self.data[self.column_index(col,type="column index")]))
        return points
    

    def gen_sample_data(self):
        sample_data = deepcopy(self.data)
        block = randint(0,8)
        num_in_block = len(self.block_index(block, ignore_initial=True))
        random_blocks = sample(range(num_in_block),2)
        block1, block2 = [self.block_index(block, ignore_initial=True)[ind] for ind in random_blocks]
        sample_data[block1], sample_data[block2] = sample_data[block2], sample_data[block1]
        return sample_data

def solve(problem_data=None):
    SP = AI(problem_data)
    
    SP.fill_randomly()
    best_SP = deepcopy(SP)
    current_score = SP.evaluation_points()
    best_score = current_score
    T = .5
    loop = 0
    
    while (loop < 400000):
        try:
            candidate_data = SP.gen_sample_data()
            SP_candidate = AI(candidate_data, SP.initial_values)
            candidate_score = SP_candidate.evaluation_points()
            delta = float(current_score - candidate_score)
            
            if (exp((delta/T)) - random() > 0):
                SP = SP_candidate
                current_score = candidate_score 
        
            if (current_score < best_score):
                best_SP = deepcopy(SP)
                best_score = best_SP.evaluation_points()
        
            if candidate_score == -162:
                SP = SP_candidate
                break
    
            T = .99999*T
            loop += 1
        except:
            print("An error has occured." )           
    if best_score == -162:
        print("\nSudoku is solved. Solution is written to file.")
    else:
        print("\nCannot solve Sudoku. (%s/%s points)."%(best_score,-162))
    SP.view_results()


if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        try:
            input = np.array([int(s) for s in sys.argv[1]])
        except:
            print("Sudoku must be 81 entries.")
        assert len(input) == 81, "Sudoku must have 81 entries."
        solve(problem_data=input)
    else:
        solve()
