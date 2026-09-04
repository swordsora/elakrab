import csv, json, subprocess
from pathlib import Path
base=Path('/home/ubuntu/upload/tawoos.mdb'); out=Path('/home/ubuntu/tawoos-pwa')
def export(table):
    p=subprocess.run(['mdb-export',str(base),table],check=True,capture_output=True,text=True,encoding='utf-8')
    return csv.DictReader(p.stdout.splitlines())
customers=[]
for r in export('Cus_Names'):
    customers.append({'code':str(r.get('Cus_Code') or '').strip(),'name':str(r.get('Cus_Name') or '').strip(),'city':str(r.get('Cus_City') or '').strip(),'address':str(r.get('Cus_Address') or '').strip(),'phone':str(r.get('Tel_1') or '').strip()})
customers=[x for x in customers if x['code']]
with (out/'customers.json').open('w',encoding='utf-8') as f: json.dump(customers,f,ensure_ascii=False,separators=(',',':'))
# Map product code to product pricing for classifying historical sale price.
products={x['code']:x for x in json.loads((out/'products.json').read_text(encoding='utf-8'))}
history={}
for r in export('Inv_Sale_Base'):
    inv=str(r.get('Inv_No') or '').strip(); code=str(r.get('Cus_Name') or '').strip(); date=str(r.get('Inv_Date') or '').strip()
    if not code or not inv: continue
    # Details are joined below by invoice number.
    history.setdefault(code,{'invoices':set(),'lastDate':'','items':{}})
    history[code]['invoices'].add(inv)
    if date: history[code]['lastDate']=date
# Re-read detail and attach prior products by invoice/customer index.
inv_customer={}
for r in export('Inv_Sale_Base'):
    inv=str(r.get('Inv_No') or '').strip(); code=str(r.get('Cus_Name') or '').strip(); date=str(r.get('Inv_Date') or '').strip()
    if inv and code: inv_customer[inv]=(code,date)
for r in export('Inv_Sale_Det'):
    inv=str(r.get('Inv_No') or '').strip(); rel=inv_customer.get(inv)
    if not rel: continue
    cus,date=rel; pcode=str(r.get('I_Code') or '').strip(); name=str(r.get('I_Name') or '').strip(); qty=float(str(r.get('Qu1') or '0').replace(',','') or 0); price=float(str(r.get('S_Price') or '0').replace(',','') or 0)
    prod=products.get(pcode,{}); w=float(prod.get('wholesale') or 0); retail=float(prod.get('retail') or 0)
    if abs(price-w)<=abs(price-retail): mode='wholesale'
    else: mode='retail'
    rec=history.setdefault(cus,{'invoices':set(),'lastDate':date,'items':{}})
    key=pcode or name
    old=rec['items'].get(key)
    rec['items'][key]={'code':pcode,'name':name,'lastPrice':price,'mode':mode,'lastDate':date,'totalQty':round((old or {}).get('totalQty',0)+qty,2)}
result=[]
for code,rec in history.items():
    result.append({'customerCode':code,'invoiceCount':len(rec['invoices']),'lastDate':rec['lastDate'],'items':list(rec['items'].values())})
with (out/'customer_history.json').open('w',encoding='utf-8') as f: json.dump(result,f,ensure_ascii=False,separators=(',',':'))
print('customers',len(customers),'history customers',len(result),'files ready')
