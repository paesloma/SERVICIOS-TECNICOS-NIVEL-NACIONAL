import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os

# Configuración de la página
st.set_page_config(page_title="Red de Talleres Ecuador", layout="wide")

# Estilo visual
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stSelectbox, .stTextInput { color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛠️ Sistema de Gestión de Talleres - Cobertura Nacional")

@st.cache_data
def load_data():
    file_path = "base_datos_talleres.csv"
    
    if not os.path.exists(file_path):
        return None

    try:
        # Cargamos con sep=';' porque tu archivo usa punto y coma
        df = pd.read_csv(file_path, sep=';', encoding='utf-8')
        
        # Eliminamos filas que estén completamente vacías (las que tienen muchos ;;;;;)
        df = df.dropna(subset=['NOMBRE DEL TALLER (MAYUSCULAS)'])
        
        # Limpieza de nombres de ciudad
        df['CIUDAD_MAPA'] = df['CIUDAD BASE'].astype(str).str.upper().str.strip()
        
        # Coordenadas
        coords = {
            'AMBATO': [-1.2417, -78.6195], 'BABAHOYO': [-1.8022, -79.5344],
            'DURAN': [-2.1701, -79.8220], 'EL COCA': [-0.4667, -76.9833],
            'GUAYAQUIL': [-2.1894, -79.8891], 'IBARRA': [0.3517, -78.1223],
            'LAGO AGRIO': [0.0860, -76.8820], 'LOJA': [-3.9931, -79.2042],
            'MACHALA': [-3.2581, -79.9554], 'MANTA': [-0.9677, -80.7127],
            'PORTOVIEJO': [-1.0546, -80.4545], 'QUEVEDO': [-1.0225, -79.4600],
            'QUITO': [-0.1807, -78.4678], 'RIOBAMBA': [-1.6636, -78.6546],
            'SALINAS': [-2.2230, -80.9580], 'SANTO DOMINGO': [-0.2530, -79.1754],
            'TUNGURAHUA - AMBATO': [-1.2417, -78.6195]
        }
        
        df['Lat'] = df['CIUDAD_MAPA'].apply(lambda x: coords.get(x, [-1.8312, -78.1834])[0])
        df['Lon'] = df['CIUDAD_MAPA'].apply(lambda x: coords.get(x, [-1.8312, -78.1834])[1])
        
        return df.fillna("No disponible")
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        return None

df = load_data()

if df is not None:
    # --- BUSCADOR ---
    st.sidebar.header("🔍 Panel de Búsqueda")
    query = st.sidebar.text_input("Buscar Taller, Ciudad o Línea:", "").upper()

    df_filtered = df.copy()
    if query:
        df_filtered = df[
            df['NOMBRE DEL TALLER (MAYUSCULAS)'].str.upper().str.contains(query, na=False) |
            df['CIUDAD BASE'].str.upper().str.contains(query, na=False) |
            df['LINEAS QUE MANEJAN'].str.upper().str.contains(query, na=False)
        ]

    # --- MAPA E INFO ---
    col1, col2 = st.columns([2, 1])

    with col1:
        centro = [df_filtered['Lat'].mean(), df_filtered['Lon'].mean()] if not df_filtered.empty else [-1.8312, -78.1834]
        m = folium.Map(location=centro, zoom_start=7, tiles="CartoDB dark_matter")
        
        for _, r in df_filtered.iterrows():
            folium.Marker(
                location=[r['Lat'], r['Lon']],
                popup=f"{r['NOMBRE DEL TALLER (MAYUSCULAS)']}",
                icon=folium.Icon(color="blue", icon="wrench", prefix="fa")
            ).add_to(m)
        st_folium(m, width="100%", height=500)

    with col2:
        if len(df_filtered) == 1:
            res = df_filtered.iloc[0]
            st.success(f"### {res['NOMBRE DEL TALLER (MAYUSCULAS)']}")
            st.write(f"📍 **Ciudad:** {res['CIUDAD BASE']}")
            st.write(f"📞 **Contacto:** {res['NUMEROS DE CONTACTO']}")
            st.warning(f"🌎 **Cobertura:** {res['COBERTURA INST AA Y LINEA BLANCA']}")
        else:
            st.info(f"Mostrando {len(df_filtered)} talleres.")

    # --- TABLA INFERIOR ---
    st.markdown("---")
    st.dataframe(df_filtered[["NOMBRE DEL TALLER (MAYUSCULAS)", "CIUDAD BASE", "NUMEROS DE CONTACTO", "LINEAS QUE MANEJAN"]], use_container_width=True, hide_index=True)
else:
    st.error("Archivo 'base_datos_talleres.csv' no detectado.")
