Sistema de Gestão de Ensino (Skills Manager)

Este projeto é uma aplicação web desenvolvida em Python utilizando o framework Flask. O sistema foi desenhado para facilitar a gestão académica de uma instituição de ensino, permitindo o controlo centralizado de turmas, alunos, professores e atividades avaliativas.

    Contexto Académico: Este software foi desenvolvido como parte dos requisitos do 6º período de Engenharia de Software na Unisenai, para a disciplina de Backend Development.

A arquitetura do projeto segue o padrão MVC (Model-View-Controller), garantindo uma organização clara entre a lógica de negócio, a interface do utilizador e a gestão de dados.

📋 Funcionalidades Principais

O sistema possui um controlo de acesso baseado em cargos (Role-Based Access Control), dividindo as funcionalidades entre Administradores e Professores.

    Nota: O sistema é de gestão interna. Os alunos não possuem acesso direto (login); os seus dados, entregas e notas são geridos exclusivamente pelos administradores e professores.

🔐 Acesso e Segurança

    Autenticação: Sistema de login e registo seguro com hash de senhas (via Bcrypt).

    Códigos de Verificação: O registo de novos administradores ou professores é restrito e exige um código de validação específico para cada cargo, garantindo que apenas pessoal autorizado se cadastre.

    Gestão de Sessão: O sistema mantém o utilizador logado e suporta a funcionalidade de "Lembrar senha".

👤 Painel do Administrador

O administrador tem a visão global da instituição e gere a estrutura base:

    Gestão de Professores: Visualizar a lista de docentes e remover acessos quando necessário.

    Gestão de Turmas: Criar, editar e remover turmas, além de associar os professores responsáveis a cada uma delas.

    Gestão de Alunos: Cadastrar novos alunos, editar informações e gerir a sua alocação nas turmas.

    Monitorização: Acesso aos detalhes de desempenho dos alunos, visualizando as notas atribuídas pelos professores em diferentes atividades.

🎓 Painel do Professor

O professor gere o conteúdo académico das turmas às quais está vinculado:

    Gestão de Tarefas (Assignments):

        Criação de novas tarefas com definição de nome, valor (nota) e data de entrega.

        Upload de Ficheiros: Possibilidade de anexar enunciados ou materiais de apoio (PDF) às tarefas.

        Edição e remoção de tarefas existentes.

    Lançamento de Notas: Interface dedicada para atribuir e atualizar as notas dos alunos em cada atividade específica.

    Relatórios de Turma: Visualização do progresso dos alunos da sua turma.

🌐 API Integrada

O backend disponibiliza endpoints que retornam dados em formato JSON, permitindo a consulta programática de:

    Listagem de Turmas e Alunos.

    Detalhes das Tarefas (Assignments).

    Informações dos Professores. Esta estrutura facilita futuras integrações ou o desenvolvimento de novos frontends.

🛠 Tecnologias Utilizadas

O núcleo do projeto é focado no desenvolvimento Backend robusto e modular:

    Linguagem: Python 3

    Framework Web: Flask (seguindo arquitetura MVC)

    Base de Dados: PostgreSQL (via SQLAlchemy ORM)

    Segurança: Flask-Bcrypt (Hashing de senhas)

    Uploads: Gestão segura de ficheiros (PDFs)

    Frontend: HTML5, CSS3 (Bootstrap) e Jinja2 para renderização de templates.

🚀 Como Executar o Projeto

Siga os passos abaixo para colocar o sistema a funcionar no seu ambiente local.

Pré-requisitos

    Python 3.x instalado.

    PostgreSQL instalado e configurado (ou ajuste para outro banco de dados no ficheiro de configuração).

Instalação

    Instalar as dependências:
    Bash

pip install -r requirements.txt

Configurar Variáveis de Ambiente: Crie um ficheiro .env na raiz do projeto com as configurações do banco de dados e as chaves de segurança (baseado no config.py e project_model.txt):
Snippet de código

# Configuração da Base de Dados
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
DB_NAME=nome_do_banco

# Códigos de Registo (Defina os seus)
TEACHER_REGISTER_CODE=123
ADMIN_REGISTER_CODE=456

Inicializar a Base de Dados e Executar: O sistema irá criar as tabelas automaticamente na primeira execução.
Bash

    python app.py

    Aceder: Abra o navegador em http://127.0.0.1:5000.

📂 Estrutura do Projeto

    controllers/: Contém a lógica das rotas (Blueprints) para Admin, Professor, Utilizador e API.

    models/: Definição das tabelas da base de dados (Classes ORM).

    view/templates/: Ficheiros HTML (Jinja2) da interface do utilizador.

    uploads/: Diretório onde os ficheiros das tarefas são armazenados.

    utils/: Funções auxiliares e decoradores de segurança.
