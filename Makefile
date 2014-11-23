# Makefile to create the bar- and mixing cards.                      \
                                                                     \
Usage is described in README.md

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
	python3 $< -s $(fest).txt

unsorted: drinks.py $(fest).txt
	python3 $< $(fest).txt

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
