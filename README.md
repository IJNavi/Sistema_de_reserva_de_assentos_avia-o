# Sistema de Reserva de Assentos A�reos

Sistema de reservas para companhia a�rea fict�cia desenvolvido em Python com orienta��o a objetos.

## ?? Funcionalidades

- Cadastro e login de passageiros
- Visualiza��o de voos dispon�veis
- Mapa interativo de assentos com legendas
- Reserva, cancelamento e modifica��o de assentos
- Controle de restri��es (idade para assentos de emerg�ncia)
- Sistema de logs de todas as opera��es
- Persist�ncia de dados em JSON
- Controle de concorr�ncia para m�ltiplos usu�rios

## ??? Tecnologias

- Python 3.x (compat�vel com Python 2)
- M�dulos padr�o: json, threading, logging, re, datetime
- Paradigma de orienta��o a objetos
- Interface de linha de comando (CLI)

## ?? Estrutura do Projeto

```
sistema_reservas/
??? main.py
??? entities/
?   ??? passageiro.py
?   ??? voo.py
?   ??? assento.py
??? database/
?   ??? data_manager.py
?   ??? dados.json
??? utils/
?   ??? logger.py
?   ??? validators.py
??? interface/
    ??? cli.py
```

## ?? Como Executar

```bash
# Clone o reposit�rio
git clone <url-do-repositorio>

# Execute o programa
python main.py
```

## ?? Requisitos Atendidos

- [x] Cadastro de passageiros com valida��o
- [x] Visualiza��o de assentos por voo
- [x] Reserva com controle de concorr�ncia
- [x] Restri��o para menores em assentos de emerg�ncia
- [x] Sistema de logging completo
- [x] Persist�ncia de dados
- [x] Interface CLI funcional

## ?? Multiplataforma

O sistema funciona tanto em **Windows** quanto em **Linux**, utilizando apenas bibliotecas padr�o do Python.

## ?? Licen�a

Este projeto foi desenvolvido para fins acad�micos.