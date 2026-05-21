import json
import urllib.request
import os
from datetime import datetime, timedelta

# === SOZLAMALAR ===
SUPABASE_URL = "https://rztbawzfeqqtpbifkgjd.supabase.co"
SUPABASE_KEY = "sb_publishable_mF63LJOpb_lzR_P_WmmZEA_W5oc8JPD"
BOT_TOKEN = "8535445836:AAHkniWDqi25cLPDutKQY5valMv_naeQ1PI"
CHAT_ID = "-800338592"  # Ish guruhi

today = datetime.now().strftime('%Y-%m-%d')
tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
weekday = datetime.now().weekday()  # 0=Dushanba

# === FUNKSIYALAR ===
def supabase_get(table, params=""):
    url = f"{SUPABASE_URL}/rest/v1/{table}?select=*{params}"
    req = urllib.request.Request(url, headers={
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    })
    try:
        res = urllib.request.urlopen(req)
        return json.loads(res.read().decode())
    except Exception as e:
        print(f"Supabase xato ({table}): {e}")
        return []

def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = json.dumps({
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req)
        print("Xabar yuborildi!")
    except Exception as e:
        print(f"Telegram xato: {e}")

def fmoney(n):
    if not n: return ""
    return f"{int(n):,} so'm".replace(",", " ")

# === MA'LUMOTLAR OLISH ===
orders = supabase_get("orders", "&status=neq.topshirildi")
all_orders = supabase_get("orders")
remont_list = supabase_get("remont", "&status=neq.topshirildi")

# === BUYURTMALAR TASNIFI ===
bugun = [o for o in orders if o.get('due_date') == today]
ertaga = [o for o in orders if o.get('due_date') == tomorrow]
kechikkan = [o for o in orders if o.get('due_date') and o['due_date'] < today and o.get('status') != 'topshirildi']
tayyor = [o for o in orders if o.get('status') == 'tayyor']
yangi = [o for o in orders if o.get('status') == 'yangi']

# === REMONT TASNIFI ===
remont_bugun = [r for r in remont_list if r.get('due_date') == today]
remont_ertaga = [r for r in remont_list if r.get('due_date') == tomorrow]
remont_tayyor = [r for r in remont_list if r.get('status') == 'tayyor']
remont_kechikkan = [r for r in remont_list if r.get('due_date') and r['due_date'] < today]

# === KUNLIK XABAR ===
msg = f"<b>Murad Jewellery</b>\n"
msg += f"Sana: {today}\n"
msg += "=" * 25 + "\n\n"

# Buyurtmalar
if bugun:
    msg += f"BUGUN TOPSHIRISH ({len(bugun)} ta):\n"
    for o in bugun:
        msg += f"• <b>{o.get('client', '')}</b>\n"
        if o.get('metal_type'):
            msg += f"  {o['metal_type']}"
            if o.get('metal_gram'):
                msg += f" {o['metal_gram']}g"
            msg += "\n"
        if o.get('phone'):
            msg += f"  Tel: {o['phone']}\n"
        if o.get('remain'):
            msg += f"  Qoldiq: {fmoney(o['remain'])}\n"
    msg += "\n"

if ertaga:
    msg += f"ERTAGA TOPSHIRISH ({len(ertaga)} ta):\n"
    for o in ertaga:
        msg += f"• <b>{o.get('client', '')}</b>\n"
        if o.get('metal_type'):
            msg += f"  {o['metal_type']}\n"
        if o.get('phone'):
            msg += f"  Tel: {o['phone']}\n"
    msg += "\n"

if kechikkan:
    msg += f"KECHIKKAN BUYURTMALAR ({len(kechikkan)} ta):\n"
    for o in kechikkan:
        msg += f"• <b>{o.get('client', '')}</b> - {o.get('due_date', '')}\n"
        if o.get('phone'):
            msg += f"  Tel: {o['phone']}\n"
    msg += "\n"

if tayyor:
    msg += f"TAYYOR - KUTMOQDA ({len(tayyor)} ta):\n"
    for o in tayyor:
        msg += f"• <b>{o.get('client', '')}</b>\n"
        if o.get('remain'):
            msg += f"  Qoldiq: {fmoney(o['remain'])}\n"
    msg += "\n"

if yangi:
    msg += f"YANGI BUYURTMALAR ({len(yangi)} ta):\n"
    for o in yangi:
        msg += f"• <b>{o.get('client', '')}</b>\n"
        if o.get('description'):
            msg += f"  {o['description'][:50]}\n"
    msg += "\n"

if not bugun and not ertaga and not kechikkan and not tayyor:
    msg += "Yaqin kunlarda topshirish yoq!\n\n"

# Remont
if remont_bugun or remont_ertaga or remont_kechikkan or remont_tayyor:
    msg += "--- REMONT ---\n"
    if remont_bugun:
        msg += f"Bugun ({len(remont_bugun)} ta):\n"
        for r in remont_bugun:
            msg += f"• <b>{r.get('client', '')}</b> - {r.get('item', '')}\n"
    if remont_ertaga:
        msg += f"Ertaga ({len(remont_ertaga)} ta):\n"
        for r in remont_ertaga:
            msg += f"• <b>{r.get('client', '')}</b> - {r.get('item', '')}\n"
    if remont_tayyor:
        msg += f"Tayyor ({len(remont_tayyor)} ta):\n"
        for r in remont_tayyor:
            msg += f"• <b>{r.get('client', '')}</b> - {r.get('item', '')}\n"
    if remont_kechikkan:
        msg += f"Kechikkan ({len(remont_kechikkan)} ta):\n"
        for r in remont_kechikkan:
            msg += f"• <b>{r.get('client', '')}</b> - {r.get('due_date', '')}\n"
    msg += "\n"

msg += "murodzar.netlify.app"

send_telegram(msg)

# === HAFTALIK HISOBOT (faqat Dushanba) ===
if weekday == 0:
    week_orders = [o for o in all_orders if str(o.get('created_at', ''))[:10] >= week_ago]
    topshirildi_count = len([o for o in week_orders if o.get('status') == 'topshirildi'])
    active_count = len([o for o in all_orders if o.get('status') in ['yangi', 'jarayonda']])
    total_sum = sum(o.get('price') or 0 for o in week_orders)
    total_prepay = sum(o.get('prepay') or 0 for o in week_orders)
    total_remain = sum(o.get('remain') or 0 for o in all_orders if o.get('status') != 'topshirildi')

    week_msg = f"<b>Haftalik Hisobot - Murad Jewellery</b>\n"
    week_msg += "=" * 25 + "\n\n"
    week_msg += f"Bu hafta yangi: <b>{len(week_orders)} ta</b>\n"
    week_msg += f"Topshirildi: <b>{topshirildi_count} ta</b>\n"
    week_msg += f"Hozir ishda: <b>{active_count} ta</b>\n"
    if total_sum:
        week_msg += f"\nUmumiy summa: <b>{fmoney(total_sum)}</b>\n"
    if total_prepay:
        week_msg += f"Oldindan tolangan: <b>{fmoney(total_prepay)}</b>\n"
    if total_remain:
        week_msg += f"Qoldiq tolovlar: <b>{fmoney(total_remain)}</b>\n"
    week_msg += f"\nmurodzar.netlify.app"

    send_telegram(week_msg)
    print("Haftalik hisobot yuborildi!")
