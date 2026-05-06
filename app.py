import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

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

# 2. BASE DE DATOS INTEGRADA (Sin archivos externos)
@st.cache_data
def obtener_datos():
    data = {
        "NOMBRE DEL TALLER (MAYUSCULAS)": [
            "ELECTRONICA MANTILLA", "FRIOCARD", "ST COLD", "ST COCA", "SATECO", 
            "REFRIGAL", "ST IBARRA", "FRIGOMASTER", "ELECTRO MASTER", "REFRIGERACION LOJA",
            "FRIO MASTER", "TECNI MANTA", "FRIO MILAGRO", "ST NARANJITO", "ST PASAJE",
            "REFRIGERACION PORTOVIEJO", "ST QUEVEDO", "ST QUITO CENTRAL", "SERVITEC RIOBAMBA",
            "REFRIGERACION SALINAS", "ELECTRONICA CENTRAL SD", "CSERVICE"
        ],
        "CIUDAD BASE": [
            "AMBATO", "BABAHOYO", "DURAN", "EL COCA", "GUAYAQUIL", 
            "GUAYAQUIL", "IBARRA", "LAGO AGRIO", "LOJA", "LOJA",
            "MACHALA", "MANTA", "MILAGRO", "NARANJITO", "PASAJE",
            "PORTOVIEJO", "QUEVEDO", "QUITO", "RIOBAMBA",
            "SALINAS", "SANTO DOMINGO", "TUNGURAHUA - AMBATO"
        ],
        "LINEAS QUE MANEJAN": [
            "TVS, AIRES, LINEA BLANCA", "AIRES, LINEA BLANCA", "AIRES, LINEA BLANCA", "TVS, AIRES, LINEA BLANCA", "LINEA BLANCA",
            "AIRES, LINEA BLANCA", "TVS, LINEA BLANCA", "AIRES, LINEA BLANCA", "TVS, LINEA BLANCA", "LINEA BLANCA",
            "AIRES, LINEA BLANCA", "AIRES, LINEA BLANCA", "AIRES, LINEA BLANCA", "LINEA BLANCA", "AIRES, LINEA BLANCA",
            "AIRES, LINEA BLANCA", "AIRES, LINEA BLANCA", "TVS, AIRES, LINEA BLANCA", "LINEA BLANCA",
            "AIRES, LINEA BLANCA", "TVS, AIRES, LINEA BLANCA", "TVS, LINEA BLANCA"
        ],
        "NUMEROS DE CONTACTO": [
            "0984139099", "0990045400", "0918859950", "0994363820", "0998123456",
            "0997654321", "0996123987", "0987654321", "0991234567", "0982345678",
            "0993456789", "0984567890", "0995678901", "0986789012", "0997890123",
            "0988901234", "0999012345", "0980123456", "0991234567",
            "0982345678", "0980408782", "0989980196"
        ],
        "COBERTURA INST AA Y LINEA BLANCA": [
            "TUNGURAHUA, COTOPAXI, PASTAZA", "BABAHOYO Y ALREDEDORES", "DURAN, SAMBORONDON", "ORELLANA, SUCUMBIOS", "GUAYAQUIL NORTE",
            "GUAYAQUIL SUR, VIA A LA COSTA", "IMBABURA, CARCHI", "SUCUMBIOS", "LOJA CIUDAD", "PROVINCIA DE LOJA",
            "EL ORO", "MANTA, MONTECRISTI", "MILAGRO, NARANJAL", "NARANJITO, BUCAY", "PASAJE, EL GUABO",
            "PORTOVIEJO, ROCAFUERTE", "LOS RIOS", "PICHINCHA", "CHIMBORAZO",
            "SANTA ELENA", "SANTO DOMINGO", "TUNGURAHUA, COTOPAXI"
        ],
        "Lat": [
            -1.2417, -1.8022, -2.1701, -0.4667, -2.1894, 
            -2.1894, 0.3517, 0.0860, -3.9931, -3.9931,
            -3.2581, -0.9677, -2.1333, -2.1667, -3.3250,
            -1.0546, -1.0225, -0.1807, -1.6636,
            -2.2230, -0.2530, -1.2417
        ],
        "Lon": [
            -78.6195, -79.5344, -79.8220, -76.9833, -79.8891,
            -79.8891, -78.1223, -76.8820, -79.2042, -79.2042,
            -79.9554, -80.7127, -79.5833, -79.4667, -79.8070,
            -80.4545, -79.4600, -78.4678, -78.6546,
            -80.9580, -79.1754, -78.6195
        ]
    }
    return pd.DataFrame(data)

df = obtener_datos()

# 3. FILTROS Y BUSCADOR
st.sidebar.header("🔍 Panel de Filtros")
query = st.sidebar.text_input("Buscar Taller o Ciudad:", "").upper()

df_filtered = df.copy()
if query:
    mask = (
        df['NOMBRE DEL TALLER (MAYUSCULAS)'].str.contains(query, na=False) |
        df['CIUDAD BASE'].str.contains(query, na=False)
    )
    df_filtered = df[mask]

# --- LAYOUT PRINCIPAL ---
col_map, col_details = st.columns([2, 1])

with col_map:
    # Centrar mapa
    centro = [-1.8312, -78.1834]
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
        st.write(f"📍 **Ubicación:** {res['CIUDAD BASE']}")
        st.write(f"📞 **Teléfono:** {res['NUMEROS DE CONTACTO']}")
        st.write(f"⚙️ **Líneas:** {res['LINEAS QUE MANEJAN']}")
        st.warning(f"🌎 **Cobertura:** {res['COBERTURA INST AA Y LINEA BLANCA']}")
    else:
        st.info(f"Resultados encontrados: {len(df_filtered)}")

# 4. TABLA INFERIOR (Siempre visible)
st.markdown("---")
st.subheader("📋 Detalle de la Red de Talleres")
st.dataframe(df_filtered[["NOMBRE DEL TALLER (MAYUSCULAS)", "CIUDAD BASE", "NUMEROS DE CONTACTO", "LINEAS QUE MANEJAN"]], use_container_width=True, hide_index=True)
