#!/bin/sh
# The installation script of PSCyr package for teTeX-2.0.  For other
# systems see details in README.* files.

TEXMF=`kpsewhich -expand-var='$TEXMFMAIN'`
mkdir -p $TEXMF/{tex/latex,fonts/tfm/public,fonts/vf/public,fonts/type1/public,fonts/afm/public,doc/fonts,dvips}/pscyr
mv dvips/pscyr/* $TEXMF/dvips/pscyr
mv tex/latex/pscyr/* $TEXMF/tex/latex/pscyr
mv fonts/tfm/public/pscyr/* $TEXMF/fonts/tfm/public/pscyr
mv fonts/vf/public/pscyr/* $TEXMF/fonts/vf/public/pscyr
mv fonts/type1/public/pscyr/* $TEXMF/fonts/type1/public/pscyr
mv fonts/afm/public/pscyr/* $TEXMF/fonts/afm/public/pscyr
mv LICENSE doc/README.koi doc/PROBLEMS ChangeLog $TEXMF/doc/fonts/pscyr

VARTEXFONTS=`kpsewhich -expand-var='$VARTEXFONTS'`
rm -f $VARTEXFONTS/pk/modeless/public/pscyr/*

mktexlsr

# Solution for teTeX-2.0
echo -e "\n# PSCyr\nMap pscyr.map\n" >> $TEXMF/web2c/updmap.cfg
updmap
