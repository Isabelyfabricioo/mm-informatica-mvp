
# MM Informática

Sistema web desenvolvido para auxiliar a MM Informática no cadastro e consulta de produtos e no acompanhamento das negociações com clientes.

## Funcionalidades

- Cadastro de produtos.
- Consulta e pesquisa de produtos.
- Edição e exclusão de produtos.
- Cadastro de interesses de clientes.
- Acompanhamento do status das negociações.
- Controle de disponibilidade dos produtos.

## Tecnologias utilizadas

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Pytest
- GitHub Actions

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/Isabelyfabricioo/mm-informatica-mvp.git
```

### 2. Acessar a pasta

```bash
cd mm-informatica-mvp
```

### 3. Criar o ambiente virtual

```bash
python -m venv .venv
```

### 4. Ativar o ambiente virtual

No Windows:

```bash
.venv\Scripts\activate
```

### 5. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### 6. Executar o sistema

```bash
python run.py
```

Acessar pelo navegador:

http://127.0.0.1:5000

## Testes automatizados

Para executar os testes:

```bash
python -m pytest tests/ -v
```

O projeto utiliza GitHub Actions para executar os testes automaticamente a cada atualização enviada ao repositório.

## Repositório

https://github.com/Isabelyfabricioo/mm-informatica-mvp
