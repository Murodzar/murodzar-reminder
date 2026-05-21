import json
import urllib.request
from datetime import datetime, timedelta

SUPABASE_URL = "https://rztbawzfeqqtpbifkgjd.supabase.co"
SUPABASE_KEY = "YOUR_SUPABASE_KEY"
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

today = datetime.now().strftime('%Y-%m-%d')
tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
weekday = datetime.now().weekday()
week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

def db(table, params=""):
    url = f"{SUPABASE_URL}/rest/v1/{table}?select=*{params}"

    req = urllib.request.Request(
        url,
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}"
        }
    )

    try:
        return json.loads(
            urllib.request.urlopen(req).read().decode()
        )

    except Exception as e:
        print("DB Xato:", e)
        return []

def tg(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = json.dumps({
        "chat_id": CHAT_ID,
        "text": text
    }).encode()

    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json"
        }
    )

    try:
        urllib.request.urlopen(req)

    except Exception as e:
        print("Telegram xato:", e)

def fm(n):
    if not n:
        return ""

    return f"{int(n):,} som".replace(",", " ")

# DATABASE
orders = db("orders", "&status=neq.topshirildi")
all_orders = db("orders")
remont_list = db("remont", "&status=neq.topshirildi")

# ORDERS
bugun = [
    o for o in orders
    if str(o.get('due_date', ''))[:10] == today
]

ertaga = [
    o for o in orders
    if str(o.get('due_date', ''))[:10] == tomorrow
]

kechikkan = [
    o for o in orders
    if o.get('due_date')
    and str(o['due_date'])[:10] < today
]

tayyor = [
    o for o in orders
    if o.get('status') == 'tayyor'
]

yangi = [
    o for o in orders
    if o.get('status') == 'yangi'
]

# REMONT
r_bugun = [
    r for r in remont_list
    if str(r.get('due_date', ''))[:10] == today
]

r_ertaga = [
    r for r in remont_list
    if str(r.get('due_date', ''))[:10] == tomorrow
]

r_tayyor = [
    r for r in remont_list
    if r.get('status') == 'tayyor'
]

r_kechik = [
    r for r in remont_list
    if r.get('due_date')
    and str(r['due_date'])[:10] < today
]

# MESSAGE
msg = f"💍 Murad Jewellery - {today}\n"
msg += "=" * 30 + "\n\n"

# BUGUN
if bugun:
    msg += f"🔴 BUGUN TOPSHIRISH ({len(bugun)} ta):\n"

    for o in bugun:
        msg += f"• {o.get('client','')}\n"

        if o.get('metal_type'):
            msg += f"  {o['metal_type']}"

            if o.get('metal_gram'):
                msg += f" {o['metal_gram']}g"

            msg += "\n"

        if o.get('phone'):
            msg += f"  Tel: {o['phone']}\n"

        if o.get('remain'):
            msg += f"  Qoldiq: {fm(o['remain'])}\n"

    msg += "\n"

# ERTAGA
if ertaga:
    msg += f"🟡 ERTAGA TOPSHIRISH ({len(ertaga)} ta):\n"

    for o in ertaga:
        msg += f"• {o.get('client','')}"

        if o.get('metal_type'):
            msg += f" | {o['metal_type']}"

        msg += "\n"

    msg += "\n"

# KECHIKKAN
if kechikkan:
    msg += f"⚠️ KECHIKKAN ({len(kechikkan)} ta):\n"

    for o in kechikkan:
        msg += f"• {o.get('client','')}"

        if o.get('due_date'):
            msg += f" - {str(o['due_date'])[:10]}"

        msg += "\n"

        if o.get('phone'):
            msg += f"  Tel: {o['phone']}\n"

    msg += "\n"

# TAYYOR
if tayyor:
    msg += f"✅ TAYYOR - KUTMOQDA ({len(tayyor)} ta):\n"

    for o in tayyor:
        msg += f"• {o.get('client','')}"

        if o.get('remain'):
            msg += f" | Qoldiq: {fm(o['remain'])}"

        msg += "\n"

    msg += "\n"

# YANGI
if yangi:
    msg += f"🆕 YANGI BUYURTMALAR ({len(yangi)} ta):\n"

    for o in yangi:
        msg += f"• {o.get('client','')}\n"

    msg += "\n"

# REMONT
if r_bugun or r_ertaga or r_tayyor or r_kechik:

    msg += "🔧 REMONT:\n"

    for r in r_bugun:
        msg += f"Bugun: {r.get('client','')} - {r.get('item','')}\n"

    for r in r_ertaga:
        msg += f"Ertaga: {r.get('client','')} - {r.get('item','')}\n"

    for r in r_tayyor:
        msg += f"Tayyor: {r.get('client','')} - {r.get('item','')}\n"

    for r in r_kechik:
        msg += f"Kechikkan: {r.get('client','')} - {str(r.get('due_date',''))[:10]}\n"

    msg += "\n"

# EMPTY
if (
    not bugun
    and not ertaga
    and not kechikkan
    and not tayyor
    and not yangi
):
    msg += "✅ Faol buyurtma yoq!\n\n"

msg += "🌐 murodzar.netlify.app"

# SEND
tg(msg)

# WEEKLY REPORT
if weekday == 0:

    week_o = [
        o for o in all_orders
        if str(o.get('created_at', ''))[:10] >= week_ago
    ]

    topsh = len([
        o for o in week_o
        if o.get('status') == 'topshirildi'
    ])

    active = len([
        o for o in all_orders
        if o.get('status') in ['yangi', 'jarayonda']
    ])

    total = sum(
        o.get('price') or 0
        for o in week_o
    )

    qoldiq = sum(
        o.get('remain') or 0
        for o in all_orders
        if o.get('status') != 'topshirildi'
    )

    w = "📊 Haftalik Hisobot - Murad Jewellery\n"
    w += "=" * 30 + "\n\n"

    w += f"Yangi: {len(week_o)} ta\n"
    w += f"Topshirildi: {topsh} ta\n"
    w += f"Ishda: {active} ta\n"

    if total:
        w += f"Summa: {fm(total)}\n"

    if qoldiq:
        w += f"Qoldiq tolovlar: {fm(qoldiq)}\n"

    w += "\n🌐 murodzar.netlify.app"

    tg(w)

    print("Haftalik hisobot yuborildi!")

print("Tayyor!")
