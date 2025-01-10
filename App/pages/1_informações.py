import streamlit as st
from utils import return_models, inicialize_variables, return_metrics_dfs, return_models_exp

st.set_page_config(page_title="Informações", page_icon=r"C:\Users\yamim\OneDrive\Documentos\App Streamlit Projeto Predição Dias Atrasados\Imgs\Home_PageIcon1.png", layout="wide")

inicialize_variables()

st.title('Informações, dados e estatísticas')

exibition = st.selectbox('Selecione uma exibição: ', ['Informações técnicas dos modelos', 'Sobre os Dados'], key='exibition_pag_info')

st.subheader('Informações sobre dos modelos utilizados')

# ----------------- Checkboxes com os nomes dos modelos

models_names_n_todos = [type(model).__name__ for model in return_models()]

models_names_n_todos = list(set(models_names_n_todos))

models_names_n_todos.insert(0, 'Todos')

options = {}

col_options_models_info1, col_options_models_info2 = st.columns(2)

for idx, option in enumerate(models_names_n_todos):

    if idx % 2 == 0:
        if option == 'Todos':
            options[option] = col_options_models_info1.checkbox(option, value=True) # Deixando a opção todos selecionada previamente
        
        else:
            options[option] = col_options_models_info1.checkbox(option)

    else:
        options[option] = col_options_models_info2.checkbox(option)


# -------------- Páginas de informações ----------------------

tab_inst_hiper_metr, tab_ranking_otm, tab_saiba_mais = st.tabs(['Instaciamento, HiperParâmetros e Métricas', 'Ranking e Otimismo', 'Saiba mais sobre os algoritmos'])

st.markdown('---')

# ---------------- armazenando opçoes escolhidas ----------------

options_selected = []

for option, state in  options.items():

    if state:
        options_selected.append(option)


# --------------------- Tratamento de inconsistências -----------------------

if 'Todos' in options_selected and len(options_selected) > 1:
    st.error('Você só pode selecionar "Todos" se for a única opção selecionada.')


# ---------------- Inserindo informações nas páginas ---------------------
else:
    with tab_inst_hiper_metr:
        st.success("""
            - A MAE (Mean Absolute Error) calcula a média dos erros absolutos entre as previsões (𝑦^y^) e os valores reais (𝑦 y) sendo fácil de interpretar, pois está na mesma escala dos dados e trata todos os erros de forma uniforme.
            - A MSE (Mean Squared Error) usa o quadrado dos erros, penalizando mais os erros grandes, o que é útil quando discrepâncias maiores têm maior impacto no problema. No entanto, como os valores ficam em unidades quadradas, pode ser menos intuitivo.
            - A RMSE (Root Mean Squared Error) é a raiz quadrada da MSE, trazendo os erros de volta à escala original dos dados, mas mantendo a penalização maior para erros grandes. A escolha entre elas depende do quanto você quer penalizar erros maiores e da necessidade de interpretar os valores diretamente na escala dos dados.
            """)
        st.markdown('---')

    if options_selected == ['Todos']:
        st.write("Você selecionou todos os modelos.")
        with tab_inst_hiper_metr:
            for model in return_models():
                parametros = f'{model}'.split('(')[1]
                parametros = parametros.split(')')[0]

                if parametros == '' or parametros == 'random_state=42':
                    st.write(f"Modelo: {type(model).__name__}")
                    st.markdown(f"`{model}`")

                    st.markdown('&nbsp;', unsafe_allow_html=True)
                    st.markdown('***Métricas do modelo***')

                    st.write(return_metrics_dfs()[type(model).__name__])

                else:
                    st.write(f"Modelo: {type(model).__name__} - Com Otimização de HiperParâmetros")
                    st.markdown(f"`{model}`")

                    st.markdown('&nbsp;', unsafe_allow_html=True)
                    st.markdown('***Métricas do modelo***')

                    st.write(return_metrics_dfs()[f'{type(model).__name__} - tunned'])

                st.markdown("---")

        with tab_saiba_mais:
            models_names = []
            for model in return_models():
                models_names.append(type(model).__name__)
            
            for unique_model_name in set(models_names):
                st.success(return_models_exp()[unique_model_name])
    else:
        with tab_inst_hiper_metr:
            for model_name in options_selected:
                for model in return_models():
                    if type(model).__name__ == model_name:
                        parametros = f'{model}'.split('(')[1]
                        parametros = parametros.split(')')[0]

                        if parametros == '' or parametros == 'random_state=42':
                            st.write(f"Modelo: {type(model).__name__}")
                            st.markdown(f"`{model}`")

                            st.markdown('&nbsp;', unsafe_allow_html=True)
                            st.markdown('***Métricas do modelo***')


                            st.write(return_metrics_dfs()[type(model).__name__])

                            st.markdown('---')

                        else:
                            st.write(f"Modelo: {type(model).__name__} - Com Otimização de HiperParâmetros")
                            st.markdown(f"`{model}`")

                            st.markdown('&nbsp;', unsafe_allow_html=True)
                            st.markdown('***Métricas do modelo***')


                            st.write(return_metrics_dfs()[f'{type(model).__name__} - tunned'])

                            st.markdown('---')



        with tab_saiba_mais:
            models_names = []
            
            for model_name in options_selected:
                for model in return_models():
                    if type(model).__name__ == model_name:
                        models_names.append(model_name)

            for unique_model_name in set(models_names):
                st.success(return_models_exp()[unique_model_name])

