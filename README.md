# inventario-discos
Projeto voluntário em prol da cultura de Santa Catarina.

Opção 1 lê o arquivo definido em `setup.ini`. O arquivo precisar estar no formato txt, em UTF-8 e na seguinte estrutura:
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

A opção 8 gera um arquivo txt somente com os dados.

Por fim, a opção 9 finaliza o programa.

Após inserir ou atualizar um registro, caso seja especificado a letra e o número da ordem alfabética, todos os registros
posteriores referentes a essa letra serão incrementados. Caso os valores não sejam especificados, será inserido como o
último registro naquela letra correspondente.

Os dados do arquivo serão armazenados em um banco `sqlite` que fica dentro do próprio projeto. 

## Pré-requisitos
- Sistema operacional Ubuntu 22.04 ou Windows 10;
- Python 3.11;
- wkhtmltopdf

## Instalação
- Execute na raíz do projeto `pip install -r requirements.txt` para instalar as dependências.;
- Instale no seu sistema operacional o aplicativo [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html) 
para geração de PDFs;
- Configure o arquivo `setup.ini`;
- Execute no seu ambiente de desenvolvimento `python src/main.py`.


## Um passo extra que pode ser necessário

Rodando o código no linux, eu tive que adicionar à variável de ambiente PYTHONPATH para que
o código rodasse localmente:

```
export PYTHONPATH=/home/bufulin/Desktop/bufulink/inventario-discos/:$PYTHONPATH
```

Isso serve para que seja possível identificar o módulo `src`. 

# Testes
Execute no seu ambiente de desenvolvimento `python -m unittest` a partir da raíz do projeto.
