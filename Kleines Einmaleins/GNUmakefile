.PHONY: all clean CLEAN rebuild
TARGETS:=Einmaleins-bis-20x20.pdf Einmaleins-bis-10x10.pdf

all: $(TARGETS)

%.pdf: %.tex
	latexmk -lualatex $<

CLEAN: clean
	rm -f $(TARGETS)

clean:
	rm -f *.aux *.log *.out *.synctex.gz *.fdb_latexmk *.fls *.synctex* $(addprefix table-,$(TARGETS:.pdf=.tex)) $(TARGETS:.pdf=.lua)

rebuild: CLEAN all
