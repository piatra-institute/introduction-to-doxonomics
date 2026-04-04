$pdf_mode = 1;
$pdflatex = 'pdflatex -interaction=nonstopmode -halt-on-error %O %S';
$biber = 'biber %O %S';
$makeindex = 'makeindex %O -o %D %S';
$clean_ext = 'bbl run.xml';
