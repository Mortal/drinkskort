all:
	python drinks.py;
	xetex -output-driver="xdvipdfmx -q -E -p a4 -l" barcardmain.tex;
	pdflatex mixingcardmain.tex;