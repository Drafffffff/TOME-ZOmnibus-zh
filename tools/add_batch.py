import json,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
keys=list(json.loads((root/'strings.json').read_text()))
p=root/'translations.json'
d=json.loads(p.read_text()) if p.exists() else {}
for line in sys.stdin.read().splitlines():
    if not line.strip():continue
    n,s=line.split('|',1)
    d[keys[int(n)]]=s.replace('\\n','\n').replace('\\t','\t')
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('Translated',len(d),'/',len(keys))
