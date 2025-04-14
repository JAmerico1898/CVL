📊 Análise Custo-Volume-Lucro (CVL) — Aplicativo Educacional

🧾 Visão Geral

Este aplicativo interativo em Streamlit foi desenvolvido para apoiar o ensino e aprendizado da Análise Custo-Volume-Lucro (CVL). Pensado para estudantes e professores de Ciências Contábeis, ele possibilita a criação de simulações práticas e análises dinâmicas, facilitando a compreensão dos principais conceitos da contabilidade gerencial.

🎯 Recursos

✅ Interatividade completa: ajuste parâmetros e veja os resultados em tempo real

📈 Visualizações claras: gráficos que ilustram relações entre custos, volume e lucro

🧪 Cenários pré-definidos: exemplos para diferentes tipos de negócios

📊 Análises automáticas: interpretações textuais com base nos cálculos

📁 Exportação de dados: download dos resultados em formato CSV

⚙️ Funcionalidades
Conceitos demonstrados:
Margem de contribuição (unitária e percentual)

Ponto de equilíbrio (em unidades e valores monetários)

Simulação de cenários (otimista, base, pessimista)

Margem de segurança

Alavancagem operacional

Análise de lucro/prejuízo

Parâmetros personalizáveis:
Preço de venda unitário

Custo variável unitário

Custos fixos totais

Quantidade de produtos vendidos

Tipo de moeda

🚀 Instalação
🔧 Pré-requisitos
Python 3.8 ou superior

pip instalado

📦 Passo a passo
bash
Copiar
Editar
# Clone o repositório
git clone https://github.com/JAmerico1898/CVL.git
cd CVL

# (Opcional) Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Execute o aplicativo
streamlit run CVL.py
📚 Dependências
Este aplicativo utiliza as seguintes bibliotecas:

streamlit

pandas

plotly

numpy

base64 (interna da biblioteca padrão do Python)

🧠 Como Usar
Selecione um cenário pré-definido ou insira seus próprios parâmetros

Ajuste os valores conforme necessário

Observe os resultados e gráficos atualizados automaticamente

Use o slider para simular diferentes volumes de venda

Experimente os diferentes cenários (otimista, base, pessimista)

Clique em "Exportar" para baixar os resultados

🎓 Finalidade Educacional
Este projeto foi desenvolvido para:

Apoiar professores em aulas de Contabilidade Gerencial e Contabilidade de Custos

Ajudar alunos a visualizar conceitos abstratos de forma concreta

Estimular a prática de simulações do tipo “e se?”

Oferecer uma ferramenta acessível de estudo independente

🤝 Contribuições
Sinta-se à vontade para contribuir com melhorias!

bash
Copiar
Editar
# Faça um fork do projeto
# Crie uma branch para sua funcionalidade
git checkout -b feature/nova-funcionalidade

# Commit das alterações
git commit -m 'Adiciona nova funcionalidade'

# Push para o repositório
git push origin feature/nova-funcionalidade

# Abra um Pull Request
📬 Contato
José Américo — tesouraria.rj@gmail.com
🔗 Projeto no GitHub: github.com/JAmerico1898/CVL

Desenvolvido por Prof. José Américo como ferramenta educacional para o ensino de Contabilidade Gerencial e Análise Custo-Volume-Lucro.
