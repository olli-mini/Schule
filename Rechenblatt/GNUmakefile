.PHONY: all clean CLEAN rebuild aufgaben
CURRDATE:=$(shell date +"%Y-%m-%dT%H-%M")
TARGETS:=Addition-und-Subtraktion-bis-20.pdf Addition-und-Subtraktion-bis-100.pdf Multiplikation-und-Division-bis-15x15.pdf Multiplikation-und-Division-bis-10x10.pdf

all: aufgaben $(TARGETS)

aufgaben:
	python3 ./Rechenblatt.py

%.pdf: %.tex
	latexmk -lualatex $<
	cp -a $@ $(CURRDATE)_$@

CLEAN: clean
	rm -f $(TARGETS)

clean:
	rm -f *.aux *.log *.out *.synctex.gz *.fdb_latexmk *.fls *.synctex* $(wildcard aufgaben-*.tex) $(wildcard aufgaben-*.aux)

rebuild: CLEAN all
