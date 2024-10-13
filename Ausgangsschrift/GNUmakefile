.PHONY: all clean CLEAN rebuild
TARGETS:=Ausgangsschrift.pdf Leseprobe-Rotkäppchen.pdf Prima-Probe.pdf

all: $(TARGETS)

%.pdf: %.tex
	latexmk -lualatex $<

CLEAN: clean
	rm -f $(TARGETS)

clean:
	rm -f *.aux *.log *.out *.synctex.gz *.fdb_latexmk *.fls *.synctex*

rebuild: CLEAN all
