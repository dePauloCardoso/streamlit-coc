import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# Carrega o CSV
@st.cache_data  # Usando cache para evitar recarregamento desnecessário
def load_data():
    return pd.read_csv("data/COC_2025_B2B_e_B2C-Combo2025_A25_B2C.csv", sep=',')  # Substitua 'seu_arquivo.csv' pelo nome correto

df = load_data()


# Define a cor de fundo
st.markdown(
    """
    <style>
    div[data-testid="stAppViewContainer"] {
        background-color: #161B33;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Exibe a imagem
st.sidebar.image("https://github.com/dePauloCardoso/streamlit-coc/blob/main/logo-coc-secundario-2.png?raw=true")

# Inicializa os filtros no session_state
if "SEGMENTO" not in st.session_state:
    st.session_state.SEGMENTO = ""
if "SERIE" not in st.session_state:
    st.session_state.SERIE = ""
if "SKU_COMBO_EBS" not in st.session_state:
    st.session_state.SKU_COMBO_EBS = ""
if "SKU_KIT_EBS" not in st.session_state:
    st.session_state.SKU_KIT_EBS = ""
if "SKU_ITENS_EBS" not in st.session_state:
    st.session_state.SKU_ITENS_EBS = ""
if "TIPO_PRODUTO" not in st.session_state:
    st.session_state.TIPO_PRODUTO = ""
if "FREQUÊNCIA" not in st.session_state:
    st.session_state.FREQUÊNCIA = ""
if "COLECAO" not in st.session_state:
    st.session_state.COLECAO = ""

# # Mapeamento de Série baseado no Segmento
# serie_map = {
#     "INF": ["", "INF I", "INF II", "INF III", "INF IV", "INF V"],
#     "FUND AI": ["", "1O ANO", "2O ANO", "3O ANO", "4O ANO", "5O ANO"],
#     "FUND AF": ["", "6O ANO", "7O ANO", "8O ANO", "9O ANO"],
#     "EM": ["", "1A SERIE", "2A SERIE", "3A SERIE"],
#     "PV": ["", "APROVA +", "ELETIVAS", "SEMI"],
#     "VÁRIOS": ["", "VARIOS"]
# }

# Interface Streamlit
st.sidebar.title("Consulta de Produtos")

# SEGMENTO 
segmento_options = [""] + [
    'ENSINO INFANTIL','ENSINO FUNDAMENTAL 1','ENSINO FUNDAMENTAL 2',
    'ENSINO MEDIO','PRE - VESTIBULAR'
    ]
# Determina o índice atual para o selectbox, evitando erro se o valor não estiver na lista
current_segmento_index = segmento_options.index(st.session_state.SEGMENTO) if st.session_state.SEGMENTO in segmento_options else 0
st.session_state.SEGMENTO = st.sidebar.selectbox("Segmento", segmento_options, index=current_segmento_index)

# SERIE 
serie_options = [""] + [
    'BERCARIO',	'1 ANO', '2 ANO', '3 ANO', 
    '4 ANO', '5 ANO', '6 ANO', '7 ANO', '8 ANO', 
    '9 ANO', 'EXTENSIVO', 'SEMI EXTENSIVO',	
    'INTENSIVO'
    ]
# Determina o índice atual para o selectbox, evitando erro se o valor não estiver na lista
current_serie_index = serie_options.index(st.session_state.SERIE) if st.session_state.SERIE in serie_options else 0
st.session_state.SERIE = st.sidebar.selectbox("Serie", serie_options, index=current_serie_index)

# Campos de entrada para os filtros
st.session_state.SKU_COMBO_EBS = st.sidebar.text_input("SKU_COMBO_EBS", st.session_state.SKU_COMBO_EBS)
st.session_state.SKU_KIT_EBS = st.sidebar.text_input("SKU_KIT_EBS", st.session_state.SKU_KIT_EBS)
st.session_state.SKU_ITENS_EBS = st.sidebar.text_input("SKU_ITENS_EBS", st.session_state.SKU_ITENS_EBS)

# TIPO_PRODUTO 
tipo_options = [""] + ['ALUNO', 'PROFESSOR']

# Determina o índice atual para o selectbox, evitando erro se o valor não estiver na lista
current_tipo_index = tipo_options.index(st.session_state.TIPO_PRODUTO) if st.session_state.TIPO_PRODUTO in tipo_options else 0
st.session_state.TIPO_PRODUTO = st.sidebar.selectbox("Tipo", tipo_options, index=current_tipo_index)

# COLEÇÃO (Corrigido a sintaxe da lista e a lógica do selectbox)
colecao_options = [""] + [ 
    'EXPLORAR', 'AGENDA IMPRESSA', 'AVULSO', 
    'INFINITO', 'AZUL', 'TERCEIRAO EXTENSIVO 1000',
    'TERCEIRAO SEMIEXTENSIVO 500', 'AMARELA',
    'PV EXTENSIVO 1000', 'PV SEMI EXTENSIVO ANUAL 500',
    'PV SEMI EXTENSIVO 1 SEM 500', 'PV SEMI EXTENSIVO 2 SEM 500',
    'PV INTENSIVO 300'
]
# Determina o índice atual para o selectbox, evitando erro se o valor não estiver na lista
current_colecao_index = colecao_options.index(st.session_state.COLECAO) if st.session_state.COLECAO in colecao_options else 0
st.session_state.COLECAO = st.sidebar.selectbox("Coleção", colecao_options, index=current_colecao_index)

# Botão para limpar filtros
def limpar_filtros():
    for key in st.session_state.keys():
        st.session_state[key] = ""

st.sidebar.button("Limpar Filtros", on_click=limpar_filtros)

# Aplica os filtros diretamente no DataFrame
filtro = pd.Series([True] * len(df))  # Inicializa com todos verdadeiros
if st.session_state.SEGMENTO:
    filtro &= df['SEGMENTO'].astype(str).str.contains(st.session_state.SEGMENTO, na=False)
if st.session_state.SERIE:
    filtro &= df['SERIE'].astype(str).str.contains(st.session_state.SERIE, na=False)
if st.session_state.SKU_COMBO_EBS:
    filtro &= df['SKU_COMBO_EBS'] == st.session_state.SKU_COMBO_EBS
if st.session_state.SKU_KIT_EBS:
    filtro &= df['SKU_KIT_EBS'] == st.session_state.SKU_KIT_EBS
if st.session_state.SKU_ITENS_EBS:
    filtro &= df['SKU_ITENS_EBS'] == st.session_state.SKU_ITENS_EBS
if st.session_state.TIPO_PRODUTO:
    filtro &= df['TIPO_PRODUTO'] == st.session_state.TIPO_PRODUTO
if st.session_state.FREQUÊNCIA:
    filtro &= df['FREQUÊNCIA'] == st.session_state.FREQUÊNCIA
if st.session_state.COLECAO:
    filtro &= df['COLECAO'] == st.session_state.COLECAO

df_filtrado = df[filtro]

# Exibe os resultados em tabela
if not df_filtrado.empty:
    colunas_desejadas = ['SEGMENTO', 'SERIE', 'SKU_COMBO_EBS',
                        'SKU_KIT_EBS', 'SKU_ITENS_EBS', 'DESCRIÇÃO LISTA DE PREÇO EBS', 
                        'TIPO_PRODUTO', 'FREQUÊNCIA', 'COLECAO']
    df_filtrado = df_filtrado[colunas_desejadas]
    st.dataframe(df_filtrado, use_container_width=True)
else:
    st.write("Nenhum produto encontrado para estes filtros.")