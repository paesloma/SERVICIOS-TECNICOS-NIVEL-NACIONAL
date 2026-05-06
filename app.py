import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os

# Configuración de la página
st.set_page_config(page_title="Red de Talleres Ecuador", layout="wide")

# Estilo visual para fondo oscuro
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stSelectbox, .stTextInput { color: white; }
    .stDataFrame { background-color: #161b22; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛠️ Sistema de Gestión de Talleres - Cobertura Nacional")

# Función para cargar y limpiar datos
@st.cache_data
def load_data():
    # Nombre del archivo que debes subir a GitHub
    file_path = "base_datos_talleres.csv"
    
    if not os.path.exists(file_path):
        return None

    # Leer CSV
    df = pd.read_csv(file_path)
    
    # Estandarizar ciudades para el mapa
    df['CIUDAD_MAPA'] = df['CIUDAD BASE'].astype(str).str.upper().str.strip()
    
    # Diccionario de coordenadas de ciudades principales
    coords = {
        'AMBATO': [-1.2417, -78.6195], 'BABAHOYO': [-1.8022, -79.5344],
        'DURAN': [-2.1701, -79.8220], 'EL COCA': [-0.4667, -76.9833],
        'GUAYAQUIL': [-2.1894, -79.8891], 'GUYAQUIL': [-2.1894, -79.8891],
        'IBARRA': [0.3517, -78.1223], 'LAGO AGRIO': [0.0860, -76.8820],
        'LOJA': [-3.9931, -79.2042], 'MACHALA': [-3.2581, -79.9554],
        'MANTA': [-0.9677, -80.7127], 'MILAGRO': [-2.1333, -79.5833],
        'NARANJITO': [-2.1667, -79.4667], 'PASAJE': [-3.3250, -79.8070],
        'PORTOVIEJO': [-1.0546, -80.4545], 'QUEVEDO': [-1.0225, -79.4600],
        'QUITO': [-0.1807, -78.4678], 'RIOBAMBA': [-1.6636, -78.6546],
        'SALINAS': [-2.2230, -80.9580], 'SANTO DOMINGO': [-0.2530, -79.1754]
    }
    
    # Asignar coordenadas (si no existe, usa el centro de Ecuador)
    df['Lat'] = df['CIUDAD_MAPA'].apply(lambda x: coords.get(x, [-1.8312, -78.1834])[0])
    df['Lon'] = df['CIUDAD_MAPA'].apply(lambda x: coords.get(x, [-1.8312, -78.1834])[1])
    
    return df.fillna("No disponible")

# Cargar la base de datos
df = load_data()

if df is not None:
    # --- SIDEBAR ---
    st.sidebar.header("🔍 Panel de Búsqueda")
    query = st.sidebar.text_input("Buscar por Nombre, Ciudad o Línea Técnica:", "").upper()

    # Filtrar datos
    if query:
        mask = (
            df['NOMBRE DEL TALLER (MAYUSCULAS)'].str.upper().str.contains(query) |
            df['CIUDAD BASE'].str.upper().str.contains(query) |
            df['LINEAS QUE MANEJAN'].str.upper().str.contains(query)
        )
        df_filtered = df[mask]
    else:
        df_filtered = df

    # --- CUERPO PRINCIPAL ---
    col1, col2 = st.columns([2, 1])

    with col1:
        # Mapa
        centro_mapa = [df_filtered['Lat'].mean(), df_filtered['Lon'].mean()] if not df_filtered.empty else [-1.8312, -78.1834]
        m = folium.Map(location=centro_mapa, zoom_start=7, tiles="CartoDB dark_matter")
        
        for _, r in df_filtered.iterrows():
            folium.Marker(
                location=[r['Lat'], r['Lon']],
                popup=f"<b>{r['NOMBRE DEL TALLER (MAYUSCULAS)']}</b><br>Telf: {r['NUMEROS DE CONTACTO']}",
                icon=folium.Icon(color="blue", icon="wrench", prefix="fa")
            ).add_to(m)
        
        st_folium(m, width="100%", height=500)

    with col2:
        # Información detallada
        if len(df_filtered) == 1:
            res = df_filtered.iloc[0]
            st.success(f"### {res['NOMBRE DEL TALLER (MAYUSCULAS)']}")
            st.write(f"📍 **Ciudad:** {res['CIUDAD BASE']}")
            st.write(f"📞 **Contacto:** {res['NUMEROS DE CONTACTO']}")
            st.write(f"⚙️ **Líneas:** {res['LINEAS QUE MANEJAN']}")
            st.warning(f"🌎 **Cobertura:** {res['COBERTURA INST AA Y LINEA BLANCA']}")
        else:
            st.info(f"Se encontraron {len(df_filtered)} talleres. Escribe en el buscador o toca un punto en el mapa.")

    # --- TABLA INFERIOR (SIEMPRE VISIBLE) ---
    st.markdown("---")
    st.subheader("📋 Detalle General de Talleres")
    columnas_display = ["NOMBRE DEL TALLER (MAYUSCULAS)", "CIUDAD BASE", "NUMEROS DE CONTACTO", "LINEAS QUE MANEJAN", "COBERTURA INST AA Y LINEA BLANCA"]
    st.dataframe(df_filtered[columnas_display], use_container_width=True, hide_index=True)

else:
    st.error("⚠️ El archivo 'base_datos_talleres.csv' no se encuentra. Por favor súbelo a GitHub.")
