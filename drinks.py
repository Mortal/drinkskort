# -*- coding: utf-8 -*-
# Time-stamp: <2014-11-12 13:50:02 moss>

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


#####################################
# The function which does the magic #
#####################################
def makedrinks():
    # Initialize dictories
    drinksdict = collections.OrderedDict()
    secretdrinkdict = collections.OrderedDict()
    currentdrinkdict = None

    # Read the input file
    drinksfile = codecs.open(drinksfilename, 'r', encoding=ENCODING)

    # Read the file line by line
    for line in drinksfile:

        # Get the current drink
        if line.startswith('='):
            currentdrinkdict = collections.OrderedDict()

            # Get name of drink without any newline
            currentdrinkname = line.strip('= \n')

            # Sort into secret and normal drinks
            if currentdrinkname.startswith('?'):
                currentdrinkname = currentdrinkname.strip('? ')
                secretdrinkdict[currentdrinkname] = currentdrinkdict
            else:
                drinksdict[currentdrinkname] = currentdrinkdict

        # Soda
        elif line.startswith('--'):
            currentsoda = line.strip(' -\n')

            # Handle multiple soda entries
            if 'soda' in currentdrinkdict:
                currentdrinkdict['soda'].append(currentsoda)
            else:
                currentdrinkdict['soda'] = [currentsoda]

        # Spirit
        elif line.startswith('-'):
            currentspirit = line.strip(' -\n')
            if 'spirit' in currentdrinkdict:
                currentdrinkdict['spirit'].append(currentspirit)
            else:
                currentdrinkdict['spirit'] = [currentspirit]

        # Other
        elif line.startswith('!'):
            currentother = line.strip(' !\n')
            if 'other' in currentdrinkdict:
                currentdrinkdict['other'].append(currentother)
            else:
                currentdrinkdict['other'] = [currentother]

        # Price
        elif line.startswith('$'):
            currentprice = line.strip(' $\n')
            currentdrinkdict['price'] = currentprice

        # This makes sure every other line is ignored.
        # Maybe we should print a warning (with line number)?
        else:
            pass

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
    barcard = codecs.open('barcard.tex', 'w', encoding=ENCODING)
    for drink in drinksdict:
        drinkline = '\section*{' + drink + '}\n'
        drinkline += '\\begin{itemize}\n'

        # Write every other thing:
        currentingredients = drinksdict[drink]
        for spirit in currentingredients['spirit']:
            drinkline += '\t\item ' + spirit + '\n'
        for soda in currentingredients['soda']:
            drinkline += '\t\item ' + soda + '\n'
        for other in currentingredients['other']:
            drinkline += '\t\item ' + other + '\n'

        drinkline += '\t\item ' + currentingredients['price'] + '\n'
        drinkline += '\end{itemize}\n\n'
        barcard.writelines(drinkline)
    barcard.close()

    # Combine and sort the normal and secret drinks.
    drinksdict = collections.OrderedDict(list(drinksdict.items()) + list(secretdrinkdict.items()))
    drinksdict_sorted = sorted(drinksdict)

    # Open file for the mixing card ("blandeliste")
    mixingcard = codecs.open('mixing.tex', 'w', encoding=ENCODING)

    # Do TeX-stuff
    mixingcardline = '\\begin{table}{lllll}\n'
    mixingcardline += '\\toprule Navn & Sprut & Sodavand & Severing & Pris \\\ \n'
    mixingcard.writelines(mixingcardline)

    # Loop over all drinks
    for drink in drinksdict_sorted:
        mixingcardline = '\midrule ' + drink + ' & '
        for spirit in currentingredients['spirit']:
            mixingcardline += spirit + ' '
        mixingcardline += '& '
        for soda in currentingredients['soda']:
            mixingcardline += soda + ' '
        mixingcardline += '& '
        for other in currentingredients['other']:
            mixingcardline += other + ' '
        mixingcardline += '& '
        mixingcardline += currentingredients['price'] + '\\\ \n'
        mixingcard.writelines(mixingcardline)
    mixingcardline = '\end{table}'
    mixingcard.writelines(mixingcardline)
    mixingcard.close()

    # Wuhu! Done!


if __name__ == '__main__':
    makedrinks()
