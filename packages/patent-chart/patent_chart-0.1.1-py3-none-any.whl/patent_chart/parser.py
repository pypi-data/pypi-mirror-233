import re
import pathlib
from enum import Enum
from collections import namedtuple
from dataclasses import dataclass
from typing import Union

from pypdf import PdfReader

def extract_claim_text_from_pages(pages):
    claim_signals = ['What is claimed is:', 'We claim:']
    end_signals = ['k k k k k']

    claim_chunks = []
    signal_found_previous_page = False
    for page in pages:
        end_signal_index = len(page)
        for end_signal in end_signals:
            try:
                end_signal_index = page.index(end_signal)
            except ValueError:
                continue
            else:
                break
        if signal_found_previous_page:
            claim_chunks.append(page[:end_signal_index])
        else:
            for signal in claim_signals:
                if signal in page:
                    signal_found_previous_page = True
                    claim_chunks.append(page[page.index(signal) + len(signal):])

    # clean up claim chunks
    claim_chunks = [l.lstrip(' ') for l in ''.join(claim_chunks).splitlines()]
    # filter out lines that are composed of only whitespace
    claim_chunks = [line for line in claim_chunks if line.strip()]
    return ''.join(claim_chunks)

Token = namedtuple('Token', ['type', 'lexeme'])

class ClaimsLexer(Enum):
    # TODO: move start claims section into here instead of as a pre-processing step. That way we can just run this on the whole patent rather than pre-processing the claims first. If we do that, also uncomment the end claims section delimiter.
    # DELIMITER_END_CLAIMS_SECTION = re.compile(r'k k k k k')
    DELIMITER_START_CLAIM = re.compile(r'[1-9][0-9]*\.')
    # TODO: handle multiple dependency, which would include language like:
    #   claim 3 or 4
    #   claim 1 or claim 2
    #   claim 1, 7, 12, or 15
    #   claim 1, claim 7, claim 12, or claim 15
    #   any of the preceding claims
    DEPENDENCY = re.compile(r'[Cc]laim [1-9][0-9]*')
    DELIMITER_END_PREAMBLE = re.compile(r':')
    DELIMITER_END_ELEMENT = re.compile(r';')
    DELIMITER_END_CLAIM = re.compile(r'\.')
    # TODO: add transition type:
    #   comprising
    #   consisting of
    #   consisting essentially of
    #   etc...
    TEXT = re.compile(r'[\w,\'\"!?\(\)\-—]+')
    WHITESPACE = re.compile(r'\s+')

    def __repr__(self):
        return self.name
    
def lex_claims(claim_text):
    tokens = []
    while claim_text:
        for token_type in ClaimsLexer:
            match = token_type.value.match(claim_text)
            if match:
                tokens.append(Token(type=token_type, lexeme=match.group()))
                claim_text = claim_text[match.end():]
                break
    return tokens

# Base recursive descent parser
class RecursiveDescentParserBase:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        
    def peek(self):
        return self.tokens[self.current_token_index]
    
    def is_at_end(self):
        return self.current_token_index == len(self.tokens)
    
    def previous(self):
        return self.tokens[self.current_token_index - 1]

    def advance(self):
        self.current_token_index += 1
        return self.previous()

    def check(self, type):
        if self.is_at_end():
            return False
        return type == self.peek().type

    def match(self, *token_types):
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True
        return False
    
    def consume(self, token_type):
        if self.match(token_type):
            return self.previous()
        else:
            raise Exception(f'Expected {token_type.name}')

    def parse(self):
        pass

# Define dataclasses for concrete syntax tree for claims parser
@dataclass
class Claims:
    claims: list['Claim']

@dataclass
class Claim:
    delimiter_start_claim: ClaimsLexer.DELIMITER_START_CLAIM
    claim_content: list[Union['ClaimText', 'ClaimDelimiterEndPreamble', 'ClaimDelimiterEndElement', 'ClaimWhitespace', 'ClaimDependency']]
    delimiter_end_claim: ClaimsLexer.DELIMITER_END_CLAIM

@dataclass
class ClaimText:
    text: ClaimsLexer.TEXT

@dataclass
class ClaimDelimiterEndPreamble:
    delimiter_end_preamble: ClaimsLexer.DELIMITER_END_PREAMBLE

@dataclass
class ClaimDelimiterEndElement:
    delimiter_end_element: ClaimsLexer.DELIMITER_END_ELEMENT

@dataclass
class ClaimWhitespace:
    whitespace: ClaimsLexer.WHITESPACE

@dataclass
class ClaimDependency:
    dependency: ClaimsLexer.DEPENDENCY

