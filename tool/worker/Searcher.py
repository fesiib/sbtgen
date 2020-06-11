import astor, ast, sys

import worker.Runner as Runner
import methods.Generic as Generic
import worker.Checker as Checker
import Default

def calculate(str_branch, name_args, path_branch):
    for i in range(Default.RERUN_DEF):
        ret = Generic.calculate(i, str_branch, name_args, path_branch)
        if ret != None:
            return ret
    return None

def ans_print(str_branch, str_lineno, ans):
    f = open(Default.collect, 'a')
    if ans == None:
        print(str_branch + ' - ' + str_lineno, file=f)
    else: 
        if not Checker.check(ans, str_branch):
            print("Found answer is incorrect for '{}': {}".format(str_branch, ans))
            sys.exit(7)
        print(str_branch, end = ' ', file = f)
        for i in ans:
            print(i, end = ' ', file = f)
        print(' ' + str_lineno, file = f)    
    f.close()

class Searcher(astor.TreeWalk):
    def CustomSetup(self):
        self.id_branch = 0
        self.name_func = ''
        self.name_args = []
        self.path_branch = []
    
    def pre_FunctionDef(self):
        self.id_branch = 0
        self.name_func = self.cur_node.name
        self.name_args = []
        self.path_branch = []
        for elem in self.cur_node.args.args:
            self.name_args.append(elem.arg)
        if Default.FUNC_NAME_DEF != None:
            if Default.FUNC_NAME_DEF != self.name_func:
                return True
        return False
    
    def pre_If(self):
        
        self.id_branch += 1
        cur_id = self.id_branch

        #iT
        #print(cur_id, ' T ', self.path_branch, astor.dump_tree(self.cur_node.body))
        str_branch = self.name_func + ' ' + str(cur_id) + ' T'
        ans = calculate(str_branch, self.name_args, self.path_branch)
        body = self.cur_node.body
        str_lineno = '(#line={})'.format(self.cur_node.lineno)
        if not Default.ADD_LINENO:
            str_lineno = ''
        ans_print(str_branch, str_lineno, ans)
        
        #iF
        #print(cur_id, ' F ', self.path_branch, astor.dump_tree(self.cur_node.body))
        str_branch = self.name_func + ' ' + str(cur_id) + ' F'
        ans = calculate(str_branch, self.name_args, self.path_branch)
        orelse = self.cur_node.orelse
        ans_print(str_branch, '', ans)
        
        self.path_branch.append((cur_id, 'T'))
        self.walk(body)
        self.path_branch.pop()
        
        self.path_branch.append((cur_id, 'F'))
        self.walk(orelse)
        self.path_branch.pop()
        return True
    
    def pre_For(self):
        return True

    def pre_While(self):
        return True

