LebryDB: Uma Simples Biblioteca para Gerenciamento de Dados NoSQL em Formato JSON

A  LebryDB é uma biblioteca Python que oferece uma solução simples para gerenciar dados NoSQL em formato JSON. Com ela, você pode criar e gerenciar uma base de dados NoSQL em seu aplicativo Python sem a necessidade de um sistema de gerenciamento de banco de dados completo. A classe permite a inserção, atualização, exclusão e consulta de documentos, tornando-a ideal para projetos que não exigem complexidade excessiva de um banco de dados tradicional.

Recursos Principais:

Inserção Simples: Adicione novos documentos à base de dados com facilidade usando um par de chave-valor simples.

Atualização de Documentos: Atualize documentos existentes para refletir as informações mais recentes.

Exclusão de Documentos: Remova documentos da base de dados quando eles não forem mais necessários.

Consultas Simples: Realize consultas básicas em seus dados com filtros personalizados.

Como Usar:

python
Copy code
# Importe a classe LebryDB
from lebrydb import LebryDB

# Crie uma instância da base de dados
db = LebryDB("dados.json")

# Inserindo um novo documento
novo_documento = {"nome": "Alice", "idade": 30}
db.inserir("chave1", novo_documento)

# Atualizando um documento existente
atualizacao = {"idade": 31}
db.atualizar("chave1", atualizacao)

# Consultando documentos
resultados = db.consultar({"idade": 31})
print("Resultados da consulta:", resultados)
Observações:

A classe LebryDB é uma opção leve para projetos que requerem um armazenamento simples de documentos NoSQL em formato JSON. Embora não seja adequada para cenários mais complexos que envolvem consultas avançadas ou transações, é uma escolha sólida para tarefas de gerenciamento de dados simples.

