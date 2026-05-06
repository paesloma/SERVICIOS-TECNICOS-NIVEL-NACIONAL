import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Configuración inicial
st.set_page_config(page_title="Gestión de Talleres Ecuador", layout="wide")

# Estilo personalizado para mejorar la visibilidad
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stSelectbox, .stTextInput { color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛠️ Sistema de Talleres y Cobertura Nacional")

# Función para cargar y procesar los datos
@st.cache_data
def cargar_datos():
    # Leer el archivo CSV cargado
    df = pd.read_csv("DATOS ST 04 2026 (4).xlsx - Respuestas de formulario 1.csv")
    
    # Limpiar nombres de ciudad para cruzar con las coordenadas
    df['CIUDAD BASE LIMPIA'] = df['CIUDAD BASE'].astype(str).str.upper().str.strip()
    
    # Diccionario de coordenadas aproximadas para las ciudades encontradas en el CSV
    coordenadas = {
        'AMBATO': (-1.2417, -78.6195),
        'TUNGURAHUA - AMBATO': (-1.2417, -78.6195),
        'BABAHOYO': (-1.8022, -79.5344),
        'DURAN': (-2.1701, -79.8220),
        'EL COCA': (-0.4667, -76.9833),
        'GUAYAQUIL': (-2.1894, -79.8891),
        'GUYAQUIL': (-2.1894, -79.8891), # Contemplando posible error de tipeo en base
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
    
    # Asignar Latitud y Longitud
    df['Lat'] = df['CIUDAD BASE LIMPIA'].map(lambda x: coordenadas.get(x, (0, 0))[0])
    df['Lon'] = df['CIUDAD BASE LIMPIA'].map(lambda x: coordenadas.get(x, (0, 0))[1])
    
    # Filtrar o descartar aquellos que no tengan coordenadas asignadas
    df = df[df['Lat'] != 0]
    
    # Rellenar valores nulos para evitar errores en Streamlit
    df = df.fillna('No especificado')
    
    return df

df = cargar_datos()

# --- SIDEBAR: BUSCADOR Y LISTA ---
st.sidebar.header("⚙️ Opciones de Filtro")

# Buscador de texto automático (por taller, ciudad o cobertura)
busqueda = st.sidebar.text_input("🔍 Buscar Taller, Ciudad o Cobertura:", "").strip().upper()

# Lista desplegable
nombres_taller = ["TODOS"] + sorted(df["NOMBRE DEL TALLER (MAYUSCULAS)"].unique().tolist())
seleccion_lista = st.sidebar.selectbox("Seleccione el Taller:", nombres_taller)

# Lógica de filtrado combinada
if busqueda:
    df_filtrado = df[
        df["NOMBRE DEL TALLER (MAYUSCULAS)"].str.upper().str.contains(busqueda) | 
        df["CIUDAD BASE"].str.upper().str.contains(busqueda) |
        df["COBERTURA INST AA Y LINEA BLANCA"].str.upper().str.contains(busqueda)
    ]
else:
    if seleccion_lista == "TODOS":
        df_filtrado = df
    else:
        df_filtrado = df[df["NOMBRE DEL TALLER (MAYUSCULAS)"] == seleccion_lista]

# --- VISUALIZACIÓN ---
col_map, col_info = st.columns([2, 1])

with col_map:
    # Determinar centro y zoom del mapa según los resultados
    if len(df_filtrado) == 1:
        centro = [df_filtrado["Lat"].iloc[0], df_filtrado["Lon"].iloc[0]]
        zoom = 12
    elif len(df_filtrado) > 1 and len(df_filtrado) < len(df):
        centro = [df_filtrado["Lat"].mean(), df_filtrado["Lon"].mean()]
        zoom = 8
    else:
        centro = [-1.8312, -78.1834] # Centro de Ecuador
        zoom = 7

    m = folium.Map(location=centro, zoom_start=zoom, tiles="CartoDB dark_matter")
    
    for _, r in df_filtrado.iterrows():
        popup_html = f"""
        <div style='color: black;'>
            <b>{r['NOMBRE DEL TALLER (MAYUSCULAS)']}</b><br>
            <b>Ciudad:</b> {r['CIUDAD BASE']}<br>
            <b>Líneas:</b> {r['LINEAS QUE MANEJAN']}<br>
            <b>Contacto:</b> {r['NUMEROS DE CONTACTO']}<br>
            <hr>
            <b>Cobertura:</b> {r['COBERTURA INST AA Y LINEA BLANCA']}
        </div>
        """
        # Cambié el color a verde para diferenciarlo del mapa anterior si gustas
        folium.CircleMarker(
            location=[r['Lat'], r['Lon']],
            radius=9, color='#00ff00', fill=True, fill_color='#00ff00', fill_opacity=0.8,
            popup=folium.Popup(popup_html, max_width=300)
        ).add_to(m)
    
    st_folium(m, width="100%", height=500)

with col_info:
    if len(df_filtrado) == 1:
        row = df_filtrado.iloc[0]
        st.success(f"📍 Taller: {row['NOMBRE DEL TALLER (MAYUSCULAS)']}")
        st.write(f"**Ciudad Base:** {row['CIUDAD BASE']}")
        st.write(f"**Dirección:** {row['DIRECCION ']}")
        st.write(f"**Teléfonos:** {row['NUMEROS DE CONTACTO']}")
        st.write(f"**Líneas que manejan:** {row['LINEAS QUE MANEJAN']}")
        st.write(f"**Email:** {row['CORREOS ELECTRONICOS ']}")
        st.warning(f"**Cobertura de Instalación:** {row['COBERTURA INST AA Y LINEA BLANCA']}")
    elif len(df_filtrado) > 1:
        st.info(f"Se encontraron {len(df_filtrado)} resultados. Selecciona uno en el mapa o en el filtro para ver los detalles exactos.")
    else:
        st.error("No se encontraron resultados para tu búsqueda.")

# Tabla inferior - Siempre visible como me indicaste previamente
columnas_tabla = [
    "NOMBRE DEL TALLER (MAYUSCULAS)", 
    "CIUDAD BASE", 
    "LINEAS QUE MANEJAN", 
    "NUMEROS DE CONTACTO",
    "COBERTURA INST AA Y LINEA BLANCA"
]
st.dataframe(df_filtrado[columnas_tabla], hide_index=True, use_container_width=True)
