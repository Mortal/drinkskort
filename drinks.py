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


#####################
# Initial variables #
#####################

# Encoding is always utf8!
ENCODING = 'utf8'

# ... except the input to plain TeX
OUTPUT_ENCODING = 'latin1'

# Name of drinks file defining drinks. Default 'drinks.txt'
drinksfilename = 'drinks.txt'


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

        # Unrecognized line.
        # Maybe we should print a warning (with line number)?
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
            amount = '\t'
            if '-' in spirit:
                # Split returns an array of strings.
                # amount is the first of these
                amount, spirit = spirit.split('-')
                amount = amount.strip() + '\t'
                spirit = spirit.strip()
            yield r'%s& %s\og' % (amount, spirit)

        for soda in currentingredients['soda']:
            yield r'& %s\og' % soda

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
            u'{soda} & {other} & {price} kr\\\\ \n'
        )
        mixingcardline = mixingcardformat.format(
            color='\\rowcolor{Gray} ' if drinknumber % 2 == 0 else '',
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

    # \section*{name}
    # \begin{itemize}
    # 	\item spirits
    # 	\item sodas
    # 	\item others
    # 	\item price
    # \end{itemize}

    # Write to .tex file. Loop over the number of drinks.
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
    # XeTeX is installed on imf computers...
    # Also xetex seems to have problems when called as a subprocess. Why i dont know.
    # Use make instead?
    # subprocess.check_call(
    #     'xetex -output-driver="xdvipdfmx -q -E -p a4 -l" barcardmain.tex'.split())
    # subprocess.check_call(
    #     'latexmk -pdf mixingcardmain.tex'.split())
    # Wuhu! Done!


# Run the function if file is called directly
if __name__ == '__main__':
    makedrinks()
