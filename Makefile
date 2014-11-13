# Makefile to create the bar- and mixing cards.                      \
                                                                     \
Usage: make fest=INPUT all  to generate the pdf's                    \
       make clean           to remove output files (not incl pdf's)  \
       make clean-deep      to remove all output files               \
Example:                                                             \
       make fest=vinterfest all

#
# Generating output
#

# Default input file is drinks.txt
fest ?= drinks

# Run it all!
all: $(fest) bar mixing

# Generate the lists
$(fest): drinks.py $(fest).txt
	python $< $(fest).txt

# Create the barcards
bar:
	xetex -output-driver="xdvipdfmx -q -E -p a4 -l" barcardmain.tex

# Create the mixing card
mixing:
	pdflatex mixingcardmain.tex


#
# Removing the output
#

clean: clean-junk clean-tex

clean-deep: clean clean-out

clean-junk:
	$(RM) *.log *.aux

clean-tex:
	$(RM) mixing.tex barcard.tex

clean-out:
	$(RM) *.pdf
