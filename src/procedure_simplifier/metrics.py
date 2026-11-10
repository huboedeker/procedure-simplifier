"""Reproducible text comparison. Counts are not labor, token or image metrics."""
import argparse
import hashlib
import json
from pathlib import Path
import re

WORD_PATTERN = r'\b[\w’-]+\b'

def compare(source, output):
    source, output = Path(source), Path(output)
    a, b = source.read_bytes(), output.read_bytes()
    n, m = (len(re.findall(WORD_PATTERN, x.decode('utf-8'))) for x in [a,b])
    return dict(source_words=n, output_words=m,
                reduction_percent=round(100*(1-m/n),1) if n else None,
                method='Unicode regex '+WORD_PATTERN+' on both complete UTF-8 input files; caller records included/excluded scope.',
                source_sha256=hashlib.sha256(a).hexdigest(),output_sha256=hashlib.sha256(b).hexdigest(),
                limitation='No labor, token, cost, comprehension or image-content reduction implied.' if n else 'Empty baseline: percentage unavailable; no labor/token inference.')

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('source',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    try: result=compare(a.source,a.output)
    except (OSError,UnicodeError) as exc:p.exit(1,str(exc)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
