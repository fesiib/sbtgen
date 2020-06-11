import data.ObjectiveVal as Val
import worker.Runner as Runner
import Default

import sys

def interp(s):
    if s == '':
        return ''
    s = s.strip('\n').strip(' ')
    if s[0] == '(':
        # find according ')' bracket
        i = 1
        balance = 1
        while i < len(s):
            if s[i] == '(':
                balance += 1
            elif s[i] == ')': 
                balance -= 1
                if balance < 0:
                    print('There is a problem in Modifier: ', s)
                    sys.exit(7)
                if balance == 0:
                    break
            i += 1
        if i >= len(s):
            print('There is a problem in Modifier: ', s)
            sys.exit(6)    
        
        s = interp(s[1:i]) + s[(i + 1):]
        return interp(s)
    ls = s.split(' ')
    
    if len(ls) < 2:
        return ls[0]
    
    fi = max(0.0, float(ls[0]))
    se = max(0.0, float(interp(' '.join(ls[2:]))))
    
    if ls[1] == 'or':
        return str(min(fi, se))
    if ls[1] == 'and':
        return str(0.5*fi + 0.5*se)
    sys.exit(6)

def evaluate(args, str_branch, path_branch):
    Runner.run(Default.source, str_branch.split(' ')[0], args)
    
    str_branch = str_branch.split(' ')

    ret = Val.ObjectiveVal()

    f = open(Default.modify, 'r')
    
    #Branch Distance
    i = 0
    last_evals = ''
    while i < len(path_branch):
        str_cur = f.readline()
        if str_cur == '':
            assert False
        str_cur = str_cur.strip('\n').split(' ')
        str_evals = f.readline().strip('\n')
        if str_cur[1] == str(path_branch[i][0]):
            if str_cur[2] == path_branch[i][1]:    
                i += 1
                continue
            else:
                last_evals = str_evals
                break
    ret.bd = len(path_branch) - i
    #print(str_branch, args)
    if last_evals == '':
        assert ret.bd == 0
        while True:
            str_cur = f.readline()
            if str_cur == '':
                return Val.ObjectiveVal()
            str_cur = str_cur.strip('\n').split(' ')
            str_evals = f.readline().strip('\n')
            if str_cur[0] == str_branch[0] and str_cur[1] == str_branch[1]:
                if str_cur[2] == str_branch[2]:
                    last_evals = '0'
                else:
                    last_evals = str_evals
                break
    assert last_evals != ''
    f.close()
    #Approach Level
    ret.al = max(0.0, float(interp(last_evals)))
    ret.normalize()
    
    #print(ret.al + ret.bd, args, str_branch[1], str_branch[2])

    return ret