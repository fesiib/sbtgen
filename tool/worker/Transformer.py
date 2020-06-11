import ast, astor, sys

import Default

K_DEF = Default.K_DEF

def make_approach_lvl_statement(body):
    
    body = ast.parse(astor.to_source(body))
    walker = SmallModifier()
    walker.CustomSetup()
    walker.walk(body)
    return astor.to_source(body).strip('\n').replace('\n', '').replace('    ', '')

def make_approach_lvl_statement_rev(body):
    
    body = ast.parse(astor.to_source(body))
    walker = RevSmallModifier()
    walker.CustomSetup()
    walker.walk(body)
    return astor.to_source(body).strip('\n').replace('\n', '').replace('    ', '')


class SmallModifier(astor.TreeWalk):
    def CustomSetup(self):
        self.result = ''
        self.k = K_DEF
    
    def post_BoolOp(self):
        replacement = '"( " + ' + astor.to_source(self.cur_node.values[0]).strip('\n')
        op = ast.dump(self.cur_node.op)

        for value in self.cur_node.values[1:]:    
            if (op == 'Or()'):
                replacement += ' + " and " + ' + astor.to_source(value).strip('\n')
            elif (op == 'And()'):
                replacement += ' + " or " + ' + astor.to_source(value).strip('\n')
            else:
                print('Does not support such operator ', op)
                sys.exit(4)
        replacement += ' + " )"'
        new_node = ast.parse(replacement)
        if (self.parent == None):
            print("Unexpected error: there must be parent")
            sys.exit(4)
        else:
            self.replace(new_node)    
        
        return True
    
    def pre_Compare(self):
        replacement = '"( " + '
        lef = astor.to_source(self.cur_node.left).strip('\n')
        for i in range(len(self.cur_node.ops)):
            op = ast.dump(self.cur_node.ops[i])
            rig = astor.to_source(self.cur_node.comparators[i]).strip('\n')
            if op == 'Eq()':
                replacement += 'str(int({} == {}) * {})'.format(lef, rig, self.k)
            elif op == 'NotEq()':
                replacement += 'str(abs({} - {}))'.format(lef, rig)
            elif op == 'Lt()':
                replacement += 'str({1} - {0})'.format(lef, rig)
            elif op == 'LtE()':
                replacement += 'str({1} - {0} + {2})'.format(lef, rig, self.k)
            elif op == 'Gt()':
                replacement += 'str({} - {})'.format(lef, rig)
            elif op == 'GtE()':
                replacement += 'str({} - {} + {})'.format(lef, rig, self.k)
            else:
                print('Does not support such comparator', op)
                sys.exit(4)
            lef = rig
            if i < len(self.cur_node.ops) - 1:
                replacement += ' + " or " + '
        replacement += ' + " )"'
        new_node = ast.parse(replacement)
        if (self.parent == None):
            print("Unexpected error: there must be parent")
            sys.exit(4)
        else:
            self.replace(new_node)    
        return False


class RevSmallModifier(astor.TreeWalk):
    def CustomSetup(self):
        self.result = ''
        self.k = K_DEF
    
    def post_BoolOp(self):
        replacement = '"( " + ' + astor.to_source(self.cur_node.values[0]).strip('\n')
        op = ast.dump(self.cur_node.op)

        for value in self.cur_node.values[1:]:    
            if (op == 'Or()'):
                replacement += ' + " or " + ' + astor.to_source(value).strip('\n')
            elif (op == 'And()'):
                replacement += ' + " and " + ' + astor.to_source(value).strip('\n')
            else:
                print('Does not support such operator ', op)
                sys.exit(4)
        replacement += ' + " )"'
        new_node = ast.parse(replacement)
        if (self.parent == None):
            print("Unexpected error: there must be parent")
            sys.exit(4)
        else:
            self.replace(new_node)    
        
        return True
    
    def pre_Compare(self):
        replacement = '"( " + '
        lef = astor.to_source(self.cur_node.left).strip('\n')
        for i in range(len(self.cur_node.ops)):
            op = ast.dump(self.cur_node.ops[i])
            rig = astor.to_source(self.cur_node.comparators[i]).strip('\n')
            if op == 'Eq()':
                replacement += 'str(abs({} - {}))'.format(lef, rig)
            elif op == 'NotEq()':
                replacement += 'str(int({} == {}) * {})'.format(lef, rig, self.k)
            elif op == 'Lt()':
                replacement += 'str({} - {} + {})'.format(lef, rig, self.k)
            elif op == 'LtE()':
                replacement += 'str({} - {})'.format(lef, rig)
            elif op == 'Gt()':
                replacement += 'str({1} - {0} + {2})'.format(lef, rig, self.k)
            elif op == 'GtE()':
                replacement += 'str({1} - {0})'.format(lef, rig)
            else:
                print('Does not support such comparator', op)
                sys.exit(4)
            lef = rig
            if i < len(self.cur_node.ops) - 1:
                replacement += ' + " and " + '
        replacement += ' + " )"'
        new_node = ast.parse(replacement)
        if (self.parent == None):
            print("Unexpected error: there must be parent")
            sys.exit(4)
        else:
            self.replace(new_node)    
        return False
