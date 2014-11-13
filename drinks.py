# -*- coding: utf-8 -*-
# Time-stamp: <2014-11-12 13:53:29 moss>

######################################
# Scipt for handling drinks          #
#                                    #
# Made by:  Mads Fabricius Scmidt    #
#           Jakob Rørstes Mosumgaard #
######################################

###########
# Modules #
###########
import codecs
import subprocess
import collections
import argparse


#####################
# Initial variables #
#####################

# Encoding is always utf8!
ENCODING = 'utf8'

# ... except the input to plain TeX
# Wich is why we use xetex :-)
OUTPUT_ENCODING = 'utf8'

# Name of drinks file defining drinks. Default 'drinks.txt'
drinksfilename = 'drinks.txt'

# Verbose (Print warnings)
verbose = False

# Sort barcards by price
sortbarcard = False


def readdrinks(drinksfile):
    drinks = []

    # Read the file line by line
    for line in drinksfile:
        # Get the current drink
        if line.startswith('='):
            name = line[1:].strip()

            # Sort into secret and normal drinks
            if name.startswith('?'):
                secret = True
                name = name[1:].strip()
            else:
                secret = False

            currentdrinkdict = {
                'name': name,
                'soda': [],
                'spirit': [],
                'other': [],
                'price': '',
                'secret': secret,
            }
            drinks.append(currentdrinkdict)

        # Soda
        elif line.startswith('--'):
            currentsoda = line[2:].strip()
            currentdrinkdict['soda'].append(currentsoda)

        # Spirit
        elif line.startswith('-'):
            currentspirit = line[1:].strip()
            currentdrinkdict['spirit'].append(currentspirit)

        # Other
        elif line.startswith('!'):
            currentother = line[1:].strip()
            currentdrinkdict['other'].append(currentother)

        # Price
        elif line.startswith('$'):
            currentprice = line[1:].strip()
            currentdrinkdict['price'] = currentprice
        # Comment
        elif line.startswith('#'):
            pass
        # Empty line
        elif line.startswith('\n'):
            pass
        # Unrecognized line.
        # Maybe we should print a warning (with line number)?
        else:
            if verbose:
                print('Unrecognized line: ' + line.strip())
            else:
                pass

    return drinks


def generatebarcard(drinks):
    for currentingredients in drinks:
        if currentingredients['secret']:
            # Skip secret drinks
            continue

        drink = currentingredients['name']
        yield r'\drik %s' % drink
        yield r'\til %s' % currentingredients['price']

        # Write every other thing:
        yield r'\med %'

        for spirit in currentingredients['spirit']:
            amount = '\t\t'
            if '-' in spirit:
                # Split returns an array of strings.
                # amount is the first of these
                amount, spirit = spirit.split('-')
                amount = amount.strip() + '\t'
                spirit = spirit.strip()
            yield r'%s& %s \og' % (amount, spirit)

        for soda in currentingredients['soda']:
            yield '\t\t& %s \og' % soda

        for other in currentingredients['other']:
            yield '\t\t' + r'\serveret I et %s med is' % other
            yield ''


def generatemixingcard(drinks):
    # Do TeX-stuff
    yield r'\begin{tabular}{lllll}'
    yield r'\toprule Navn & Sprut & Sodavand & Severing & Pris \\'
    yield r'\midrule'

    # Loop over all drinks
    for drinknumber, currentingredients in enumerate(drinks):
        drink = currentingredients['name']
        mixingcardformat = (
            u'{color}{drink} & {ingredients} & '
            u'{soda} & {other} & {price} kr\\\\\n'
        )
        mixingcardline = mixingcardformat.format(
            color='\\rowcolor{Gray}%\n' if drinknumber % 2 == 0 else '',
            drink=drink,
            ingredients=', '.join(' '.join(part for part in spirit.split('-'))
                                  for spirit in currentingredients['spirit']),
            soda=' '.join(currentingredients.get('soda', [])),
            other=' '.join(currentingredients['other']),
            price=currentingredients['price'],
            )

        yield mixingcardline

    yield r'\bottomrule'
    yield r'\end{tabular}'


#####################################
# The function which does the magic #
#####################################
def makedrinks():
    with codecs.open(drinksfilename, 'r', encoding=ENCODING) as drinksfile:
        drinks = readdrinks(drinksfile)

    # Now we make the barcards ("drinkskort").
    # This won't contain the secret drinks.
    # Right now the drinks aren't sorted.
    # The current format of the output is:
    # \drink [name]
    # \til [price]
    # \med %
    #     [amount]    & [kind] \og
    #                 & [kind] \og
    #                 & [soda] \og
    #     \serveret i et [other] med is


    # Write to .tex file. Loop over the number of drinks.

    if sortbarcard:
        print('Sorting barcard ' + str(drinks))
        price_sorted_drinks = sorted(drinks, key=lambda drink: drink['price'])
        drinks = price_sorted_drinks
        print(str(drinks))

    with codecs.open('barcard.tex', 'w', encoding=OUTPUT_ENCODING) as barcard:
        for line in generatebarcard(drinks):
            barcard.write('%s\n' % line)

    # Sort all drinks by name
    drinks_sorted = sorted(drinks, key=lambda drink: drink['name'])

    # Open file for the mixing card ("blandeliste")
    with codecs.open('mixing.tex', 'w', encoding=ENCODING) as mixingcard:
        for line in generatemixingcard(drinks_sorted):
            mixingcard.write('%s\n' % line)

    # As we are having problems with utf8 and plain tex we use xetex as this has nooo problem
    # with utf8
    # XeTeX is installed on imf computers...
    # Also xetex seems to have problems when called as a subprocess. Why i dont know.
    # Use makefile instead.
    # subprocess.check_call(
    #     'xetex -output-driver="xdvipdfmx -q -E -p a4 -l" barcardmain.tex'.split())
    # subprocess.check_call(
    #     'latexmk -pdf mixingcardmain.tex'.split())
    # Wuhu! Done!

def setupargparser():
    global verbose
    global sortbarcard
    global drinksfilename

    parser = argparse.ArgumentParser(
        description='Make barcards')

    parser.add_argument('filename')
    parser.add_argument('-v','--verbose', action='store_true', default=False,
        help='Do you want verbose output?')
    parser.add_argument('-s','--sortbarcards', action='store_true',default=False,
        help='Do you want barcards sorted?')

    args = parser.parse_args()
    drinksfilename = args.filename
    verbose = args.verbose
    sortbarcard = args.sortbarcards




# Run the function if file is called directly
if __name__ == '__main__':
    setupargparser()
    makedrinks()
