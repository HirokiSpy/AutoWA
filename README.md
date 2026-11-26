# AutoWA

AutoWA ialah aplikasi desktop ringkas berasaskan Python untuk menjadualkan penghantaran **satu mesej WhatsApp** kepada nombor telefon atau kumpulan pada waktu tertentu. Antara muka menggunakan Bahasa Melayu dan dibina dengan Tkinter.

> Gunakan aplikasi ini hanya untuk komunikasi yang sah dan kepada penerima yang bersetuju menerima mesej daripada anda. Elakkan spam, mesej pukal, atau penggunaan yang melanggar syarat WhatsApp.

## Ciri-ciri

- Menjadualkan mesej kepada nombor telefon antarabangsa atau kumpulan WhatsApp.
- Memasukkan waktu dalam format 12 jam (AM/PM), sama ada menaip atau memilih daripada senarai.
- Melihat kira detik dan membatalkan jadual sebelum penghantaran bermula.
- Menggunakan WhatsApp Web melalui Google Chrome dengan bantuan `pywhatkit`.

## Keperluan

- Python **3.10 atau lebih baharu**.
- Google Chrome dipasang pada komputer.
- Akaun WhatsApp yang boleh digunakan dengan WhatsApp Web.
- Pakej Python dalam `requirements.txt`.
- Tkinter, yang biasanya disertakan bersama Python. Pada sesetengah distro Linux, pasang pakej sistem `python3-tk` jika Tkinter tiada.

## Pemasangan dan penggunaan

1. Klon repositori dan masuk ke direktori projek:

   ```bash
   git clone https://github.com/HirokiSpy/AutoWA.git
   cd AutoWA
   ```

2. (Disyorkan) Cipta dan aktifkan persekitaran maya:

   **Windows (PowerShell):**
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   **macOS / Linux:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Pasang kebergantungan:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Jalankan aplikasi:

   ```bash
   python AutoWA.py
   ```

5. Pilih jenis sasaran, masukkan nombor telefon lengkap dengan kod negara (contohnya `+60123456789`) atau maklumat kumpulan, taip mesej, tetapkan waktu, kemudian tekan **Mula Jadual**.

Pastikan WhatsApp Web boleh dibuka dan akaun anda telah log masuk apabila tiba waktu penghantaran. Jika perlu, log masuk secara manual dalam Chrome terlebih dahulu.

## Nota penting

- Aplikasi dan komputer mesti kekal hidup sehingga waktu yang dijadualkan. Jadual tidak disimpan selepas aplikasi ditutup.
- Jika waktu yang dipilih sudah berlalu pada hari ini, aplikasi menjadualkannya untuk hari berikutnya.
- Pembatalan tersedia sebelum proses penghantaran bermula; penghantaran yang sudah dimulakan tidak boleh dibatalkan melalui aplikasi.
- Selepas penghantaran berjaya, kod aplikasi cuba menutup Chrome. Pada Windows dan Linux, arahan yang digunakan boleh menutup **semua proses Chrome** yang sedang berjalan. Simpan kerja dalam Chrome sebelum menggunakan AutoWA.
- Penghantaran bergantung pada sambungan internet, keadaan WhatsApp Web, dan tingkah laku `pywhatkit`; penghantaran tidak dijamin.
- Aplikasi ini tidak mengesahkan kebenaran penerima atau kesahihan nombor/ID kumpulan. Semak maklumat sasaran sebelum menjadualkan.

## Penyelesaian masalah

- **Tkinter tidak ditemui:** pasang sokongan Tkinter untuk pemasangan Python anda. Pada Ubuntu/Debian, biasanya `sudo apt install python3-tk`.
- **Chrome atau WhatsApp Web tidak dapat dibuka:** pastikan Chrome dipasang, sambungan internet tersedia, dan anda telah log masuk ke WhatsApp Web.
- **Ralat kebergantungan:** aktifkan persekitaran maya yang betul dan jalankan semula `python -m pip install -r requirements.txt`.

## Kebergantungan

- [`pywhatkit`](https://github.com/Ankit404butfound/PyWhatKit) — automasi WhatsApp Web.
- Tkinter — antara muka grafik (pustaka standard Python, tertakluk pada pakej sistem).

## Lesen

Repositori ini belum menyatakan lesen. Sehingga lesen ditambah, tiada kebenaran penggunaan semula atau pengedaran yang diberikan secara tersirat.
