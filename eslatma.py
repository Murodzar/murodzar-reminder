import json, urllib.request
from datetime import datetime, timedelta

SUPABASE_URL = "https://rztbawzfeqqtpbifkgjd.supabase.co"
SUPABASE_KEY = "sb_publishable_mF63LJOpb_lzR_P_WmmZEA_W5oc8JPD"
BOT_TOKEN = "8535445836:AAHkniWDqi25cLPDutKQY5valMv_naeQ1PI"
CHAT_ID = "-1003998737387"

today = datetime.now().strftime('%Y-%m-%d')
tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
weekday = datetime.now().weekday()
week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

def db(table, params=""):
    url = f"{SUPABASE_URL}/rest/v1/{table}?select=*{params}"
    req = urllib.request.Request(url, headers={
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    })
    try:
        return json.loads(urllib.request.urlopen(req).read().decode())
    except Exception as e:
        print(f"DB xato: {e}")
        return []

def tg(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = json.dumps({"chat_id": CHAT_ID, "text": text}).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req)
        print("Yuborildi!")
    except Exception as e:
        print(f"TG xato: {e}")

def fm(n):
    if not n: return ""
    return f"{int(n):,} som".replace(",", " ")

# Ma'lumotlar
orders = db("orders", "&status=neq.topshirildi")
all_orders = db("orders")
remont_list = db("remont", "&status=neq.topshirildi")

bugun = [o for o in orders if o.get('due_date') == today]
ertaga = [o for o in orders if o.get('due_date') == tomorrow]
kechikkan = [o for o in orders if o.get('due_date') and o['due_date'] < today]
tayyor = [o for o in orders if o.get('status') == 'tayyor']
jarayonda = [o for o in orders if o.get('status') == 'jarayonda']
yangi = [o for o in orders if o.get('status') == 'yangi']

r_bugun = [r for r in remont_list if r.get('due_date') == today]
r_ertaga = [r for r in remont_list if r.get('due_date') == tomorrow]
r_tayyor = [r for r in remont_list if r.get('status') == 'tayyor']
r_kechik = [r for r in remont_list if r.get('due_date') and r['due_date'] < today]
r_jarayonda = [r for r in remont_list if r.get('status') == 'jarayonda']

# Kunlik xabar
msg = f"Murad Jewellery - {today}\n"
msg += "=" * 28 + "\n\n"

# Buyurtmalar holati
if bugun:
    msg += f"BUGUN TOPSHIRISH ({len(bugun)} ta):\n"
    for o in bugun:
        msg += f"• {o.get('client','')}\n"
        if o.get('metal_type'):
            msg += f"  {o['metal_type']}"
            if o.get('metal_gram'): msg += f" {o['metal_gram']}g"
            msg += "\n"
        if o.get('phone'): msg += f"  Tel: {o['phone']}\n"
        if o.get('remain'): msg += f"  Qoldiq: {fm(o['remain'])}\n"
    msg += "\n"

if ertaga:
    msg += f"ERTAGA TOPSHIRISH ({len(ertaga)} ta):\n"
    for o in ertaga:
        msg += f"• {o.get('client','')}"
        if o.get('metal_type'): msg += f" | {o['metal_type']}"
        msg += "\n"
    msg += "\n"

if kechikkan:
    msg += f"KECHIKKAN ({len(kechikkan)} ta):\n"
    for o in kechikkan:
        msg += f"• {o.get('client','')} - {o.get('due_date','')}\n"
        if o.get('phone'): msg += f"  Tel: {o['phone']}\n"
    msg += "\n"

if tayyor:
    msg += f"TAYYOR - KUTMOQDA ({len(tayyor)} ta):\n"
    for o in tayyor:
        msg += f"• {o.get('client','')}"
        if o.get('remain'): msg += f" | Qoldiq: {fm(o['remain'])}"
        msg += "\n"
    msg += "\n"

if jarayonda:
    msg += f"JARAYONDA ({len(jarayonda)} ta):\n"
    for o in jarayonda:
        msg += f"• {o.get('client','')}"
        if o.get('metal_type'): msg += f" | {o['metal_type']}"
        if o.get('metal_gram'): msg += f" {o['metal_gram']}g"
        if o.get('due_date'): msg += f" | {o['due_date']}"
        msg += "\n"
    msg += "\n"

if yangi:
    msg += f"YANGI ({len(yangi)} ta):\n"
    for o in yangi:
        msg += f"• {o.get('client','')}\n"
    msg += "\n"

if not orders:
    msg += "Faol buyurtma yoq!\n\n"

# Remont
if r_bugun or r_ertaga or r_tayyor or r_kechik or r_jarayonda:
    msg += "--- REMONT ---\n"
    for r in r_bugun:
        msg += f"Bugun: {r.get('client','')} - {r.get('item','')}\n"
    for r in r_ertaga:
        msg += f"Ertaga: {r.get('client','')} - {r.get('item','')}\n"
    for r in r_tayyor:
        msg += f"Tayyor: {r.get('client','')} - {r.get('item','')}\n"
    for r in r_kechik:
        msg += f"Kechikkan: {r.get('client','')} - {r.get('due_date','')}\n"
    for r in r_jarayonda:
        msg += f"Jarayonda: {r.get('client','')} - {r.get('item','')}\n"
    msg += "\n"

msg += "murodzar.github.io"
tg(msg)

# Haftalik hisobot (faqat Dushanba)
if weekday == 0:
    week_o = [o for o in all_orders if str(o.get('created_at',''))[:10] >= week_ago]
    topsh = len([o for o in week_o if o.get('status') == 'topshirildi'])
    active = len([o for o in all_orders if o.get('status') in ['yangi','jarayonda']])
    total = sum(o.get('price') or 0 for o in week_o)
    qoldiq = sum(o.get('remain') or 0 for o in all_orders if o.get('status') != 'topshirildi')

    w = f"Haftalik Hisobot - Murad Jewellery\n"
    w += "=" * 28 + "\n\n"
    w += f"Yangi: {len(week_o)} ta\n"
    w += f"Topshirildi: {topsh} ta\n"
    w += f"Ishda: {active} ta\n"
    if total: w += f"Summa: {fm(total)}\n"
    if qoldiq: w += f"Qoldiq tolovlar: {fm(qoldiq)}\n"
    w += "\nmurodzar.github.io"
    tg(w)

print("Tayyor!")
