# inventario-discos
Projeto voluntário em prol da cultura de Santa Catarina.

Opção 1 lê o arquivo definido em `setup.ini`. O arquivo precisar estar no formato txt e na seguinte estrutura:
```
Nº: numero
Título: Titulo do album
Intérpretes: nome do interprete
Data: data | Volumes: volume
Observação: observação quando houver
```

A opção 2 criará a base de dados, com base no arquivo especificado em `setup.ini`.

A opção 3 lista os dados inseridos na base de dados.

A opção 4 serve para adicionar uma nova entrada no arquivo.

A opção 5 consulta um registro pelo número sequencial.

A opção 6 atualiza um registro pelo número sequencial.

A opção 7 gera o PDF com os dados.

Por fim, a opção 8 finaliza o programa.

Após inserir ou atualizar um registro, todos os registros da correspondente ordem alfabética são atualizados na base com
seus novos sequenciais.

Os dados do arquivo serão armazenados em um banco `sqlite` que fica dentro do próprio projeto. 

## Instalação
Execute no seu ambiente de desenvolvimento `python src/main.py`.

# Testes
Execute no seu ambiente de desenvolvimento `python -m unittest` a partir da raíz do projeto.
