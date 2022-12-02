import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
import plotly.express as px

dados_copa = pd.read_csv('data\dados_copa.csv')
selecoes = dados_copa['Selecao'].sort_values().unique()

st.title(':trophy: Copa do mundo 2022 :trophy:')

with st.sidebar:
    menu = st.selectbox('Menu', options = ['Seleções', 'Gráficos'])

if menu == 'Seleções':
    escolha = st.selectbox('Escolha o país', selecoes)

    dados_filtrados = dados_copa[dados_copa['Selecao'] == escolha]

    st.image(dados_filtrados['URL'].iloc[0], caption = escolha)

    st.header('Goleiros')

    st.table(dados_filtrados[dados_filtrados['Posicao']=='GK'][['Posicao','Jogador', 'Idade', 'Time']].reset_index(drop = True))

    st.header('Defensores')

    st.table(dados_filtrados[dados_filtrados['Posicao'].str.startswith('DF')][['Posicao','Jogador', 'Idade', 'Time']].reset_index(drop = True))

    st.header('Meio-campos')

    st.table(dados_filtrados[dados_filtrados['Posicao'].str.startswith('MF')][['Posicao','Jogador', 'Idade', 'Time']].reset_index(drop = True))

    st.header('Atacantes')

    st.table(dados_filtrados[dados_filtrados['Posicao'].str.startswith('FW')][['Posicao','Jogador', 'Idade', 'Time']].reset_index(drop = True))

if menu == 'Gráficos':
    col1, col2 = st.columns(2)
    with col1:
        filtros = st.multiselect('Filtrar por país', options= selecoes)
    with col2:
        numero_times = st.slider(label = 'Selecione a quantidade de times', min_value = 5, max_value = 15)
    if filtros:
        dados_copa = dados_copa[dados_copa['Selecao'].isin(filtros)]
    
    times_com_mais_jogadores = pd.DataFrame(dados_copa['Time'].value_counts(ascending=False)).reset_index(names='Times').head(numero_times)
    times_com_mais_jogadores.rename(columns = {'Time': 'Quantidade'}, inplace = True)
    fig1 = ff.create_table(times_com_mais_jogadores)
    fig2 = px.bar(times_com_mais_jogadores, x = 'Times', y ='Quantidade', 
                    title = f'Top {numero_times} times com mais jogadores em seleções',
                    text='Quantidade', template='simple_white')

    st.plotly_chart(fig2)           
    st.plotly_chart(fig1)