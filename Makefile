.PHONY: all clean distclean watch

MAIN = main
LATEXMK = latexmk
# Artifacts removed by `make clean` and after each build.
# `make distclean` additionally removes the PDF and the latexmk tracking files
# ($(MAIN).fdb_latexmk, $(MAIN).fls), forcing a fully fresh rebuild next time.
ARTIFACTS = *.aux *.bbl *.bcf *.blg *.idx *.ilg *.ind *.log *.out *.run.xml *.toc

all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex preamble.tex frontmatter/*.tex chapters/*.tex appendices/*.tex bibliography/*.bib
	$(LATEXMK) -pdf -interaction=nonstopmode $(MAIN).tex
	rm -f $(ARTIFACTS)

watch:
	$(LATEXMK) -pdf -pvc -interaction=nonstopmode $(MAIN).tex

clean:
	rm -f $(ARTIFACTS)

distclean:
	rm -f $(ARTIFACTS) $(MAIN).pdf $(MAIN).fdb_latexmk $(MAIN).fls
