# Modulos
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Configuração para contar histórias (matplotlib):
plt.rcParams[ 'font.family' ] = 'monospace'
plt.rcParams[ 'font.size' ] = 8
plt.rcParams[ 'font.weight' ] = 'bold'
plt. rcParams[ 'figure.facecolor' ] = '#464545'
plt.rcParams[ 'axes.facecolor' ] = '#464545'
plt.rcParams[ 'axes.titleweight' ] = 'bold'
# plt.rcParams[ 'axes.titlecolor ' ] = 'black'
plt.rcParams[ 'axes.titlesize' ] = 9
plt.rcParams[ 'axes.labelcolor' ] ='darkgray'
plt.rcParams[ 'axes.labelweight' ] = 'bold'
plt.rcParams[ 'axes.edgecolor' ] = 'darkgray'
plt.rcParams[ 'axes.linewidth' ] = 0.2
plt.rcParams[ 'ytick. color' ] = 'darkray'
plt.rcParams[ 'xtick.color' ] = 'darkray'
plt.rcParams[ 'axes.titlecolor' ] = '#FFFFFF'
plt.rcParams[ 'axes.titlecolor' ] = 'white'
plt.rcParams[ 'axes.edgecolor' ] = 'darkray'
plt.rcParams[ 'axes.linewidth' ] = 0,85
plt.rcParams[ 'ytick.major.size' ] = 0


# --- App (início):
BR_real_estate_appreciation = pd.read_csv( 'data/BR_real_estate_appreciation_Q1_2023.csv' )
BR_real_estate_appreciation[ 'Annual_appreciation' ] = round (BR_real_estate_appreciation[ 'Annual_appreciation' ], 2 )* 100

# Configuração da página:
st.set_page_config(
    page_title= "Propriedades residenciais (Brasil)" ,
    page_icon= "🏢" ,
    layout= "centrado" ,
    initial_sidebar_state= "collapsed" ,
)

# Header:
st.header( 'Valorização de imóveis residenciais em Brasil' )

st.sidebar.markdown( ''' > **Como usar este aplicativo** 

1. Para selecionar uma cidade (**ponto verde**). 
2. Para comparar a cidade selecionada com outras 50 cidades ( **pontos brancos**) 
3. Comparar a cidade escolhida com a **média nacional** e a distribuição dos dados.
4. Extrair insights como "Uma valorização acima da média nacional + preço por metro quadrado abaixo da média = possível *oportunidade*". 
''' )

# Widgets:
cities = sorted ( list (BR_real_estate_appreciation[ 'Location' ].unique()))
your_city = st.selectbox(
    '🌎 Selecione uma cidade' ,
    cities
)

selected_city = BR_real_estate_appreciation.query( 'Location == @sua_cidade' )
other_cities = BR_real_estate_appreciation.query( 'Localização != @sua_cidade' )

# QUADRO 1: Apreciação anual (12 meses):
chart_1, ax = plt.subplots(figsize=( 3 , 4.125 ))
# Background:
sns.tripplot(
    data= other_cities,
    y = 'Annual_appreciation' ,
    color = 'white' ,
    jitter= 0.85 ,
    size= 8 ,
    linewidth= 1 ,
    edgecolor= 'gainsboro' ,
    alpha= 0.7
 )
# Destaque:
sns.tripplot(
    data= selected_city,
    y = 'Annual_appreciation' ,
    color ='#00FF7F' ,
    jitter= 0.15 ,
    size= 12 ,
    linewidth= 1 ,
    edgecolor= 'k' ,
    label= f' {your_city} '
 )

# Exibindo medidas de posição:
avg_annual_val = BR_real_estate_appreciation[ 'Annual_appreciation' ].median()
q1_annual_val = np.percentile(BR_real_estate_appreciation[ 'Annual_appreciation' ], 25 )
q3_annual_val = np.percentile(BR_real_estate_appreciation[ 'Annual_appreciation' ], 75 )

# Linhas de plotagem (referência):
ax.axhline(y=avg_annual_val, color= '#DA70D6' , linestyle= '--' , lw= 0.75 )
ax.axhline(y=q1_annual_val, color= 'white' , linestyle= '--' , lw= 0.75 )
ax.axhline(y=q3_annual_val, color= 'white' , linestyle= '--' , lw= 0.75 )

# Adicionando os rótulos para medidas de posição:
ax.text( 1.15 , q1_annual_val, 'Q1' , ha= 'center ' , va= 'center' , color= 'white' , fontsize= 8 , fontweight= 'bold')
ax.texto(1.3 , avg_annual_val, 'Median' , ha= 'center' , va= 'center' , color= '#DA70D6' , fontsize= 8 , fontweight= 'bold' )
ax.text( 1.15 , q3_annual_val, 'Q3' , ha = 'center' , va= 'center' , color= 'white' , fontsize= 8 , fontweight= 'bold' )

# para preencher a área entre as linhas:
ax.fill_betweenx([q1_annual_val, q3_annual_val], - 2 , 1 , alpha= 0.2 , color= 'cinza')
# para definir os limites do eixo x para mostrar toda a gama de dados:
ax.set_xlim(- 1 , 1 )

