import streamlit as st

st.set_page_config(page_title="Home", page_icon=r"C:\Users\yamim\OneDrive\Documentos\App Streamlit Projeto Predição Dias Atrasados\Imgs\Home_PageIcon1.png", layout="wide")

st.title('Descrição do Projeto')

st.header('Bem Vindo!')

coluna_texto_corpo1, coluna_texto_corpo2 = st.columns(2)

coluna_texto_corpo1.write('Bem-vindo à nossa ferramenta de previsão de atraso na produção!\n'
         'Com essa ferramenta, você pode prever o atraso na produção de um item com base em seu código, quantidade e processo de produção.\n'
        'Basta inserir as informações do item e clicar em "Prever" para obter uma estimativa do atraso em dias.\n')


coluna_texto_corpo2.write('Esperamos que essa ferramenta ajude você a planejar sua produção de forma mais eficiente e evitar atrasos.\n'    
        'Para saber a média de dias de atraso por item, acesse a página:\n'
        'Para acessar a página de predições, preencha o formulário: ')

st.sidebar.title('Menu')