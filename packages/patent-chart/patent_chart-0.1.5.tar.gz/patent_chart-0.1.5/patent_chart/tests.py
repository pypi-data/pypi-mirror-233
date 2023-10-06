import pathlib

import pydantic

from patent_chart import parser

class PatentParsedContent(pydantic.BaseModel):
    unique_id: parser.PatentUniqueID
    claims: parser.Claims
    pages: list[str]


if __name__ == '__main__':
    from pprint import pprint
    dir = pathlib.Path.cwd().parent / 'chart_examples' / 'Oracle' / '2019-11-08 Defendants_ Contentions'
    patent_448_path = dir / 'US7069448.pdf'
    # claims = parse_claims_from_path(patent_448_path)
    # pprint(claims)
    # claim = claims.claims[0]
    # print(serialize_claim(claim))
    # print(serialize_claim_elements(claim))
    # print(serialize_claim_elements(claims.claims[1]))

    # Test parsing of patent claims and unique id using PatentParser
    # patent_parser = parser.PatentParser(patent_448_path)
    # claims = patent_parser.parse_claims()
    # pprint(claims)
    # unique_id = patent_parser.parse_unique_id()
    # pprint(unique_id)

    # parsed_content = PatentParsedContent(
    #     unique_id=unique_id,
    #     claims=claims,
    #     pages=patent_parser.pages_text,
    # )

    # print(parsed_content.model_dump_json())

    # Try krishna
    krishna_path = dir / 'Prior Art' / '448 Refs' / 'DEFENDANTS-00001314 (US 7,600,131 - Krishna).pdf'

    krishna_parser = parser.PatentParser(krishna_path)
    pprint(krishna_parser.pages_text)

    # claims = krishna_parser.parse_claims()
    # pprint(claims)

    ellis_path = dir / 'Prior Art' / '448 Refs' / 'DEFENDANTS-00001230 (US 6,484,257 - Ellis).pdf'

    
    ellis_parser = parser.PatentParser(ellis_path)
    # ellis_parser._pages_text = ellis_pages
    claims_text = parser.extract_claim_text_from_pages(ellis_parser.pages_text)
    pprint(claims_text)
    unique_id = ellis_parser.parse_unique_id()
    print(unique_id)
    claims = ellis_parser.parse_claims()
    pprint(claims)