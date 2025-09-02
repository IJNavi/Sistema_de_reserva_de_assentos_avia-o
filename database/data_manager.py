import json
import threading
from pathlib import Path


class DataManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.data_file = Path('database/dados.json')
        self.data = self._carregar_dados()

    def _carregar_dados(self):
        if self.data_file.exists():
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {
            'passageiros': {},
            'voos': {},
            'reservas': {}
        }

    def salvar_dados(self):
        with self._lock:
            with open(self.data_file, 'w') as f:
                json.dump(self.data, f, indent=2)

    def get_passageiro(self, cpf):
        return self.data['passageiros'].get(cpf)

    def add_passageiro(self, passageiro):
        self.data['passageiros'][passageiro.cpf] = passageiro.to_dict()
        self.salvar_dados()

    def get_voo(self, numero_voo):
        return self.data['voos'].get(numero_voo)

    def add_voo(self, voo):
        self.data['voos'][voo.numero] = voo.to_dict()
        self.salvar_dados()

    def get_reserva(self, cpf, numero_voo):
        return self.data['reservas'].get(f"{cpf}_{numero_voo}")

    def add_reserva(self, cpf, numero_voo, numero_assento):
        self.data['reservas'][f"{cpf}_{numero_voo}"] = {
            'cpf': cpf,
            'numero_voo': numero_voo,
            'numero_assento': numero_assento
        }
        self.salvar_dados()

    def remove_reserva(self, cpf, numero_voo):
        key = f"{cpf}_{numero_voo}"
        if key in self.data['reservas']:
            del self.data['reservas'][key]
            self.salvar_dados()