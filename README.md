# Previsor de Atrasos na Produção

Bem-vindo ao **Previsor de Atrasos na Produção**! Este aplicativo é uma ferramenta poderosa e intuitiva que utiliza **modelos preditivos** para ajudar na tomada de decisões, oferecendo estimativas confiáveis sobre atrasos na produção de itens.

**Obs:** o App ainda não está documentado, devido a situação em que foi desenvolvido, em breve será resolvido.

## O que este app faz?

- **Previsão de atrasos**: Insira as informações do item (código, quantidade e processo) e obtenha a estimativa de dias de atraso.
- **Análise de modelos**: Visualize métricas como MAE, MSE e RMSE para entender o desempenho de cada modelo.
- **Dados históricos**: Explore as médias de atrasos para automação e prestadores com tabelas e gráficos.
- **Comparativos visuais**: Compare previsões de diferentes modelos e veja as estatísticas descritivas detalhadas.

---

## Como usar?

### 1. **Home**
Na página inicial:
- Leia uma breve descrição do projeto.
- Descubra as principais funcionalidades do app.
- Navegue para as páginas de Predições ou Informações.

### 2. **Predições**
- Insira os dados necessários para predição.
- Escolha entre **"Resumo"** ou **"Detalhes"** para exibir os resultados.
- Compare os montadores automação e prestador com métricas e gráficos interativos.
- Visualize tabelas de previsão de todos os modelos e estatísticas descritivas.

### 3. **Informações**
- Explore detalhes sobre os modelos usados, incluindo seus hiperparâmetros e métricas de desempenho.
- Veja explicações intuitivas sobre cada modelo.
- Descubra o ranking dos melhores modelos com base em métricas como MAE, MSE e RMSE.
- Analise o "otimismo" e "pessimismo" dos modelos nas previsões.

---

## Principais Modelos Utilizados
- **KNeighborsRegressor**
- **ElasticNet**
- **LGBMRegressor**
- **DecisionTreeRegressor**
- **MLPRegressor** (Rede Neural)
- Outros modelos robustos e otimizados para alta precisão.

---

## Dados Utilizados
- **Entrada**: Dados como código do item, quantidade e processo de produção.
- **Saída**: Previsões de atraso (em dias), com visualizações e comparações detalhadas.

---

## Tecnologias e Ferramentas
- **Linguagem**: Python
- **Framework**: Streamlit
- **Gráficos**: Plotly
- **Bibliotecas**: pandas, scikit-learn, LightGBM

---

## Como executar o app localmente?
1. Clone este repositório:
   ```bash
   git clone https://github.com/ju-sants/automacao-Global-System.git
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Inicie o aplicativo:
   ```bash
   streamlit run Home.py
   ```
4. Acesse o app no navegador:
   ```
   http://localhost:8501
   ```

---

## Autor
Criado por **Juan**. Se tiver dúvidas ou sugestões, fique à vontade para entrar em contato!

---

**Aproveite o app e tome decisões mais inteligentes na sua produção!**

