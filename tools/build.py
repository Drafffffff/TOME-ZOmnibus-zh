"""Build the Chinese edition of the installed Lite package, retaining its save ID."""
import json, re, shutil, subprocess, zipfile, hashlib
from pathlib import Path
from catalog import ROOT, tokens

src=ROOT/'upstream/lite'
out=ROOT/'build/lite'
if out.exists(): shutil.rmtree(out)
shutil.copytree(src,out)
d=json.loads((ROOT/'translations.json').read_text())
# Use the shipped game's terminology for names embedded in longer sentences.
terms={'亵渎之触':'诅咒之触','乌尔基斯':'厄奇斯','博学多才':'渊博学识','“熟练”':'“熟能生巧”','交易技巧':'欺诈圣手','纳洛精灵的传承':'纳鲁精灵的馈赠','沙虫女王':'沙虫女皇','基础药剂':'领悟药剂','腐化力量':'堕落力量','掠夺战斗':'掠夺格斗','灵巧／无赖':'灵巧／街头格斗','法杖战斗':'法杖格斗','宝石镶嵌':'装备附魔','物质即能量':'宝石能量','巫妖形态':'巫妖转生','自然／反魔技能系':'自然／反魔法技能系'}
for s,t in d.items():
    for a,b in terms.items():t=t.replace(a,b)
    d[s]=t
# Explicitly reviewed raw display literals. Do not translate internal enum values,
# birth descriptor IDs, object matching names, key command IDs or persisted keys.
raw=set(json.loads((ROOT/'extra_strings.json').read_text()))
raw -= {'Honorary Roguelike Win','ZOmnibus Lite','The cosmetic/informational/UI addons from ZOmnibus.','[ZOmnibus]'}
raw={s for s in raw if not s.startswith('Semi-Roguelike (')}
raw |= {'<<?? unknown>>','Extract gems','Reality adjustment','Accept','Cancel','Mark as Seen','Continue',' (%d)','Wall Clock'}
patches=[]
for p in sorted(out.rglob('*.lua')):
    text=p.read_text(); edits=[]
    for m,s in tokens(text):
        before=text[max(0,m.start()-100):m.start()]; after=text[m.end():m.end()+90]
        if s not in raw:continue
        if re.search(r'_t\s*\(?\s*$',before):continue
        if re.match(r'\s*\)?\s*:tformat',after):continue
        edits.append((m.start(),m.end(),'_t('+m.group()+')'))
    for a,b,new in reversed(edits):text=text[:a]+new+text[b:]
    if edits: patches.append({'file':str(p.relative_to(out)),'wrapped_literals':len(edits)})
    if p.name=='hooks-landmark.lua':
        old="(e.lever and '' or 'not ')"
        assert old in text
        text=text.replace(old,"(e.lever and _t'already ' or _t'not ')")
    p.write_text(text)

# Native I18N argument mapping removes English grammatical suffixes.
orders={
 'There %s %d non-unique metallic item%s in your transmogrification chest.  Extract gem%s from %s?':[2],
 'Delete %d note%s?':[1],
}
q=lambda s:json.dumps(s,ensure_ascii=False)
locale=['-- Simplified Chinese translation for ZOmnibus Lite 17.9.5. GPL-3.0-or-later.', 'locale "zh_hans"','']
fmt=re.compile(r'%(?:[-+ #0]*\d*(?:\.\d+)?)[cdiouxXeEfgGqs%]')
for s,t in d.items():
    a=[m.group() for m in fmt.finditer(s) if m.group()!='%%']
    b=[m.group() for m in fmt.finditer(t) if m.group()!='%%']
    order=orders.get(s)
    expected=[a[i-1] for i in order] if order else a
    assert expected==b, (s,a,t,b)
    if order:
        mapping='{'+','.join(f'[{i}]={v}' for i,v in enumerate(order,1))+'}'
        locale.append(f't({q(s)}, {q(t)}, "tformat", {mapping})')
    else:locale.append(f't({q(s)}, {q(t)})')
loc=out/'data/locales/zh_hans.lua';loc.parent.mkdir(parents=True,exist_ok=True)
loc.write_text('\n'.join(locale)+'\n')
# Check coverage of all original literal translation call sites.
required=json.loads((ROOT/'strings.json').read_text())
assert set(required)<=set(d)
for p in out.rglob('*.lua'):
    subprocess.run(['/opt/homebrew/bin/luajit','-b',str(p),'/dev/null'],check=True,capture_output=True)
archive=ROOT/'dist/tome-zomnibus_lite.teaa'
# Preserve upstream ZIP metadata and, crucially, stored image entries.
# The native image loader cannot decode PNGs from deflated PhysicsFS entries.
with zipfile.ZipFile(ROOT/'upstream/tome-zomnibus_lite.teaa') as upstream, zipfile.ZipFile(archive,'w') as z:
    for original_info in upstream.infolist():
        z.writestr(original_info,(out/original_info.filename).read_bytes())
    z.writestr('data/locales/zh_hans.lua',loc.read_bytes(),compress_type=zipfile.ZIP_STORED)
report={'upstream_sha256':hashlib.sha256((ROOT/'upstream/tome-zomnibus_lite.teaa').read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'translations':len(d),'required_literal_strings':len(required),'raw_literal_patches':patches,'source_lua_files':len(list(src.rglob('*.lua'))),'lua_files_compiled':len(list(out.rglob('*.lua')))}
(ROOT/'dist/validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(ROOT/'dist/translations.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
