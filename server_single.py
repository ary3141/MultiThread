import socket 
import os 
import time  

def handle_request(client_socket):  # Fungsi buat ngurusin permintaan dari klien
    request = client_socket.recv(1024).decode('utf-8')  # Baca data dari klien sampai 1024 byte, terus ubah jadi string
    print("Received request:")  # Tulis "Received request:" di konsol
    #print(request)  # Tunjukin permintaan yang diterima

    # Simulasi delay
    time.sleep(2)  # Tunggu 2 detik

    # Parsing header HTTP
    headers = request.split('\n')  # Bagi permintaan jadi beberapa baris
    filename = headers[0].split()[1]  # Ambil nama file yang diminta dari baris pertama

    # Hapus garis miring di depan nama file
    if filename == '/':  # Kalau nama file-nya '/'
        filename = 'index.html'  # Ganti jadi 'index.html'
    else:
        filename = filename[1:]  # Kalau enggak, hapus garis miring di depan

    try:
        # Buka dan baca file yang diminta
        with open(filename, 'rb') as fin:  # Buka file dalam mode baca biner
            content = fin.read()  # Baca isi file

        # Bikin respon HTTP
        print('HTTP/1.1 200 OK')
        response = 'HTTP/1.1 200 OK\r\n\r\n'.encode('utf-8') + content  # Bikin respon HTTP 200 OK dan tambahin isi file

    except FileNotFoundError:  # Kalau file-nya enggak ketemu
        # Kirim respon HTTP 404 kalau file enggak ketemu
        print('HTTP/1.1 404 Not Found')
        print('File Not Found')
        response = 'HTTP/1.1 404 Not Found\r\n\r\nFile Not Found'.encode('utf-8')  # Bikin respon HTTP 404 Not Found

    # Kirim respon ke klien
    client_socket.sendall(response)  # Kirim semua respon ke klien
    client_socket.close()  # Tutup koneksi sama klien

def main():  # Fungsi utama
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Bikin socket server pakai IPv4 dan TCP
    server_socket.bind(('0.0.0.0', 6789))  # Ikat socket ke IP 0.0.0.0 dan port 6789
    server_socket.listen(1)  # Bikin socket siap dengerin koneksi masuk, maksimal 1 antrian
    print("Listening on port 6789...")  # Tulis "Listening on port 6789..." di konsol

    while True:  # Loop buat nerima koneksi klien
        client_socket, addr = server_socket.accept()  # Terima koneksi klien
        print("Accepted connection from {}".format(addr))  # Tulis alamat klien yang terhubung
        handle_request(client_socket)  # Panggil fungsi handle_request buat ngurusin permintaan klien

if __name__ == "__main__":  # Cek kalau skrip dijalankan sebagai program utama
    main()  # Panggil fungsi utama
