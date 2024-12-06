# Editor de Tributações em Notas Fiscais Eletrônicas

Este é um projeto desenvolvido em Python que permite editar tributações em Notas Fiscais Eletrônicas (NF-e). O projeto utiliza o Pony ORM para o gerenciamento de banco de dados e o módulo `xml.etree.ElementTree` para manipulação de arquivos XML, que são o formato padrão das NF-e.

## Funcionalidades

- **Leitura de XML**: Abre e interpreta arquivos XML de Notas Fiscais Eletrônicas.
- **Edição de Tributações**: Modifica os valores de tributações dentro do XML de acordo com as regras fornecidas.
- **Validação de Dados**: Verifica a validade dos dados da NF-e após as edições, garantindo a integridade dos valores de tributos.
- **Armazenamento de Dados**: Utiliza o Pony ORM para armazenar e consultar informações sobre as NF-e e suas respectivas tributações.

## Tecnologias

- **Python**: Linguagem de programação utilizada para o desenvolvimento do projeto.
- **Pony ORM**: Biblioteca de mapeamento objeto-relacional para facilitar a interação com o banco de dados.
- **xml.etree.ElementTree**: Biblioteca para análise e manipulação de arquivos XML, usada para editar os dados das NF-e.

