import streamlit as st
from utils import return_models, inicialize_variables


st.set_page_config(page_title="Informações", page_icon=r"C:\Users\yamim\OneDrive\Documentos\App Streamlit Projeto Predição Dias Atrasados\Imgs\Home_PageIcon1.png", layout="wide")

inicialize_variables()

exibition = st.selectbox('Selecione uma exibição: ', ['Informações técnicas dos modelos', 'Sobre os Dados'], key='exibition_pag_info')

st.title('Informações sobre dos modelos utilizados')



col_inst_hiper_metr, col_ranking_otm, col_saiba_mais = st.columns(3)


with col_inst_hiper_metr:
    if st.button('Instaciamento, HiperParâmetros e Métricas', key='inst_hiper_metr_btn'):
        st.session_state['active_button'] = 'inst_hiper_metr'

with col_ranking_otm:
    if st.button('Ranking e Otimismo', key='ranking_otm', use_container_width=True):
        st.session_state['active_button'] = 'ranking_otm'


with col_saiba_mais:
    if st.button('Saiba mais sobre os algoritmos', key='saiba_mais_btn'):
        st.session_state['active_button'] = 'saiba_mais'

st.markdown('---')


models_names_n_todos = [type(model).__name__ for model in return_models()]

models_names_n_todos = list(set(models_names_n_todos))

models_names_n_todos.insert(0, 'Todos')

options = {}

col_options_models_info1, col_options_models_info2 = st.columns(2)

for idx, option in enumerate(models_names_n_todos):

    if idx % 2 == 0:
        options[option] = col_options_models_info1.checkbox(option)

    else:
        options[option] = col_options_models_info2.checkbox(option)

st.markdown('---')



if st.session_state['active_button'] == 'inst_hiper_metr':

    st.subheader('Instaciamento, HiperParâmetros e Métricas')

    options_selected = []

    for option, state in  options.items():

        if state:
            options_selected.append(option)

    if options_selected == ['Todos']:

        st.write("Você selecionou todos os modelos.")
        for model in return_models():
            st.write(f"Modelo: {type(model).__name__}")
            st.markdown(f"`{model}`")
            st.markdown("---")

    elif 'Todos' in options_selected:
        st.error('Você só pode selecionar "Todos" se for a única opção selecionada.')
    
    else:

        for model_name in options_selected:
                
                for model in return_models():

                    parametros = f'{model}'.split('(')[1]
                    parametros = parametros.split(')')[0]

                    if type(model).__name__ == model_name and (parametros == '' or parametros == 'random_state=42'):

                        st.write('Modelo: ', model_name)
                        st.markdown(f"`{model}`")

                        st.markdown('**-Métricas-**')
                        st.write('...')

                        st.markdown('---')
                    
                    elif type(model).__name__ == model_name:
                         
                        st.write('Modelo: ', model_name, ' - Com Otimização de HiperParâmetros')
                        st.markdown(f"`{model}`")

                        st.markdown('**-Métricas-**')
                        st.write('...')

                        st.markdown('---')
                    

elif st.session_state['active_button'] == 'ranking_otm':
    st.subheader('Ranking e Otimismo dos modelos')
    st.write('Nada por aqui...')
 


elif st.session_state['active_button'] == 'saiba_mais':
    st.subheader('Saiba mais sobre os algoritmos')
    st.write('Nada por aqui...')

else:
    st.subheader('O que você quer ver?')