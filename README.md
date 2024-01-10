# URL Status Checker

URL Status Checker adalah alat sederhana untuk memeriksa status respons dari sejumlah URL. Alat ini memudahkan pengecekan status url ketika kita sedang melakukan proses bug hunting & Alat ini juga bisa di kombinasikan  untuk memeriksa semua list url yang telah di dapat dari Waybacksurls Tools [https://github.com/username/repo/blob/main/documentation.md](https://www.geeksforgeeks.org/waybackurls-fetch-all-the-urls-that-the-wayback-machine-knows-about-for-a-domain).
 , memberikan kemampuan untuk memeriksa sejumlah URL dengan cepat.

## Instalasi

1. Pastikan Python telah terinstal di sistem Anda.
2. Clone repositori ini atau unduh file [url_status_checker.py](url_status_checker.py).
3. Install dependensi dengan menjalankan perintah berikut:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Options
- `-f, --file`: Nama file input yang berisi daftar URL.
- `-u, --urls`: Daftar URL (dipisahkan spasi) jika tidak menggunakan file.
- `-o, --output`: Nama file output untuk menyimpan hasil status respons.
- `-r, --response-codes`: Kode respons yang ingin disertakan (dipisahkan spasi).
- `-v, --verbose`: Mode verbose untuk mencetak informasi lebih lanjut.
- `-ts, --time-sec`: Timeout dalam detik untuk setiap permintaan.

### Example Usage

1. Pemeriksaan URL dari file:

    ```bash
    python url_status_checker.py -f urls.txt -o output.txt -r 200 404 -v
    ```

2. Pemeriksaan URL langsung:

    ```bash
    python url_status_checker.py -u https://example.com https://example.org -o output.txt
    ```

3. Menampilkan bantuan:

    ```bash
    python url_status_checker.py --help
    ```

## Catatan

- Pastikan untuk memasang dependensi yang diperlukan dengan menjalankan perintah instalasi di atas.
- Gunakan opsi `-h` atau `--help` untuk mendapatkan bantuan terkait penggunaan.

