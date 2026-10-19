import json, urllib.request, os
from datetime import datetime, timedelta

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ.get("CHAT_ID", "-1003998737387")
PERSONAL_CHAT_ID = "244117895"

print(f"CHAT_ID: {CHAT_ID}")
print(f"CHAT_ID type: {type(CHAT_ID)}")

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

def db_light(table, fields):
    url = f"{SUPABASE_URL}/rest/v1/{table}?select={fields}"
    req = urllib.request.Request(url, headers={
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    })
    try:
        return json.loads(urllib.request.urlopen(req).read().decode())
    except Exception as e:
        print(f"DB xato ({table}): {e}")
        return []

def tg(text, chat_id=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = json.dumps({"chat_id": chat_id or CHAT_ID, "text": text}).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        res = urllib.request.urlopen(req)
        print("Yuborildi! Status:", res.status)
    except Exception as e:
        print(f"TG xato: {e}")

def tg_file(content, filename, caption, chat_id):
    """Telegram ga fayl yuborish (multipart/form-data)"""
    import io
    boundary = "----BackupBoundary"
    body = b""
    # chat_id
    body += f"--{boundary}\r\n".encode()
    body += f'Content-Disposition: form-data; name="chat_id"\r\n\r\n'.encode()
    body += f"{chat_id}\r\n".encode()
    # caption
    body += f"--{boundary}\r\n".encode()
    body += f'Content-Disposition: form-data; name="caption"\r\n\r\n'.encode()
    body += f"{caption}\r\n".encode()
    # document
    body += f"--{boundary}\r\n".encode()
    body += f'Content-Disposition: form-data; name="document"; filename="{filename}"\r\n'.encode()
    body += b'Content-Type: application/json\r\n\r\n'
    body += content.encode()
    body += f"\r\n--{boundary}--\r\n".encode()

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": f"multipart/form-data; boundary={boundary}"
    })
    try:
        res = urllib.request.urlopen(req)
        print(f"Backup yuborildi! Status: {res.status}")
    except Exception as e:
        print(f"Backup yuborishda xato: {e}")

def fm(n):
    if not n: return ""
    return f"{int(n):,} som".replace(",", " ")

def get_date(val):
    if not val: return ""
    return str(val)[:10]

orders = db("orders", "&status=neq.topshirildi")
all_orders = db("orders")
remont_list = db("remont", "&status=neq.topshirildi")

bugun = [o for o in orders if get_date(o.get('due_date')) == today]
ertaga = [o for o in orders if get_date(o.get('due_date')) == tomorrow]
kechikkan = [o for o in orders if get_date(o.get('due_date')) and get_date(o.get('due_date')) < today]
tayyor = [o for o in orders if o.get('status') == 'tayyor']
jarayonda = [o for o in orders if o.get('status') == 'jarayonda']
yangi = [o for o in orders if o.get('status') == 'yangi']

r_bugun = [r for r in remont_list if get_date(r.get('due_date')) == today]
r_ertaga = [r for r in remont_list if get_date(r.get('due_date')) == tomorrow]
r_tayyor = [r for r in remont_list if r.get('status') == 'tayyor']
r_kechik = [r for r in remont_list if get_date(r.get('due_date')) and get_date(r.get('due_date')) < today]
r_jarayonda = [r for r in remont_list if r.get('status') == 'jarayonda']

msg = f"Murad Jewellery - {today}\n"
msg += "=" * 28 + "\n\n"

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
        msg += f"• {o.get('client','')} - {get_date(o.get('due_date',''))}\n"
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
        if o.get('due_date'): msg += f" | {get_date(o['due_date'])}"
        msg += "\n"
    msg += "\n"

if yangi:
    msg += f"YANGI ({len(yangi)} ta):\n"
    for o in yangi:
        msg += f"• {o.get('client','')}\n"
    msg += "\n"

if not orders:
    msg += "Faol buyurtma yoq!\n\n"

if r_bugun or r_ertaga or r_tayyor or r_kechik or r_jarayonda:
    msg += "--- REMONT ---\n"
    for r in r_bugun:
        msg += f"Bugun: {r.get('client','')} - {r.get('item','')}\n"
    for r in r_ertaga:
        msg += f"Ertaga: {r.get('client','')} - {r.get('item','')}\n"
    for r in r_tayyor:
        msg += f"Tayyor: {r.get('client','')} - {r.get('item','')}\n"
    for r in r_kechik:
        msg += f"Kechikkan: {r.get('client','')} - {get_date(r.get('due_date',''))}\n"
    for r in r_jarayonda:
        msg += f"Jarayonda: {r.get('client','')} - {r.get('item','')}\n"
    msg += "\n"

msg += "murodgold.com"
tg(msg)

# ===== YAKSHANBA: HAFTALIK HISOBOT + AVTOMATIK BACKUP =====
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
    w += "\nmurodgold.com"
    tg(w)

    # Avtomatik backup - rasmlar va signature'siz
    print("Backup tayyorlanmoqda...")
    try:
        o_data = db_light("orders", "id,code,client,phone,description,metal_type,metal_gram,metal_sof,status,price,prepay,remain,due_date,note,created_at,updated_at")
        r_data = db_light("remont", "id,client,phone,item,problem,metal,status,price,due_date,created_at,updated_at")
        x_data = db_light("xarid", "id,name,phone,passport,date,metal_type,gram,price_gram,total,note,status,created_at")
        q_data = db_light("qarz", "id,name,phone,passport,date,metal,gram,qiymat,total,tolandan,qoldiq,return_date,status,note,created_at,updated_at")
        c_data = db("catalog")
        n_data = db("notes")

        backup = {
            "exported_at": datetime.now().isoformat(),
            "version": "1.0",
            "source": "auto-weekly",
            "data": {
                "orders": o_data,
                "remont": r_data,
                "xarid": x_data,
                "qarz": q_data,
                "catalog": c_data,
                "notes": n_data
            }
        }
        backup_json = json.dumps(backup, ensure_ascii=False, indent=2)
        filename = f"murad-jewellery-backup-{today}.json"
        caption = (
            f"💾 Haftalik Avtomatik Backup\n"
            f"📅 {today}\n\n"
            f"📦 Buyurtmalar: {len(o_data)}\n"
            f"🔧 Remont: {len(r_data)}\n"
            f"🥇 Xarid: {len(x_data)}\n"
            f"💰 Qarz: {len(q_data)}\n"
            f"🏺 Katalog: {len(c_data)}"
        )
        tg_file(backup_json, filename, caption, PERSONAL_CHAT_ID)
    except Exception as e:
        print(f"Backup xato: {e}")
        tg(f"⚠️ Avtomatik backup xato: {e}", PERSONAL_CHAT_ID)

print("Tayyor!")
