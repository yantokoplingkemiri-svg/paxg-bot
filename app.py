from flask import Flask
import threading
import Hasil_1  # Memanggil skrip bot Anda yang sudah ada

app = Flask(__name__)

@app.route('/')
def home():
    return "PAXG Bot is running!"

def run_bot():
    # Skrip bot Anda akan berjalan di background
    pass

if __name__ == '__main__':
    # Jalankan bot di thread terpisah agar tidak memblokir server web
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=10000)