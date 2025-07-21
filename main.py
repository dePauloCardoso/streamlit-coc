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

# Campos de entrada para os filtros
st.session_state.SKU_COMBO_EBS = st.sidebar.text_input("SKU_COMBO_EBS", st.session_state.SKU_COMBO_EBS)
st.session_state.SKU_KIT_EBS = st.sidebar.text_input("SKU_KIT_EBS", st.session_state.SKU_KIT_EBS)
st.session_state.SKU_ITENS_EBS = st.sidebar.text_input("SKU_ITENS_EBS", st.session_state.SKU_ITENS_EBS)

# # Dropdowns para os filtros
# segmento_options = ["", "INF", "FUND AI", "FUND AF", "EM", "PV", "VÁRIOS"]
# st.session_state.segmento = st.sidebar.selectbox("Segmento", segmento_options, index=segmento_options.index(st.session_state.segmento))

# # Atualiza as opções do dropdown de série baseado no segmento escolhido
# serie_options = serie_map.get(st.session_state.segmento, [""])
# st.session_state.serie = st.sidebar.selectbox("Série", serie_options, index=serie_options.index(st.session_state.serie) if st.session_state.serie in serie_options else 0)

# # Outros filtros
# envio_options = ["", "V1", "V2", "V3", "V4"]
# st.session_state.envio = st.sidebar.selectbox("Envio", envio_options, index=envio_options.index(st.session_state.envio))

# usuario_options = ["", "Aluno", "Professor"]
# st.session_state.usuario = st.sidebar.selectbox("Usuário", usuario_options, index=usuario_options.index(st.session_state.usuario))

# personalizacao_options = ["", "CAMILA MOREIRA", "CCPA", "CELLULA MATER", "DOM BOSCO", "DOM BOSCO BALSAS", "ELO", "FATO", "FILOMENA", "GABARITO MG", "GABARITO RS", "MACK", "MAXX JUNIOR", "MELLO DANTE", "REDE AGNUS", "REDE VIVO", "REFERENCIAL", "ROSALVO", "SAE", "SANTO ANJO", "SECULO", "STATUS", "TAMANDARE"]
# st.session_state.personalizacao = st.sidebar.selectbox("Personalização", personalizacao_options, index=personalizacao_options.index(st.session_state.personalizacao))

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

df_filtrado = df[filtro]

# Exibe os resultados em tabela
if not df_filtrado.empty:
    colunas_desejadas = ['SEGMENTO', 'SERIE', 'SKU_COMBO_EBS',
                        'SKU_KIT_EBS', 'SKU_ITENS_EBS', 'TIPO_PRODUTO', 'FREQUÊNCIA','DESCRIÇÃO LISTA DE PREÇO EBS']
    df_filtrado = df_filtrado[colunas_desejadas]
    st.dataframe(df_filtrado, use_container_width=True)
else:
    st.write("Nenhum produto encontrado para estes filtros.")