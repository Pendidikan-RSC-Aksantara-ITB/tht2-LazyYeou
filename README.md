[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/VGGaLmn4)
# THT2_2026

*You know the drill* lah ya. Aturan secara umum masih sama seperti THT 1, dengan beberapa penyesuaian. Kebijakan terkait penggunaan AI masih tetap sama.

## Ketentuan Umum

1. Yaudah kerjain aja, smngt (ez lah kalian jago semua kok)
2. Log progres pengerjaan digabung di Technical Journal aja.
3. Kerjakan nomor ke-`i` di dalam folder `src/i/`.

## Soal

### 1. Tentang Diri dan RSC (??? poin)

#### a. Esai

Buatlah esai minimal 350 kata mengenai dirimu tentang *passion*-mu dalam sains dan teknologi serta apa yang membawamu ke RSC Aksantara ITB. Jelaskan juga rencanamu jika lolos seleksi dan resmi menjadi bagian dari Aksantara ITB. Esai harus ditulis dengan $\LaTeX$ dengan menyertakan file kode sumber (`.tex`) di dalam folder yang sesuai beserta PDF hasil kompilasinya. Dilarang keras menggunakan AI, akan dicek dengan berbagai kakas *AI checker*.

#### b. Meme

Buatlah sebuah meme karya orisinal sendiri terkait RSC, Aksantara, atau boleh juga tentang ITB *in general*, lalu kirimkan meme-nya ke grup Ca-Aksantara 2026 beserta kata-kata penyemangat minimal 2 kalimat untuk Ca-Aksantara lainnya. Makin gacor makin tinggi nilainya. Cukup cantumkan meme-nya saja di folder yang sesuai.

#### c. Diskusi

Diskusikan salah satu soal dari THT 2 ini di grup Ca-RSC Aksantara ITB 2026. Ambil screenshot diskusi tersebut dan cantumkan di folder yang sesuai.

### 2. GCS (45 poin)

#### A. SPA (5 poin)

Jelaskan apa itu SPA (Single Page Application) dan bagaimana SPA berbeda dari aplikasi web tradisional? Sebutkan juga beberapa keuntungan dan kerugian menggunakan SPA dalam pengembangan web.

#### B. Service dalam Backend (5 poin)

Jelaskan apa itu Service dalam konteks Backend (misalnya Flask/FastAPI), dan bagaimana service membantu modularitas dalam pengembangan backend?

#### C. Implementasi GCS (35 poin)

Buatlah sebuah aplikasi GCS (Ground Control Station) sederhana untuk manajemen waypoint.

##### Spesifikasi Teknologi

- **Backend**: Golang dengan framework Gin, Echo, atau Fiber
- **Database**: SQLite
- **Frontend**: Svelte/SvelteKit
- **Containerization**: Frontend dan Backend harus di-*containerize* menggunakan Docker dan dikelola menggunakan Docker Compose.

##### Deskripsi Fitur

###### A. Tampilan peta full-window

- Aplikasi menampilkan peta full-window menggunakan pustaka Leaflet.js atau Mapbox GL JS.
- Waypoint ditampilkan sebagai marker SVG kustom dari [logo Aksantara ITB](./aksantara.svg) di peta.

###### B. Manajemen Waypoint

- Aplikasi menampilkan floating sidebar yang berisi daftar waypoint yang telah dibuat.
- Pengguna dapat menambahkan waypoint dengan mengklik pada peta. Setiap waypoint harus memiliki ID unik, koordinat (latitude dan longitude), ketinggian, dan nama yang dapat diedit.
- Tiap item waypoint di sidebar memiliki tombol untuk mengedit nama waypoint dan menghapus waypoint.
- Terdapat tombol "save" di sidebar untuk menyimpan semua waypoint ke database SQLite melalui API backend.

###### C. Validasi dan Error Handling
- Latitude harus berada di rentang -90 hingga 90,
- longitude harus berada di rentang -180 hingga 180, 
- ketinggian harus berupa angka positif,
- nama waypoint tidak boleh kosong.
- Tampilkan pesan error yang sesuai di UI jika ada input yang tidak valid.
- Tampilkan pesan konfirmasi saat waypoint berhasil ditambahkan, diedit, dihapus, atau disimpan.

##### Pengumpulan

Cukup cantumkan file kode sumber di dalam folder yang sesuai beserta screenshot aplikasi yang sedang berjalan.

### 3. Path Planning dan Swarm Control (45 poin)

#### A. Penjelasan (10 poin)

