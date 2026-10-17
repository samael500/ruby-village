"""Repeat existing author harnesses against separate independent production export."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/chapter-1-rc/qa/residents-bridge-audio-467'
for name,old,new in [('residents-runtime.py','evidence/residents-runtime','residents'),('bridge-three-hex.py','evidence/bridge-three-hex','bridges'),('release-browser.py','release/current-export','pruned-export')]:
 source=ROOT/'scripts/qa'/name
 text=source.read_text().replace('http://127.0.0.1:5180/ruby-village/','http://127.0.0.1:5297/ruby-village/').replace("root/'docs/chapter-1-rc/"+old+"'","root/'docs/chapter-1-rc/qa/residents-bridge-audio-467/"+new+"'")
 exec(compile(text,str(source),'exec'),{'__file__':str(source),'__name__':'__main__'})
