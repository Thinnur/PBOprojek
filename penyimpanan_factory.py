from typing import Dict
from models.penyimpanan import Penyimpanan

class PenyimpananFactory:
    @staticmethod
    def create_storage(nama: str) -> Penyimpanan:
        return Penyimpanan(nama)
    
    @staticmethod
    def create_all_storage() -> dict:
        return {
            "Tunai": PenyimpananFactory.create_storage("Tunai"),
            "Bank": PenyimpananFactory.create_storage("Bank"),
            "Dompet-Digital": PenyimpananFactory.create_storage("Dompet-Digital")
        }