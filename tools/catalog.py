import re, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKEN = re.compile(r'--\[(=*)\[.*?\]\1\]|--[^\n]*|\[(=*)\[.*?\]\2\]|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', re.S)

def tokens(text):
    for m in TOKEN.finditer(text):
        raw = m.group()
        if raw.startswith('--'): continue
        if raw.startswith('['):
            n = len(m.group(2) or '')
            s = raw[n+2:-(n+2)]
            if s.startswith('\n'): s = s[1:]
        else:
            s = re.sub(r'\\(\d{1,3}|.)', lambda x: chr(int(x[1])) if x[1].isdigit() else {'n':'\n','t':'\t','r':'\r','a':'\a','b':'\b','f':'\f','v':'\v'}.get(x[1], x[1]), raw[1:-1])
        yield m, s

def main():
    rows = {}
    for p in sorted((ROOT/'upstream/lite').rglob('*.lua')):
        text = p.read_text()
        for m,s in tokens(text):
            if not re.search('[a-zA-Z]', s): continue
            before, after = text[max(0,m.start()-100):m.start()], text[m.end():m.end()+90]
            # All existing translation calls, plus other strings for manual review.
            marked = bool(re.search(r'_t\s*\(?\s*$', before) or re.match(r'\s*\)?\s*:tformat', after))
            row = rows.setdefault(s, {'src':s,'marked':False,'sites':[]})
            row['marked'] |= marked
            row['sites'].append({'file':str(p.relative_to(ROOT/'upstream/lite')),'line':text.count('\n',0,m.start())+1,'context':(before[-65:]+m.group()+after[:35])})
    out = list(rows.values())
    (ROOT/'catalog.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
    marked = [r for r in out if r['marked']]
    (ROOT/'strings.json').write_text(json.dumps({r['src']:'' for r in marked},ensure_ascii=False,indent=2))
    for i,r in enumerate(marked): print(f'{i:03d} {json.dumps(r["src"],ensure_ascii=False)}')
    print('TOTAL',len(marked),'ALL',len(out))

if __name__=='__main__': main()
