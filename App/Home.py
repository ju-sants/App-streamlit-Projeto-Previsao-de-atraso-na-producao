import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração inicial
st.set_page_config(
    page_title="Home",
    page_icon="App/Imgs/Home_PageIcon1.png",
    layout="wide"
)

# Título principal
st.title("Bem-vindo ao Previsor de Atrasos na Produção 🎯")

# Subtítulo
st.header("📊 Gerencie sua produção com precisão e eficiência!")

# Divisão em colunas para o texto introdutório
col1, col2 = st.columns(2)

with col1:
    st.write("""
    Nossa ferramenta utiliza modelos preditivos avançados para estimar atrasos na produção de itens com base em:
    - **Código do item**
    - **Quantidade**
    - **Processo de produção**
    
    Com essas previsões, você pode tomar decisões mais informadas, reduzir custos e evitar gargalos. 🚀
    """)
    
with col2:
    st.image("App/Imgs/Home_PageIcon1.png", use_container_width=True)

# Separador visual
st.markdown("---")

# Funcionalidades principais
st.header("🔍 Funcionalidades do Aplicativo")
st.markdown("""
1. **Predição de Atrasos**: Estime atrasos com base em características dos itens e modelos avançados.
2. **Análise de Modelos**: Explore métricas como MAE, MSE e RMSE para entender o desempenho dos modelos.
3. **Dados Históricos**: Consulte médias de atrasos para montadores automação e prestadores.
4. **Comparações Visuais**: Use gráficos e tabelas para insights rápidos e objetivos.
""")

# Gráfico resumido com dados históricos
try:
    tabela_medias_auto = pd.read_csv('App/Data_2_app/Tabelas/tabela_medias_produto_automacao.csv')
    tabela_medias_prest = pd.read_csv('App/Data_2_app/Tabelas/tabela_medias_produto_prestador.csv')

    st.subheader("📈 Resumo das Médias de Atraso")
    col_auto, col_prest = st.columns(2)

    with col_auto:
        st.write("**Automação**")
        fig_auto = px.bar(tabela_medias_auto, x="ITEM UNIFICADO", y="media_dias", title="Média de Atrasos - Automação")
        st.plotly_chart(fig_auto, use_container_width=True)

    with col_prest:
        st.write("**Prestador**")
        fig_prest = px.bar(tabela_medias_prest, x="ITEM UNIFICADO", y="media_dias", title="Média de Atrasos - Prestador")
        st.plotly_chart(fig_prest, use_container_width=True)

except FileNotFoundError:
    st.warning("⚠️ Arquivos de dados históricos não encontrados. Faça predições para gerar os dados!")

# Links para navegação
st.markdown("---")
st.header("📂 Acesse as Funcionalidades")
st.markdown("""
- [Página de Predições](./Página_de_Predição)
- [Informações e Métricas dos Modelos](./Informações)
""")

# Rodapé
st.sidebar.title("Menu")
st.sidebar.markdown("""
- **Home**
- [Predições](./Página_de_Predição)
- [Informações](./Informações)
""")
