from typing import Dict, List, Tuple
from models.penyimpanan import Penyimpanan
from models.penyimpanan_factory import PenyimpananFactory
from views.keuangan_view import KeuanganView

class PengelolaKeuangan:
    def __init__(self):
        # Initialize storage
        self.penyimpanan = PenyimpananFactory.create_all_storage()
        self.view = KeuanganView()
        self._setup_callbacks()
    
    def _setup_callbacks(self):
        self.view.set_callbacks(
            self.proses_tambah_transaksi,
            self.get_semua_saldo,
            self.get_transaksi
        )
    
    def proses_tambah_transaksi(self, jenis: str, jumlah: float, tipe: str, keterangan: str):
        try:
            if jenis not in self.penyimpanan:
                raise ValueError("Jenis penyimpanan tidak valid!")
                
            penyimpanan = self.penyimpanan[jenis]
            if not keterangan.strip():
                keterangan = "-"
                
            penyimpanan.tambah_transaksi(jumlah, tipe, keterangan)
            return True
            
        except Exception as e:
            raise ValueError(f"Error menambah transaksi: {str(e)}")
    
    def get_semua_saldo(self) -> List[Tuple[str, float]]:
        """Get saldo from all storage types"""
        try:
            result = []
            for nama, penyimpanan in self.penyimpanan.items():
                # Ensure saldo is loaded from file
                penyimpanan.saldo = penyimpanan._muat_saldo()
                result.append((nama, penyimpanan.saldo))
            return result
        except Exception as e:
            print(f"Error loading saldo: {e}")  # Debug print
            return [("Tunai", 0.0), ("Bank", 0.0), ("Dompet-Digital", 0.0)]
    
    def get_transaksi(self, jenis: str) -> str:
        try:
            if jenis not in self.penyimpanan:
                raise ValueError("Jenis penyimpanan tidak valid!")
            return self.penyimpanan[jenis].get_transaksi()
        except Exception as e:
            raise ValueError(f"Error mengambil transaksi: {str(e)}")