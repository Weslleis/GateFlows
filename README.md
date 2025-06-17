# Controle Log

## 📝 Descrição do Projeto

**Controle Log** é uma aplicação web desenvolvida com **Flask** para o gerenciamento completo do fluxo de acesso de fornecedores e veículos. Ela otimiza e centraliza o registro de entradas e saídas, sendo ideal para portarias, almoxarifados e pontos de controle.

**Principais funcionalidades:**

* **Cadastro detalhado:** Registra data, hora de entrada, fornecedor, nome e CPF do motorista, placa do caminhão, hora de saída e observações.
* **Validação inteligente:** Valida automaticamente o formato de CPF e placas (padrão Mercosul e nacional).
* **Gestão de registros:** Permite filtrar os acessos por período, editar horários de saída e excluir registros.
* **Relatórios:** Gera e baixa relatórios em PDF dos acessos filtrados para auditorias e análises.

## 🚀 Tecnologias Utilizadas

* **Backend:** Python 3, Flask
* **Banco de Dados:** SQLite (com SQLAlchemy ORM)
* **Frontend:** HTML, CSS, JavaScript
* **Geração de PDF:** ReportLab

## ⚙️ Configuração e Instalação

Siga estes passos para configurar e rodar o projeto em seu ambiente local:

### Pré-requisitos

Certifique-se de ter o **Python 3** e o **pip** (gerenciador de pacotes do Python) instalados em sua máquina.

### Passos para Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/controle-log.git](https://github.com/seu-usuario/controle-log.git)
    cd controle-log
    ```
    *(Substitua `https://github.com/seu-usuario/controle-log.git` pelo URL real do seu repositório.)*

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    # No Windows:
    .\venv\Scripts\activate
    # No macOS/Linux:
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Se você ainda não tem um `requirements.txt`, crie-o executando `pip freeze > requirements.txt` após instalar todas as dependências como Flask, SQLAlchemy, ReportLab etc.)*

4.  **Crie o banco de dados:**
    O banco de dados `database.db` será criado automaticamente na primeira execução do `app.py` se ele não existir.

5.  **Execute a aplicação:**
    ```bash
    python app.py
    ```

A aplicação estará disponível em `http://127.0.0.1:5000/` em seu navegador.

## 💡 Como Usar

### Página Inicial (Registro)

* Acesse `http://127.0.0.1:5000/`.
* Preencha os campos do formulário para registrar um novo acesso de fornecedor.
* Os campos **CPF** e **Placa Caminhão** possuem validação automática.
* Mensagens de sucesso ou erro aparecerão na parte superior da tela.

### Registros Salvos

* Clique no botão "Ver Registros Salvos" na página inicial ou acesse `http://127.0.0.1:5000/registros`.
* Nesta página, você pode:
    * **Filtrar** registros por `Data Início` e `Data Fim`.
    * **Limpar Filtro** para ver todos os registros novamente.
    * **Gerar PDF** dos registros atualmente filtrados.
    * **Editar Hora Saída** de um registro existente.
    * **Excluir** um registro (com confirmação).

## 📄 Estrutura do Projeto

```plaintext
GateFlows/
├── app.py                # Lógica principal da aplicação Flask
├── models.py             # Definições do modelo de banco de dados (SQLAlchemy)
├── requirements.txt      # Dependências do projeto Python
├── static/
│   ├── login.css         # Estilos da página de login
│   ├── style.css         # Estilo geral da aplicação
│   └── img/
│       └── fundo.jpg     # Imagem de fundo usada na aplicação
├── templates/
│   ├── editar.html       # Página para editar hora de saída de um registro
│   ├── index.html        # Página principal de registro
│   ├── login.html        # Página de login de usuário
│   └── registros.html    # Página para visualizar, filtrar e gerenciar registros
└── instance/
    └── database.db       # Banco de dados SQLite (gerado automaticamente)
```


---

## 🤝 Contribuição

Contribuições são **muito bem-vindas**!  
Se você tiver ideias para melhorias, encontrar bugs ou quiser colaborar com o projeto, fique à vontade para:

- **Abrir uma _issue_** com sugestões, dúvidas ou problemas encontrados.
- **Enviar um _pull request_** com melhorias no código, correções ou novas funcionalidades.

Sua ajuda faz a diferença! 🚀
