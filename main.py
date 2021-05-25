grammar = [
    'S->B',
    'B->C',
    'B->CcB',
    'C->adD',
    'D->Ae',
    'A->b',
    'A->Ab',
    'B->d'
]


# parse the grammar and split the rules in a dict with key values- nt symbols
def parseGrammar():
    fa = {}
    for rulepart in grammar:
        x = rulepart.split('->')
        if not x[0] in fa:
            fa[x[0]] = []

        symbols = []
        for symbol in x[1]:
            symbols.append(symbol)
        fa[x[0]].append(symbols)

    return fa


dict = parseGrammar()

non_term = [x for x in dict.keys()]
term = []
for j in dict.values():
    for i in j:
        for k in i:
            if k.islower() and k not in term:
                term.append(k)
start_symbol = 'S'

print('Lab 4 Condition: Simple Precedence Parsing')
print('Terminals:')
print(term)
print('Non-Terminals')
print(non_term)
print('Production Rules')
print(grammar)
print('Converting Production Rules to Dict')
print(dict)


# First-last Table Generation
print('*******************')
print(' ')
print('1. First/Last table')

# we create a similar dictionary like in parseGrammar function
# in this case we have as keys the non-terminals
# and as values a set for first symbols and a set for last symbols

index = []
first = []
last = []

for symbol in dict:
    index.append(symbol)
    to_find = []
    to_find.append(symbol)
    found = []
    first_symbol = []

    # FIRST SET
    i = 0
    while i < len(to_find):
        if to_find[i] in dict:
            found.append(to_find[i])
            for rule in dict[to_find[i]]:
                if rule[0] not in first_symbol:
                    first_symbol.append(rule[0])
                if rule[0] in non_term and rule[0] not in found:
                    to_find.append(rule[0])
        i += 1

    first.append(first_symbol)
    to_find = []
    to_find.append(symbol)
    found = []
    last_symbol = []

    # LAST SET
    i = 0
    while i < len(to_find):
        if to_find[i] in dict:
            found.append(to_find[i])
            for rule in dict[to_find[i]]:
                if rule[-1] not in last_symbol:
                    last_symbol.append(rule[-1])
                if rule[-1] in non_term and rule[-1] not in found:
                    to_find.append(rule[-1])
        i += 1
    last.append(last_symbol)

# print the FIRST LAST table

print('\t{:<5} {:<25} {:25}'.format('', ' FIRST', 'LAST'))
for i in range(5):
    print('\t{:<5}: {:<15} {:15}'.format(index[i], str(first[i]), str(last[i])))



idx = 0
# create a dictionary with terminals and nonterminals
all_symbols = {}
for symbol in non_term:
    all_symbols[symbol] = idx
    idx += 1
for symbol in term:
    all_symbols[symbol] = idx
    idx += 1


simple_pr_table= [[[] for x in range(idx + 1)] for y in range(idx + 1)]
idx = 1
# Append the nonterminals
for symbol in non_term:
    simple_pr_table[0][idx].append(symbol)
    simple_pr_table[idx][0].append(symbol)
    idx +=1
# Append the terminals
for symbol in term:
    for ch in symbol:
        simple_pr_table[0][idx].append(ch)
        simple_pr_table[idx][0].append(ch)
    idx +=1

# First Rule
# Find (=) rules by analysing each two symbols of a production
for key in dict:
    for prod in dict[key]:
        if len(prod) > 1:
            for idx in range(len(prod) - 1):
                first_symbol = prod[idx]
                second_symbol = prod[idx + 1]
                # Add the equal sign to the precedence table
                if '=' not in simple_pr_table[all_symbols[first_symbol] + 1][all_symbols[second_symbol] + 1]:
                    simple_pr_table[all_symbols[first_symbol] + 1][all_symbols[second_symbol] + 1].append('=')



