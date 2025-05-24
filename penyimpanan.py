from abc import ABC, abstractmethod
import os
from datetime import datetime

class IPenyimpanan(ABC):
    @abstractmethod
    def tambah_transaksi(self, jumlah: float, tipe_transaksi: str, keterangan: str):
        pass
    
    @abstractmethod
    def get_saldo(self) -> float:
        pass
    
    @abstractmethod
    def get_transaksi(self) -> str:
        pass

class Penyimpanan(IPenyimpanan):
    def __init__(self, nama: str):
        self.nama = nama
        self.nama_file = f"keuangan_{nama.lower()}.txt"
        self.saldo = self._muat_saldo()
        
        # Buat file jika belum ada
        if not os.path.exists(self.nama_file):
            with open(self.nama_file, 'w') as f:
                pass
    
    def _muat_saldo(self) -> float:
        """Load saldo from transaction file"""
        try:
            if not os.path.exists(self.nama_file):
                return 0.0
                
            with open(self.nama_file, 'r') as f:
                lines = f.readlines()
                if not lines:
                    return 0.0
                    
                saldo = 0.0
                for line in lines:
                    if line.strip():
                        try:
                            parts = line.strip().split('|')
                            tipe = parts[1]
                            jumlah = float(parts[2].replace(',', '').replace('Rp ', ''))
                            
                            if tipe == "masuk":
                                saldo += jumlah
                            elif tipe == "keluar":
                                saldo -= jumlah
                        except (IndexError, ValueError) as e:
                            print(f"Error parsing line {line}: {e}")  # Debug print
                            continue
                            
                return saldo
        except Exception as e:
            print(f"Error reading file {self.nama_file}: {e}")  # Debug print
            return 0.0
    
    def get_saldo(self) -> float:
        """Dapatkan saldo terkini"""
        return self._muat_saldo()  # Selalu hitung ulang dari file
        
    def tambah_transaksi(self, jumlah: float, tipe_transaksi: str, keterangan: str):
        if tipe_transaksi not in ["masuk", "keluar"]:
            raise ValueError("Tipe transaksi harus 'masuk' atau 'keluar'")
        
        if jumlah <= 0:
            raise ValueError("Jumlah harus lebih dari 0")
            
        saldo_baru = self.saldo + jumlah if tipe_transaksi == "masuk" else self.saldo - jumlah
        tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(self.nama_file, 'a') as f:
            f.write(f"{tanggal}|{tipe_transaksi}|{jumlah:,.2f}|{keterangan}|{saldo_baru:,.2f}\n")
            
        self.saldo = saldo_baru
    
    def get_transaksi(self) -> str:
        try:
            if not os.path.exists(self.nama_file):
                return ""
                
            with open(self.nama_file, 'r') as f:
                return f.read()
        except Exception as e:
            raise ValueError(f"Error membaca transaksi: {str(e)}")