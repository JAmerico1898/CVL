import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import base64
from io import BytesIO

# Configuração da página
st.set_page_config(
    page_title="Análise Custo-Volume-Lucro (CVL)",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #0277BD;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .section {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
    }
    .highlight {
        color: #FF5722;
        font-weight: bold;
    }
    .formula {
        background-color: #e1f5fe;
        padding: 0.8rem;
        border-left: 5px solid #0288d1;
        margin-bottom: 1rem;
        border-radius: 5px;
    }
    .tooltip {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted #0288d1;
        cursor: help;
    }
    .conclusion {
        background-color: #e8f5e9;
        padding: 1rem;
        border-radius: 5px;
        margin-top: 1rem;
        border-left: 5px solid #4caf50;
    }
    .warning {
        background-color: #fff8e1;
        padding: 1rem;
        border-radius: 5px;
        margin-top: 1rem;
        border-left: 5px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)

# Função para criar cenários pré-definidos
def get_predefined_cases():
    return {
        "Selecione um cenário": {
            "pvu": 50.0,
            "cvu": 20.0,
            "cf": 60000.0,
            "quantidade": 2000,
            "descricao": "Configure os valores manualmente"
        },
        "Fábrica de Móveis": {
            "pvu": 800.0,
            "cvu": 320.0,
            "cf": 240000.0,
            "quantidade": 600,
            "descricao": "Uma pequena indústria moveleira com custos fixos altos e boa margem de contribuição."
        },
        "Loja de Roupas": {
            "pvu": 120.0,
            "cvu": 72.0,
            "cf": 96000.0,
            "quantidade": 4000,
            "descricao": "Uma loja de varejo com custos fixos moderados (aluguel, funcionários) e margem menor."
        },
        "Consultoria Contábil": {
            "pvu": 300.0,
            "cvu": 60.0,
            "cf": 180000.0,
            "quantidade": 1200,
            "descricao": "Empresa de serviços com baixo custo variável e alto custo fixo (salários)."
        },
        "Restaurante": {
            "pvu": 45.0,
            "cvu": 18.0,
            "cf": 126000.0,
            "quantidade": 7500,
            "descricao": "Negócio alimentício com custos fixos consideráveis e volume alto."
        }
    }

# Função para calcular a margem de contribuição
def calcular_mc(pvu, cvu):
    return pvu - cvu

# Função para calcular o ponto de equilíbrio em unidades
def calcular_pe_unidades(cf, mc_unitaria):
    if mc_unitaria <= 0:
        return float('inf')
    return cf / mc_unitaria

# Função para calcular o ponto de equilíbrio em valor monetário
def calcular_pe_valor(pe_unidades, pvu):
    return pe_unidades * pvu

# Função para calcular o lucro
def calcular_lucro(quantidade, mc_unitaria, cf):
    return quantidade * mc_unitaria - cf

# Função para gerar dados para o gráfico
def gerar_dados_grafico(pvu, cvu, cf, quantidade_max):
    # Criar um range de quantidade de 0 até o máximo escolhido
    quantidades = np.linspace(0, quantidade_max * 1.5, 100)
    
    # Calcular receita total, custo total e lucro para cada quantidade
    receita_total = [q * pvu for q in quantidades]
    custo_total = [cf + q * cvu for q in quantidades]
    lucro = [r - c for r, c in zip(receita_total, custo_total)]
    
    # Retornar os dados em um DataFrame
    return pd.DataFrame({
        'Quantidade': quantidades,
        'Receita Total': receita_total,
        'Custo Total': custo_total,
        'Lucro': lucro
    })

