# Sistema de Reserva de Assentos Aéreos

Sistema de reservas para companhia aérea fictícia desenvolvido em Python com orientação a objetos.

## 🚀  Funcionalidades

- Cadastro e login de passageiros
- Visualização de voos disponíveis
- Mapa interativo de assentos com legendas
- Reserva, cancelamento e modificação de assentos
- Controle de restrições (idade para assentos de emergência)
- Sistema de logs de todas as operações
- Persistência de dados em JSON
- Controle de concorrência para múltiplos usuários

## 🛠️ Tecnologias

- Python 3.x (compatível com Python 2)
- Módulos padrão: json, threading, logging, re, datetime
- Paradigma de orientação a objetos
- Interface de linha de comando (CLI)

## 📦 Estrutura do Projeto

```
sistema_reservas/
├── main.py
├── entities/
│   ├── passageiro.py
│   ├── voo.py
│   └── assento.py
├── database/
│   ├── data_manager.py
│   └── dados.json
├── utils/
│   ├── logger.py
│   └── validators.py
└── interface/
    └── cli.py
```

## 🚀  Como Executar

```bash
# Clone o repositório
git clone <url-do-repositorio>

# Execute o programa
python main.py
```

## 📋 Requisitos Atendidos

- [x] Cadastro de passageiros com validação
- [x] Visualização de assentos por voo
- [x] Reserva com controle de concorrência
- [x] Restrição para menores em assentos de emergência
- [x] Sistema de logging completo
- [x] Persistência de dados
- [x] Interface CLI funcional

## 👥 Multiplataforma

O sistema funciona tanto em **Windows** quanto em **Linux**, utilizando apenas bibliotecas padrão do Python.

## 📝  Licença

Este projeto foi desenvolvido para fins acadêmicos.
