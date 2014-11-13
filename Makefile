# Makefile to create the bar- and mixing cards.                      \
                                                                     \
Usage: make fest=INPUT  to generate the pdf's                        \
       make clean           to remove output files (not incl pdf's)  \
       make clean-deep      to remove all output files               \
Example:                                                             \
       make fest=vinterfest

#
# Generating output
#

# Defaults 
fest ?= drinks
sort ?= sorted

# Run it all!
all: $(sort) bar_$(fest).pdf mixing_$(fest).pdf

# Generate the lists
sorted: drinks.py $(fest).txt
	python $< -s $(fest).txt

unsorted: drinks.py $(fest).txt
	python $< $(fest).txt

# Create the barcards
bar_$(fest).pdf:
	xetex -jobname=bar_$(fest) -output-driver="xdvipdfmx -q -E -p a4 -l" barcardmain.tex

# Create the mixing card
mixing_$(fest).pdf:
	pdflatex -jobname=mixing_$(fest) mixingcardmain.tex

# Test the input file
test: drinks.py
	python $< -v $(fest).txt


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
