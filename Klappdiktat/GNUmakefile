.PHONY: all clean CLEAN rebuild
TARGETS:=Klappdiktat.pdf
SNIPPETS:=$(patsubst %.txt,%.tex,$(wildcard *.txt))

all: $(TARGETS) $(SNIPPETS)

%.pdf: %.tex
	latexmk -lualatex $<

%.tex: %.txt ./Klappdiktat.py
	python3 ./Klappdiktat.py $<

CLEAN: clean
	rm -f $(TARGETS) $(SNIPPETS)

clean:
	rm -f *.aux *.log *.out *.synctex.gz *.fdb_latexmk *.fls *.synctex*

rebuild: CLEAN all
