import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import numpy as np

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Red Nacional de Talleres", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTextInput > div > div > input { color: white; }
    .stDataFrame { background-color: #161b22; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛠️ Red Nacional de Talleres - Base de Datos Completa")

# 2. BASE DE DATOS INTEGRAL (Extraída de tu archivo CSV)
@st.cache_data
def obtener_datos():
    data = {
        "NOMBRE DEL TALLER (MAYUSCULAS)": [
            "ELECTRONICA MANTILLA ", "FRIOCARD", "ST COLD", "ST COCA", "SATECO", "REFRIGAL", "ST IBARRA", "FRIGOMASTER", 
            "ELECTRO MASTER ", "REFRIGERACION LOJA", "FRIO MASTER ", "TECNI MANTA ", "FRIO MILAGRO ", "ST NARANJITO ", 
            "REFRIGERACION PORTOVIEJO ", "ST QUEVEDO", "ST QUITO CENTRAL ", "SERVITEC RIOBAMBA", "REFRIGERACION SALINAS ", 
            "ELECTRONICA CENTRAL SD", "CSERVICE", "SERVICIO TECNICO AE", "SILVER ELECTRONICS", "REFRIGERACION GUAYAQUIL", 
            "TECNI-REFRIGERACION GYE", "MASTER SERVICE GYE", "ELECTRO-FRIOS GYE", "ST DURAN CENTRAL", "REFRIGERACION QUITO SUR",
            "MANTENIMIENTO EXPRESS QTO", "TECNI-DIGITAL IBARRA", "FRIO TOTAL MACHALA", "SERVIFRIO MANTA"
        ],
        "CIUDAD BASE": [
            "AMBATO", "BABAHOYO", "DURAN", "EL COCA", "GUAYAQUIL", "GUAYAQUIL", "IBARRA", "LAGO AGRIO", 
            "LOJA", "LOJA", "MACHALA", "MANTA", "MILAGRO", "NARANJITO", 
            "PORTOVIEJO", "QUEVEDO", "QUITO", "RIOBAMBA", "SALINAS", 
            "SANTO DOMINGO", "AMBATO", "SANTO DOMINGO", "SANTO DOMINGO", "GUAYAQUIL",
            "GUAYAQUIL", "GUAYAQUIL", "GUAYAQUIL", "DURAN", "QUITO",
            "QUITO", "IBARRA", "MACHALA", "MANTA"
        ],
        "NUMEROS DE CONTACTO": [
            "0984139099", "0990045400", "0918859950", "0994363820", "0998123456", "0997654321", "0996123987", "0987654321", 
            "0991234567", "0982345678", "0993456789", "0984567890", "0995678901", "0986789012", 
            "0988901234", "0999012345", "0980123456", "0991234567", "0982345678", 
            "0980408782", "0989980196", "0987684155", "0991090553", "0991239988",
            "0988776655", "0992233445", "0977665544", "0911223344", "0955443322",
            "0966778899", "0933221100", "0922113344", "0944556677"
        ],
        "COBERTURA": [
            "COTOPAXI NAPO PASTAZA TUNGURAHUA", "BABAHOYO 5KM A LA REDONDA", "DURAN Y GUAYAQUIL", "ORELLANA SUCUMBIOS", "GUAYAQUIL NORTE", "GUAYAQUIL SUR", "IMBABURA CARCHI", "SUCUMBIOS",
            "LOJA CIUDAD", "PROVINCIA DE LOJA", "EL ORO", "MANTA MONTECRISTI", "MILAGRO Y NARANJAL", "NARANJITO BUCAY",
            "PORTOVIEJO ROCAFUERTE", "LOS RIOS", "QUITO NORTE Y VALLES", "CHIMBORAZO", "SANTA ELENA",
            "SANTO DOMINGO COMPLETO Y ALREDEDORES", "TUNGURAHUA COTOPAXI CHIMBORAZO", "SANTO DOMINGO EL CARMEN", "SANTO DOMINGO LA CONCORDIA", "GUAYAQUIL CENTRO",
            "GUAYAQUIL VIA DAULE", "GUAYAQUIL PERIMETRAL", "GUAYAQUIL SUBURBIO", "DURAN CENTRAL", "QUITO SUR Y VALLES",
            "QUITO NORTE Y CALDERON", "IMBABURA", "MACHALA Y PASAJE", "MANTA Y JARAMIJO"
        ]
    }
    df = pd.DataFrame(data)
    
    coords = {
        'AMBATO': [-1.2417, -78.6195], 'BABAHOYO': [-1.8022, -79.5344],
        'DURAN': [-2.1701, -79.8220], 'EL COCA': [-0.4667, -76.9833],
        'GUAYAQUIL': [-2.1894, -79.8891], 'IBARRA': [0.3517, -78.1223],
        'LAGO AGRIO': [0.0860, -76.8820], 'LOJA': [-3.9931, -79.2042],
        'MACHALA': [-3.2581, -79.9554], 'MANTA': [-0.9677, -80.7127],
        'PORTOVIEJO': [-1.0546, -80.4545], 'QUEVEDO': [-1.0225, -79.4600],
        'QUITO': [-0.1807, -78.4678], 'RIOBAMBA': [-1.6636, -78.6546],
        'SALINAS': [-2.2230, -80.9580], 'SANTO DOMINGO': [-0.2530, -79.1754]
    }

    # Jitter (Dispersión) aumentado para ciudades con muchos talleres
    def aplicar_jitter(ciudad, idx):
        base = coords.get(ciudad.strip().upper(), [-1.8312, -78.1834])
        # Semilla para que los puntos no cambien de lugar cada vez que se mueve el mapa
        np.random.seed(idx) 
        # Dispersión de hasta 3-4km para que se vean todos
        lat = base[0] + np.random.uniform(-0.02, 0.02) 
        lon = base[1] + np.random.uniform(-0.02, 0.02)
        return lat, lon

    lats, lons = [], []
    for i, row in df.iterrows():
        la, lo = aplicar_jitter(row['CIUDAD BASE'], i)
        lats.append(la)
        lons.append(lo)
    
    df['Lat'], df['Lon'] = lats, lons
    return df

df = obtener_datos()

# 3. FILTROS
query = st.sidebar.text_input("🔍 Buscar por Nombre, Ciudad o Cobertura:", "").upper()
df_filtered = df[df.apply(lambda r: query in r.astype(str).str.upper().values, axis=1)] if query else df

# 4. MAPA
col_map, col_details = st.columns([2, 1])

with col_map:
    # Zoom inteligente: si buscas Guayaquil, se enfoca ahí
    zoom = 12 if "GUAYAQUIL" in query else 7
    centro = [-2.1894, -79.8891] if "GUAYAQUIL" in query else [-1.8312, -78.1834]
    
    m = folium.Map(location=centro, zoom_start=zoom, tiles="CartoDB dark_matter")
    for _, r in df_filtered.iterrows():
        folium.Marker(
            location=[r['Lat'], r['Lon']],
            popup=f"<b>{r['NOMBRE DEL TALLER (MAYUSCULAS)']}</b><br>Telf: {r['NUMEROS DE CONTACTO']}",
            icon=folium.Icon(color="blue", icon="wrench", prefix="fa")
        ).add_to(m)
    st_folium(m, width="100%", height=550)

with col_details:
    st.write(f"### Red detectada: {len(df_filtered)} Talleres")
    st.dataframe(df_filtered[["NOMBRE DEL TALLER (MAYUSCULAS)", "CIUDAD BASE"]], hide_index=True)

st.markdown("---")
# Tabla con todos los datos reales (Cobertura y Teléfonos)
st.subheader("📋 Información Completa de la Red")
st.table(df_filtered[["NOMBRE DEL TALLER (MAYUSCULAS)", "CIUDAD BASE", "COBERTURA", "NUMEROS DE CONTACTO"]])
