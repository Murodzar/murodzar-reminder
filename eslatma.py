import json, urllib.request, os
from datetime import datetime, timedelta

try:
    import urllib.request as req
    supabase_url = os.environ['SUPABASE_URL']
    supabase_key = os.environ['SUPABASE_KEY']
    bot = os.environ['BOT_TOKEN']
    chat = os.environ['CHAT_ID']

    # Supabase dan buyurtmalarni olish
    url = f"{supabase_url}/rest/v1/orders?select=*&status=neq.topshirildi"
    request = urllib.request.Request(url, headers={
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}"
    })
    response = urllib.request.urlopen(request)
    orders = json.loads(response.read().decode())
except Exception as e:
    print(f"Xato: {e}")
    orders = []

today = datetime.now().strftime('%Y-%m-%d')
tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

def send(text):
    url = f"https://api.telegram.org/bot{bot}/sendMessage"
    data = json.dumps({"chat_id": chat, "text": text}).encode()
    urllib.request.urlopen(urllib.request.Request(url, data, {"Content-Type": "application/json"}))

bugun = [o for o in orders if o.get('due_date') == today]
ertaga = [o for o in orders if o.get('due_date') == tomorrow]
kechikkan = [o for o in orders if o.get('due_date') and o['due_date'] < today]
tayyor = [o for o in orders if o.get('status') == 'tayyor']

msg = f"Murad Jewellery - {today}\n\n"

if bugun:
    msg += f"BUGUN TOPSHIRISH ({len(bugun)} ta):\n"
    for o in bugun:
        msg += f"- {o.get('client','')}\n"
        if o.get('metal_type'):
            msg += f"  {o['metal_type']}"
            if o.get('metal_gram'):
                msg += f" {o['metal_gram']}g"
            msg += "\n"
        if o.get('phone'):
            msg += f"  Tel: {o['phone']}\n"
        if o.get('remain'):
            msg += f"  Qoldiq: {int(o['remain'])} som\n"

if ertaga:
    msg += f"\nERTAGA ({len(ertaga)} ta):\n"
    for o in ertaga:
        msg += f"- {o.get('client','')}\n"
        if o.get('metal_type'):
            msg += f"  {o['metal_type']}\n"

if kechikkan:
    msg += f"\nKECHIKKAN ({len(kechikkan)} ta):\n"
    for o in kechikkan:
        msg += f"- {o.get('client','')} - {o.get('due_date','')}\n"

if tayyor:
    msg += f"\nTAYYOR-KUTMOQDA ({len(tayyor)} ta):\n"
    for o in tayyor:
        msg += f"- {o.get('client','')}\n"
        if o.get('remain'):
            msg += f"  Qoldiq: {int(o['remain'])} som\n"

if not bugun and not ertaga and not kechikkan:
    msg += "Yaqin kunlarda topshirish yoq!\n"

msg += "\nmurodzar.netlify.app"
send(msg)
print("Xabar yuborildi!")
