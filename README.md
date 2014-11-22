TÅGEKAMMERET                                             November 2014


                           -- SEKR TeX --

System til at generere drinkskort og blandelister.

** Funktion:
Tager en inputfil (fx "drinks.txt") og omdanner til to pdf-filer.
I "bar_drinks.pdf" findes drinkskortene og i "mixing_drinks.pdf"
findes blandelisten.


** Kræver:
* Python > 3.2
* XeTeX
* pdfLaTeX


** Filer:
- README.md (denne fil)
- Makefile (til at køre det hele)
- drinks.py (til at omdanne input til egenede lister)
- barcardmain.tex (til drinkskort)
- mixingcardmain.tex (til blandeliste)
- example.txt (inputfil med forklaringer)
- drinks.txt (standard input)
- vinterfest.txt (inputfil fra vinterfesten 2014)


** Anvendelse:
Scriptet kaldes ved at skrive en af følgende kommandoer i en terminal.

* make
--------> Kører scriptet med standard sortering (alfabetisk på
          blandelisten og efter pris på drinkskortet) på standard
	  input (som er drinks.txt).

* make fest=vinterfest
--------> Samme som ovenfor blot på filen vinterfest.txt med outputtet
          bar_vinterfest.pdf og mixing_vinterfest.pdf.
	    ...  Kan selvfølgelig også være en anden fest ;)

* make sort=unsorted fest=vinterfest
--------> Fjerner sorteringen efter pris på drinkskortet. Kan også
          køres uden fest=...

* make test fest=karneval
--------> Tester inputfilen uden at producere pdf-filer. Der kommer
          en besked hvis nogle af de indtastede linjer ikke kan
	  genkendes.

* make clean
--------> Fjerner de midlertidige filer.

* make clean-deep
--------> Fjerner de midlertidige filer OG pdf-filerne.


** Inputfilen:
Drinks indskrives i en txt-fil efter et bestemt system (se nedenfor).
Standardfilen er drinks.txt.
Det er muligt at lave en speciel fil til hver fest, fx vinterfest.txt

Format af inputfilen er (se også example.txt):
 *   Første tegn i hver linje fortæller typen af ingridiensen
 *   # Angiver en kommentar - og er dermed ikke en ingrediens ;)
 *   = Betyder navnet på drinken
 *   =? betyder hemmelig drink der kun kommer på barkort)
 *   - skal foran spiritus mængden af spiritus og typen. dvs der kan komme to - i samme sætning
 *   -- skal foran sodavand/juice
 *   ! skal foran hvad det serveres i
 *   $ skal foran pris. Undlad enhed -- kr skrives af TeX
 *   Tomme linjer ignoreres
 *   Faktisk bliver alt hvor der ikke står =,-,! eller $ ignoreret.



/ TK-IT