import Default
import methods.PatternSearch as PatternSearch
import data.Vector as Vector
import data.ObjectiveVal as ObjectiveVal

def calculate(how_ini, branch, args, path_branch):
    vector = Vector.Vector(len(args))
    if how_ini == 0:
        vector.initialize_with_zeros()
    elif how_ini < 4:
        vector.initialize_with_rd_small()
    elif how_ini < 7:
        vector.initialize_with_rd_medium()
    else:
        vector.initialize_with_rd()
    if (Default.AVM_DEF == 'IteratedPatternSearch'):
        pattern_search = PatternSearch.PatternSearch(Default.ACC_FACTOR_DEF)
        for i in range(vector.leng):
            pattern_search.setup(vector.vars, i, branch, path_branch)
            next = pattern_search.evaluate()
            last = ObjectiveVal.ObjectiveVal()
            cnt = 0
            while cnt < Default.MAX_ITERATIONS_DEF:
                cnt += 1
                pattern_search.initialize()
                if (pattern_search.explore()):
                    pattern_search.pattern_move()
                if (next.better_than(last) == False):
                    break
                last = next
                next = pattern_search.evaluate()
            if last.best_answer():
                return vector.vars
    return None