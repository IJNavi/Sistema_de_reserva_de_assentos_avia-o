import threading
import logging
from getpass import getpass
from database.data_manager import DataManager
from utils.logger import Logger
from utils.validators import validar_cpf, validar_email, calcular_idade
from entities.passageiro import Passageiro
from entities.voo import Voo


class CLIInterface:
    def __init__(self):
        self.data_manager = DataManager()
        self.logger = Logger()
        self.usuario_logado = None
        self.lock = threading.Lock()

    def menu_principal(self):
        while True:
            print("\n=== Sistema de Reservas Aéreas ===")
            print("1. Login")
            print("2. Cadastrar")
            print("3. Sair")

            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                self.login()
            elif opcao == '2':
                self.cadastrar_passageiro()
            elif opcao == '3':
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida!")

    def cadastrar_passageiro(self):
        print("\n=== Cadastro de Passageiro ===")

        cpf = input("CPF: ")
        cpf_validado = validar_cpf(cpf)
        if not cpf_validado:
            print("CPF inválido!")
            return

        if self.data_manager.get_passageiro(cpf_validado):
            print("CPF já cadastrado!")
            return

        nome = input("Nome completo: ")
        data_nascimento = input("Data de nascimento (DD/MM/AAAA): ")
        email = input("E-mail: ")

        if not validar_email(email):
            print("E-mail inválido!")
            return

        passageiro = Passageiro(cpf_validado, nome, data_nascimento, email)
        self.data_manager.add_passageiro(passageiro)
        self.logger.log(logging.INFO, f"Novo passageiro cadastrado: {nome}", cpf_validado)
        print("Cadastro realizado com sucesso!")

    def login(self):
        print("\n=== Login ===")
        cpf = input("CPF: ")
        cpf_validado = validar_cpf(cpf)

        if not cpf_validado:
            print("CPF inválido!")
            return

        passageiro_data = self.data_manager.get_passageiro(cpf_validado)
        if not passageiro_data:
            print("Passageiro não encontrado!")
            return

        self.usuario_logado = Passageiro.from_dict(passageiro_data)
        self.logger.log(logging.INFO, "Login realizado", self.usuario_logado.cpf)
        self.menu_usuario()

    def menu_usuario(self):
        while self.usuario_logado:
            print(f"\n=== Bem-vindo, {self.usuario_logado.nome} ===")
            print("1. Visualizar voos")
            print("2. Visualizar assentos de um voo")
            print("3. Fazer reserva")
            print("4. Cancelar reserva")
            print("5. Modificar reserva")
            print("6. Logout")

            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                self.visualizar_voos()
            elif opcao == '2':
                self.visualizar_assentos()
            elif opcao == '3':
                self.fazer_reserva()
            elif opcao == '4':
                self.cancelar_reserva()
            elif opcao == '5':
                self.modificar_reserva()
            elif opcao == '6':
                self.logger.log(logging.INFO, "Logout", self.usuario_logado.cpf)
                self.usuario_logado = None
            else:
                print("Opção inválida!")

    def visualizar_voos(self):
        print("\n=== Voos Disponíveis ===")
        voos = self.data_manager.data['voos']
        for numero, voo_data in voos.items():
            print(f"Voo {numero}: {voo_data['origem']} -> {voo_data['destino']} - {voo_data['data_hora']}")

    def visualizar_assentos(self):
        numero_voo = input("Número do voo: ")
        voo_data = self.data_manager.get_voo(numero_voo)

        if not voo_data:
            print("Voo não encontrado!")
            return

        voo = Voo.from_dict(voo_data)
        self._mostrar_mapa_assentos(voo)

    def _mostrar_mapa_assentos(self, voo):
        print(f"\n=== Mapa de Assentos - Voo {voo.numero} ===")
        print("Legenda: [ ] Disponível  [X] Ocupado  [*] Sua reserva  [E] Emergência")

        assentos_por_fileira = voo.aeronave['configuracao'][1]
        fileiras = sorted(set(int(num[:-1]) for num in voo.assentos.keys()))

        for fileira in fileiras:
            linha = f"{fileira:2d} "
            for letra in 'ABCDEF'[:assentos_por_fileira]:
                numero_assento = f"{fileira}{letra}"
                assento = voo.assentos[numero_assento]

                if assento.passageiro_cpf == self.usuario_logado.cpf:
                    simbolo = "[*]"
                elif not assento.disponivel:
                    simbolo = "[X]"
                elif assento.emergencia:
                    simbolo = "[E]"
                else:
                    simbolo = "[ ]"

                linha += f"{simbolo} "
            print(linha)

    def fazer_reserva(self):
        numero_voo = input("Número do voo: ")
        voo_data = self.data_manager.get_voo(numero_voo)

        if not voo_data:
            print("Voo não encontrado!")
            return

        # Verificar se já tem reserva
        if self.data_manager.get_reserva(self.usuario_logado.cpf, numero_voo):
            print("Você já possui uma reserva neste voo!")
            return

        voo = Voo.from_dict(voo_data)
        self._mostrar_mapa_assentos(voo)

        numero_assento = input("Número do assento desejado (ex: 1A): ").upper()

        if numero_assento not in voo.assentos:
            print("Assento inválido!")
            return

        assento = voo.assentos[numero_assento]

        with self.lock:  # Controle de concorrência
            if not assento.disponivel:
                print("Assento já ocupado!")
                return

            # Verificar restrição de idade para saída de emergência
            if assento.emergencia:
                idade = calcular_idade(self.usuario_logado.data_nascimento)
                if idade < 18:
                    print("Menores de 18 anos não podem reservar assentos de emergência!")
                    return

            # Fazer reserva
            assento.reservar(self.usuario_logado.cpf)
            self.data_manager.add_reserva(self.usuario_logado.cpf, numero_voo, numero_assento)
            self.data_manager.add_voo(voo)  # Atualiza os assentos no voo

            self.logger.log(logging.INFO,
                            f"Reserva realizada - Voo: {numero_voo}, Assento: {numero_assento}",
                            self.usuario_logado.cpf)
            print("Reserva realizada com sucesso!")

    def cancelar_reserva(self):
        numero_voo = input("Número do voo: ")
        reserva = self.data_manager.get_reserva(self.usuario_logado.cpf, numero_voo)

        if not reserva:
            print("Reserva não encontrada!")
            return

        voo_data = self.data_manager.get_voo(numero_voo)
        voo = Voo.from_dict(voo_data)
        assento = voo.assentos[reserva['numero_assento']]

        with self.lock:
            assento.liberar()
            self.data_manager.remove_reserva(self.usuario_logado.cpf, numero_voo)
            self.data_manager.add_voo(voo)

            self.logger.log(logging.INFO,
                            f"Reserva cancelada - Voo: {numero_voo}, Assento: {reserva['numero_assento']}",
                            self.usuario_logado.cpf)
            print("Reserva cancelada com sucesso!")

    def modificar_reserva(self):
        numero_voo = input("Número do voo: ")
        reserva = self.data_manager.get_reserva(self.usuario_logado.cpf, numero_voo)

        if not reserva:
            print("Reserva não encontrada!")
            return

        # Primeiro cancela a reserva atual
        voo_data = self.data_manager.get_voo(numero_voo)
        voo = Voo.from_dict(voo_data)
        assento_antigo = voo.assentos[reserva['numero_assento']]

        with self.lock:
            assento_antigo.liberar()

            # Mostra assentos disponíveis
            self._mostrar_mapa_assentos(voo)

            numero_novo_assento = input("Número do novo assento: ").upper()

            if numero_novo_assento not in voo.assentos:
                print("Assento inválido!")
                return

            novo_assento = voo.assentos[numero_novo_assento]

            if not novo_assento.disponivel:
                print("Assento já ocupado!")
                return

            # Verificar restrição de idade para saída de emergência
            if novo_assento.emergencia:
                idade = calcular_idade(self.usuario_logado.data_nascimento)
                if idade < 18:
                    print("Menores de 18 anos não podem reservar assentos de emergência!")
                    return

            # Fazer nova reserva
            novo_assento.reservar(self.usuario_logado.cpf)
            self.data_manager.add_reserva(self.usuario_logado.cpf, numero_voo, numero_novo_assento)
            self.data_manager.add_voo(voo)

            self.logger.log(logging.INFO,
                            f"Reserva modificada - De: {reserva['numero_assento']} Para: {numero_novo_assento}",
                            self.usuario_logado.cpf)
            print("Reserva modificada com sucesso!")