#    MTUOC-sentence-splitter
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

from sentence_splitter import SentenceSplitter, split_text_into_sentences


def segmenta(cadena):
    segmenter = SrxSegmenter(rules[srxlang],cadena)
    segments=segmenter.extract()
    resposta=[]
    for segment in segments[0]:
        segment=segment.replace("’","'")
        resposta.append(segment)
    resposta="\n".join(resposta)
    return(resposta)



def translate(segment):
    return(segment[::-1])


parser = argparse.ArgumentParser(description='A script to segment a text file.')
parser.add_argument("-i", "--input_file", type=str, help="The input file to segment.", required=True)
parser.add_argument("-o", "--output_file", type=str, help="The output segmented file.", required=True)
parser.add_argument("-l", "--lang", type=str, help="The language code (en, es, fr...", required=True)
parser.add_argument("-p", "--paramark", action="store_true", help="Add the <p> paragraph mark (useful for Hunalign).", required=False)


args = parser.parse_args()
infile=args.input_file
outfile=args.output_file

lang=args.lang

print("LANG:",lang)
splitter = SentenceSplitter(language=lang)

paramark=args.paramark

entrada=codecs.open(infile,"r",encoding="utf-8",errors="ignore")
sortida=codecs.open(outfile,"w",encoding="utf-8")
for linia in entrada:
    linia=linia.rstrip()
    segments=splitter.split(linia)
    for segment in segments:
        sortida.write(segment+"\n")
    
    if paramark: sortida.write("<p>\n")
    
    