# Função para criar o gráfico CVL
def criar_grafico_cvl(df, pe_unidades, moeda, quantidade_atual=None):
    fig = go.Figure()
    
    # Adicionar linhas de receita e custo
    fig.add_trace(go.Scatter(
        x=df['Quantidade'], 
        y=df['Receita Total'],
        mode='lines',
        name='Receita Total',
        line=dict(color='#4CAF50', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['Quantidade'], 
        y=df['Custo Total'],
        mode='lines',
        name='Custo Total',
        line=dict(color='#F44336', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['Quantidade'], 
        y=df['Lucro'],
        mode='lines',
        name='Lucro',
        line=dict(color='#2196F3', width=3)
    ))
    
    # Adicionar linha horizontal em y=0
    fig.add_shape(
        type="line",
        x0=0,
        y0=0,
        x1=max(df['Quantidade']),
        y1=0,
        line=dict(color="black", width=1, dash="dash"),
    )
    
    # Adicionar linha vertical no ponto de equilíbrio
    fig.add_shape(
        type="line",
        x0=pe_unidades,
        y0=min(min(df['Lucro']), 0),
        x1=pe_unidades,
        y1=max(df['Receita Total']),
        line=dict(color="black", width=1, dash="dash"),
    )
    
    # Marcar o ponto de equilíbrio
    pe_receita = pe_unidades * df['Receita Total'].iloc[-1] / df['Quantidade'].iloc[-1]
    fig.add_trace(go.Scatter(
        x=[pe_unidades],
        y=[pe_receita],
        mode='markers',
        name='Ponto de Equilíbrio',
        marker=dict(color='black', size=12, symbol='star')
    ))
    
    # Se uma quantidade atual foi especificada, marcar essa posição
    if quantidade_atual is not None:
        # Encontrar a receita, custo e lucro para a quantidade atual
        idx = np.abs(df['Quantidade'] - quantidade_atual).argmin()
        receita_atual = df['Receita Total'].iloc[idx]
        custo_atual = df['Custo Total'].iloc[idx]
        lucro_atual = df['Lucro'].iloc[idx]
        
        # Adicionar um ponto destacando a posição atual
        fig.add_trace(go.Scatter(
            x=[quantidade_atual, quantidade_atual, quantidade_atual],
            y=[receita_atual, custo_atual, 0],
            mode='markers+lines',
            name='Situação Atual',
            marker=dict(color='#673AB7', size=10),
            line=dict(color='#673AB7', width=1, dash='dot')
        ))
    
    # Adicionar áreas sombreadas para lucro e prejuízo
    fig.add_trace(go.Scatter(
        x=df['Quantidade'],
        y=df['Lucro'],
        fill='tozeroy',
        fillcolor='rgba(76, 175, 80, 0.2)',
        line=dict(width=0),
        name='Área de Lucro',
        showlegend=False,
        hoverinfo='none'
    ))
    
    # Configurar o layout
    fig.update_layout(
        title=f'Análise Custo-Volume-Lucro (CVL)',
        xaxis_title='Quantidade (unidades)',
        yaxis_title=f'Valor ({moeda})',
        hovermode='x unified',
        height=600,
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Adicionar anotação para o ponto de equilíbrio
    fig.add_annotation(
        x=pe_unidades,
        y=pe_receita,
        text=f"PE: {pe_unidades:.0f} unidades",
        showarrow=True,
        arrowhead=1,
        ax=40,
        ay=-40
    )
    
    return fig

# Função para criar um gráfico de barras de margem de contribuição
def criar_grafico_mc(pvu, cvu, mc, moeda):
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=['Preço de Venda', 'Custo Variável', 'Margem de Contribuição'],
        y=[pvu, cvu, mc],
        marker_color=['#2196F3', '#F44336', '#4CAF50']
    ))
    
    fig.update_layout(
        title='Composição da Margem de Contribuição por Unidade',
        yaxis_title=f'Valor ({moeda})',
        height=400,
        template='plotly_white'
    )
    
    return fig

# Função para gerar PDF (simples - exporta como CSV nesta implementação)
def gerar_relatorio(dados, resultados):
    # Criar um DataFrame com os resultados
    df_resultados = pd.DataFrame({
        'Métrica': [
            'Preço de Venda Unitário', 
            'Custo Variável Unitário', 
            'Custo Fixo Total',
            'Quantidade Vendida',
            'Margem de Contribuição Unitária',
            'Margem de Contribuição Percentual',
            'Ponto de Equilíbrio (unidades)',
            'Ponto de Equilíbrio (valor)',
            'Receita Total',
            'Custo Total',
            'Lucro/Prejuízo'
        ],
        'Valor': [
            f"{resultados['moeda']} {dados['pvu']:.2f}",
            f"{resultados['moeda']} {dados['cvu']:.2f}",
            f"{resultados['moeda']} {dados['cf']:.2f}",
            f"{dados['quantidade']} unidades",
            f"{resultados['moeda']} {resultados['mc_unitaria']:.2f}",
            f"{resultados['mc_percentual']:.1f}%",
            f"{resultados['pe_unidades']:.0f} unidades",
            f"{resultados['moeda']} {resultados['pe_valor']:.2f}",
            f"{resultados['moeda']} {resultados['receita_total']:.2f}",
            f"{resultados['moeda']} {resultados['custo_total']:.2f}",
            f"{resultados['moeda']} {resultados['lucro']:.2f}"
        ]
    })
    
    # Converter para CSV
    csv = df_resultados.to_csv(index=False)
    
    # Codificar para download
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="analise_cvl.csv" class="btn">Download do Relatório (CSV)</a>'
    return href

# Função para interpretar os resultados
def interpretar_resultados(dados, resultados):
    interpretacao = ""
    
    # Verificar se está acima ou abaixo do ponto de equilíbrio
    if dados['quantidade'] < resultados['pe_unidades']:
        gap = resultados['pe_unidades'] - dados['quantidade']
        interpretacao += f"""
        <div class='warning'>
            <strong>Situação de Prejuízo:</strong> A empresa está operando <strong>{gap:.0f} unidades abaixo</strong> do ponto de equilíbrio.
            Com {dados['quantidade']} unidades vendidas, a empresa tem um prejuízo de {resultados['moeda']} {abs(resultados['lucro']):.2f}.
        </div>
        <div class='conclusion'>
            <strong>Recomendação:</strong> Para atingir o ponto de equilíbrio, é necessário vender mais {gap:.0f} unidades 
            ou reduzir custos fixos em {resultados['moeda']} {abs(resultados['lucro']):.2f}.
        </div>
        """
    else:
        margem = dados['quantidade'] - resultados['pe_unidades']
        margem_percentual = (margem / resultados['pe_unidades']) * 100
        interpretacao += f"""
        <div class='conclusion'>
            <strong>Situação de Lucro:</strong> A empresa está operando <strong>{margem:.0f} unidades acima</strong> do ponto de equilíbrio 
            (margem de segurança de {margem_percentual:.1f}%).
            Com {dados['quantidade']} unidades vendidas, a empresa tem um lucro de {resultados['moeda']} {resultados['lucro']:.2f}.
        </div>
        """
    
    # Análise da margem de contribuição
    if resultados['mc_percentual'] < 30:
        interpretacao += f"""
        <div class='warning'>
            <strong>Margem de Contribuição Baixa:</strong> A margem de contribuição de {resultados['mc_percentual']:.1f}% é relativamente baixa.
            Isso significa que para cada {resultados['moeda']} 100 em vendas, apenas {resultados['mc_percentual']:.1f} contribuem para cobrir 
            os custos fixos e gerar lucro.
        </div>
        """
    elif resultados['mc_percentual'] > 60:
        interpretacao += f"""
        <div class='conclusion'>
            <strong>Margem de Contribuição Alta:</strong> A margem de contribuição de {resultados['mc_percentual']:.1f}% é excelente.
            Isso significa que para cada {resultados['moeda']} 100 em vendas, {resultados['mc_percentual']:.1f} contribuem para cobrir 
            os custos fixos e gerar lucro.
        </div>
        """
    
    return interpretacao

# Dicionário de termos
def carregar_dicionario():
    termos = {
        "Análise CVL": "Estudo da relação entre custos, volume de produção/vendas e lucro. Ajuda a tomar decisões sobre preços, mix de produtos e estrutura de custos.",
        "Margem de Contribuição": "Diferença entre o preço de venda e o custo variável unitário. Representa quanto cada unidade vendida contribui para cobrir os custos fixos e gerar lucro.",
        "Ponto de Equilíbrio": "Nível de atividade onde a receita total iguala o custo total, resultando em lucro zero. É o ponto a partir do qual a empresa começa a ter lucro.",
        "Custos Fixos": "Custos que não variam com o volume de produção, como aluguel, salários administrativos e depreciação.",
        "Custos Variáveis": "Custos que variam proporcionalmente com o volume de produção, como matéria-prima e comissões de vendas.",
        "Margem de Segurança": "Diferença entre o volume atual de vendas e o ponto de equilíbrio. Indica quanto as vendas podem cair antes que a empresa comece a ter prejuízo.",
        "Alavancagem Operacional": "Medida de quanto um aumento nas vendas afetará o lucro operacional. Uma alta alavancagem significa que pequenas mudanças nas vendas causarão grandes mudanças no lucro."
    }
    return termos

# Função principal
def main():
    # Título principal
    st.markdown("<h1 class='main-header'>Análise Custo-Volume-Lucro (CVL)</h1>", unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Configurações")
    
    # Seleção de moeda
    moeda = st.sidebar.selectbox(
        "Selecione a moeda:",
        options=["R$", "US$", "€", "£"],
        index=0
    )
    
    # Casos pré-definidos
    st.sidebar.subheader("Casos Práticos")
    casos = get_predefined_cases()
    caso_selecionado = st.sidebar.selectbox(
        "Selecione um cenário pronto ou configure manualmente:",
        options=list(casos.keys())
    )
    
    if caso_selecionado != "Selecione um cenário":
        st.sidebar.info(casos[caso_selecionado]["descricao"])
    
    # Inputs do usuário na sidebar
    st.sidebar.subheader("Parâmetros do Cenário")
    
    # Definir valores padrão com base no caso selecionado
    valores_padrao = casos[caso_selecionado] if caso_selecionado != "Selecione um cenário" else casos["Selecione um cenário"]
    
    # Preço de venda unitário
    pvu = st.sidebar.number_input(
        "Preço de Venda Unitário (PVU):",
        min_value=0.01,
        value=valores_padrao["pvu"],
        format="%.2f",
        help="Valor pelo qual cada unidade do produto/serviço é vendida."
    )
    
    # Custo variável unitário
    cvu = st.sidebar.number_input(
        "Custo Variável Unitário (CVU):",
        min_value=0.01,
        max_value=pvu,
        value=min(valores_padrao["cvu"], pvu),
        format="%.2f",
        help="Custo que varia diretamente com a quantidade produzida (matéria-prima, embalagem, etc)."
    )
    
    # Custo fixo total
    cf = st.sidebar.number_input(
        "Custo Fixo Total:",
        min_value=0.0,
        value=valores_padrao["cf"],
        format="%.2f",
        help="Custos que permanecem constantes independentemente do volume (aluguel, salários administrativos, etc)."
    )
    
    # Quantidade vendida
    quantidade = st.sidebar.number_input(
        "Quantidade Vendida (unidades):",
        min_value=0,
        value=valores_padrao["quantidade"],
        help="Número de unidades vendidas no período."
    )
    
    # Adicionar seção para simulações de cenários
    st.sidebar.subheader("Simulação de Cenários")
    
    cenario = st.sidebar.radio(
        "Selecione um cenário para simular:",
        ["Base", "Otimista", "Pessimista"]
    )
    
    # Fatores de ajuste para cada cenário
    fatores_cenario = {
        "Base": {"pvu": 1.0, "cvu": 1.0, "cf": 1.0},
        "Otimista": {"pvu": 1.1, "cvu": 0.95, "cf": 0.98},
        "Pessimista": {"pvu": 0.95, "cvu": 1.05, "cf": 1.1}
    }
    
    # Ajustar valores com base no cenário
    pvu_simulado = pvu * fatores_cenario[cenario]["pvu"]
    cvu_simulado = cvu * fatores_cenario[cenario]["cvu"]
    cf_simulado = cf * fatores_cenario[cenario]["cf"]
    
    # Mostrar os valores ajustados se não for o cenário base
    if cenario != "Base":
        st.sidebar.markdown("**Valores ajustados para o cenário:**")
        st.sidebar.markdown(f"* PVU: {moeda} {pvu_simulado:.2f} ({'+' if pvu_simulado > pvu else ''}{((pvu_simulado/pvu)-1)*100:.1f}%)")
        st.sidebar.markdown(f"* CVU: {moeda} {cvu_simulado:.2f} ({'+' if cvu_simulado > cvu else ''}{((cvu_simulado/cvu)-1)*100:.1f}%)")
        st.sidebar.markdown(f"* CF: {moeda} {cf_simulado:.2f} ({'+' if cf_simulado > cf else ''}{((cf_simulado/cf)-1)*100:.1f}%)")
    
    # Cálculos principais
    mc_unitaria = calcular_mc(pvu_simulado, cvu_simulado)
    mc_percentual = (mc_unitaria / pvu_simulado) * 100 if pvu_simulado > 0 else 0
    pe_unidades = calcular_pe_unidades(cf_simulado, mc_unitaria)
    pe_valor = calcular_pe_valor(pe_unidades, pvu_simulado)
    lucro = calcular_lucro(quantidade, mc_unitaria, cf_simulado)
    receita_total = quantidade * pvu_simulado
    custo_total = cf_simulado + (quantidade * cvu_simulado)
    
    # Armazenar resultados em um dicionário
    dados = {
        "pvu": pvu_simulado,
        "cvu": cvu_simulado,
        "cf": cf_simulado,
        "quantidade": quantidade
    }
    
    resultados = {
        "mc_unitaria": mc_unitaria,
        "mc_percentual": mc_percentual,
        "pe_unidades": pe_unidades,
        "pe_valor": pe_valor,
        "lucro": lucro,
        "receita_total": receita_total,
        "custo_total": custo_total,
        "moeda": moeda
    }
    
    # Introdução Teórica
    with st.expander("📚 Fundamentos da Análise Custo-Volume-Lucro", expanded=False):
        st.header("O que é Análise Custo-Volume-Lucro (CVL)?")
        st.write("A Análise CVL é uma ferramenta gerencial que examina o comportamento de receitas totais, custos totais e lucro operacional à medida que ocorrem mudanças no volume de produção, preço de venda, custo variável unitário ou custos fixos.")
        
        st.subheader("Conceitos Fundamentais:")
        st.markdown("- **Margem de Contribuição:** Diferença entre o preço de venda e o custo variável unitário. Representa quanto cada unidade vendida contribui para cobrir os custos fixos e gerar lucro.")
        st.markdown("- **Ponto de Equilíbrio:** Nível de vendas onde a receita total iguala o custo total, resultando em lucro zero.")
        st.markdown("- **Estrutura de Custos:** Divisão entre custos fixos e variáveis que impacta diretamente o ponto de equilíbrio.")
        
        st.subheader("Principais Fórmulas:")
        st.info("**Margem de Contribuição Unitária:** MC = Preço de Venda Unitário - Custo Variável Unitário")
        st.info("**Margem de Contribuição Percentual:** MC% = (MC ÷ PVU) × 100%")
        st.info("**Ponto de Equilíbrio em Unidades:** PE = Custos Fixos Totais ÷ Margem de Contribuição Unitária")
        st.info("**Ponto de Equilíbrio em Valor:** PE$ = PE × Preço de Venda Unitário")
        st.info("**Lucro Operacional:** Lucro = (PVU - CVU) × Quantidade - Custos Fixos")
        st.info("**Margem de Segurança:** MS = (Vendas Atuais - Vendas no Ponto de Equilíbrio) ÷ Vendas Atuais")
        
        st.subheader("Aplicações da Análise CVL:")
        st.markdown("- Determinar o volume de vendas necessário para atingir um lucro-alvo")
        st.markdown("- Avaliar o impacto de mudanças nos preços")
        st.markdown("- Analisar diferentes estruturas de custos")
        st.markdown("- Avaliar a viabilidade de novos produtos ou serviços")
        st.markdown("- Planejar mix de produtos para maximizar o lucro")
        
        st.subheader("Limitações:")
        st.markdown("- Assume comportamento linear de receitas e custos")
        st.markdown("- Pressupõe que todos os custos podem ser classificados como fixos ou variáveis")
        st.markdown("- Considera apenas um único produto (para múltiplos produtos, é necessário usar o conceito de mix de vendas)")
        

    
    # Exibir cálculos principais
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<h3 class='sub-header'>Margem de Contribuição</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='section'>
            <p><strong>Unitária:</strong> {moeda} {mc_unitaria:.2f}</p>
            <p><strong>Percentual:</strong> {mc_percentual:.1f}%</p>
            <p><em>De cada {moeda} 100 em vendas, {mc_percentual:.1f} contribuem para cobrir custos fixos e gerar lucro.</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("<h3 class='sub-header'>Ponto de Equilíbrio</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='section'>
            <p><strong>Em unidades:</strong> {pe_unidades:.0f} unidades</p>
            <p><strong>Em valor:</strong> {moeda} {pe_valor:.2f}</p>
            <p><em>A empresa precisa vender {pe_unidades:.0f} unidades para não ter lucro nem prejuízo.</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("<h3 class='sub-header'>Resultado Operacional</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class='section'>
            <p><strong>Receita Total:</strong> {moeda} {receita_total:.2f}</p>
            <p><strong>Custo Total:</strong> {moeda} {custo_total:.2f}</p>
            <p><strong>Lucro/Prejuízo:</strong> <span class='highlight'>{moeda} {lucro:.2f}</span></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Slider para simulação de quantidade
    st.markdown("<h3 class='sub-header'>Simule diferentes volumes de vendas</h3>", unsafe_allow_html=True)
    
    # Determinar o valor máximo para o slider (2x o ponto de equilíbrio ou a quantidade atual, o que for maior)
    max_slider = max(int(pe_unidades * 2), quantidade, 100)
    
    # Slider para quantidade
    quantidade_simulada = st.slider(
        "Ajuste a quantidade vendida:",
        min_value=0,
        max_value=max_slider,
        value=quantidade,
        step=1
    )
    
    # Calcular o lucro para a quantidade simulada
    lucro_simulado = calcular_lucro(quantidade_simulada, mc_unitaria, cf_simulado)
    receita_simulada = quantidade_simulada * pvu_simulado
    custo_simulado = cf_simulado + (quantidade_simulada * cvu_simulado)
    
    # Mostrar resultados da simulação
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Receita Total Simulada",
            value=f"{moeda} {receita_simulada:.2f}",
            delta=f"{receita_simulada - receita_total:.2f}" if quantidade_simulada != quantidade else None
        )
    
    with col2:
        st.metric(
            label="Custo Total Simulado",
            value=f"{moeda} {custo_simulado:.2f}",
            delta=f"{custo_simulado - custo_total:.2f}" if quantidade_simulada != quantidade else None,
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="Lucro/Prejuízo Simulado",
            value=f"{moeda} {lucro_simulado:.2f}",
            delta=f"{lucro_simulado - lucro:.2f}" if quantidade_simulada != quantidade else None
        )
    
    # Gerar dados para o gráfico
    df = gerar_dados_grafico(pvu_simulado, cvu_simulado, cf_simulado, max(quantidade, quantidade_simulada, pe_unidades * 1.5))
    
    # Criar os gráficos
    st.markdown("<h3 class='sub-header'>Visualização Gráfica</h3>", unsafe_allow_html=True)
    
    # Gráfico principal de CVL
    fig_cvl = criar_grafico_cvl(df, pe_unidades, moeda, quantidade_simulada)
    st.plotly_chart(fig_cvl, use_container_width=True)
    
    # Gráfico de composição da margem de contribuição
    fig_mc = criar_grafico_mc(pvu_simulado, cvu_simulado, mc_unitaria, moeda)
    st.plotly_chart(fig_mc, use_container_width=True)
    
    # Interpretação dos resultados
    st.markdown("<h3 class='sub-header'>Análise e Interpretação</h3>", unsafe_allow_html=True)
    
    # Chamada da função para interpretar os resultados
    interpretacao_html = interpretar_resultados(
        {"pvu": pvu_simulado, "cvu": cvu_simulado, "cf": cf_simulado, "quantidade": quantidade_simulada}, 
        {
            "mc_unitaria": mc_unitaria,
            "mc_percentual": mc_percentual,
            "pe_unidades": pe_unidades,
            "pe_valor": pe_valor,
            "lucro": lucro_simulado,
            "receita_total": receita_simulada,
            "custo_total": custo_simulado,
            "moeda": moeda
        }
    )
    
    st.markdown(interpretacao_html, unsafe_allow_html=True)
    
    # Tabela com métricas detalhadas
    with st.expander("Métricas Detalhadas", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Dados de Entrada")
            st.markdown(f"""
            * **Preço de Venda Unitário:** {moeda} {pvu_simulado:.2f}
            * **Custo Variável Unitário:** {moeda} {cvu_simulado:.2f}
            * **Custo Fixo Total:** {moeda} {cf_simulado:.2f}
            * **Quantidade Vendida:** {quantidade_simulada} unidades
            """)
        
        with col2:
            st.subheader("Resultados Calculados")
            st.markdown(f"""
            * **Margem de Contribuição Unitária:** {moeda} {mc_unitaria:.2f}
            * **Margem de Contribuição Percentual:** {mc_percentual:.1f}%
            * **Ponto de Equilíbrio (unidades):** {pe_unidades:.0f}
            * **Ponto de Equilíbrio (valor):** {moeda} {pe_valor:.2f}
            * **Receita Total:** {moeda} {receita_simulada:.2f}
            * **Custo Total:** {moeda} {custo_simulado:.2f}
            * **Lucro/Prejuízo:** {moeda} {lucro_simulado:.2f}
            """)
        
        if quantidade_simulada > 0:
            # Cálculo de métricas adicionais
            margem_seguranca_unidades = quantidade_simulada - pe_unidades
            margem_seguranca_percentual = (margem_seguranca_unidades / quantidade_simulada) * 100 if quantidade_simulada > 0 else 0
            
            # Cálculo da alavancagem operacional com verificação de divisão por zero
            alavancagem = "Não aplicável (lucro zero ou negativo)"
            if lucro_simulado > 0:
                alavancagem = f"{((receita_simulada - quantidade_simulada * cvu_simulado) / lucro_simulado):.2f}"

            st.subheader("Métricas Adicionais")
            st.markdown(f"""
            * **Margem de Segurança (unidades):** {margem_seguranca_unidades:.0f}
            * **Margem de Segurança (%):** {margem_seguranca_percentual:.1f}%
            * **Alavancagem Operacional:** {alavancagem}
            """)
    
    # Área para download de relatório
    st.markdown("<h3 class='sub-header'>Exportar Resultados</h3>", unsafe_allow_html=True)
    
    # Gerar link para download
    dados_export = {
        "pvu": pvu_simulado,
        "cvu": cvu_simulado,
        "cf": cf_simulado,
        "quantidade": quantidade_simulada
    }
    
    resultados_export = {
        "mc_unitaria": mc_unitaria,
        "mc_percentual": mc_percentual,
        "pe_unidades": pe_unidades,
        "pe_valor": pe_valor,
        "lucro": lucro_simulado,
        "receita_total": receita_simulada,
        "custo_total": custo_simulado,
        "moeda": moeda
    }
    
    relatorio_html = gerar_relatorio(dados_export, resultados_export)
    st.markdown(relatorio_html, unsafe_allow_html=True)
    
    # Dicionário de termos contábeis
    with st.expander("📖 Dicionário de Termos Contábeis", expanded=False):
        termos = carregar_dicionario()
        
        for termo, definicao in termos.items():
            st.markdown(f"**{termo}**: {definicao}")
            st.markdown("---")

# Executar o aplicativo
if __name__ == "__main__":
    main()
    
    #