# Usage of covgen.py
USAGE_DEF = 'usage: python3 covgen.py <input.py> -a <method> -v <0/1> -f <function name>'


# Timeout (not implemented)
TIMEOUT_DEF = 15


# Method of search, currently only Iterated Pattern Search is available
AVM_DEF = 'IteratedPatternSearch'

# Acceleration factor for Pattern Search
ACC_FACTOR_DEF = 2

# K that is used for Approach Level calculations
K_DEF = 1

# Normalization function of Approach Level. Must be an integer from [0,1]
NORMALIZATION_DEF = 1

# Maximum iterations of explorations in the Pattern Search
MAX_ITERATIONS_DEF = 1000


# Some kind of verbose feature, print out line-numbers for True branches
ADD_LINENO = False


# Function name for which we generate inputs, by default, we generate inputs for all functions in the given source code
FUNC_NAME_DEF = None


# Rerun of Method (more specifically, Iterated Pattern Search by default)
RERUN_DEF = 30

# Modified source code
source = ''


# Do not print output
NO_OUTPUT = False

# File where we collect answers
collect = 'collector_999999.txt'

# File where we put output of Default.source
modify = 'modify_999999.txt'