# Eixos e títulos:
plt.xticks([])
plt.ylabel( 'Valorização média (%)' )
plt.title( 'Valorização (%) nos últimos 12 meses' , peso= 'bold' , loc= 'center' , pad= 15 , color= 'gainsboro' )
plt.legend(loc= 'center' , bbox_to_anchor= ( 0.5 , - 0.1 ), ncol= 2 , framealpha= 0 , labelcolor= '#00FF7F' )
plt.tight_layout()

# QUADRO 2: Preço (R$) por m²:
chart_2, ax = plt.subplots(figsize=( 3 , 3,95 ))
# Background:
sns.tripplot(
    data= other_cities,
    y = 'BRL_per_squared_meter' ,
    color = 'white' ,
    jitter= 0.95 ,
    size= 8 ,
    linewidth= 1 ,
    edgecolor= 'gainsboro' ,
    alpha= 0.7
 )
# Destaque:
sns.tripplot(
    data= selected_city,
    y = 'BRL_per_squared_meter' ,
    color = '#00FF7F',
    jitter= 0.15 ,
    size= 12 ,
    linewidth= 1 ,
    edgecolor= 'k' ,
    label= f' {your_city} '
 )

# Mostrando as medidas de posição:
avg_price_m2 = BR_real_estate_appreciation[ 'BRL_per_squared_meter' ].median()
q1_price_m2 = np. percentile(BR_real_estate_appreciation[ 'BRL_per_squared_meter' ], 25 )
q3_price_m2 = np.percentile(BR_real_estate_appreciation[ 'BRL_per_squared_meter' ], 75 )

# Linhas de plotagem (referência):
ax.axhline(y=avg_price_m2, color= '#DA70D6' , linestyle= '--' , lw= 0.75 )
ax.axhline(y=q1_price_m2, color= 'white' , linestyle= '--' , lw= 0.75 )
ax.axhline(y=q3_price_m2, color= 'white' , linestyle= '--' , lw= 0.75 )

# Adicionando os rótulos para medidas de posição:
ax.text( 1.15 , q1_price_m2, 'Q1' , ha= 'center ' , va= 'center' , color= 'white' , fontsize= 8 , fontweight= 'bold')
ax.texto(1.35 , avg_price_m2, 'Median' , ha= 'center' , va= 'center' , color= '#DA70D6' , fontsize= 8 , fontweight= 'bold' )
ax.text( 1.15 , q3_price_m2, 'Q3' , ha = 'center' , va= 'center' , color= 'white' , fontsize= 8 , fontweight= 'bold' )

# para preencher a área entre as linhas:
ax.fill_betweenx([q1_price_m2, q3_price_m2], - 2 , 1 , alpha= 0.2 , color= 'cinza')
# para definir os limites do eixo x para mostrar o intervalo completo dos dados:
ax.set_xlim(- 1 , 1 )

# Eixos e títulos:
plt.xticks([])
plt.ylabel( 'Price (R\\$) ' )
plt.legend(loc= 'center' , bbox_to_anchor=( 0.5 , - 0.1 ), ncol= 2 , framealpha= 0 , labelcolor= '#00FF7F' )
plt.title( 'Preço médio (R\\$) por $m^2$' , peso= 'bold' , loc= 'center' , pad= 15 , color= 'gainsboro' )
plt.tight_layout()

# Dividindo os gráficos em duas colunas:
left, right = st.columns( 2 )

# Colunas (conteúdo):
with left:
    st.pyplot(chart_1)
with right:
    st.pyplot(chart_2)

# Texto informativo:
st.markdown( ''' 
<span style="color:white;font-size:10pt"> ⚪ Cada ponto representa uma cidade </span> 
<span style="color:#DA70D6;font-size:10pt"> ▫ <b> Valor médio </b></span> 
<span style="color:white;font-size:10pt"> ◽ Valores mais baixos (<b> inferior </b>) 
◽ Valores mais altos (<b> superior </b) >) <br> 
◽ **T1** (primeiro quartil):onde 25% dos dados se enquadram em 
◽ **T3** (terceiro quartil): onde 75% dos dados se enquadram em 
</span>

''' ,unsafe_allow_html= True )

# Mostrando os dados numéricos (como um dataframe):
st.dataframe(
    BR_real_estate_appreciation.query( 'Location == @your_city' )[[
      'Location' , 'Annual_appreciation' ,
      'BRL_per_squared_meter' ] ]
)

# Adicionando alguns índices de referência:
st.markdown( ''' > **Índices de referência (inflação):** 

* IPCA: **6%** (Índice Nacional de Preços ao Consumidor Amplo) 
* IGP-M: **4 %** (Índice Geral de Preços do Mercado) 

> Dados baseados em informes públicos que contabilizam imóveis residenciais para 50 cidades brasileiras (primeiro trimestre de 2023). 
''')

# Autoria:
st.markdown( 'Leonardo Azevedo' )
# aqui você pode adicionar a autoria e links úteis (por exemplo, Linkedin, GitHub e assim por diante)
st.markdown( '---' )
# --- (Fim do aplicativo )
