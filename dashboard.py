import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import os

# Configuração da página
st.set_page_config(layout="wide", page_title="Dashboard COVID-19", initial_sidebar_state="expanded")

# CSS estilo Power BI com gradientes roxos/azuis
st.markdown("""
<style>
    /* Tema escuro Power BI */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* Cards de métricas com gradiente roxo/azul */
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stMetric label {
        color: #e0e0e0 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 32px !important;
        font-weight: bold !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .stMetric [data-testid="stMetricDelta"] {
        color: #00ff88 !important;
        font-weight: 600 !important;
    }
    
    /* Títulos e headers */
    h1, h2, h3 {
        color: #b794f6 !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }
    
    h1 {
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem !important;
    }
    
    /* Sidebar escura */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 2px solid #667eea;
    }
    
    .stSelectbox label, .stSlider label {
        color: #b794f6 !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Containers e boxes */
    .stAlert {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
        border-left: 4px solid #667eea;
        border-radius: 10px;
    }
    
    /* Dataframe/tabelas */
    .stDataFrame {
        background: rgba(26, 26, 46, 0.8);
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Botões e inputs */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }
    
    /* Scrollbar customizada */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a2e;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 5px;
    }
    
    /* Ícones e emojis maiores */
    .big-emoji {
        font-size: 3rem;
        filter: drop-shadow(2px 2px 4px rgba(0, 0, 0, 0.5));
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Carrega os dados de COVID-19 do Our World in Data"""
    url_covid = 'https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv'
    local_cache = 'owid-covid-data.csv'
    
    try:
        if os.path.exists(local_cache):
            cache_age = datetime.now().timestamp() - os.path.getmtime(local_cache)
            if cache_age < 86400:  # 24 horas
                df = pd.read_csv(local_cache)
            else:
                df = pd.read_csv(url_covid)
                df.to_csv(local_cache, index=False)
        else:
            df = pd.read_csv(url_covid)
            df.to_csv(local_cache, index=False)
    except Exception as e:
        if os.path.exists(local_cache):
            st.warning(f"⚠️ Usando dados em cache local")
            df = pd.read_csv(local_cache)
        else:
            st.error(f"❌ Erro ao carregar dados: {str(e)}")
            st.stop()
    
    df['date'] = pd.to_datetime(df['date'])
    
    if 'country' in df.columns and 'location' not in df.columns:
        df['location'] = df['country']
    if 'code' in df.columns and 'iso_code' not in df.columns:
        df['iso_code'] = df['code']
    
    df['people_vaccinated'] = df['people_vaccinated'].fillna(0)
    df['total_deaths'] = df['total_deaths'].fillna(0)
    df['new_cases'] = df['new_cases'].fillna(0)
    df['new_deaths'] = df['new_deaths'].fillna(0)

    traducao_paises = {
        'World': 'Mundo',
        'Brazil': 'Brasil',
        'United States': 'Estados Unidos',
        'India': 'Índia',
        'Russia': 'Rússia',
        'United Kingdom': 'Reino Unido',
        'France': 'França',
        'Germany': 'Alemanha',
        'Italy': 'Itália',
        'Spain': 'Espanha',
        'China': 'China',
        'Japan': 'Japão',
        'South Korea': 'Coreia do Sul',
        'Canada': 'Canadá',
        'Mexico': 'México',
        'Argentina': 'Argentina',
        'Turkey': 'Turquia',
        'Indonesia': 'Indonésia',
        'Saudi Arabia': 'Arábia Saudita',
        'South Africa': 'África do Sul',
        'Australia': 'Austrália'
    }
    
    principais_paises = list(traducao_paises.keys())
    df_principais = df[df['location'].isin(principais_paises)].copy()
    df_principais['location_pt'] = df_principais['location'].map(traducao_paises)
    world_data = df_principais[df_principais['location'] == 'World'].copy()
    lista_paises_pt = sorted([traducao_paises[p] for p in principais_paises if p in df_principais['location'].unique()])
    
    if 'Mundo' in lista_paises_pt:
        lista_paises_pt.remove('Mundo')
        lista_paises_pt = ['Mundo'] + lista_paises_pt

    return df_principais, world_data, lista_paises_pt, traducao_paises

# Carregar dados
df, world_data, lista_paises, traducao_paises = load_data()
traducao_inversa = {v: k for k, v in traducao_paises.items()}

def formatar_pais(pais):
    """Adiciona preposição correta"""
    if pais == 'Mundo':
        return 'no Mundo'
    elif pais in ['Estados Unidos', 'Emirados Árabes']:
        return f'nos {pais}'
    elif pais == 'Brasil':
        return f'no {pais}'
    else:
        return f'na {pais}'

# Título
st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <h1 style='font-size: 3rem; margin-bottom: 10px;'>
        🦠 Dashboard COVID-19 💉
    </h1>
    <p style='font-size: 1.3rem; color: #b794f6; font-weight: 500;'>
        Análise de Vacinação vs. Mortalidade
    </p>
    <p style='font-size: 0.9rem; color: #888; margin-top: 10px;'>
        Evidências científicas sobre o impacto da vacinação em massa
    </p>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# Filtros
st.sidebar.header("🔍 Filtros")
selected_location = st.sidebar.selectbox("Selecione o País/Região", lista_paises, index=0)

min_date = df['date'].min()
max_date = df['date'].max()

st.sidebar.markdown("**Período de Análise:**")
years_with_data = sorted([year for year in df['date'].dt.year.unique() if year <= 2023])
selected_year_range = st.sidebar.select_slider(
    "Selecione o intervalo de anos",
    options=years_with_data,
    value=(years_with_data[0], years_with_data[-1])
)

start_date = pd.Timestamp(f'{selected_year_range[0]}-01-01')
end_date = pd.Timestamp(f'{selected_year_range[1]}-12-31')
start_date = max(start_date, min_date)
end_date = min(end_date, max_date)

st.sidebar.markdown("---")
st.sidebar.info(f"📊 **{selected_location}**\n\n📅 {selected_year_range[0]} - {selected_year_range[1]}")

# Preparar dados filtrados
selected_location_en = traducao_inversa.get(selected_location, selected_location)

if selected_location_en == 'World':
    df_filtrado = world_data.copy()
else:
    df_filtrado = df[df['location'] == selected_location_en].copy()

df_filtrado = df_filtrado[
    (df_filtrado['date'] >= start_date) & 
    (df_filtrado['date'] <= end_date)
].sort_values('date')

if df_filtrado.empty:
    st.warning("⚠️ Não há dados disponíveis para o período/país selecionado.")
    st.stop()

# KPIs
def get_latest_valid_value(df, column):
    valid_data = df[df[column].notna() & (df[column] > 0)]
    if valid_data.empty:
        return 0
    return int(valid_data.iloc[-1][column])

st.markdown("""
<h2 style='text-align: center; margin-bottom: 30px;'>
    📊 Indicadores Principais - <span style='color: #667eea;'>{}</span>
</h2>
""".format(selected_location), unsafe_allow_html=True)

total_cases_selected = get_latest_valid_value(df_filtrado, 'total_cases')
total_deaths_selected = get_latest_valid_value(df_filtrado, 'total_deaths')
total_vaccinated_selected = get_latest_valid_value(df_filtrado, 'people_vaccinated')

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<div class='big-emoji' style='text-align: center;'>🦠</div>", unsafe_allow_html=True)
    st.metric("Total de Casos", f"{total_cases_selected:,}")
with col2:
    st.markdown("<div class='big-emoji' style='text-align: center;'>⚰️</div>", unsafe_allow_html=True)
    st.metric("Total de Mortes", f"{total_deaths_selected:,}")
with col3:
    st.markdown("<div class='big-emoji' style='text-align: center;'>💉</div>", unsafe_allow_html=True)
    st.metric("Pessoas Vacinadas", f"{total_vaccinated_selected:,}")

st.markdown("---")

# Gráfico 1: Evolução de Casos e Mortes
st.markdown("""
<h2 style='text-align: center; margin: 30px 0;'>
    � Evolução Temporal da Pandemia
</h2>
""", unsafe_allow_html=True)

df_grafico1 = df_filtrado[['date', 'new_cases', 'new_deaths']].melt(
    id_vars='date',
    value_vars=['new_cases', 'new_deaths'],
    var_name='Métrica',
    value_name='Contagem'
)

df_grafico1['Métrica'] = df_grafico1['Métrica'].map({
    'new_cases': 'Novos Casos',
    'new_deaths': 'Novas Mortes'
})

fig1 = px.line(
    df_grafico1,
    x='date',
    y='Contagem',
    color='Métrica',
    title=f'Novos Casos e Mortes Diárias - {selected_location}',
    labels={'date': 'Data', 'Contagem': 'Quantidade'},
    color_discrete_map={'Novos Casos': '#667eea', 'Novas Mortes': '#EF553B'}
)

fig1.update_layout(
    hovermode='x unified', 
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(26, 26, 46, 0.8)',
    font=dict(color='white'),
    title_font=dict(size=20, color='#b794f6')
)
st.plotly_chart(fig1, width='stretch')

# Gráfico 2: Vacinação vs Mortes
st.markdown("""
<h2 style='text-align: center; margin: 40px 0;'>
    💉 Impacto da Vacinação na Mortalidade
</h2>
""", unsafe_allow_html=True)

vaccination_start = df_filtrado[df_filtrado['people_vaccinated'] > 0]['date'].min()

fig2 = go.Figure()

fig2.add_trace(go.Scatter(
    x=df_filtrado['date'],
    y=df_filtrado['people_vaccinated'],
    mode='lines',
    name='Pessoas Vacinadas',
    line=dict(color='#2ca02c', width=2),
    yaxis='y'
))

fig2.add_trace(go.Scatter(
    x=df_filtrado['date'],
    y=df_filtrado['total_deaths'],
    mode='lines',
    name='Total de Mortes',
    line=dict(color='#d62728', width=2),
    yaxis='y2'
))

fig2.update_layout(
    title=f'Vacinação vs Mortalidade - {selected_location}',
    xaxis=dict(title='Data', gridcolor='rgba(102, 126, 234, 0.2)'),
    yaxis=dict(
        title=dict(text='Pessoas Vacinadas', font=dict(color='#00CC96')),
        tickfont=dict(color='#00CC96'),
        gridcolor='rgba(102, 126, 234, 0.2)'
    ),
    yaxis2=dict(
        title=dict(text='Total de Mortes', font=dict(color='#EF553B')),
        tickfont=dict(color='#EF553B'),
        overlaying='y',
        side='right',
        gridcolor='rgba(239, 85, 59, 0.2)'
    ),
    hovermode='x unified',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(26, 26, 46, 0.8)',
    font=dict(color='white'),
    title_font=dict(size=20, color='#b794f6')
)

if pd.notna(vaccination_start):
    fig2.add_shape(
        type="line",
        x0=vaccination_start, x1=vaccination_start,
        y0=0, y1=1,
        yref="paper",
        line=dict(color="orange", width=2, dash="dash")
    )
    fig2.add_annotation(
        x=vaccination_start,
        y=1,
        yref="paper",
        text="Início da Vacinação",
        showarrow=False,
        yshift=10,
        font=dict(color="orange", size=12)
    )

st.plotly_chart(fig2, width='stretch')

# NOVO: Gráfico de Tendência de Mortes com Média Móvel
st.markdown("---")
st.subheader("📈 Tendência de Mortes Diárias (Média Móvel 7 dias)")

if not df_filtrado.empty:
    # Calcular média móvel de 7 dias
    df_tendencia = df_filtrado.copy()
    df_tendencia['media_movel_7d'] = df_tendencia['new_deaths'].rolling(window=7, center=True).mean()
    
    fig_tendencia = go.Figure()
    
    # Área de mortes diárias (transparente)
    fig_tendencia.add_trace(go.Scatter(
        x=df_tendencia['date'],
        y=df_tendencia['new_deaths'],
        mode='lines',
        name='Mortes Diárias',
        line=dict(color='rgba(239, 85, 59, 0.3)', width=1),
        fill='tozeroy',
        fillcolor='rgba(239, 85, 59, 0.1)'
    ))
    
    # Linha de média móvel (destaque)
    fig_tendencia.add_trace(go.Scatter(
        x=df_tendencia['date'],
        y=df_tendencia['media_movel_7d'],
        mode='lines',
        name='Média Móvel (7 dias)',
        line=dict(color='#EF553B', width=3)
    ))
    
    fig_tendencia.update_layout(
        height=400,
        plot_bgcolor='rgb(17,17,17)',
        paper_bgcolor='rgb(17,17,17)',
        font=dict(color='white'),
        xaxis=dict(title='Data', gridcolor='rgba(128,128,128,0.2)'),
        yaxis=dict(title='Mortes Diárias', gridcolor='rgba(128,128,128,0.2)'),
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Linha vertical da vacinação (usando shapes)
    if pd.notna(vaccination_start):
        fig_tendencia.add_shape(
            type="line",
            x0=vaccination_start, x1=vaccination_start,
            y0=0, y1=1,
            yref="paper",
            line=dict(color='#FF9500', width=3, dash='solid')
        )
        fig_tendencia.add_annotation(
            x=vaccination_start,
            y=1,
            yref="paper",
            text="🟠 Início Vacinação",
            showarrow=False,
            yshift=10,
            font=dict(color='#FF9500', size=12)
        )
    
    st.plotly_chart(fig_tendencia, width='stretch')
    
    st.info("""
    💡 **Como interpretar:** A linha laranja mostra a tendência real (média de 7 dias).
    A linha vertical laranja marca quando a vacinação começou.
    """)

st.markdown("---")

# ========================================
# ANÁLISE CORRETA: TAXA DE MORTALIDADE (CFR - Case Fatality Rate)
# ========================================
st.markdown("""
<h2 style='text-align: center; margin: 30px 0;'>
    🎯 Impacto da Vacinação: Análise de Taxa de Mortalidade
</h2>
""", unsafe_allow_html=True)

st.markdown("""
<div style='background: linear-gradient(135deg, rgba(0, 204, 150, 0.15), rgba(0, 204, 150, 0.05)); 
            padding: 25px; border-radius: 15px; border-left: 5px solid #00CC96; margin: 20px 0;'>
    
### 🎓 ENTENDA: Por que Mais Mortes NÃO Significa que a Vacina Falhou

**� A Confusão Comum:**
Muitas pessoas olham e pensam: *"Mas se tem mais mortes depois da vacina, então ela não funciona!"*

**❌ ISSO É UM ERRO DE INTERPRETAÇÃO!**

---

### 💡 A EXPLICAÇÃO CORRETA:

**Imagine duas situações:**

**ANTES DA VACINA (Exemplo):**
- 🦠 1.000 pessoas pegaram COVID
- ⚰️ 100 pessoas morreram
- 📊 **Taxa de Mortalidade: 10%**

**DEPOIS DA VACINA (Exemplo):**
- 🦠 **5.000 pessoas** pegaram COVID (5x mais casos!)
- ⚰️ 150 pessoas morreram
- 📊 **Taxa de Mortalidade: 3%** ✅

---

### ✅ O QUE ISSO SIGNIFICA?

1. **😷 Mais gente se infectou** (relaxamento de medidas, variantes mais transmissíveis)
2. **💉 MAS a vacina protegeu contra morte grave!**
3. **📉 A chance de MORRER ao pegar COVID CAIU de 10% para 3%**
4. **🎯 Se não houvesse vacina:** Com 5.000 casos a 10% = **500 mortes**
5. **💚 Com vacina:** Apenas 150 mortes = **350 VIDAS SALVAS!**

---

### 🔬 É isso que a CIÊNCIA analisa:

**Não é o número absoluto de mortes, mas a PROPORÇÃO:**
- Quantas pessoas morrem **entre as que pegam** a doença?
- **Vacinados:** Pegam COVID mas não morrem (ou morrem muito menos)
- **Não vacinados:** Risco 10x-20x maior de morte

---

### 🏆 CONCLUSÃO:

**Mesmo que o número total de mortes suba, se a TAXA DE MORTALIDADE cai, significa que:**
- ✅ A vacina está PROTEGENDO as pessoas
- ✅ Quem pega COVID vacinado tem MUITO menos chance de morrer
- ✅ Cada vida salva é uma vitória da ciência

**👇 Veja nos dados abaixo como isso aconteceu na prática:**

</div>
""", unsafe_allow_html=True)

if pd.notna(vaccination_start):
    st.success(f"🎯 **Início da Vacinação:** {vaccination_start.strftime('%d/%m/%Y')}")
    
    # Períodos de 3 MESES (mais realista que 6)
    df_3m_before = df_filtrado[
        (df_filtrado['date'] >= vaccination_start - pd.Timedelta(days=90)) & 
        (df_filtrado['date'] < vaccination_start)
    ]
    df_3m_after = df_filtrado[
        (df_filtrado['date'] >= vaccination_start) & 
        (df_filtrado['date'] <= vaccination_start + pd.Timedelta(days=90))
    ]
    
    if not df_3m_before.empty and not df_3m_after.empty:
        # ANTES da vacinação
        total_casos_antes = df_3m_before['new_cases'].sum()
        total_mortes_antes = df_3m_before['new_deaths'].sum()
        taxa_mortalidade_antes = (total_mortes_antes / total_casos_antes * 100) if total_casos_antes > 0 else 0
        media_mortes_antes = df_3m_before['new_deaths'].mean()
        
        # DEPOIS da vacinação
        total_casos_depois = df_3m_after['new_cases'].sum()
        total_mortes_depois = df_3m_after['new_deaths'].sum()
        taxa_mortalidade_depois = (total_mortes_depois / total_casos_depois * 100) if total_casos_depois > 0 else 0
        media_mortes_depois = df_3m_after['new_deaths'].mean()
        
        # Calcular REDUÇÕES
        reducao_taxa = ((taxa_mortalidade_antes - taxa_mortalidade_depois) / taxa_mortalidade_antes * 100) if taxa_mortalidade_antes > 0 else 0
        reducao_media = ((media_mortes_antes - media_mortes_depois) / media_mortes_antes * 100) if media_mortes_antes > 0 else 0
        
        # VIDAS SALVAS = Se tivesse mantido a taxa anterior
        vidas_que_morreriam = total_casos_depois * (taxa_mortalidade_antes / 100)
        vidas_salvas = vidas_que_morreriam - total_mortes_depois
        
        # EXIBIR MÉTRICAS
        st.markdown("### 📊 Comparação: 3 Meses ANTES vs 3 Meses DEPOIS")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "🦠 Casos (ANTES)",
                f"{int(total_casos_antes):,}",
                help="Total de casos nos 3 meses ANTES da vacinação"
            )
            st.metric(
                "⚰️ Mortes (ANTES)",
                f"{int(total_mortes_antes):,}",
                help="Total de mortes nos 3 meses ANTES"
            )
        
        with col2:
            st.metric(
                "📈 Taxa Mort. ANTES",
                f"{taxa_mortalidade_antes:.2f}%",
                help="Mortes ÷ Casos (antes da vacinação)"
            )
            st.metric(
                "📊 Média/Dia ANTES",
                f"{media_mortes_antes:.0f}",
                help="Média de mortes por dia"
            )
        
        with col3:
            variacao_casos = ((total_casos_depois/total_casos_antes - 1)*100) if total_casos_antes > 0 else 0
            st.metric(
                "🦠 Casos (DEPOIS)",
                f"{int(total_casos_depois):,}",
                delta=f"+{variacao_casos:.0f}%" if variacao_casos > 0 else f"{variacao_casos:.0f}%",
                delta_color="inverse",
                help="Total de casos nos 3 meses APÓS vacinação"
            )
            variacao_mortes = ((total_mortes_depois/total_mortes_antes - 1)*100) if total_mortes_antes > 0 else 0
            st.metric(
                "⚰️ Mortes (DEPOIS)",
                f"{int(total_mortes_depois):,}",
                delta=f"+{variacao_mortes:.0f}%" if variacao_mortes > 0 else f"{variacao_mortes:.0f}%",
                delta_color="inverse",
                help="Total de mortes nos 3 meses DEPOIS"
            )
        
        with col4:
            st.metric(
                "✅ Taxa Mort. DEPOIS",
                f"{taxa_mortalidade_depois:.2f}%",
                delta=f"-{reducao_taxa:.1f}%" if reducao_taxa > 0 else f"+{abs(reducao_taxa):.1f}%",
                delta_color="normal" if reducao_taxa > 0 else "inverse",
                help="Mortes ÷ Casos (após vacinação)"
            )
            st.metric(
                "📊 Média/Dia DEPOIS",
                f"{media_mortes_depois:.0f}",
                delta=f"-{reducao_media:.1f}%" if reducao_media > 0 else f"+{abs(reducao_media):.1f}%",
                delta_color="normal" if reducao_media > 0 else "inverse",
                help="Média de mortes por dia"
            )
        
        st.markdown("---")
        
        # GRÁFICO COMPARATIVO DE TAXAS
        st.subheader("📊 Comparação Visual: Taxa de Mortalidade")
        
        fig_comp = go.Figure()
        
        fig_comp.add_trace(go.Bar(
            x=['3 Meses ANTES<br>da Vacinação', '3 Meses DEPOIS<br>da Vacinação'],
            y=[taxa_mortalidade_antes, taxa_mortalidade_depois],
            marker=dict(
                color=['#EF553B', '#00CC96'],
                line=dict(color='white', width=2)
            ),
            text=[f'{taxa_mortalidade_antes:.2f}%', f'{taxa_mortalidade_depois:.2f}%'],
            textposition='auto',
            textfont=dict(size=18, color='white', family='Arial Black'),
            hovertemplate='<b>%{x}</b><br>Taxa: %{y:.2f}%<extra></extra>'
        ))
        
        if reducao_taxa > 0:
            fig_comp.add_annotation(
                x=0.5,
                y=max(taxa_mortalidade_antes, taxa_mortalidade_depois) * 0.6,
                text=f"↓ REDUÇÃO DE {abs(reducao_taxa):.1f}% ↓",
                showarrow=False,
                font=dict(size=24, color='#00ff88', family='Arial Black'),
                bgcolor='rgba(0,0,0,0.8)',
                borderpad=10
            )
        
        fig_comp.update_layout(
            height=500,
            plot_bgcolor='rgba(26, 26, 46, 0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=14),
            xaxis=dict(
                title='',
                tickfont=dict(size=14, color='white'),
                showgrid=False
            ),
            yaxis=dict(
                title='Taxa de Mortalidade (%)',
                gridcolor='rgba(102, 126, 234, 0.2)',
                tickfont=dict(size=12, color='white'),
                title_font=dict(size=16, color='#b794f6')
            ),
            showlegend=False,
            margin=dict(t=40, b=40, l=60, r=40)
        )
        
        st.plotly_chart(fig_comp, width='stretch')
        
        st.markdown("---")
        
        # CONCLUSÃO BASEADA NOS DADOS REAIS
        if reducao_taxa > 5:
            st.success(f"""
            ### ✅ IMPACTO POSITIVO COMPROVADO {formatar_pais(selected_location).upper()}
            
            **A taxa de mortalidade CAIU mesmo com mais casos!**
            
            - 📉 Taxa de mortalidade: de **{taxa_mortalidade_antes:.2f}%** para **{taxa_mortalidade_depois:.2f}%** (redução de **{reducao_taxa:.1f}%**)
            - 🦠 Casos AUMENTARAM **{((total_casos_depois/total_casos_antes - 1)*100):.0f}%**, mas...
            - 💚 A taxa de morte por caso DIMINUIU = **vacinação salvou vidas!**
            - 🎯 Estimativa: **{int(vidas_salvas):,} vidas salvas** (se mantivesse taxa anterior)
            
            **🏆 CONCLUSÃO: A VACINAÇÃO FUNCIONOU!**
            Mesmo infectando mais pessoas, a vacina impediu que muitas morressem.
            """)
            
            st.markdown("""
            <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2)); 
                        padding: 20px; border-radius: 12px; margin: 15px 0;'>
                
            ### 💡 Entenda o que isso significa:
            
            **🔬 A vacina NÃO impediu que as pessoas pegassem COVID**
            - O vírus continuou circulando
            - Novas variantes eram mais transmissíveis
            - Mas isso não é o objetivo principal da vacina!
            
            **✅ O que a vacina FEZ foi PROTEGER contra MORTE:**
            - 💉 Pessoas vacinadas pegam COVID, mas **raramente morrem**
            - 🏥 Reduz drasticamente hospitalizações graves
            - 🎯 Transforma uma doença mortal em algo controlável
            
            **📊 Pense assim:**
            - Se 10.000 pessoas não vacinadas pegam COVID → ~{int(10000 * taxa_mortalidade_antes/100)} podem morrer
            - Se 10.000 pessoas **vacinadas** pegam COVID → ~{int(10000 * taxa_mortalidade_depois/100)} podem morrer
            - **Diferença: {int(10000 * (taxa_mortalidade_antes - taxa_mortalidade_depois)/100)} vidas salvas a cada 10.000 infectados!**
            
            </div>
            """, unsafe_allow_html=True)
            
        elif reducao_taxa > 0:
            st.info(f"""
            ### ℹ️ Impacto Positivo Moderado {formatar_pais(selected_location)}
            
            - Redução modesta de **{reducao_taxa:.1f}%**
            - Outros fatores também influenciam (medidas sanitárias, variantes)
            - A vacinação continua sendo essencial para proteção individual
            """)
            
            st.markdown("""
            <div style='background: rgba(102, 126, 234, 0.15); padding: 15px; border-radius: 10px; margin: 10px 0;'>
            
            💡 **Lembre-se:** A vacina protege contra MORTE, não contra infecção.
            
            Mesmo com impacto moderado na taxa geral, cada vida salva importa!
            
            </div>
            """, unsafe_allow_html=True)
            
        else:
            st.warning(f"""
            ### ⚠️ Contexto Importante {formatar_pais(selected_location)}
            
            **Por que o aumento nas mortes após vacinação?**
            
            🦠 **Variantes mais letais:** Delta e Ômicron surgiram APÓS o início da vacinação
            ⏰ **Tempo de imunização:** Leva semanas para a população desenvolver imunidade
            📈 **Ondas subsequentes:** Países enfrentaram novas ondas durante a vacinação inicial
            🌍 **Contexto global:** Transmissão comunitária alta durante início da vacinação
            
            **✅ Importante:** Estudos globais confirmam que a vacinação salvou MILHÕES de vidas ao longo do tempo!
            """)
            
            st.markdown("""
            <div style='background: rgba(255, 149, 0, 0.15); padding: 15px; border-radius: 10px; margin: 10px 0;'>
            
            ### 🔍 Por que parece que não funcionou aqui?
            
            **1. Timing:** Vacinação começou durante pico de casos
            **2. Cobertura:** Leva meses para vacinar população inteira
            **3. Variantes:** Surgiram versões mais perigosas do vírus
            
            **MAS ATENÇÃO:** Isso NÃO significa que a vacina não funciona!
            
            Em TODOS os países, estudos mostram que:
            - 🏥 Vacinados têm 90%+ menos risco de morte
            - 💉 Hospitalizações graves caíram drasticamente
            - 🌍 Países com alta vacinação controlaram a pandemia
            
            **A vacina salva vidas individualmente, mesmo quando os números gerais são complexos!**
            
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("ℹ️ Não há dados de vacinação disponíveis para análise.")

st.markdown("---")

# =============================================================
# NOVO: Evolução da Taxa de Mortalidade (CFR) vs Progresso da Vacinação
# =============================================================
st.subheader("🧬 Evolução da Taxa de Mortalidade vs Progresso da Vacinação")

# Calcula CFR diária e média móvel de 30 dias + progresso relativo de vacinação
if not df_filtrado.empty:
    df_cfr = df_filtrado.copy()
    # Evita divisão por zero atribuindo NaN quando new_cases == 0
    df_cfr['cfr_diaria'] = np.where(df_cfr['new_cases'] > 0, df_cfr['new_deaths'] / df_cfr['new_cases'], np.nan)
    df_cfr['cfr_mm30'] = df_cfr['cfr_diaria'].rolling(window=30, min_periods=7).mean()

    # Progresso relativo da vacinação (não é cobertura real sem população; escala 0-100%)
    max_vac = df_cfr['people_vaccinated'].max()
    if max_vac > 0:
        df_cfr['vac_progress_pct'] = df_cfr['people_vaccinated'] / max_vac * 100
    else:
        df_cfr['vac_progress_pct'] = 0

    fig_cfr = go.Figure()

    # Linha CFR média móvel
    fig_cfr.add_trace(go.Scatter(
        x=df_cfr['date'], y=df_cfr['cfr_mm30'] * 100,
        mode='lines', name='CFR Média Móvel 30d (%)',
        line=dict(color='#f093fb', width=3)
    ))

    # Linha de progresso vacinação (eixo secundário)
    fig_cfr.add_trace(go.Scatter(
        x=df_cfr['date'], y=df_cfr['vac_progress_pct'],
        mode='lines', name='Progresso Vacinação (relativo %)',
        line=dict(color='#667eea', width=2, dash='dash'),
        yaxis='y2'
    ))

    fig_cfr.update_layout(
        height=450,
        plot_bgcolor='rgba(26, 26, 46, 0.75)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        xaxis=dict(title='Data', gridcolor='rgba(128,128,128,0.15)'),
        yaxis=dict(title='CFR (%)', gridcolor='rgba(128,128,128,0.2)'),
        yaxis2=dict(title='Vacinação Relativa (%)', overlaying='y', side='right', showgrid=False)
    )

    # Linha vertical da vacinação (usando shapes)
    if pd.notna(vaccination_start):
        fig_cfr.add_shape(
            type="line",
            x0=vaccination_start, x1=vaccination_start,
            y0=0, y1=1,
            yref="paper",
            line=dict(color='orange', width=2, dash='dot')
        )
        fig_cfr.add_annotation(
            x=vaccination_start,
            y=1,
            yref="paper",
            text='Início Vacinação',
            showarrow=False,
            yshift=10,
            font=dict(color='orange', size=12)
        )

    st.plotly_chart(fig_cfr, width='stretch')

    # Correlação pós-início vacinação
    if pd.notna(vaccination_start):
        df_corr = df_cfr[df_cfr['date'] >= vaccination_start].copy()
        df_corr = df_corr.dropna(subset=['cfr_mm30'])
        if len(df_corr) > 10:
            corr_pearson = df_corr['cfr_mm30'].corr(df_corr['vac_progress_pct'])
            st.info(f"🔗 Correlação (Pearson) entre CFR média móvel e progresso relativo da vacinação: **{corr_pearson:.2f}**")
            # Scatter com linha de tendência
            fig_scatter = go.Figure()
            fig_scatter.add_trace(go.Scatter(
                x=df_corr['vac_progress_pct'], y=df_corr['cfr_mm30'] * 100,
                mode='markers', name='Observações',
                marker=dict(color='#b794f6', size=6, line=dict(color='white', width=0.5))
            ))
            # Regressão linear simples
            coef = np.polyfit(df_corr['vac_progress_pct'], df_corr['cfr_mm30'] * 100, 1)
            x_fit = np.linspace(df_corr['vac_progress_pct'].min(), df_corr['vac_progress_pct'].max(), 50)
            y_fit = coef[0]*x_fit + coef[1]
            fig_scatter.add_trace(go.Scatter(
                x=x_fit, y=y_fit,
                mode='lines', name='Tendência Linear',
                line=dict(color='#00CC96', width=2)
            ))
            fig_scatter.update_layout(
                height=400,
                plot_bgcolor='rgba(26, 26, 46, 0.75)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(title='Progresso Vacinação Relativo (%)'),
                yaxis=dict(title='CFR Média Móvel 30d (%)'),
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
            )
            st.plotly_chart(fig_scatter, width='stretch')
        else:
            st.warning('Dados insuficientes após início da vacinação para calcular correlação confiável.')
    else:
        st.warning('Sem data de início de vacinação para correlação.')

st.markdown("---")

# Comparação 6 meses
st.markdown("""
<h2 style='text-align: center; margin: 40px 0;'>
    ⚖️ Comparação: 6 Meses Antes vs Depois
</h2>
<p style='text-align: center; color: #888; font-size: 1.1rem;'>
    Análise de períodos equivalentes para medir o impacto real da vacinação
</p>
""", unsafe_allow_html=True)

if pd.notna(vaccination_start):
    df_6m_antes = df_filtrado[
        (df_filtrado['date'] >= vaccination_start - pd.Timedelta(days=180)) & 
        (df_filtrado['date'] < vaccination_start)
    ]
    df_6m_depois = df_filtrado[
        (df_filtrado['date'] >= vaccination_start) & 
        (df_filtrado['date'] <= vaccination_start + pd.Timedelta(days=180))
    ]
    
    if not df_6m_antes.empty and not df_6m_depois.empty:
        mortes_media_antes = df_6m_antes['new_deaths'].mean()
        mortes_media_depois = df_6m_depois['new_deaths'].mean()
        
        if mortes_media_antes > 0:
            reducao_percentual = ((mortes_media_antes - mortes_media_depois) / mortes_media_antes) * 100
        else:
            reducao_percentual = 0
        
        vidas_salvas = (mortes_media_antes - mortes_media_depois) * 180
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("⚰️ Mortes/Dia (6m ANTES)", f"{mortes_media_antes:.0f}")
        
        with col2:
            delta_text = f"-{reducao_percentual:.1f}%" if reducao_percentual > 0 else f"+{abs(reducao_percentual):.1f}%"
            st.metric(
                "💚 Mortes/Dia (6m DEPOIS)",
                f"{mortes_media_depois:.0f}",
                delta=delta_text,
                delta_color="normal" if reducao_percentual > 0 else "inverse"
            )
        
        with col3:
            if vidas_salvas > 0:
                st.metric("💚 Vidas Salvas (Est.)", f"{abs(int(vidas_salvas)):,}")
            else:
                st.metric("⚠️ Impacto", f"{abs(int(vidas_salvas)):,}", delta="Variantes")
        
        # Gráfico de barras
        fig_simples = go.Figure()
        
        fig_simples.add_trace(go.Bar(
            x=['6 Meses ANTES', '6 Meses DEPOIS'],
            y=[mortes_media_antes, mortes_media_depois],
            marker=dict(color=['#EF553B', '#00CC96']),
            text=[f'{mortes_media_antes:.0f}', f'{mortes_media_depois:.0f}'],
            textposition='auto'
        ))
        
        if reducao_percentual > 0:
            fig_simples.add_annotation(
                x=0.5,
                y=max(mortes_media_antes, mortes_media_depois) * 0.7,
                text=f"↓ REDUÇÃO DE {abs(reducao_percentual):.1f}% ↓",
                showarrow=False,
                font=dict(size=20, color='#00ff88'),
                bgcolor='rgba(0,0,0,0.7)'
            )
        
        fig_simples.update_layout(
            yaxis_title='Média de Mortes Diárias',
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(26, 26, 46, 0.8)',
            font=dict(color='white'),
            height=500
        )
        
        st.plotly_chart(fig_simples, width='stretch')
        
        # NOVO: Gráfico de LINHA comparando os 2 períodos
        st.markdown("### 📊 Comparação Detalhada: Antes vs Depois")
        
        fig_comparacao = go.Figure()
        
        # Período ANTES (vermelho)
        df_antes_plot = df_6m_antes.copy()
        df_antes_plot['dias_relativos'] = (df_antes_plot['date'] - vaccination_start).dt.days
        
        fig_comparacao.add_trace(go.Scatter(
            x=df_antes_plot['dias_relativos'],
            y=df_antes_plot['new_deaths'],
            mode='lines',
            name='6 Meses ANTES',
            line=dict(color='#EF553B', width=2),
            fill='tozeroy',
            fillcolor='rgba(239, 85, 59, 0.2)'
        ))
        
        # Período DEPOIS (verde)
        df_depois_plot = df_6m_depois.copy()
        df_depois_plot['dias_relativos'] = (df_depois_plot['date'] - vaccination_start).dt.days
        
        fig_comparacao.add_trace(go.Scatter(
            x=df_depois_plot['dias_relativos'],
            y=df_depois_plot['new_deaths'],
            mode='lines',
            name='6 Meses DEPOIS',
            line=dict(color='#00CC96', width=2),
            fill='tozeroy',
            fillcolor='rgba(0, 204, 150, 0.2)'
        ))
        
        fig_comparacao.update_layout(
            height=400,
            plot_bgcolor='rgb(17,17,17)',
            paper_bgcolor='rgb(17,17,17)',
            font=dict(color='white'),
            xaxis=dict(
                title='Dias (relativos ao início da vacinação)',
                gridcolor='rgba(128,128,128,0.2)',
                zeroline=True,
                zerolinecolor='#FF9500',
                zerolinewidth=2
            ),
            yaxis=dict(title='Mortes Diárias', gridcolor='rgba(128,128,128,0.2)'),
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        # Linha vertical no dia da vacinação (x=0 é o marco referência)
        fig_comparacao.add_shape(
            type="line",
            x0=0, x1=0,
            y0=0, y1=1,
            yref="paper",
            line=dict(color='#FF9500', width=3, dash='solid')
        )
        fig_comparacao.add_annotation(
            x=0,
            y=1,
            yref="paper",
            text="Vacinação Inicia",
            showarrow=False,
            yshift=10,
            font=dict(color='#FF9500', size=12)
        )
        
        st.plotly_chart(fig_comparacao, width='stretch')
        
        st.info("""
        📊 **Interpretação:** Este gráfico sobrepõe os dois períodos de 6 meses.
        - 🔴 **Vermelho:** 180 dias ANTES da vacinação
        - 🟢 **Verde:** 180 dias DEPOIS da vacinação
        - 🟠 **Linha vertical:** Marco zero = Início da vacinação
        """)
        
        st.markdown("---")
        
        if reducao_percentual > 5:
            st.success(f"""
            ### ✅ IMPACTO POSITIVO COMPROVADO
            
            - 🎯 Redução de **{abs(reducao_percentual):.1f}%**
            - 💚 Aproximadamente **{abs(int(vidas_salvas)):,} vidas salvas**
            
            **🏆 A VACINAÇÃO SALVOU VIDAS!**
            """)

st.markdown("---")

# ========================================
# SEÇÃO COMPARATIVA: BRASIL vs OUTROS PAÍSES
# ========================================
st.header("🌍 Análise Comparativa: Brasil vs Mundo")

st.markdown("""
Esta seção compara o **início da vacinação** e a **taxa de mortalidade** entre diferentes países,
evidenciando o **impacto do atraso** no calendário vacinal brasileiro.
""")

# Calcular início da vacinação para cada país
paises_analise = []

for pais_pt in lista_paises:
    if pais_pt == 'Mundo':
        continue
    
    pais_en = traducao_inversa.get(pais_pt, pais_pt)
    df_pais = df[df['location'] == pais_en].copy()
    
    if df_pais.empty:
        continue
    
    vacinacao_inicio = df_pais[df_pais['people_vaccinated'] > 0]['date'].min()
    
    if pd.notna(vacinacao_inicio):
        df_antes = df_pais[df_pais['date'] < vacinacao_inicio]
        df_depois = df_pais[
            (df_pais['date'] >= vacinacao_inicio) & 
            (df_pais['date'] <= vacinacao_inicio + pd.Timedelta(days=180))
        ]
        
        mortes_antes = df_antes['total_deaths'].max() if not df_antes.empty else 0
        mortes_depois_inicio = df_depois['total_deaths'].iloc[0] if not df_depois.empty else mortes_antes
        mortes_depois_fim = df_depois['total_deaths'].max() if not df_depois.empty else mortes_antes
        
        novas_mortes_pos_vac = mortes_depois_fim - mortes_depois_inicio
        dias_pos_vac = len(df_depois)
        taxa_mortalidade_pos_vac = novas_mortes_pos_vac / dias_pos_vac if dias_pos_vac > 0 else 0
        
        paises_analise.append({
            'País': pais_pt,
            'Início Vacinação': vacinacao_inicio,
            'Mortes Antes': int(mortes_antes),
            'Taxa Mortes/Dia (Pós-Vac)': round(taxa_mortalidade_pos_vac, 1),
            'Total Mortes': int(df_pais['total_deaths'].max())
        })

df_comparativo = pd.DataFrame(paises_analise)

if not df_comparativo.empty:
    df_comparativo = df_comparativo.sort_values('Início Vacinação')
    df_comparativo['Início Vacinação'] = df_comparativo['Início Vacinação'].dt.strftime('%d/%m/%Y')
    
    st.subheader("📊 Tabela Comparativa: Início da Vacinação por País")
    
    def highlight_brazil(row):
        if row['País'] == 'Brasil':
            return ['background-color: #ffcccc'] * len(row)
        return [''] * len(row)
    
    st.dataframe(
        df_comparativo.style.apply(highlight_brazil, axis=1),
        width='stretch',
        hide_index=True
    )
    
    # Análise do Brasil
    st.markdown("---")
    st.subheader("🇧🇷 O Caso do Brasil: Análise do Atraso Vacinal")
    
    brasil_data = df_comparativo[df_comparativo['País'] == 'Brasil']
    
    if not brasil_data.empty:
        brasil_inicio = pd.to_datetime(brasil_data['Início Vacinação'].iloc[0], format='%d/%m/%Y')
        brasil_mortes_antes = brasil_data['Mortes Antes'].iloc[0]
        brasil_taxa_pos = brasil_data['Taxa Mortes/Dia (Pós-Vac)'].iloc[0]
        
        df_temp = pd.DataFrame(paises_analise)
        paises_antes = df_temp[df_temp['Início Vacinação'] < brasil_inicio].sort_values('Início Vacinação')
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🇧🇷 Brasil - Início", brasil_inicio.strftime('%d/%m/%Y'))
        
        with col2:
            st.metric("⚰️ Mortes Antes", f"{brasil_mortes_antes:,}")
        
        with col3:
            if not paises_antes.empty:
                primeiro_pais = paises_antes.iloc[0]
                dias_atraso = (brasil_inicio - primeiro_pais['Início Vacinação']).days
                st.metric(
                    f"⏰ Atraso vs {primeiro_pais['País']}",
                    f"{dias_atraso} dias",
                    delta=f"{dias_atraso} dias de atraso",
                    delta_color="inverse"
                )
        
        st.markdown("---")
        
        st.error(f"""
        ### ⚠️ Contexto Histórico
        
        **O Brasil teve um atraso de {dias_atraso if not paises_antes.empty else 'dezenas de'} dias** em relação aos primeiros países.
        
        **Consequências:**
        - ⚰️ Até o início da vacinação: **{brasil_mortes_antes:,} mortes**
        - 📊 Países que vacinaram cedo controlaram melhor a mortalidade
        - 🦠 Circulação prolongada favoreceu novas variantes
        """)
        
        if not paises_antes.empty:
            st.markdown("### 📈 Comparação com Países Pioneiros")
            
            for _, pais_cedo in paises_antes.head(5).iterrows():
                dias_diferenca = (brasil_inicio - pais_cedo['Início Vacinação']).days
                reducao_taxa = ((brasil_taxa_pos - pais_cedo['Taxa Mortes/Dia (Pós-Vac)']) / brasil_taxa_pos * 100) if brasil_taxa_pos > 0 else 0
                
                st.info(f"""
                **{pais_cedo['País']}** começou em **{pais_cedo['Início Vacinação'].strftime('%d/%m/%Y')}**
                - ✅ **{dias_diferenca} dias ANTES** do Brasil
                - 📉 Taxa pós-vacinação: **{pais_cedo['Taxa Mortes/Dia (Pós-Vac)']:.1f} mortes/dia**
                - 🎯 Diferença: **{abs(reducao_taxa):.1f}%** {'menor' if reducao_taxa > 0 else 'maior'}
                """)

st.markdown("---")

# ========================================
# SEÇÃO: NEGACIONISMO E IMPACTO NA SAÚDE PÚBLICA
# ========================================
st.header("🚨 O Custo do Negacionismo Científico")

st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 30px; border-radius: 15px; margin: 20px 0;'>
    <h3 style='color: white; margin: 0 0 20px 0;'>⚠️ Como a Desinformação Custou Vidas</h3>
    <p style='color: white; font-size: 16px; line-height: 1.8;'>
        Durante a pandemia de COVID-19, o <b>negacionismo científico</b> e a <b>desinformação</b> 
        tiveram impacto direto no número de mortes evitáveis. Este dashboard mostra claramente 
        que <b>países que adotaram a vacinação mais cedo salvaram mais vidas</b>.
    </p>
</div>
""", unsafe_allow_html=True)

col_neg1, col_neg2 = st.columns(2)

with col_neg1:
    st.error("""
    ### 🚫 Narrativas Negacionistas
    
    **Mitos que custaram vidas:**
    
    1. **"A vacina foi desenvolvida rápido demais"**
       - ❌ FALSO: Tecnologia mRNA estava em desenvolvimento há 30+ anos
       
    2. **"Vacinas causam mais mortes que a doença"**
       - ❌ FALSO: Dados globais mostram redução de 90%+ em mortes
       
    3. **"Imunidade natural é melhor"**
       - ❌ FALSO: Risco de morte 11x maior sem vacina
       
    4. **"É apenas uma gripezinha"**
       - ❌ FALSO: 7+ milhões de mortes globais
    """)

with col_neg2:
    st.success("""
    ### ✅ Evidências Científicas
    
    **O que os dados REALMENTE mostram:**
    
    1. **Vacinas são seguras e eficazes**
       - ✅ Bilhões de doses aplicadas com segurança
       
    2. **Reduziram hospitalizações em 95%**
       - ✅ Comprovado em todos os países
       
    3. **Salvaram 20+ milhões de vidas em 2021**
       - ✅ Estudo publicado na The Lancet
       
    4. **Países que vacinaram cedo venceram**
       - ✅ Veja a tabela comparativa abaixo
    """)

st.markdown("---")

# Impacto específico no Brasil
st.subheader("🇧🇷 O Caso Brasileiro: Negacionismo Governamental")

st.warning("""
### ⚠️ Cronologia do Negacionismo no Brasil

**2020:**
- 🚫 Março: Presidente chama COVID de "gripezinha"
- 🚫 Julho-Dezembro: Governo recusa 70 milhões de doses da Pfizer
- 🚫 Outubro: "Quem é de direita toma cloroquina"

**2021:**
- 🚫 Janeiro: Atraso de 2+ meses no início da vacinação
- 🚫 Março-Abril: Colapso hospitalar em Manaus
- ⚰️ Resultado: 400+ mil mortes evitáveis segundo estudos

**Consequências Mensuráveis:**
- 📊 Brasil teve uma das maiores taxas de mortalidade per capita
- ⏰ Atraso vacinal custou milhares de vidas (veja tabela abaixo)
- 🦠 Negligência favoreceu surgimento de variantes (Gamma/P.1)
""")

st.markdown("---")

# ========================================
# SEÇÃO: NEGACIONISMO E SUAS CONSEQUÊNCIAS
# ========================================
st.header("⚠️ Negacionismo Científico e Suas Consequências Fatais")

st.markdown("""
<div style='background: linear-gradient(135deg, rgba(239, 85, 59, 0.2), rgba(239, 85, 59, 0.1)); 
            padding: 20px; border-radius: 15px; border-left: 5px solid #EF553B;'>
    
### 🚫 O Papel do Negacionismo na Pandemia

Durante a pandemia de COVID-19, o **negacionismo científico** teve consequências devastadoras:

</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### 📉 Impactos Diretos do Negacionismo:
    
    - **🦠 Minimização da gravidade:** Tratamento da COVID-19 como "gripezinha"
    - **💉 Recusa de vacinas:** Campanhas anti-vacina sem base científica
    - **😷 Rejeição de máscaras:** Desconsideração de medidas de proteção
    - **🏥 Descrédito da ciência:** Ataques a instituições científicas
    - **💊 Promoção de "tratamentos milagrosos":** Medicamentos sem eficácia comprovada
    - **📊 Distorção de dados:** Manipulação de estatísticas oficiais
    """)

with col2:
    st.markdown("""
    #### ⚰️ Consequências Mensuráveis:
    
    - **Atraso na vacinação:** Países que adotaram políticas negacionistas vacinaram mais tarde
    - **Mortes evitáveis:** Milhares de mortes que poderiam ter sido prevenidas
    - **Colapso hospitalar:** Sistemas de saúde sobrecarregados desnecessariamente
    - **Desigualdade:** Populações vulneráveis mais afetadas
    - **Circulação prolongada:** Favorecimento do surgimento de novas variantes
    - **Trauma coletivo:** Impacto psicológico e social duradouro
    """)

st.error("""
### 🎯 Lições da Pandemia

**O que os dados nos mostram:**

1. **📊 Países com políticas baseadas em ciência** tiveram melhores resultados
2. **💉 Vacinação em massa salvou milhões de vidas** globalmente
3. **⏰ Cada dia de atraso na vacinação** custou vidas
4. **🔬 Ciência funcionou:** Vacinas foram desenvolvidas em tempo recorde
5. **⚠️ Negacionismo matou:** Rejeitar a ciência teve consequências fatais

**A evidência é clara: seguir a ciência salva vidas. Negar a ciência custa vidas.**
""")

st.markdown("---")

# Conclusão Final
st.header("🎯 Conclusões Principais")

col1, col2 = st.columns(2)

with col1:
    st.success("""
    ### ✅ Evidências da Vacinação
    
    **O dashboard demonstra:**
    
    1. 💉 Início claro da vacinação marcado
    2. 📉 Redução na média de mortes
    3. 📊 Desaceleração da curva
    4. 🎯 Impacto quantificável
    """)

with col2:
    st.info("""
    ### � Limitações Reconhecidas
    
    **Importante considerar:**
    
    - Correlação ≠ Causalidade
    - Análise descritiva
    - Múltiplas variáveis
    - Contexto específico de cada país
    """)

st.markdown("""
---
### 🌟 Mensagem Final

Os dados demonstram claramente que **a vacinação está associada à redução de mortes** por COVID-19. 

A linha laranja nos gráficos marca um divisor: **antes e depois da vacinação**. 
A mudança no padrão de mortalidade é visível e representa vidas salvas.

💡 **Continue vacinado e proteja quem você ama.**
""")

st.markdown("---")

# Rodapé
st.caption("�📊 **Fonte:** Our World in Data (OWID)")
st.caption("🛠️ **Tecnologias:** Streamlit, Pandas e Plotly")
st.caption("📅 **Última atualização:** " + df['date'].max().strftime('%d/%m/%Y'))
