import os
import re
from pathlib import Path

def is_valid_directory(directory):
    """
    Mengecek apakah directory valid dan berisi file .sql
    
    Args:
        directory (str): Path directory yang akan dicek
    Returns:
        bool: True jika valid, False jika tidak
    """
    # Cek apakah path exists dan adalah directory
    if not os.path.exists(directory) or not os.path.isdir(directory):
        return False
    
    # Cek apakah ada file .sql
    sql_files = [f for f in os.listdir(directory) if f.endswith('.sql')]
    return len(sql_files) > 0

def rename_files(directory):
    """
    Fungsi untuk merename file sesuai format: XX. Nama_perubahan V1.1.sql
    Mempertahankan nomor urut di depan nama file.
    
    Args:
        directory (str): Path direktori yang berisi file-file yang akan direname
    """
    # Pattern untuk mencari nomor versi
    version_pattern = r'[vV]?\d+\.\d+'
    # Pattern untuk mencari nomor urut di awal nama
    sequence_pattern = r'^\d+\.'
    # Pattern untuk format nama yang benar
    valid_pattern = r'^\d+\.\s[\w_]+\sV\d+\.\d+\.sql$'
    
    # Hitung total file SQL
    sql_files = [f for f in os.listdir(directory) if f.endswith('.sql')]
    total_files = len(sql_files)
    processed_files = 0
    
    print(f"\nDitemukan {total_files} file SQL di directory {directory}")
    print("Memulai proses rename...\n")
    
    # Iterasi setiap file dalam direktori
    for filename in sql_files:
        # Cek apakah nama file sudah sesuai aturan
        if re.match(valid_pattern, filename):
            continue
        
        # Ambil nama dasar dan ekstensi
        base_name = os.path.splitext(filename)[0]
        
        # Cari nomor urut di awal nama
        sequence_match = re.match(sequence_pattern, base_name)
        sequence_num = sequence_match.group() if sequence_match else ""
        
        # Cari nomor versi dalam nama file
        version_match = re.search(version_pattern, filename)
        version = version_match.group() if version_match else "V1.0"
        
        # Hapus nomor urut dan versi dari nama dasar untuk diproses
        base_name = re.sub(sequence_pattern, '', base_name)
        base_name = re.sub(version_pattern, '', base_name)
        
        # Bersihkan spasi berlebih dan karakter khusus
        base_name = re.sub(r'[^\w\s-]', '', base_name)
        base_name = base_name.strip().replace(' ', '_')
        base_name = base_name.replace('-', '_')  # Ganti dash dengan underscore
        
        # Format nama baru dengan nomor urut di depan
        new_name = f"{sequence_num} {base_name} V{version.replace('v', '').replace('V', '')}.sql"
        
        # Path lengkap file lama dan baru
        old_file = os.path.join(directory, filename)
        new_file = os.path.join(directory, new_name)
        
        try:
            # Rename file
            os.rename(old_file, new_file)
            processed_files += 1
            print(f"[{processed_files}/{total_files}] Berhasil rename: {filename} -> {new_name}")
        except Exception as e:
            print(f"Error saat rename {filename}: {str(e)}")
    
    print(f"\nProses selesai! {processed_files} dari {total_files} file berhasil direname.")

def main():
    print("Program Rename File SQL")
    print("======================")
    
    while True:
        # Minta input directory dari user
        directory = input("\nMasukkan path directory (atau 'q' untuk keluar): ").strip()
        
        # Cek jika user ingin keluar
        if directory.lower() == 'q':
            print("Program selesai.")
            break
        
        # Ubah ke path absolut
        directory = os.path.abspath(directory)
        
        # Validasi directory
        if not is_valid_directory(directory):
            print("\nError: Directory tidak valid atau tidak berisi file SQL!")
            print("Pastikan:")
            print("1. Path directory benar")
            print("2. Directory berisi minimal 1 file .sql")
            continue
        
        # Konfirmasi dengan user
        print(f"\nDirectory yang dipilih: {directory}")
        confirm = input("Lanjutkan proses rename? (y/n): ").strip().lower()
        
        if confirm == 'y':
            rename_files(directory)
        else:
            print("Proses dibatalkan.")
        
        # Tanya apakah ingin melanjutkan dengan directory lain
        again = input("\nIngin memproses directory lain? (y/n): ").strip().lower()
        if again != 'y':
            print("Program selesai.")
            break

if __name__ == "__main__":
    main()
