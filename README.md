# inscribe-sui

# Tutorial Penggunaan suibot.py

Selamat datang di tutorial penggunaan suibot.py! Dalam tutorial ini, kita akan membahas langkah-langkah untuk menggunakan skrip suibot.py untuk melakukan minting pada jaringan blockchain Sui.

## Langkah 1: Persiapkan Lingkungan Pengembangan

Pastikan bahwa Anda telah memenuhi persyaratan lingkungan pengembangan yang dibutuhkan. Berikut beberapa hal yang perlu dipersiapkan:

1. Instal Python: Pastikan Python sudah terinstal di komputer Anda. Jika belum, unduh dan instal Python dari [python.org](https://www.python.org/).

2. Instal Dependencies: Instal semua dependencies yang dibutuhkan dengan menjalankan perintah berikut di terminal:


       pip install pysui
   
Beberapa hal yang dapat Anda coba:

Coba lagi: Terkadang, timeout terjadi karena gangguan jaringan atau kelebihan beban pada server. Coba lagi setelah beberapa saat.

Ganti Server Miror PyPI: Bisa jadi server PyPI yang Anda gunakan saat ini mengalami masalah. Anda dapat mengganti server miror PyPI dengan yang lain. Anda dapat mengatur server miror menggunakan opsi -i atau --index-url. Misalnya:



     pip install -i https://pypi.org/simple/ pysui

Perbarui pip: Pastikan Anda menggunakan versi pip terbaru. Perbarui pip dengan perintah:


    pip install --upgrade pip

Unduh dan Instal Manual: Unduh paket pysui dan dependensinya secara manual dari PyPI, lalu instal menggunakan perintah lokal. Contohnya:



    pip download pysui
    pip install --no-index --find-links=/path/to/downloaded/wheels pysui

Langkah 2: Konfigurasi Kunci dan Alamat
Isi file suibot.py dengan kunci pribadi dan alamat yang sesuai pada bagian berikut:

python


    keys = [
    {
    'key': 'private_key_1',
    'address': '0x1234567890abcdefABCDEF1234567890abcdefAB'
    },
    # Tambahkan kunci dan alamat lainnya jika diperlukan
    ]

jika terdapat error tambahkan 0x 
contoh:2914awdwa2v1v1v2
menjadi:0x2914awdwa2v1v1v2

Langkah 3: Konfigurasi Node Blockchain
Pastikan untuk mengganti URL node blockchain sesuai dengan yang tersedia:

python
Copy code

    rpc_url = "https://sui-rpc.publicnode.com"
    ws_url = "wss://sui-rpc.publicnode.com/websocket"
    
Langkah 4: Inisialisasi dan Jalankan suibot.py
Jalankan skrip suibot.py dan lihat apakah semuanya berjalan dengan lancar:


    python suibot.py
    
Langkah 5: Observasi dan Pantau
Biarkan skrip berjalan dan observasi outputnya. Pastikan untuk memonitor log atau pesan kesalahan jika ada.

Selamat! Anda sekarang telah berhasil menggunakan suibot.py untuk melakukan minting pada jaringan blockchain Sui. Jangan ragu untuk berkontribusi, memberikan umpan balik, atau melaporkan masalah.

Terima kasih telah mengikuti tutorial ini!

Pastikan untuk menyesuaikan tutorial ini sesuai dengan kebutuhan skrip Anda dan memberikan informasi yang cukup untuk pengguna yang ingin menggunakannya. Semoga tutorial ini membantu!
