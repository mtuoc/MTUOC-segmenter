#    MTUOC-segmenter
#    Copyright (C) 2025  Antoni Oliver
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
from charset_normalizer import from_path


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


class SrxSegmenter:
    """Handle segmentation with SRX regex format.
    """
    def __init__(self, rule: Dict[str, List[Tuple[str, Optional[str]]]], source_text: str) -> None:
        self.source_text = source_text
        self.non_breaks = rule.get('non_breaks', [])
        self.breaks = rule.get('breaks', [])

    def _get_break_points(self, regexes: List[Tuple[str, str]]) -> Set[int]:
        return set([
            match.span(1)[1]
            for before, after in regexes
            for match in regex.finditer('({})({})'.format(before, after), self.source_text)
        ])

    def get_non_break_points(self) -> Set[int]:
        """Return segment non break points
        """
        return self._get_break_points(self.non_breaks)

    def get_break_points(self) -> Set[int]:
        """Return segment break points
        """
        return self._get_break_points(self.breaks)

    def extract(self) -> Tuple[List[str], List[str]]:
        """Return segments and whitespaces.
        """
        non_break_points = self.get_non_break_points()
        candidate_break_points = self.get_break_points()

        break_point = sorted(candidate_break_points - non_break_points)
        source_text = self.source_text

        segments = []  # type: List[str]
        whitespaces = []  # type: List[str]
        previous_foot = ""
        for start, end in zip([0] + break_point, break_point + [len(source_text)]):
            segment_with_space = source_text[start:end]
            candidate_segment = segment_with_space.strip()
            if not candidate_segment:
                previous_foot += segment_with_space
                continue

            head, segment, foot = segment_with_space.partition(candidate_segment)

            segments.append(segment)
            whitespaces.append('{}{}'.format(previous_foot, head))
            previous_foot = foot
        whitespaces.append(previous_foot)

        return segments, whitespaces


def parse(srx_filepath: str) -> Dict[str, Dict[str, List[Tuple[str, Optional[str]]]]]:
    """Parse SRX file and return it.
    :param srx_filepath: is soruce SRX file.
    :return: dict
    """
    tree = lxml.etree.parse(srx_filepath)
    namespaces = {
        'ns': 'http://www.lisa.org/srx20'
    }

    rules = {}

    for languagerule in tree.xpath('//ns:languagerule', namespaces=namespaces):
        rule_name = languagerule.attrib.get('languagerulename')
        if rule_name is None:
            continue

        current_rule = {
            'breaks': [],
            'non_breaks': [],
        }

        for rule in languagerule.xpath('ns:rule', namespaces=namespaces):
            is_break = rule.attrib.get('break', 'yes') == 'yes'
            rule_holder = current_rule['breaks'] if is_break else current_rule['non_breaks']

            beforebreak = rule.find('ns:beforebreak', namespaces=namespaces)
            beforebreak_text = '' if beforebreak.text is None else beforebreak.text

            afterbreak = rule.find('ns:afterbreak', namespaces=namespaces)
            afterbreak_text = '' if afterbreak.text is None else afterbreak.text

            rule_holder.append((beforebreak_text, afterbreak_text))

        rules[rule_name] = current_rule

    return rules

def segmenta(cadena):
    segmenter = SrxSegmenter(rules[srxlang],cadena)
    segments=segmenter.extract()
    resposta=[]
    for segment in segments[0]:
        segment=segment.replace("’","'")
        resposta.append(segment)
    resposta="\n".join(resposta)
    return(resposta)

def detect_encoding(file_path):
    result = from_path(file_path).best()
    return result.encoding if result else 'utf-8'   



parser = argparse.ArgumentParser(description='A script to segment a text file.')
parser.add_argument("-i", "--input_file", type=str, help="The input file to segment.", required=True)
parser.add_argument("-o", "--output_file", type=str, help="The output segmented file.", required=True)
parser.add_argument("-s", "--srxfile", type=str, help="The SRX file to use", required=True)
parser.add_argument("-l", "--srxlang", type=str, help="The language as stated in the SRX file", required=True)
parser.add_argument("-p", "--paramark", action="store_true", help="Add the <p> paragraph mark (useful for Hunalign).", required=False)


args = parser.parse_args()
infile=args.input_file
outfile=args.output_file

srxfile=args.srxfile
srxlang=args.srxlang

paramark=args.paramark


rules = parse(srxfile)

languages=list(rules.keys())

if not srxlang in languages:
    print("Language ",srxlang," not available in ", srxfile)
    print("Available languages:",", ".join(languages))
    sys.exit()

encoding = detect_encoding(infile)
entrada = codecs.open(infile, "r", encoding=encoding, errors="ignore")
sortida=codecs.open(outfile,"w",encoding="utf-8")
for linia in entrada:
    segments=segmenta(linia)
    if len(segments)>0:
        if paramark: sortida.write("<p>\n")
        sortida.write(segments+"\n")

