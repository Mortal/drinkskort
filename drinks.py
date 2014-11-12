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
import collections


#####################
# Initial variables #
#####################

# Encoding is always utf8!
ENCODING = 'utf8'

# Name of drinks file defining drinks. Default 'drinks.txt'
drinksfilename = 'drinks.txt'


def readdrinks(drinksfile):
    # Initialize dictories
    drinks = []
    secretdrinks = []
    currentdrinkdict = None

    # Read the file line by line
    for line in drinksfile:

        # Get the current drink
        if line.startswith('='):
            currentdrinkdict = {
                'soda': [],
                'spirit': [],
                'other': [],
            }

            # Get name of drink without any newline
            name = line[1:].strip()

            # Sort into secret and normal drinks
            if name.startswith('?'):
                name = name.strip('? ')
                currentdrinkdict['name'] = name
                secretdrinks.append(currentdrinkdict)
            else:
                currentdrinkdict['name'] = name
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

        # This makes sure every other line is ignored.
        # Maybe we should print a warning (with line number)?
        else:
            pass

    return drinks, secretdrinks


def generatebarcard(drinks):
    for currentingredients in drinks:
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
            yield '\t\t& %s\\og' % soda

        for other in currentingredients['other']:
            yield '\\serveret I et %s med is\n' % other


def generatemixingcard(drinks):
    # Do TeX-stuff
    yield '\\begin{tabular}{lllll}'
    yield '\\toprule Navn & Sprut & Sodavand & Severing & Pris \\\\'
    yield '\midrule'

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

    yield '\\bottomrule'
    yield '\end{tabular}'


#####################################
# The function which does the magic #
#####################################
def makedrinks():
    with codecs.open(drinksfilename, 'r', encoding=ENCODING) as drinksfile:
        drinks, secretdrinks = readdrinks(drinksfile)

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
    with codecs.open('barcard.tex', 'w', encoding=ENCODING) as barcard:
        for line in generatebarcard(drinks):
            barcard.write('%s\n' % line)

    # Combine and sort the normal and secret drinks.
    drinks_sorted = sorted(
        drinks + secretdrinks,
        key=lambda drink: drink['name'])

    # Open file for the mixing card ("blandeliste")
    with codecs.open('mixing.tex', 'w', encoding=ENCODING) as mixingcard:
        for line in generatemixingcard(drinks_sorted):
            mixingcard.write('%s\n' % line)

    # Wuhu! Done!


# Run the function if file is called directly
if __name__ == '__main__':
    makedrinks()
