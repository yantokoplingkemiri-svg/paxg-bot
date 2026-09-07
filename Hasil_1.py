import time
import requests

# Konfigurasi Bot Telegram
TELEGRAM_BOT_TOKEN = "8715144257:AAFKVkW2K74hvrlQn6CDqzt_Mo62agaQM30"
TELEGRAM_CHAT_ID = "8227573501"

# Batas Target Harga
TARGET_TINGGI = 80000000
TARGET_RENDAH = 75000000

def get_paxg_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=pax-gold&vs_currencies=idr"
    try:
        response = requests.get(url)
        data = response.json()
        return data.get('pax-gold', {}).get('idr', 0)
    except Exception as e:
        print("Gagal mengambil harga:", e)
        return 0

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("Gagal mengirim pesan Telegram:", e)

def monitor_price():
    print("Bot pemantau harga PAXG aktif... (Tekan Ctrl+C untuk berhenti)")
    
    # Variabel pencegah spam agar notifikasi tidak dikirim terus-menerus di level harga yang sama
    status_notif = None 

    while True:
        current_price = get_paxg_price()
        
        if current_price > 0:
            print(f"Harga terkini dicek: Rp {current_price:,.0f}")
            
            # Cek kondisi target tertinggi
            if current_price >= TARGET_TINGGI and status_notif != "TINGGI":
                message = (
                    f"🚀 *ALARM TARGET TINGGI TERCAPAI!* 🚀\n\n"
                    f"💰 Harga PAXG: *Rp {current_price:,.0f} / oz*\n"
                    f"📈 Harga telah menyentuh atau melewati batas atas Rp 80.000.000!"
                )
                send_telegram_message(message)
                status_notif = "TINGGI"
                
            # Cek kondisi target terendah
            elif current_price <= TARGET_RENDAH and status_notif != "RENDAH":
                message = (
                    f"⚠️ *ALARM TARGET RENDAH / BUY THE DIP!* ⚠️\n\n"
                    f"💰 Harga PAXG: *Rp {current_price:,.0f} / oz*\n"
                    f"📉 Harga telah turun mendekati atau melewati batas bawah Rp 75.000.000!"
                )
                send_telegram_message(message)
                status_notif = "RENDAH"
                
            # Reset status jika harga kembali normal di tengah-tengah
            elif TARGET_RENDAH < current_price < TARGET_TINGGI:
                status_notif = "NORMAL"
                
        # Jeda waktu pengecekan (3600 detik = 1 jam)
        # Anda bisa mengubah angka ini (misal 300 untuk 5 menit)
        time.sleep(3600)

if __name__ == "__main__":
    monitor_price()