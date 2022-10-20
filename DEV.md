# SETUP para testes

Primeiramente, eu fiz o doc, baseado em linux entao para windows, tem que achar as coisas equivalentes. Segundo, não coloquei a instalação da virtualenv e python pois varia um pouco entre cada sistema, no geral você provalvemente vai achar ele no seu packager manager. Vou deixar alguns links.

## 1. Requisitos:
python 3.10.8
https://www.python.org/downloads/

virtualenv = 20.16.2

https://virtualenv.pypa.io/en/latest/installation.html
## 2. virtualenv:
Para o que todos tenham instalados as bibliotecas usadas no projeto automaticamente usamos um ambiente virtual, que será criado pela virtaulenv, todos os pacotes que forem instalados dentro do ambiente virtual são seperados dos pacotes que você tem instalado somente on seu PC.
Para isso, ao clonar o rep, e ter a virtualenv instalada,
Dentro do diretorio principal digite:
```python3 -m venv env```
isso irá criar uma virtualenv dentro de uma pasta chamada env.

Para usa-la digite:

```source env/bin/activate```

Para checkar se está usando o python da env digite:

```which python3```

o resultado tem que ser o diretorio da sua venv. Todos os comandos a seguir devem ser feitos usando o python da venv, para não alterar o seu sistema.

Depois para installar as bibliotecas do projeto digite:

```python3 -m pip install -r requirements.txt```

Caso voces adicionem alguma biblioteca, lembrem de gerar o requirements.txt denovo para todos sincronizarem as bibliotecas. Ele pode ser gerado assim:

```python3 -m pip freeze > requirements.txt```

para sair da venv:
```deactivate```

mais detalhes aqui: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/

## 3. Flask
No processo anterior, a env já vai instalar o flask como library, agora só falta configura-lo:
Dentro do diretorio do projeto digite:
``` export FLASK_APP=main.py"```
```export FLASK_DEBUG=1```
cuidado com espaços. O primeiro comando diz ao Flask qual nosso arquivo tem o app, pra ele rodar o server. O segundo é só para ajudar a desenvolver, com ele não será necessario interpretar o programa todas as vezes basta uma vez, e a cada vez que salvar algum arquivo ele atualiza a página automaticamente, é muito prático.

e por fim:
```flask run```
isso dará um ip: ```127.0.0.1:5000```
ao acessar do navegador vai ser possivel ver a página.
Esse ip e porta são configurados em main.py em app.run caso tenha conflitos de portas e etc.