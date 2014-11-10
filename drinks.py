import codecs
import collections


# Encoding is always utf8!
ENCODING = 'utf8'
# Name of drinks file defining drinks. Default 'drinks.txt'
drinksfilename = 'drinks.txt'

def makedrinks():
    drinksdict = collections.OrderedDict()
    secretdrinkdict = collections.OrderedDict()

    drinksfile = codecs.open(drinksfilename, 'r', encoding=ENCODING)
    currentdrinkdict = None
    for line in drinksfile:
        # print(line)
        if line.startswith('='):
            currentdrinkdict = collections.OrderedDict()
            # Get name of drink without any newline
            currentdrinkname = line.strip('= \n')
            if currentdrinkname.startswith('?'):
                # print('Drink is secret')
                currentdrinkname = currentdrinkname.strip('? ')
                secretdrinkdict[currentdrinkname] = currentdrinkdict
            else:
                drinksdict[currentdrinkname] = currentdrinkdict
        elif line.startswith('--'):
            # name of soda
            currentsoda = line.strip(' -\n')
            # print(currentsoda)
            if 'soda' in currentdrinkdict:
                currentdrinkdict['soda'].append(currentsoda)
            else:
                currentdrinkdict['soda'] = [currentsoda]
        elif line.startswith('-'):
            # name of spirit
            currentspirit = line.strip(' -\n')
            # print(currentspirit)
            if 'spirit' in currentdrinkdict:
                currentdrinkdict['spirit'].append(currentspirit)
            else:
                currentdrinkdict['spirit'] = [currentspirit]
        elif line.startswith('!'):
            currentother = line.strip(' !\n')
            # print(currentother)
            if 'other' in currentdrinkdict:
                currentdrinkdict['other'].append(currentother)
            else:
                currentdrinkdict['other'] = [currentother]
        elif line.startswith('$'):
            currentprice = line.strip(' $\n')
            # print(currentprice)
            currentdrinkdict['price'] = currentprice
        else:
            # This makes sure every other line is ignored.
            # Maybe we should print a warning?
            pass
    # print(drinksdict)
    # print(secretdrinkdict)

    # drinksdict and secretdrinks now contains all drinks

    # Now lets make the barcards which dont contain the secret drinks.
    # We do this first, as we want to sort alphabetical for the mixingcard
    # Right now it will make every drink in this format:

    # \section*{name}
    # \begin{itemize}
    #   \item spirits
    #   \item sodas
    #   \item others
    #   \item price
    # \end{itemize}

    # It should be straight forward to change this however... :-/

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

    # we combine and sort the two dictionaries.
    drinksdict = collections.OrderedDict(list(drinksdict.items()) + list(secretdrinkdict.items()))
    drinksdict_sorted = sorted(drinksdict)

    mixingcard = codecs.open('mixing.tex', 'w', encoding=ENCODING)
    mixingcardline = '\\begin{table}{lllll}\n'
    mixingcardline += '\\toprule Navn & Sprut & Sodavand & Severing & Pris \\\ \n'
    mixingcard.writelines(mixingcardline)
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


if __name__ == '__main__':
    makedrinks()
