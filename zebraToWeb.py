from string_functions import border_box_variants, superpose_all_langs, superpose_all_langs_gen, string_length, delete_empty_boxes, reduct, vocabulary, hide_negated
from zebra_clue_parser import parser, extractCons
from functools import partial

from parseToRep import parse

import re
import sys
import json

# Take cluefile.txt as argument in cmd line. File must be in same directory.
# third cmd line argument is output file.
# when testing this should be in .JSON format
if len(sys.argv) == 3:
    cluefile = sys.argv[1]
    if(sys.argv[2].endswith(".JSON")):
        outputfile = sys.argv[2]  # .JSON
    else:
        print("Output file must be .JSON")
        sys.exit(1)
else:
    print('Please supply a cluefile')
    sys.exit(1)

# parse rules and extract attribute values for each rule.
parsed_clues = parser(cluefile)
# Extract constraints from cluefile in the order they appear.
constraints = extractCons(cluefile)

# keep track of the attributes.
types = parsed_clues[0]  # ['nat', 'col', 'dri', 'smo', 'pet']


def preconds(fns): return partial(lambda s: all(fn(s) for fn in fns))


# preconditions in specification of puzzle.
pcx1 = partial(lambda s: string_length(s) == 5)  # five houses
pcx2 = partial(lambda s: all(string_length(delete_empty_boxes(reduct(
    hide_negated(s), [v]))) == 1 for v in vocabulary(s)))  # each item is in one house
pcx3 = partial(lambda s: all(all(len(re.findall(r'{}\([^)]+?\)'.format(
    t), c)) < 2 for t in types) for c in hide_negated(s).split('|')))  # each house has one item

# superposing the preconditions with the parsed rules from the cluefiles.
# output is a list of list with the attribute values of each house at each application
# of a constraint.
sp = superpose_all_langs_gen(parsed_clues[1], preconds([pcx1, pcx2, pcx3]))

rcount = 0  # rule count
d = {}
possibilities = []
cleaned_poss = []
for l in sp:
    for s in l:
        # s is a string compirsed of the attribute values for the five house.
        # in the cases where branching occurs I check for whether the output is a list of strings or just one string.
        if(len(l) == 1):
            # the string is parsed into an array of values for each house.
            # hide_negated(s) function removes all negated values in string.
            parsed = parse(hide_negated(s))
            # The result is appended to a dictionary, with the key being the corresponding constraint.
            d[f"Constraint_{constraints[rcount]}"] = parsed
        else:
            possibilities.append(hide_negated(s))
    if(len(l) != 1):
        for v in possibilities:
            cleaned_poss.append(parse(v))
        # appending a list of all the attribute values that are branches when this particular constraint is applied.
        d[f"Constraint_{constraints[rcount]}"] = cleaned_poss
    # reset for next iteration
    possibilities = []
    cleaned_poss = []
    rcount += 1


# getting format in json | [items : all data].
elements = []
elements.append(d)
solution = {"items": elements}
json.dump(solution, open(outputfile, "w"))
