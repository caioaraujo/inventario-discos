# inventario-discos
Projeto voluntário em prol da cultura de Santa Catarina.

Opção 1 lê o arquivo definido em `setup.ini`. O arquivo precisar estar no formato txt e na seguinte estrutura:
```
Nº: numero
Título: Titulo do album
Intérpretes: nome do interprete
Data: data | Volumes: volume
```

A opção 2 serve para adicionar uma nova entrada no arquivo.

A opção 3 criará a base de dados, com base no arquivo especificado em `setup.ini`.

A opção 4 lista os dados inseridos na base de dados.

Os dados do arquivo serão armazenados em um banco `sqlite` que fica dentro do próprio projeto. 

## Instalação
Execute no seu ambiente de desenvolvimento `python src/main.py`.

# Testes
Execute no seu ambiente de desenvolvimento `python -m unittest` a partir da raíz do projeto.
