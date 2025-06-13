import streamlit as st
import numpy as np
import pandas as pd
from utils import plot_ray_paths, plot_velocity_profile, Dmax
import io

st.set_page_config(page_title="Simulação de Propagação Acústica", layout="wide")

st.title("Simulação de Propagação Acústica")

# Inicialização das variáveis de estado
if 'depths' not in st.session_state:
    st.session_state.depths = np.array([0, 200, 275, 500], dtype=float)
if 'speeds' not in st.session_state:
    st.session_state.speeds = np.array([1497, 1500, 1485, 1475], dtype=float)
if 'source_pos' not in st.session_state:
    st.session_state.source_pos = [0, 40]

# Sidebar para configurações
st.sidebar.header("Configurações")

# Upload de arquivo e download do template
st.sidebar.subheader("Perfil de Velocidade")
uploaded_file = st.sidebar.file_uploader("Carregar perfil de velocidade", type=['xlsx'])

# Botão para download do template
def get_excel_template():
    df = pd.DataFrame({
        'depth': st.session_state.depths,
        'speed': st.session_state.speeds
    })
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Perfil')
        workbook = writer.book
        worksheet = writer.sheets['Perfil']
        
        # Adicionar formatação
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#D9E1F2',
            'border': 1
        })
        
        # Aplicar formatação ao cabeçalho
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
            worksheet.set_column(col_num, col_num, 15)
    
    return output.getvalue()

st.sidebar.download_button(
    label="Baixar template Excel",
    data=get_excel_template(),
    file_name="perfil_velocidade.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        
        if 'depth' in df.columns and 'speed' in df.columns:
            st.session_state.depths = df['depth'].values
            st.session_state.speeds = df['speed'].values
            st.sidebar.success("Perfil carregado com sucesso!")
        else:
            st.sidebar.error("O arquivo deve conter as colunas 'depth' e 'speed'")
    except Exception as e:
        st.sidebar.error(f"Erro ao carregar arquivo: {str(e)}")

# Controles para posição da fonte
st.sidebar.subheader("Posição da Fonte")
col1, col2 = st.sidebar.columns(2)
with col1:
    rs = col1.number_input("Rs (m)", 0, 40000, st.session_state.source_pos[0], 1000)
with col2:
    zs = col2.number_input("Zs (m)", 0, Dmax, st.session_state.source_pos[1], 10)
st.session_state.source_pos = [rs, zs]

# Editor de perfil de velocidade
st.sidebar.subheader("Editor de Perfil")
num_points = st.sidebar.number_input("Número de pontos", 2, 10, len(st.session_state.depths))

if num_points != len(st.session_state.depths):
    st.session_state.depths = np.linspace(0, Dmax, num_points)
    st.session_state.speeds = np.linspace(1497, 1475, num_points)

for i in range(num_points):
    col1, col2 = st.sidebar.columns(2)
    with col1:
        depth = col1.number_input(f"Profundidade {i+1} (m)", 0, Dmax, int(st.session_state.depths[i]))
    with col2:
        speed = col2.number_input(f"Velocidade {i+1} (m/s)", 1400, 1600, int(st.session_state.speeds[i]))
    st.session_state.depths[i] = depth
    st.session_state.speeds[i] = speed

# Layout principal
col1, col2 = st.columns(2)

with col1:
    st.subheader("Perfil de Velocidade")
    fig_profile = plot_velocity_profile(st.session_state.depths, st.session_state.speeds)
    st.pyplot(fig_profile)

with col2:
    st.subheader("Propagação de Raios")
    fig_rays = plot_ray_paths(st.session_state.depths, st.session_state.speeds, st.session_state.source_pos)
    st.pyplot(fig_rays)
