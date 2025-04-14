**Análise Custo-Volume-Lucro (CVL) - Aplicativo Educacional**

**Visão Geral**

Este aplicativo Streamlit interativo foi projetado para auxiliar no ensino e aprendizado da Análise Custo-Volume-Lucro (CVL). Desenvolvido para estudantes e professores de Ciências Contábeis, o aplicativo permite a criação de cenários, simulações e análises dinâmicas para compreender os conceitos fundamentais de contabilidade gerencial.

**Recursos**

Interatividade completa: Ajuste parâmetros para observar mudanças em tempo real
Visualizações claras: Gráficos detalhados mostrando relações entre custos, volume e lucro
Cenários pré-definidos: Exemplos práticos para diversos tipos de negócios
Análise automática: Interpretações explicativas dos resultados gerados
Exportação de dados: Baixe relatórios em CSV para análise posterior

**Funcionalidades**

Conceitos Demonstrados:

Margem de contribuição (unitária e percentual)
Ponto de equilíbrio (em unidades e valores monetários)
Simulação de cenários (otimista, base, pessimista)
Margem de segurança
Alavancagem operacional
Análise de lucro/prejuízo

**Personalização**

O aplicativo permite o ajuste dos seguintes parâmetros:

Preço de venda unitário
Custo variável unitário
Custos fixos totais
Quantidade de produtos vendidos
Tipo de moeda

**Instalação**

Pré-requisitos

Python 3.8+
pip (gerenciador de pacotes do Python)

Passos para Instalação

Clone o repositório:

bashgit clone https://github.com/seu-usuario/analise-cvl.git
cd analise-cvl

Crie um ambiente virtual (opcional, mas recomendado):

bashpython -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

Instale as dependências:

bashpip install -r requirements.txt

Execute o aplicativo:

bashstreamlit run CVL.py
Dependências
O aplicativo utiliza as seguintes bibliotecas:

streamlit
pandas
plotly
numpy
base64

**Como Usar**

Selecione um cenário pré-definido ou configure seus próprios parâmetros
Ajuste os valores dos parâmetros conforme necessário
Observe os resultados calculados e os gráficos atualizados automaticamente
Use o slider para simular diferentes volumes de venda
Experimente os diferentes cenários (otimista, base, pessimista)
Exporte os resultados usando o botão de download

**Finalidade Educacional**

Este aplicativo foi desenvolvido para:
Apoiar professores em aulas de Contabilidade Gerencial e Contabilidade de Custos
Ajudar estudantes a visualizar conceitos abstratos de forma concreta
Permitir a exploração de cenários "e se?" para aprofundar o entendimento
Fornecer uma ferramenta prática para estudo independente

**Faça um fork do projeto**

Crie uma branch para sua feature (git checkout -b feature/nova-funcionalidade)
Commit suas mudanças (git commit -m 'Adiciona nova funcionalidade')
Push para a branch (git push origin feature/nova-funcionalidade)
Abra um Pull Request

**Contato**

José Américo - tesouraria.rj@gmail.com
Link do projeto: https://github.com/JAmerico1898/CVL

Desenvolvido por Prof. José Américo como ferramenta educacional para ensino de Contabilidade Gerencial e Análise Custo-Volume-Lucro.
