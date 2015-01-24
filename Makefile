# Makefile to create the bar- and mixing cards.                      \
                                                                     \
Usage is described in README.md

#
# Generating output
#

# Defaults
fest ?= drinks
sort ?= sorted
alt  ?= nej
columns ?= new

ifeq ($(alt),nej)
    alt_arg :=
else
    alt_arg := -a
endif

ifeq ($(sort),sorted)
    sort_arg := -s
else
    sort_arg :=
endif

# Run it all!
all: bar_$(fest).pdf mixing_$(fest).pdf
	python3 $< $(sort_arg) $(alt_arg) -c $(columns) $(fest).txt

# Create the barcards
bar_$(fest).pdf: drinks.py $(fest).txt
	xetex -jobname=bar_$(fest) -output-driver="xdvipdfmx -q -E -p a4 -l" barcardmain.tex

# Create the mixing card
mixing_$(fest).pdf: drinks.py $(fest).txt
	pdflatex -jobname=mixing_$(fest) mixingcardmain.tex

# Test the input file
test: drinks.py $(fest).txt
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