<ol type="a">
<li> (5 poin) Jelaskan konsep dasar dari Artificial Potential Field (APF) dalam konteks navigasi robot. Sertakan penjelasan tentang bagaimana gaya tarik dan tolak bekerja dalam metode ini dan sertakan ilustrasi atau diagram yang digambar sendiri di kertas atau papan tulis digital.</li>
<li> (5 poin) Jelaskan perbedaan antara Uniform Cost Search (UCS), Greedy Best First Search (GBFS), dan A* Search dalam konteks algoritma pencarian jalur. Sertakan kelebihan dan kekurangan masing-masing algoritma serta situasi di mana masing-masing algoritma lebih cocok digunakan.</li>
</ol>

#### B. Implementasi (35 poin)

Perhatikan [paper ini](https://informatika.stei.itb.ac.id/~rinaldi.munir/Stmik/2024-2025/Makalah2025/Makalah-IF2211-Strategi-Algoritma-2025%20(96).pdf). Gunakan algoritma *swarming* yang dijelaskan di dalamnya untuk mengimplementasikan simulasi robot swarm di lingkungan 2D dengan pustaka Pygame. Mulanya robot-robot akan ditempatkan secara acak di dalam area tertentu (mis. 100 x 200 piksel di pojok kiri atas jendela Pygame) dan memiliki tujuan untuk mencapai target titik tertentu (mis. di pojok kanan bawah jendela Pygame). Bentuk rintangan dan cara penempatan rintangan dapat ditentukan sendiri (fixed atau random). Asumsikan robot-robot tersebut dapat berkomunikasi satu sama lain untuk berbagi informasi tentang posisi satu sama lain dan rintangan di sekitarnya. Asumsikan juga kondisi lingkungan statis (rintangan tidak bergerak) dan sepenuhnya diketahui oleh semua robot. Simulasi harus menampilkan pergerakan robot secara real-time di jendela Pygame.

Cukup cantumkan file kode sumber di dalam folder yang sesuai beserta GIF hasil rekaman simulasi (bisa dari screen recorder seperti OBS Studio atau lainnya). Detail implementasi yang tidak dijelaskan di sini dapat diasumsikan sendiri selama sesuai dengan konsep dasar yang dijelaskan di dalam paper.

### 4. System Design untuk Robot Swarm (15 poin)

Rancanglah *class diagram* dari *backend* suatu GCS (Ground Control Station) yang dapat mengelola dan memantau sekumpulan robot swarm. Robot-robot ini memiliki kemampuan untuk berkomunikasi satu sama lain dan dengan GCS. GCS harus mampu menerima data posisi, status kesehatan, dan informasi sensor dari setiap robot secara real-time. Selain itu, GCS juga harus dapat mengirim perintah navigasi ke robot-robot tersebut berdasarkan data yang diterima. Tiap robot memiliki ID unik, posisi (koordinat x, y), status kesehatan (misalnya: normal, peringatan, kritis), dan data sensor (misalnya: jarak ke rintangan terdekat, kecepatan, bebas lah suka-suka kalian). GCS harus mampu menampilkan peta area operasi dengan posisi real-time dari setiap robot serta status kesehatannya. Gunakan notasi UML untuk membuat *class diagram* tersebut.

Untuk soal ini Anda wajib menggunakan Draw.io (diakses melalui <https://app.diagrams.net/>) untuk membuat *class diagram*-nya. Setelah selesai, cukup kumpulkan file `.drawio`-nya di dalam folder yang sesuai.

### 5. Georeferencing (15 poin)

Salah satu contoh misi dalam UAV yang pernah dilakukan oleh Aksantara ITB adalah simulasi *search and rescue* dengan memodelkan korban bencana sebagai terpal yang kemudian dideteksi menggunakan kamera. Dari situ, didapatkan koordinat piksel dari citra kamera UAV. Georeferencing adalah proses mengaitkan koordinat piksel tersebut ke koordinat geografis di permukaan bumi (misalnya, lintang dan bujur).

Misalkan wahana UAV terbang di atas area datar dengan ketinggian tetap `h` meter di atas permukaan bumi. Kamera UAV memiliki sudut pandang (field of view) `FOV` derajat dan resolusi citra `W x H` piksel. Asumsikan kamera menghadap lurus ke bawah (nadir). Dengan trigonometri dan matematika SMA, hitunglah koordinat geografis `(lat, lon)` dari piksel `(x, y)` pada citra kamera dan gambarkan ilustrasi sederhana yang menjelaskan proses perhitungan tersebut (tanpa ilustrasi tidak dinilai).

Jawaban ditulis tangan di kertas atau papan tulis digital, difoto, lalu dimasukkan ke dalam folder yang sesuai.
