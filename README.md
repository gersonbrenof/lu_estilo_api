# lu_estilo_api

API desenvolvida com [FastAPI](https://fastapi.tiangolo.com/)

## Como instalar e rodar o projeto (modo local, sem Docker)

### Passo a passo completo:

```bash
# 1. Clonar o repositório
git clone https://github.com/seu-usuario/lu_estilo_api.git
cd lu_estilo_api

# 2. Criar ambiente virtual
python -m venv venv

# 3. Ativar o ambiente virtual
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
# source venv/bin/activate

# 4. Instalar as dependências
pip install -r requirements.txt

# 5. Rodar o servidor FastAPI
uvicorn main:app --reload
