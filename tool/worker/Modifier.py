import astor, ast

import worker.Transformer as Transformer
from copy import deepcopy
import Default

def make_print_statement(name_func, id_branch, bool_branch, approach_lvl):
    str_pref = 'f999999 = open("{}", "a"); '.format(Default.modify) 
    str_main = 'print("{} {} {}", file=f999999); '.format(name_func, id_branch, bool_branch)
    str_main += 'print({}, file=f999999); '.format(approach_lvl)
    str_suff = 'f999999.close()'
    print_statement = ast.parse(str_pref + ' ' + str_main + ' ' + str_suff)
    return print_statement



class Modifier(astor.TreeWalk):
    def CustomSetup(self):
        self.id_branch = 0
        self.name_func = ''
        self.name_args = []

    def pre_FunctionDef(self):
        self.id_branch = 0
        self.name_func = self.cur_node.name
        self.name_args = []
        
        for elem in self.cur_node.args.args:
            self.name_args.append(elem.arg)
        return False
    
    def pre_If(self):

        self.id_branch += 1
        body = self.cur_node.body
        approach_lvl_statement = Transformer.make_approach_lvl_statement(deepcopy(self.cur_node.test))
        body.insert(0, make_print_statement(self.name_func, self.id_branch, 'T', approach_lvl_statement))
        
        approach_lvl_statement = Transformer.make_approach_lvl_statement_rev(deepcopy(self.cur_node.test))
        body = self.cur_node.orelse
        body.insert(0, make_print_statement(self.name_func, self.id_branch, 'F', approach_lvl_statement))
        
        return False