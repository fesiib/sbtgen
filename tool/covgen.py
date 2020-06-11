import astor, ast
import sys, getopt, os

import worker.Modifier as Modifier
import worker.Runner as Runner
import worker.Searcher as Searcher
import Default

def parse_argv(argv):
    #file_name
    fname = ''
    if (len(argv) == 0):
        print(Default.USAGE_DEF)
        sys.exit(2)
    fname = argv[0]
    name_file, ext_file = os.path.splitext(fname)
    if (ext_file != '.py'):
        print(Default.USAGE_DEF)
        sys.exit(2)
    #AVM type
    avm = Default.AVM_DEF
    add_lineno = Default.ADD_LINENO
    argv = argv[1:]
    try:
        opts, args = getopt.getopt(argv, "a:v:f:n", ["avmtype=", "add_lineno=", "func_name=", "no_output"])
    except getopt.GetoptError:
        print(Default.USAGE_DEF)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-a", "--avmtype"):
            avm = arg
        if opt in ("-v", "--add_lineno"):
            if arg == '1' or arg == 'true' or arg == 't':
                add_lineno = True
        if opt in ("-f", "--func_name"):
            Default.FUNC_NAME_DEF = arg
        if opt in ("-n", "--no_output"):
            Default.NO_OUTPUT = True
    Default.AVM_DEF = avm
    Default.ADD_LINENO = add_lineno
    return fname

def main(argv):
    fname = parse_argv(argv).strip(' ')
    if not os.path.exists(fname):
        print('No such file exists:', fname)
        sys.exit(0)

    tree = astor.CodeToAst.parse_file(fname)
    
    
    modify = Modifier.Modifier()
    modify.CustomSetup()
    modify.walk(tree)

    Default.source = astor.to_source(tree)

    search = Searcher.Searcher()
    search.CustomSetup()
    search.walk(tree)

    #Remove files and print
    if os.path.exists(Default.modify):
        os.remove(Default.modify)
    if os.path.exists(Default.collect):
        if not Default.NO_OUTPUT:    
            f = open(Default.collect, 'r')
            ans = []
            while True:
                cur = f.readline()
                if cur == '':
                    break
                cur = cur.strip('\n').strip(' ').split(' ')
                if cur[2] == 'T':
                    cur[2] = 'F'
                else:
                    cur[2] = 'T'
                ans.append(cur)
            ans.sort()
            for i in ans:
                if i[2] == 'T':
                    i[2] = 'F'
                else:
                    i[2] = 'T'
                print(' '.join(i))
            f.close()

        os.remove(Default.collect)
    else:
        print('function does not exist / function does not contain branches / something went wrong')    
if __name__ == '__main__':
    #Remove files and print
    if os.path.exists(Default.modify):
        os.remove(Default.modify)
    if os.path.exists(Default.collect):
        os.remove(Default.collect)
    main(sys.argv[1:])


