from string_functions import border_box_variants

import re


def matcher(string):
    m = re.match(r'\[\'(.*?)\'\]', string)
    if m:
        return [m.groups()[0]]
    m = re.match(r'\(\'(.*)\'\)', string)
    if m:
        return border_box_variants(m.groups()[0])
    return []


def parser(fname):
    types = []
    conditions = []
    with open(fname, 'r') as clues:
        types = clues.readline().rstrip().split(',')
        for line in clues:
            if re.search(r'\+', line):
                alts = [matcher(alt) for alt in line.split('+')]
                conditions.append(
                    [item for sublist in alts for item in sublist])
            else:
                conditions.append(matcher(line))
    return (types, conditions)

# extracting the constraint numbers from the text file with the constraints and returning a list of those
# ordered in the way they appear.


def extractCons(fname):
    constraints = []
    with open(fname, 'r') as clues:
        temp = ""
        for line in clues:
            lineA = line.split(" ")
            if len(lineA) != 1:
                constraints.append(lineA[1].rstrip())
    return constraints
