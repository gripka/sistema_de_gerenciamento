# Access Management System - ENGLISH

This is an access management system developed using Django, primarily with Python for the backend, and HTML/CSS/Bootstrap for the frontend.

## Project Summary

The system allows creation, editing, and deletion of users, profiles, modules, transactions, and functions, as well as associating profiles with users to define access permissions.

## Implemented Features

### User Authentication

- User authentication with username and password.

### Password Recovery

- Password recovery via registered email.

### User Management

#### User Registration

- Registration of new users with basic information (name, email, password).

#### User Editing 

- Editing existing user information.

#### User Deletion

- Deletion of users from the system.

### Profile Management

#### Profile Creation 

- Creation of profiles defining sets of accessible transactions and functions.

#### Profile Editing 

- Editing and removal of existing profiles.

#### Profile Viewing 

- Viewing all available profiles.

### Module Management

#### Module Creation 

- Creation of system modules that can contain multiple transactions.

#### Module Editing 

- Editing and deletion of modules.

### Transaction Management

#### Transaction Definition 

- Definition of transactions that can be executed within each module.

#### Transaction Editing 

- Editing and deletion of transactions.

### Function Management

#### Function Creation 

- Creation of specific functions within modules.

#### Function Editing 

- Editing and deletion of functions.

### Profile Association

#### Profile-to-User Linking 

- Linking profiles to users to define access permissions.

#### Association Changes 

- Modification and removal of existing associations.

### User Interface

#### Responsive Web Interface 

- Responsive web interface for system access and management.

### Administrative Dashboards 

- Administrative dashboards for activity visualization and management.

### Reports 

- Reports module including:
  - Registered users;
  - User profiles;
  - List of modules;
  - List of transactions;
  - List of registered functions.

## Technologies Used

- Django (Python)
- PostgreSQL
- HTML/CSS/JavaScript/Bootstrap (for web interface)
- Git (for version control)

## Installation and Configuration

1. Clone the repository:
  ```
  git clone https://github.com/gripka/sistema_de_gerenciamento.git
  ```
2. Navigate into the project directory:
cd repository-name

3. Create a virtual environment:
python -m venv env

Example: .venv\Scripts\activate  

4. Activate the virtual environment:
- On Windows:
  ```
  env\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source env/bin/activate
  ```

5. Install dependencies:
pip install -r requirements.txt

6. Set up environment variables:
- Create a `.env` file in the root directory with the following contents:
  ```
  DEBUG=True
  SECRET_KEY=your_secret_key_here
  DATABASE_URL=postgres://username:password@localhost:5432/database_name

  EMAIL_HOST_USER=
  EMAIL_HOST_PASSWORD=
  SITE_URL=
  ```

7. Apply database migrations:
python manage.py migrate

8. Create a superuser (admin):
python manage.py createsuperuser

9. Run the development server:
python manage.py runserver


## Contribution
- Vlw tmj



# Sistema de Gerenciamento de Acesso - PORTUGUÊS

Este é um sistema de gerenciamento de acesso desenvolvido Python para controle de perfis de usuários, transações e funções.

## Resumo do Projeto

O sistema permite a criação, edição e exclusão de usuários, perfis, módulos, transações e funções, além de associar perfis a usuários para definir permissões de acesso.

## Funcionalidades Implementadas

### Autenticação de Usuários

- Autenticação de usuários com nome de usuário e senha.
  
### Recuperação de Senha 

- Recuperação de senha através do e-mail cadastrado.

### Gestão de Usuários

#### Cadastro de Usuários

- Cadastro de novos usuários com informações básicas (nome, e-mail, senha).

#### Edição de Usuários

- Edição de informações de usuários existentes.

#### Exclusão de Usuários

- Exclusão de usuários do sistema.

### Gestão de Perfis

#### Criação de Perfis

- Criação de perfis que definem conjuntos de transações e funções acessíveis.

#### Edição de Perfis

- Edição e remoção de perfis existentes.

#### Visualização de Perfis

- Visualização de todos os perfis disponíveis.

### Gestão de Módulos

#### Criação de Módulos

- Criação de módulos do sistema que podem conter várias transações.

#### Edição de Módulos

- Edição e exclusão de módulos.

### Gestão de Transações

#### Definição de Transações

- Definição de transações que podem ser executadas dentro de cada módulo.

#### Edição de Transações

- Edição e exclusão de transações.

### Gestão de Funções

#### Criação de Funções 

- Criação de funções específicas dentro dos módulos.

#### Edição de Funções 

- Edição e exclusão de funções.

### Associação de Perfis

#### Vinculação de Perfis a Usuários

- Vinculação de perfis a usuários para definir permissões de acesso.

#### Alteração de Associações

- Alteração e remoção de associações existentes.

### Interface do Usuário

#### Interface Web Responsiva 

- Interface web responsiva para acesso e gestão do sistema.

### Dashboards Administrativos

- Dashboards administrativos para visualização de atividades e gestão.

### Relatórios 

- Módulo de relatórios que inclui:
  - Usuários cadastrados;
  - Perfis de usuários;
  - Lista de módulos;
  - Lista de transações;
  - Lista de funções cadastradas.

## Tecnologias Utilizadas

- Django (Python)
- PostgreSQL
- HTML/CSS/JavaScript/Bootstrap (para interface web)
- Git (para controle de versão)

## Instalação e Configuração

1. Clone o repositório:
git clone https://github.com/gripka/sistema_de_gerenciamento.git

2. Navegue até o diretório do projeto:
cd nome-do-repositorio

3. Crie um ambiente virtual:
python -m venv env

4. Ative o ambiente virtual:
- No Windows:
  ```
  env\Scripts\activate
  ```
- No macOS e Linux:
  ```
  source env/bin/activate
  ```

5. Instale as dependências:
pip install -r requirements.txt

6. Configure as variáveis de ambiente:
- Crie um arquivo `.env` no diretório raiz com o seguinte conteúdo:
  ```
  DEBUG=True
  SECRET_KEY=sua_chave_secreta_aqui
  DATABASE_URL=postgres://usuario:senha@localhost:5432/nome-do-banco

  EMAIL_HOST_USER=
  EMAIL_HOST_PASSWORD=
  SITE_URL=
  ```

7. Aplique as migrações do banco de dados:
python manage.py migrate

8. Crie um superusuário (admin):
python manage.py createsuperuser

9. Execute o servidor de desenvolvimento:
python manage.py runserver


## Contribuição

- Vlw, tmj

