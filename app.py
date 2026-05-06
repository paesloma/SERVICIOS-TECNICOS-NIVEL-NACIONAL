import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os

# 1. Configuración inicial de la página
st.set_page_config(page_title="Sistema Nacional de Talleres", layout="wide")

# 2. Estilo personalizado (Modo Oscuro)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stSelectbox, .stTextInput { color: white; }
    div[data-testid="stExpander"] { background-color: #161b22; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛠️ Gestión de Talleres y Cobertura Nacional")

# 3. Función para cargar datos
@st.cache_data
def cargar_datos():
    # Usamos el nombre de archivo sugerido para GitHub
    file_name = "base_datos_talleres.csv"
    
    if not os.path.exists(file_name):
        st.error(f"❌ No se encontró el archivo '{file_name}'. Asegúrate de renombrarlo y subirlo a GitHub.")
        return pd.DataFrame()

    # Cargar el CSV
    df = pd.read_csv(file_name)
    
    # Limpiar nombres de ciudad para el mapeo
    df['CIUDAD_BUSQUEDA'] = df['CIUDAD BASE'].astype(str).str.upper().str.strip()
    
    # Diccionario de coordenadas para las ciudades de tu base de datos
    coordenadas = {
        'AMBATO': (-1.2417, -78.6195),
        'TUNGURAHUA - AMBATO': (-1.2417, -78.6195),
        'BABAHOYO': (-1.8022, -79.5344),
        'DURAN': (-2.1701, -79.8220),
        'EL COCA': (-0.4667, -76.9833),
        'GUAYAQUIL': (-2.1894, -79.8891),
        'GUYAQUIL': (-2.1894, -79.8891),
        'IBARRA': (0.3517, -78.1223),
        'LAGO AGRIO': (0.0860, -76.8820),
        'LOJA': (-3.9931, -79.2042),
        'MACHALA': (-3.2581, -79.9554),
        'MANTA': (-0.9677, -80.7127),
        'MILAGRO': (-2.1333, -79.5833),
        'NARANJITO': (-2.1667, -79.4667),
        'PASAJE': (-3.3250, -79.8070),
        'PORTOVIEJO': (-1.0546, -80.4545),
        'QUEVEDO': (-1.0225, -79.4600),
        'QUITO': (-0.1807, -78.4678),
        'RIOBAMBA': (-1.6636, -78.6546),
        'RIOBAMBA-GUANO': (-1.6000, -78.6000),
        'SALINAS': (-2.2230, -80.9580),
        'SANTO DOMINGO': (-0.2530, -79.1754)
    }
    
    # Asignar coordenadas (Ecuador por defecto si no encuentra la ciudad)
    df['Lat'] = df['CIUDAD_BUSQUEDA'].map(lambda x: coordenadas.get(x, (-1.8312, -78.1834))[0])
    df['Lon'] = df['CIUDAD_BUSQUEDA'].map(lambda x: coordenadas.get(x, (-1.8312, -78.1834))[1])
    
    return df.fillna('No disponible')

# Ejecutar carga
df = cargar_datos()

if not df.empty:
    # --- SIDEBAR: BUSCADOR ---
    st.sidebar.header("🔍 Filtros de Red")
    busqueda = st.sidebar.text_input("Buscar Taller, Ciudad o Línea:", "").strip().upper()
    
    # Lógica de filtrado
    if busqueda:
        df_filtrado = df[
            df["NOMBRE DEL TALLER (MAYUSCULAS)"].str.upper().str.contains(busqueda) | 
            df["CIUDAD BASE"].str.upper().str.contains(busqueda) |
            df["LINEAS QUE MANEJAN"].str.upper().str.contains(busqueda)
        ]
    else:
        df_filtrado = df

    # --- LAYOUT: MAPA Y DETALLES ---
    col_map, col_info = st.columns([2, 1])

    with col_map:
        # Centrar el mapa dinámicamente
        centro = [df_filtrado["Lat"].mean(), df_filtrado["Lon"].mean()] if not df_filtrado.empty else [-1.8312, -78.1834]
        
        m = folium.Map(location=centro, zoom_start=7, tiles="CartoDB dark_matter")
        
        for _, r in df_filtrado.iterrows():
            pop_html = f"""
            <div style='color: black; font-family: Arial;'>
                <b>{r['NOMBRE DEL TALLER (MAYUSCULAS)']}</b><br>
                <b>Telf:</b> {r['NUMEROS DE CONTACTO']}<br>
                <b>Líneas:</b> {r['LINEAS QUE MANEJAN']}
            </div>
            """
            folium.CircleMarker(
                location=[r['Lat'], r['Lon']],
                radius=8, color='#00FF00', fill=True, fill_color='#00FF00',
                popup=folium.Popup(pop_html, max_width=250)
            ).add_to(m)
        
        st_folium(m, width="100%", height=500)

    with col_info:
        if len(df_filtrado) == 1:
            row = df_filtrado.iloc[0]
            st.success(f"📍 {row['NOMBRE DEL TALLER (MAYUSCULAS)']}")
            st.write(f"**Ciudad:** {row['CIUDAD BASE']}")
            st.write(f"**Contacto:** {row['NUMEROS DE CONTACTO']}")
            st.write(f"**Líneas:** {row['LINEAS QUE MANEJAN']}")
            st.warning(f"**Cobertura:** {row['COBERTURA INST AA Y LINEA BLANCA']}")
        elif len(df_filtrado) > 1:
            st.info(f"Se encontraron {len(df_filtrado)} talleres en esta selección.")
        else:
            st.error("No se encontraron coincidencias.")

    # 4. Tabla Maestra (Siempre visible al final)
    st.markdown("### 📋 Listado Completo de la Red")
    columnas_visibles = [
        "NOMBRE DEL TALLER (MAYUSCULAS)", 
        "CIUDAD BASE", 
        "LINEAS QUE MANEJAN", 
        "NUMEROS DE CONTACTO",
        "COBERTURA INST AA Y LINEA BLANCA"
    ]
    st.dataframe(df_filtrado[columnas_visibles], use_container_width=True, hide_index=True)
