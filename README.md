# crud-midd-db-validations-deploy

#  1 instalar virtualenv de python

apt install python3-venv

# 2 crear el virtual env

python3 -m venv venv

# 3 Activar el venv

En Linux

source venv/bin/activate

En Win

source venv/script/activate

# 4 Una vez activado instalar lo requirements del archivo requirements.txt

pip install -r requirements.txt

# 5 execute project
uvicorn main:app --reload
