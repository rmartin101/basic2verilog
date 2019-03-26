all:
	pdflatex -file-line-error-style -halt-on-error design
	bibtex -min-crossrefs=1000 design
	pdflatex -file-line-error-style -halt-on-error design
	pdflatex -file-line-error-style -halt-on-error design

%.pdf : %.ps
	ps2pdf $< $@
 
%.ps  : %.dvi
	dvips -t letter -z -Ppdf -G0 -D600 $< -o
 
clean:
	${RM} *~ *.aux *.log *.dvi *.ps body.tmp head.tmp *.bbl *.blg *.bak



