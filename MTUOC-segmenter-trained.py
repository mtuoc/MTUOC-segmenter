#    MTUOC-segmenter-trained
#    Copyright (C) 2023  Antoni Oliver
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


import argparse
import sys
import codecs
import nltk

#SRX_SEGMENTER
import lxml.etree
import regex
from typing import (
    List,
    Set,
    Tuple,
    Dict,
    Optional
)


def segmenta(cadena):
    segments=segmentador.tokenize(cadena)
    resposta=[]
    for segment in segments:
        resposta.append(segment)
    resposta="\n".join(resposta)
    return(resposta)


parser = argparse.ArgumentParser(description='A script to segment a text file.')
parser.add_argument("-i", "--input_file", type=str, help="The input file to segment.", required=True)
parser.add_argument("-o", "--output_file", type=str, help="The output segmented file.", required=True)
parser.add_argument("-s", "--segmenter", type=str, help="The trained segmenter to use", required=True)
parser.add_argument("-p", "--paramark", action="store_true", help="Add the <p> paragraph mark (useful for Hunalign).", required=False)


args = parser.parse_args()
infile=args.input_file
outfile=args.output_file

segmenter=args.segmenter

paramark=args.paramark

segmentador=nltk.data.load(segmenter)

entrada=codecs.open(infile,"r",encoding="utf-8",errors="ignore")
sortida=codecs.open(outfile,"w",encoding="utf-8")
for linia in entrada:
    segments=segmenta(linia)
    if len(segments)>0:
        if paramark: sortida.write("<p>\n")
        sortida.write(segments+"\n")

