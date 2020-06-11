import Default

import worker.Runner as Runner

def check(args, str_branch):
    Runner.run(Default.source, str_branch.split(' ')[0], args)
    
    str_branch = str_branch.split(' ')

    f = open(Default.modify, 'r')
    
    #Branch Distance
    i = 0
    ret = False
    while True:
        str_cur = f.readline()
        if str_cur == '':
            break
        str_cur = str_cur.strip('\n').split(' ')
        str_evals = f.readline().strip('\n')
        if str_cur[0] == str_branch[0] and str_cur[1] == str_branch[1] and str_cur[2] == str_branch[2]:
            ret = True
            break
    f.close()
    return ret