class ClaimsParser(RecursiveDescentParserBase):
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    def claim_content(self):
        if self.match(ClaimsLexer.TEXT):
            text = self.previous()
            return ClaimText(text=text)
        elif self.match(ClaimsLexer.WHITESPACE):
            whitespace = self.previous()
            return ClaimWhitespace(whitespace=whitespace)
        elif self.match(ClaimsLexer.DEPENDENCY):
            dependency = self.previous()
            return ClaimDependency(dependency=dependency)
        elif self.match(ClaimsLexer.DELIMITER_END_PREAMBLE):
            delimiter_end_preamble = self.previous()
            return ClaimDelimiterEndPreamble(delimiter_end_preamble=delimiter_end_preamble)
        elif self.match(ClaimsLexer.DELIMITER_END_ELEMENT):
            delimiter_end_element = self.previous()
            return ClaimDelimiterEndElement(delimiter_end_element=delimiter_end_element)
        else:
            raise Exception('Expected claim text')
            
    def claim(self):
        if self.match(ClaimsLexer.DELIMITER_START_CLAIM):
            delimiter_start_claim = self.previous()
            claim_contents = []
            while not self.match(ClaimsLexer.DELIMITER_END_CLAIM):
                claim_contents.append(self.claim_content())
            delimiter_end_claim = self.previous()
            return Claim(delimiter_start_claim=delimiter_start_claim, claim_content=claim_contents, delimiter_end_claim=delimiter_end_claim)
        else:
            raise Exception('Expected claim start delimiter')
    
    def claims(self):
        claims = []
        while not self.is_at_end():
            # There can be whitespace and text between claims. So we need to chew it up
            # before parsing the next claim.
            while self.match(ClaimsLexer.WHITESPACE, ClaimsLexer.TEXT):
                pass
            if not self.is_at_end():
                claims.append(self.claim())
        return Claims(claims=claims)

    def parse(self):
        return self.claims()

def parse_claims_from_pages(pages):
    claim_text = extract_claim_text_from_pages(pages)
    tokens = lex_claims(claim_text)
    parser = ClaimsParser(tokens)
    return parser.parse()

def parse_claims_from_path(path):
    patent_pages = []
    reader = PdfReader(path)
    for page in reader.pages:
        patent_pages.append(page.extract_text())
    return parse_claims_from_pages(patent_pages)

def serialize_claim(claim):
    serialized = ''
    serialized += claim.delimiter_start_claim.lexeme
    for claim_content in claim.claim_content:
        if isinstance(claim_content, ClaimText):
            serialized += claim_content.text.lexeme
        elif isinstance(claim_content, ClaimWhitespace):
            serialized += claim_content.whitespace.lexeme
        elif isinstance(claim_content, ClaimDependency):
            serialized += claim_content.dependency.lexeme
        elif isinstance(claim_content, ClaimDelimiterEndPreamble):
            serialized += claim_content.delimiter_end_preamble.lexeme
        elif isinstance(claim_content, ClaimDelimiterEndElement):
            serialized += claim_content.delimiter_end_element.lexeme
    serialized += claim.delimiter_end_claim.lexeme
    return serialized

def serialize_claim_elements(claim):
    serialized_claim_elements = []
    # Iterate through claim content, incrementally constructing a claim element. Once a delimiter end preamble or delimiter end element is encountered, add the claim element to the list of claim elements and start a new claim element.
    claim_element = claim.delimiter_start_claim.lexeme
    for claim_content in claim.claim_content:
        if isinstance(claim_content, ClaimText):
            claim_element += claim_content.text.lexeme
        elif isinstance(claim_content, ClaimWhitespace):
            claim_element += claim_content.whitespace.lexeme
        elif isinstance(claim_content, ClaimDependency):
            claim_element += claim_content.dependency.lexeme
        elif isinstance(claim_content, ClaimDelimiterEndPreamble):
            claim_element += claim_content.delimiter_end_preamble.lexeme
            serialized_claim_elements.append(claim_element)
            claim_element = ''
        elif isinstance(claim_content, ClaimDelimiterEndElement):
            claim_element += claim_content.delimiter_end_element.lexeme
            serialized_claim_elements.append(claim_element)
            claim_element = ''
    # Add the last claim element
    claim_element += claim.delimiter_end_claim.lexeme
    serialized_claim_elements.append(claim_element)
    # Strip whitespace from claim elements
    serialized_claim_elements = [claim_element.strip() for claim_element in serialized_claim_elements]
    return serialized_claim_elements
    
if __name__ == '__main__':
    from pprint import pprint
    dir = pathlib.Path.cwd().parent / 'chart_examples' / 'Oracle' / '2019-11-08 Defendants_ Contentions'
    patent_448_path = dir / 'US7069448.pdf'
    claims = parse_claims_from_path(patent_448_path)
    pprint(claims)
    claim = claims.claims[0]
    print(serialize_claim(claim))
    print(serialize_claim_elements(claim))
    print(serialize_claim_elements(claims.claims[1]))