# Second Rule
# Find (<) rules by analysing each two elements of a production
# terminal OR nonterminal < FIRST(nonterminal)
for key in dict:
    for prod in dict[key]:
        if len(prod) > 1:
            for idx in range(len(prod) - 1):
                first_symbol = prod[idx]
                second_symbol = prod[idx + 1]
                if second_symbol in non_term:
                    second_index = index.index(second_symbol)
                    for s in first[second_index]:
                    # Add the less sign to the precedence table
                        if '<' not in simple_pr_table[all_symbols[first_symbol] + 1][all_symbols[s] + 1]:
                            simple_pr_table[all_symbols[first_symbol] + 1][all_symbols[s] + 1].append('<')

# Third Rule
# Find (>) rules by analysing each two elements of a production
for key in dict:
    for prod in dict[key]:
        if len(prod) > 1:
            for idx in range(len(prod)-1):
                first_symbol = prod[idx]
                second_symbol = prod[idx + 1]
                # a) if nonterminal is followed by a terminal
                # LAST(nonterminal) > terminal
                if first_symbol in non_term and second_symbol in term:
                    first_index = index.index(first_symbol)
                    for s in last[first_index]:
                        # Add the greater sign to the precedence table
                        if '>' not in simple_pr_table[all_symbols[s] + 1][all_symbols[second_symbol] + 1]:
                            simple_pr_table[all_symbols[s] + 1][all_symbols[second_symbol] + 1].append('>')

                # b) if nonterminal is followed by a nonterminal
                # LAST(first_symbol) > (FIRST(second_symbol) in intersection with terminals)
                if first_symbol in non_term and second_symbol in non_term:
                    first_index = index.index(first_symbol)
                    second_index = index.index(second_symbol)
                    for s1 in last[first_index]:
                        for s2 in first[second_index]:
                            if s2 in term:
                                if '>' not in simple_pr_table[all_symbols[s1] + 1][all_symbols[s2] + 1]:
                                    simple_pr_table[all_symbols[s1] + 1][all_symbols[s2] + 1].append('>')

def matrix_representation(matrix):
    for row in matrix:
        for column in row:
            print('{:<7}'.format(str(column)), end='')
        print()


print('*******************')

print('\n\n2.Simple Precedence Matrix')
matrix_representation(simple_pr_table)

print('*******************')


print('\n\nStep 3. Parse the word adbecd ')
word_analysis = 'adbecd'
stack_string = [word_analysis[0]]
for index in range(1, len(word_analysis)):
    row = all_symbols[word_analysis[index - 1]] + 1
    column = all_symbols[word_analysis[index]] + 1
    stack_string.append(simple_pr_table[row][column][0])
    stack_string.append(word_analysis[index])
print(''.join(stack_string))

while len(stack_string) != 1 and stack_string[0] != 'S':
    # Find production rules which matches sublist in Stack String List
    index1 = 0
    index2 = 1
    while 1:
        if index2 < len(stack_string) and stack_string[index2] != '<' and stack_string[index2] != '>':
            index2 += 1
        else:
            temp = stack_string[index1:index2]
            temp = ''.join(temp)
            temp = temp.replace('=', '')
            # var created to find out if the prod rule selected will match the stack_string sublist
            temp_boolean = False
            for symbol in dict:
                for rule in dict[symbol]:
                    existing_rule = ''.join(rule)
                    if existing_rule == temp:
                        temp_boolean = True
                        ch_symbol = symbol

            if temp_boolean == True:
                stack_string[index1] = ch_symbol
                if index2 < len(stack_string):
                    stack_string[index2] = ' '
                if index1 > 0:
                    stack_string[index1 - 1] = ' '
                del stack_string[index1 + 1: index2]
                break
            else:
                index1 = index2 + 1
                index2 += 2

    for index in range(len(stack_string) // 2):
        row = all_symbols[stack_string[index * 2]] + 1
        column = all_symbols[stack_string[index * 2 + 2]] + 1
        stack_string[index * 2 + 1] = simple_pr_table[row][column][0]
    print(''.join(stack_string))
    #print(stack_string)

if len(stack_string) == 1 and stack_string[0] == 'S' or stack_string[0] == 'B':
    del stack_string[0]
    stack_string.append('S')
    print(''.join(stack_string))
    print('Parsed Correctly!')
