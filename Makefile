all:
	python drinks.py -s vinterfest.txt;
	xetex -output-driver="xdvipdfmx -q -E -p a4 -l" barcardmain.tex;
	pdflatex mixingcardmain.tex;