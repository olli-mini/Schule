.PHONY: all clean CLEAN rebuild
TARGETS:=Einmaleins.pdf

all: $(TARGETS)

%.pdf: %.tex
	latexmk -lualatex $<

CLEAN: clean
	rm -f $(TARGETS)

clean:
	rm -f *.aux *.log *.out *.synctex.gz *.fdb_latexmk *.fls *.synctex*

rebuild: CLEAN all
