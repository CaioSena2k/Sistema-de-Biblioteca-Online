# **Sistema de Biblioteca Digital Híbrida 📚**

Sistema desenvolvido como Projeto Integrador para as disciplinas de **Engenharia de Software** e **Programação Orientada a Objetos (POO)** da UNIJORGE.

## **👥 Equipe de Desenvolvimento (Grupo 2\)**

| Aluno | Função / Contribuição |
| :---- | :---- |
| **William Lyrio** | Arquiteto de Software, Analista de Requisitos, Gerente Ágil e Frontend (Templates) |
| **Caio Sena** | Desenvolvimento Backend (Views, Models) e Integração de Dados |
| **Douglas Rodrigues** | Documentação, Diagramação e Levantamento de Requisitos |
| **Gabriel Portella** | Testes de Software, Validação e Controle de Qualidade |

**Professores Orientadores:**

* **Igor Gonzales** \- Engenharia de Software  
* **Jailson Santos** \- Programação Orientada a Objetos

## **🚀 Sobre o Projeto**

O **Sistema de Biblioteca Digital** é uma solução híbrida desenvolvida para modernizar a gestão de acervos. Ele permite o controle rigoroso de livros físicos (empréstimos, devoluções e estoque) e também oferece acesso a acervos digitais (leitura de PDFs), tudo em uma única plataforma web responsiva.

### **Principais Funcionalidades:**

* **Gestão de Acervo Físico:**  
  * Cadastro de livros com controle de quantidade em estoque.  
  * Empréstimo inteligente (bloqueia se estoque \= 0 ou se usuário já possui o livro).  
  * Solicitação de devolução pelo usuário e confirmação pelo administrador.  
* **Acervo Digital:**  
  * Upload e leitura de E-books (PDF) diretamente no navegador (funcionalidade configurável).  
* **Automação e Integração:**  
  * Script em Python (requests) integrado à **Google Books API** para importação automática de capas e metadados.  
* **Painel Administrativo Personalizado:**  
  * Dashboard exclusivo para gestores (Superusuários) integrado ao site.  
  * Controle de solicitações de devolução pendentes.  
  * Gestão de usuários (promover a Admin ou rebaixar a Leitor).  
* **Área do Usuário:**  
  * Perfil editável com avatar dinâmico e estatísticas de leitura.  
  * Histórico e status de empréstimos em tempo real.

## **🛠️ Tecnologias Utilizadas**

* **Linguagem:** Python 3.13  
* **Framework Web:** Django 5.2 (Padrão MVT)  
* **Banco de Dados:** SQLite (Nativo)  
* **Frontend:** HTML5, CSS3, Bootstrap 4, FontAwesome  
* **APIs:** Google Books API (via biblioteca requests)

## **⚙️ Como Rodar o Projeto Localmente**

Siga os passos abaixo para configurar o ambiente de desenvolvimento na sua máquina.

### **Pré-requisitos**

* Python 3.10 ou superior instalado.  
* Git (opcional, para clonar o repositório).

### **Passo 1: Clonar ou Baixar**

\# Clone este repositório  
git clone \[https://github.com/seu-usuario/biblioteca-digital.git\](https://github.com/seu-usuario/biblioteca-digital.git)

\# Entre na pasta do projeto  
cd biblioteca-digital

### **Passo 2: Criar Ambiente Virtual (Recomendado)**

\# Windows  
python \-m venv venv  
venv\\Scripts\\activate

\# Linux/Mac  
python3 \-m venv venv  
source venv/bin/activate

### **Passo 3: Instalar Dependências**

pip install django requests pillow

### **Passo 4: Configurar o Banco de Dados**

python manage.py makemigrations  
python manage.py migrate

### **Passo 5: Criar um Superusuário (Admin)**

Para acessar o painel de gestão, você precisa de um primeiro usuário administrador.

python manage.py createsuperuser  
\# Siga as instruções (Nome: admin, Senha: admin123)

### **Passo 6: Rodar o Servidor**

python manage.py runserver

Acesse no navegador:

* **Site Principal:** [http://127.0.0.1:8000/auth/login/](https://www.google.com/search?q=http://127.0.0.1:8000/auth/login/)  
* **Painel Django:** [http://127.0.0.1:8000/admin/](https://www.google.com/search?q=http://127.0.0.1:8000/admin/)

## **🧪 Como Testar as Funcionalidades**

1. **Login de Admin:** Entre com o usuário criado no Passo 5\.  
2. **Painel Administrativo:** No menu superior, clique em *"Olá, \[Nome\]"* \-\> *"Painel do Administrador"*.  
   * Lá você pode promover outros usuários criados.  
3. **Empréstimo:**  
   * Crie um segundo usuário (em aba anônima) através do cadastro.  
   * Tente pegar um livro emprestado.  
   * Veja o estoque diminuir na página do livro.  
4. **Devolução:**  
   * Solicite a devolução com o usuário comum.  
   * Volte para o Admin e confirme o recebimento no Painel.

## **📄 Estrutura do Projeto**

biblioteca/  
│  
├── biblioteca/         \# Configurações principais (settings, urls)  
├── livro/              \# App principal (Lógica de negócio)  
│   ├── models.py       \# Banco de dados (Livros, Emprestimos, Categorias)  
│   ├── views.py        \# Regras de negócio e controle de acesso  
│   ├── urls.py         \# Rotas do sistema  
│   └── templates/      \# Arquivos HTML (home, ver\_livro, painel\_admin)  
├── usuarios/           \# App de gestão de usuários  
│   └── models.py       \# Modelo de Usuário personalizado  
├── media/              \# Pasta onde as capas e PDFs são salvos  
├── db.sqlite3          \# Arquivo do banco de dados  
└── manage.py           \# Executor do Django

### **🎓 UNIJORGE \- 2025**