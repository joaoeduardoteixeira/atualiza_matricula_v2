# Atualizador de matrículas de beneficiários de plano de saúde

## Problema:
Ao inserir um beneficiário novo no produto não regulamentado, é gerado um número de matrícula fora dos padrões numéricos.

## Objetivo:
Ajustar matrículas via interface disponibilizada ao usuário.

## Impacto:
Autonomia para o usuário executar a tarefa, evitando que o time de TI necessite efetuar consultas e updates quando a situação ocorre.

## Funcionamento:
A página recebe um código (pessoa física, neste caso), e atualiza o código de beneficiário. A página de sucesso consta apenas cabeçalho, necessitando de ajustes personalizados de acordo com o objetivo.

## Banco de Dados:
O banco utilizado foi o Oracle e, caso seja necessário, importar a biblioteca apropriada de conexão.

## Dependências
Executar pip install -r requirements.txt no ambiente.

## Criador:
João Eduardo da Silva Teixeira

## Considerações finais:

Versão 2 da solução. 

Melhorias: Registros apresentados em tela para confirmação da ação. Suprimida página de sucesso e apresentado um popup de "ok". 
Layout: Fundo do cabeçalho retirado, linha preta como footer do cabeçalho e logo aumentado.

## Contato:
- E-mail: joaoeduardosteixeira@gmail.com
- Skype: analista.eduardo@hotmail.com
