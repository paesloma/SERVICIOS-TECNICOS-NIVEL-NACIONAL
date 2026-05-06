import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import numpy as np

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Red Nacional de 41 Talleres", layout="wide")

# Estilo visual modo oscuro
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTextInput > div > div > input { color: white; }
    .stDataFrame { background-color: #161b22; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛠️ Red Nacional de Talleres - 41 Puntos de Servicio")

# 2. BASE DE DATOS INTEGRAL (LOS 41 TALLERES)
@st.cache_data
def obtener_datos_completos():
    data = {
        "NOMBRE DEL TALLER": [
            'ELECTRONICA MANTILLA ', 'FRIOCARD', 'ST COLD', 'MULTISERVICIOS JACK', 'SERVIAIRE ECUADOR', 'PROVATEC', 'CLiMA FRIO', 'JR ELECTRIC', 'MULTITECH RUDY  CEDENO', 'CLISERIN', 'DIGICASLE CENTRO DIGITAL SA', 'PROSERVICIO SAS', 'CISTRONIC ', 'BOR AIR', 'REFRICLIMAMORAN', 'ELECTRÓNICA S.A', 'GAMASERVICES', 'FRIO-STAR', 'RRSERVICENTERRYC', 'KLIMASMART', 'SERVITEC - RONNY BARREZUETA ', 'TALLER DEL SALTO ', 'SERVICIO TECNICO PURO FRIO', 'CLIMAFRIO NARANJITO', 'SERVICIO TÉCNICO CASA FRIA', 'SERMATEC PORTOVIEJO', 'ELECTRONICA 3D', 'TECNIRIOS-ASC', 'Servifrio ', 'Tecnicservice ', 'MEGASERVICE', 'SERMATEC ELECTRONICA', 'MASTERTECH', 'GAMA ELECTRONICS', 'CSTE ELECTRONICA', 'SERVICECOOL ', 'SERVIELEC', 'SERVICIO TECNICO AE', 'SILVER ELECTRONICS', 'ELECTRONICA CENTRAL', 'CSERVICE'
        ],
        "CIUDAD BASE": [
            'AMBATO', 'BABAHOYO', 'DURAN', 'EL COCA', 'GUAYAQUIL', 'GUAYAQUIL', 'GUAYAQUIL', 'GUAYAQUIL', 'GUAYAQUIL', 'GUAYAQUIL', 'GUAYAQUIL', 'GUAYAQUIL', 'GUAYAQUIL', 'GUAYAQUIL', 'GUAYAQUIL', 'IBARRA', 'LAGO AGRIO', 'LAGO AGRIO', 'LOJA', 'MACHALA', 'MANTA', 'MANTA', 'MILAGRO', 'NARANJITO', 'PASAJE', 'PORTOVIEJO', 'PORTOVIEJO', 'QUEVEDO', 'QUEVEDO', 'QUEVEDO', 'QUITO', 'QUITO', 'QUITO', 'RIOBAMBA', 'RIOBAMBA', 'SALINAS', 'SANTO DOMINGO', 'SANTO DOMINGO', 'SANTO DOMINGO', 'SANTO DOMINGO', 'AMBATO'
        ],
        "NUMEROS": [
            '0984139099', '0990045400', '0989842610', '0939407412', '0990965410', '0992821856', '0967899084', '0959628723', '0967588262', '0963091210', '0980684211', '0967550764', '0997898383', '0995583678', '0968139739', '0994234714', '0992897319', '0997620929', '0987533656', '0993647218', '0982808932', '0994406002', '0990510831', '0999637012', '0967432580', '0993549420', '0968485502', '0999221879', '0997949393', '0989078967', '0978928040', '0985706276', '0998260143', '0994215004', '0982868384', '0992048071', '0982553943', '0987684155', '0991090553', '0980408782', '0989980196'
        ],
        "COBERTURA": [
            'TUNGURAHUA, COTOPAXI, PASTAZA', 'BABAHOYO 5KM REDONDA', 'GUAYAQUIL Y DURAN', 'ORELLANA, EL COCA, SACHA', 'GUAYAQUIL, SAMBORONDON, DURAN', 'GUAYAQUIL, VIA COSTA, DAULE', 'GUAYAS, LOS RIOS, PENINSULA', 'GUAYAQUIL, VIA DAULE, SAMBORONDON', 'GUAYAS, LOS RIOS, SANTA ELENA', 'GUAYAQUIL, DAULE, SAMBORONDON', 'GUAYAQUIL, SAMBORONDON, SALITRE', 'GUAYAQUIL, DAULE, PEDRO CARBO', 'GUAYAQUIL CIUDAD', 'GUAYAS, DURAN, DAULE', 'GUAYAQUIL CIUDAD', 'IBARRA, CARCHI', 'SUCUMBIOS, ORELLANA', 'LAGO AGRIO Y ALREDEDORES', 'PROVINCIA DE LOJA, ZAMORA', 'PROVINCIA DE EL ORO', 'MANTA, ZONAS RURALES', 'MANTA, JARAMIJO, MONTECRISTI', 'MILAGRO, NARANJAL, TRIUNFO', 'NARANJITO, BUCAY, MILAGRO', 'EL ORO, AZUAY, GUAYAS', 'MANABI CENTRAL', 'PORTOVIEJO CIUDAD', 'QUEVEDO, LA MANA, VALENCIA', 'QUEVEDO, EL EMPALME', 'QUEVEDO Y CANTONES ALEDAÑOS', 'QUITO, VALLES, CAYAMBE', 'QUITO, TAMBILLO, SANGOLQUI', 'QUITO, VALLE CHILLOS, CUMBAYA', 'CHIMBORAZO COMPLETO', 'CHIMBORAZO Y BOLIVAR', 'SANTA ELENA, SALINAS, PLAYAS', 'SANTO DOMINGO Y NORTE MANABI', 'SANTO DOMINGO, ESMERALDAS', 'SANTO DOMINGO, LA CONCORDIA', 'SANTO DOMINGO CIUDAD', 'TUNGURAHUA, COTOPAXI, CHIMBORAZO'
        ],
        "LINEAS": [
            'TVS, AIRES, LINEA BLANCA', 'AIRES, LINEA BLANCA', 'AIRES, LINEA BLANCA', 'TVS, AIRES, LINEA BLANCA', 'AIRES', 'AIRES', 'AIRES, LINEA BLANCA', 'AIRES, LINEA BLANCA', 'TVS, AIRES, LINEA BLANCA', 'TVS, AIRES, LINEA BLANCA', 'TVS, AIRES', 'AIRES', 'TVS, AIRES, LINEA BLANCA', 'AIRES, LINEA BLANCA', 'AIRES, LINEA BLANCA', 'TVS', 'TVS, AIRES', 'AIRES, LINEA BLANCA', 'TVS, LINEA BLANCA', 'TVS, AIRES, LINEA BLANCA', 'TVS, AIRES, LINEA BLANCA', 'AIRES, LINEA BLANCA', 'TVS, AIRES, LINEA BLANCA', 'AIRES, LINEA BLANCA', 'TVS, AIRES, LINEA BLANCA', 'AIRES, LINEA BLANCA', 'TVS', 'TVS, AUDIO', 'AIRES', 'TVS, AIRES, LINEA BLANCA', 'TVS, AIRES, LINEA BLANCA', 'TVS, LINEA BLANCA', 'TVS, AIRES, LINEA BLANCA', 'TVS, LINEA BLANCA', 'TVS, LINEA BLANCA', 'AIRES, LINEA BLANCA', 'AIRES, LINEA BLANCA', 'AIRES, LINEA BLANCA', 'TVS, LINEA BLANCA', 'TVS, AIRES, LINEA BLANCA', 'TVS, LINEA BLANCA'
        ]
    }
    df = pd.DataFrame(data)
    
    # Coordenadas por ciudad
    coords = {
        'AMBATO': [-1.2417, -78.6195], 'BABAHOYO': [-1.8022, -79.5344],
        'DURAN': [-2.1701, -79.8220], 'EL COCA': [-0.4667, -76.9833],
        'GUAYAQUIL': [-2.1894, -79.8891], 'IBARRA': [0.3517, -78.1223],
        'LAGO AGRIO': [0.0860, -76.8820], 'LOJA': [-3.9931, -79.2042],
        'MACHALA': [-3.2581, -79.9554], 'MANTA': [-0.9677, -80.7127],
        'PORTOVIEJO': [-1.0546, -80.4545], 'QUEVEDO': [-1.0225, -79.4600],
        'QUITO': [-0.1807, -78.4678], 'RIOBAMBA': [-1.6636, -78.6546],
        'SALINAS': [-2.2230, -80.9580], 'SANTO DOMINGO': [-0.2530, -79.1754],
        'NARANJITO': [-2.1667, -79.4667], 'PASAJE': [-3.3250, -79.8070],
        'MILAGRO': [-2.1333, -79.5833]
    }

    # Aplicar Jitter (Dispersión) para que los 41 puntos sean visibles
    def get_lat(c, i): return coords.get(c, [-1.8312, -78.1834])[0] + (np.sin(i)*0.012)
    def get_lon(c, i): return coords.get(c, [-1.8312, -78.1834])[1] + (np.cos(i)*0.012)

    df['Lat'] = [get_lat(c, i) for i, c in enumerate(df['CIUDAD BASE'])]
    df['Lon'] = [get_lon(c, i) for i, c in enumerate(df['CIUDAD BASE'])]
    
    return df

df = obtener_datos_completos()

# 3. SIDEBAR Y BUSQUEDA
st.sidebar.header("🔍 Buscador de Red")
query = st.sidebar.text_input("Buscar Taller, Ciudad o Cobertura:", "").upper()

df_filtered = df.copy()
if query:
    mask = df.apply(lambda r: query in r.astype(str).str.upper().values, axis=1)
    df_filtered = df[mask]

# 4. MAPA Y DETALLES
col_map, col_info = st.columns([2, 1])

with col_map:
    # Ajuste de vista inicial
    centro = [-1.8312, -78.1834]
    zoom = 7
    if "GUAYAQUIL" in query: centro, zoom = [-2.1894, -79.8891], 11
    if "QUITO" in query: centro, zoom = [-0.1807, -78.4678], 11

    m = folium.Map(location=centro, zoom_start=zoom, tiles="CartoDB dark_matter")
    for _, r in df_filtered.iterrows():
        folium.Marker(
            location=[r['Lat'], r['Lon']],
            popup=f"<b>{r['NOMBRE DEL TALLER']}</b><br>Telf: {r['NUMEROS']}",
            icon=folium.Icon(color="blue", icon="wrench", prefix="fa")
        ).add_to(m)
    st_folium(m, width="100%", height=500)

with col_info:
    st.metric("Talleres en Red", len(df_filtered))
    if len(df_filtered) == 1:
        res = df_filtered.iloc[0]
        st.success(f"📍 {res['NOMBRE DEL TALLER']}")
        st.write(f"**Líneas:** {res['LINEAS']}")
        st.write(f"**Teléfono:** {res['NUMEROS']}")
        st.info(f"**Cobertura:** {res['COBERTURA']}")
    else:
        st.info("Selecciona un taller o usa el buscador para ver detalles específicos.")

# 5. TABLA MAESTRA (Siempre visible)
st.markdown("---")
st.subheader("📋 Listado Maestro de la Red (41 Talleres)")
st.dataframe(df_filtered[["NOMBRE DEL TALLER", "CIUDAD BASE", "NUMEROS", "LINEAS", "COBERTURA"]], use_container_width=True, hide_index=True)
