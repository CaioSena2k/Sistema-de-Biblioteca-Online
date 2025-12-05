
# **Sistema de Biblioteca Online 📚**

Sistema desenvolvido como Projeto Integrador para as disciplinas de **Engenharia de Software** e **Programação Orientada a Objetos (POO)** da UNIJORGE.

## **👥 Equipe de Desenvolvimento (Grupo 2)**

| Aluno | Função / Contribuição |
| :--- | :--- |
| **William Lyrio** | Arquiteto de Software, Frontend e Documentação |
| **Caio Sena** | Desenvolvimento Backend (Views, Models) e Banco de Dados |
| **Douglas Rodrigues** | Levantamento de Requisitos e Casos de Uso |
| **Gabriel Portella** | Testes de Software e Controle de Qualidade |

**Professores Orientadores:**

* **Igor Gonzales** - Engenharia de Software
* **Jailson Santos** - Programação Orientada a Objetos

## **🚀 Sobre o Projeto**

O **Sistema de Biblioteca Online** é uma solução web desenvolvida para modernizar a gestão de acervos físicos. Ele permite o controle rigoroso de livros (empréstimos, devoluções e estoque), garantindo que a quantidade no sistema reflita a realidade da estante.

### **Principais Funcionalidades:**

* **Gestão de Acervo Físico (CRUD):**
    * Cadastro manual de livros com inserção de capa, título e autor.
    * **Controle de Estoque:** Definição manual da quantidade física disponível.
    * Edição e exclusão de obras pelo administrador.
* **Automação de Empréstimo:**
    * Sistema de validação que bloqueia o empréstimo se **estoque = 0**.
    * Baixa automática: Ao confirmar empréstimo, o estoque diminui (-1).
* **Painel Administrativo:**
    * Dashboard exclusivo para gestores (Superusuários).
    * Controle de devoluções: Ao confirmar a devolução, o estoque aumenta (+1) automaticamente.
* **Área do Usuário:**
    * Vitrine virtual com capas dos livros.
    * Perfil com histórico de "Meus Empréstimos" e prazos de devolução.

## **🛠️ Tecnologias Utilizadas**

* **Linguagem:** Python 3.13
* **Framework Web:** Django 5.2 (Padrão MVT)
* **Banco de Dados:** SQLite (Nativo)
* **Frontend:** HTML5, CSS3, Bootstrap 4
* **Controle de Versão:** Git e GitHub

## **⚙️ Como Rodar o Projeto Localmente**

Siga os passos abaixo para configurar o ambiente de desenvolvimento na sua máquina.

### **Passo 1: Clonar ou Baixar**

```bash
# Clone este repositório
git clone [https://github.com/CaioSena2k/Sistema-de-Biblioteca-Online.git](https://github.com/CaioSena2k/Sistema-de-Biblioteca-Online.git)

# Entre na pasta do projeto
cd Sistema-de-Biblioteca-Online
````

### **Passo 2: Criar Ambiente Virtual (Recomendado)**

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### **Passo 3: Instalar Dependências**

```bash
pip install django pillow
```

### **Passo 4: Configurar o Banco de Dados**

```bash
python manage.py makemigrations
python manage.py migrate
```

### **Passo 5: Criar um Superusuário (Admin)**

Para acessar o painel de gestão, você precisa de um primeiro usuário administrador.

```bash
python manage.py createsuperuser
# Siga as instruções (Nome, Email, Senha)
```

### **Passo 6: Rodar o Servidor**

```bash
python manage.py runserver
```

Acesse no navegador:

  * **Site Principal:** [http://127.0.0.1:8000/](https://www.google.com/search?q=http://127.0.0.1:8000/)
  * **Painel Django:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## **🧪 Como Testar as Funcionalidades**

1.  **Login de Admin:** Entre com o usuário criado no Passo 5.
2.  **Cadastro Manual:** No painel ou área de gestão, cadastre um livro novo e defina a **Quantidade = 1**.
3.  **Empréstimo:**
      * Acesse a home como um usuário comum (ou crie um novo).
      * Solicite o empréstimo do livro cadastrado.
      * Veja o estoque cair para 0 na página de detalhes.
4.  **Bloqueio:**
      * Tente pegar o mesmo livro novamente. O botão deve estar desabilitado ou dar erro.
5.  **Devolução:**
      * Volte para o Admin e confirme o recebimento.
      * Verifique se o estoque voltou para 1.

## **📄 Estrutura do Projeto**

```text
Sistema-de-Biblioteca-Online/
│
├── biblioteca/      # Configurações principais (settings, urls)
├── livro/           # App principal (Lógica de estoque e CRUD)
│   ├── models.py    # Banco de dados (Campo quantidade)
│   ├── views.py     # Regras de negócio (Decremento/Incremento)
│   └── templates/   # Telas HTML
├── usuarios/        # App de gestão de usuários (Login/Cadastro)
├── media/           # Pasta de uploads (Capas dos livros)
├── db.sqlite3       # Banco de dados
└── manage.py        # Executor do Django
```

### **🎓 UNIJORGE - 2025**
