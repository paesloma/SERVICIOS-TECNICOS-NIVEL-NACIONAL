import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Red de Talleres Ecuador", layout="wide")

# Estilo visual modo oscuro
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stSelectbox, .stTextInput { color: white; }
    div[data-testid="stExpander"] { background-color: #161b22; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛠️ Sistema de Gestión de Talleres - Cobertura Nacional")

# 2. FUNCIÓN PARA CARGAR DATOS (Optimizado para tu archivo específico)
@st.cache_data
def load_data():
    file_path = "base_datos_talleres.csv"
    
    if not os.path.exists(file_path):
        return None

    try:
        # Tu archivo usa ';' como separador y tiene filas vacías al final
        df = pd.read_csv(file_path, sep=';', encoding='utf-8')
        
        # ELIMINAR FILAS VACÍAS: Filtramos por la columna del nombre del taller
        df = df[df['NOMBRE DEL TALLER (MAYUSCULAS)'].notna()]
        
        # Limpieza de nombres de ciudad para el mapeo
        df['CIUDAD_MAPA'] = df['CIUDAD BASE'].astype(str).str.upper().str.strip()
        
        # Diccionario de coordenadas para ciudades en tu base
        coords = {
            'AMBATO': [-1.2417, -78.6195],
            'TUNGURAHUA - AMBATO': [-1.2417, -78.6195],
            'BABAHOYO': [-1.8022, -79.5344],
            'DURAN': [-2.1701, -79.8220],
            'EL COCA': [-0.4667, -76.9833],
            'GUAYAQUIL': [-2.1894, -79.8891],
            'IBARRA': [0.3517, -78.1223],
            'LAGO AGRIO': [0.0860, -76.8820],
            'LOJA': [-3.9931, -79.2042],
            'MACHALA': [-3.2581, -79.9554],
            'MANTA': [-0.9677, -80.7127],
            'MILAGRO': [-2.1333, -79.5833],
            'NARANJITO': [-2.1667, -79.4667],
            'PASAJE': [-3.3250, -79.8070],
            'PORTOVIEJO': [-1.0546, -80.4545],
            'QUEVEDO': [-1.0225, -79.4600],
            'QUITO': [-0.1807, -78.4678],
            'RIOBAMBA': [-1.6636, -78.6546],
            'SALINAS': [-2.2230, -80.9580],
            'SANTO DOMINGO': [-0.2530, -79.1754]
        }
        
        # Asignar coordenadas (si no existe la ciudad, coloca punto en centro de Ecuador)
        df['Lat'] = df['CIUDAD_MAPA'].apply(lambda x: coords.get(x, [-1.8312, -78.1834])[0])
        df['Lon'] = df['CIUDAD_MAPA'].apply(lambda x: coords.get(x, [-1.8312, -78.1834])[1])
        
        return df.fillna("Información no disponible")
    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
        return None

# 3. EJECUCIÓN Y FILTROS
df = load_data()

if df is not None:
    # --- SIDEBAR ---
    st.sidebar.header("🔍 Panel de Filtros")
    query = st.sidebar.text_input("Buscar Taller, Ciudad o Cobertura:", "").upper()

    df_filtered = df.copy()
    if query:
        # Buscamos en nombre, ciudad o cobertura
        mask = (
            df['NOMBRE DEL TALLER (MAYUSCULAS)'].str.contains(query, na=False) |
            df['CIUDAD BASE'].str.upper().str.contains(query, na=False) |
            df['COBERTURA INST AA Y LINEA BLANCA'].str.upper().str.contains(query, na=False)
        )
        df_filtered = df[mask]

    # --- LAYOUT PRINCIPAL ---
    col_map, col_details = st.columns([2, 1])

    with col_map:
        # Centrar mapa en base a los resultados
        centro = [df_filtered['Lat'].mean(), df_filtered['Lon'].mean()] if not df_filtered.empty else [-1.8312, -78.1834]
        m = folium.Map(location=centro, zoom_start=7, tiles="CartoDB dark_matter")
        
        for _, r in df_filtered.iterrows():
            pop_html = f"<b>{r['NOMBRE DEL TALLER (MAYUSCULAS)']}</b><br>Telf: {r['NUMEROS DE CONTACTO']}"
            folium.Marker(
                location=[r['Lat'], r['Lon']],
                popup=folium.Popup(pop_html, max_width=250),
                icon=folium.Icon(color="blue", icon="wrench", prefix="fa")
            ).add_to(m)
        
        st_folium(m, width="100%", height=500)

    with col_details:
        if len(df_filtered) == 1:
            res = df_filtered.iloc[0]
            st.success(f"### {res['NOMBRE DEL TALLER (MAYUSCULAS)']}")
            st.info(f"📍 **Ubicación:** {res['CIUDAD BASE']}")
            st.write(f"📞 **Teléfono:** {res['NUMEROS DE CONTACTO']}")
            st.write(f"⚙️ **Líneas:** {res['LINEAS QUE MANEJAN']}")
            st.warning(f"🌎 **Cobertura:** {res['COBERTURA INST AA Y LINEA BLANCA']}")
        else:
            st.info(f"Resultados encontrados: {len(df_filtered)}")
            st.caption("Filtra un taller específico para ver todos sus detalles aquí.")

    # 4. TABLA INFERIOR (Siempre visible)
    st.markdown("---")
    st.subheader("📋 Detalle de la Red de Talleres")
    columnas_tabla = ["NOMBRE DEL TALLER (MAYUSCULAS)", "CIUDAD BASE", "NUMEROS DE CONTACTO", "LINEAS QUE MANEJAN"]
    st.dataframe(df_filtered[columnas_tabla], use_container_width=True, hide_index=True)

else:
    st.error("⚠️ El archivo 'base_datos_talleres.csv' no fue detectado en el repositorio.")