#                         st.write('Modelo: ', model_name, ' - Com Otimização de HiperParâmetros')
#                         st.markdown(f"`{model}`")

#                         st.markdown('**-Métricas-**')
#                         st.write(return_metrics_dfs()[f"{model_name} - tunned"])

#                         st.markdown('---')
                    

# elif st.session_state['active_button'] == 'ranking_otm':
#     st.subheader('Ranking e Otimismo dos modelos')
#     st.write('Nada por aqui...')# if st.session_state['active_button'] == 'inst_hiper_metr':

#     st.subheader('Instaciamento, HiperParâmetros e Métricas')

    

#     if options_selected == ['Todos']:

#         st.write("Você selecionou todos os modelos.")
#         for model in return_models():
#             parametros = f'{model}'.split('(')[1]
#             parametros = parametros.split(')')[0]

#             if parametros == '' or parametros == 'random_state=42':
#                 st.write(f"Modelo: {type(model).__name__}")
#                 st.markdown(f"`{model}`")

#                 st.markdown('**-Métricas-**')

#                 st.write(return_metrics_dfs()[type(model).__name__])

#             else:
#                 st.write(f"Modelo: {type(model).__name__} - Com Otimização de HiperParâmetros")
#                 st.markdown(f"`{model}`")

#                 st.markdown('**-Métricas-**')

#                 st.write(return_metrics_dfs()[f'{type(model).__name__} - tunned'])

#             st.markdown("---")

#     elif 'Todos' in options_selected:
#         st.error('Você só pode selecionar "Todos" se for a única opção selecionada.')
    
#     else:

#         for model_name in options_selected:
                
#                 for model in return_models():

#                     parametros = f'{model}'.split('(')[1]
#                     parametros = parametros.split(')')[0]

#                     if type(model).__name__ == model_name and (parametros == '' or parametros == 'random_state=42'):

#                         st.write('Modelo: ', model_name)
#                         st.markdown(f"`{model}`")

#                         st.markdown('**-Métricas-**')

#                         st.write(return_metrics_dfs()[model_name])

#                         st.markdown('---')
                    
#              
 


# elif st.session_state['active_button'] == 'saiba_mais':
#     st.subheader('Saiba mais sobre os algoritmos')

#     for model_name in options_selected:
                
#                 for model in return_models():

#                     st.success(return_models_exp()[model_name])

# else:
#     st.subheader('O que você quer ver?')