import csv, json
from pathlib import Path
src=Path('/home/ubuntu/tawoos-pwa/items.csv')
out=Path('/home/ubuntu/tawoos-pwa/products.json')
items=[]
with src.open(encoding='utf-8-sig', newline='') as f:
    for r in csv.DictReader(f):
        try:
            w=float(r.get('I_S_Price_W') or 0); n=float(r.get('I_S_Price_P') or 0)
        except ValueError:
            w=n=0
        items.append({'code':str(r.get('I_Code') or ''),'name':str(r.get('I_Name') or ''),'wholesale':w,'retail':n})
with out.open('w',encoding='utf-8') as f: json.dump(items,f,ensure_ascii=False,separators=(',',':'))
print(out, len(items))
