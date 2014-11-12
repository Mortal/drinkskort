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

        currentingredients = drinksdict[drink]
        drinkline = '\drik ' + drink + '\n'
        drinkline += '\\til ' + currentingredients['price'] + '\n'
        # Write every other thing:
        drinkline += '\med %\n'
        for spirit in currentingredients['spirit']:
            amount = '\t'
            if '-' in spirit:
                # Split returns an array of strings.
                # amount is the first of these
                amount = spirit.split('-')[0].strip() + '\t'
                spirit = spirit.split('-')[1].strip()
            drinkline += '' + amount + '& ' + spirit + '\og \n'
        for soda in currentingredients['soda']:
            drinkline += '\t\t& ' + soda + '\og \n'
        for other in currentingredients['other']:
            drinkline += '\serveret I et ' + other + ' med is\n\n'
        barcard.writelines(drinkline)
    barcard.close()

    # Combine and sort the normal and secret drinks.
    drinksdict = collections.OrderedDict(
        list(drinksdict.items()) + list(secretdrinkdict.items()))
    drinksdict_sorted = sorted(drinksdict)

    # Open file for the mixing card ("blandeliste")
    mixingcard = codecs.open('mixing.tex', 'w', encoding=ENCODING)

    # Do TeX-stuff
    mixingcardline = '\\begin{tabular}{lllll}\n'
    mixingcardline += (
        '\\toprule Navn & Sprut & Sodavand & Severing & Pris \\\ \n\midrule')
    mixingcard.writelines(mixingcardline)

    # Loop over all drinks
    drinknumber = 0
    for drink in drinksdict_sorted:
        currentingredients = drinksdict[drink]
        mixingcardline = ''
        if drinknumber % 2 == 0:
            mixingcardline = '\\rowcolor{Gray} '
        mixingcardline += drink + ' &'
        # mixingcardline = '\midrule ' + drink + ' &'
        for spirit in currentingredients['spirit']:
            for sp in spirit.split('-'):
                mixingcardline += sp.strip() + ' '
            # The strip here is to avoid the space before the comma.
            mixingcardline = mixingcardline.strip() + ', '
        mixingcardline += '& '

        # some drinks do not contain any soda,
        # so this check needs to be done beforehand.
        # Maybe this needs to be done before every ingredients?
        if 'soda' in currentingredients.keys():
            for soda in currentingredients['soda']:
                mixingcardline += soda + ' '
        mixingcardline += '& '
        for other in currentingredients['other']:
            mixingcardline += other + ' '
        mixingcardline += '& '
        mixingcardline += currentingredients['price'] + ' kr\\\ \n'
        mixingcard.writelines(mixingcardline)
        drinknumber += 1
    mixingcardline = '\\bottomrule\n\end{tabular}'
    mixingcard.writelines(mixingcardline)
    mixingcard.close()

    # Wuhu! Done!


# Run the function if file is called directly
if __name__ == '__main__':
    makedrinks()
