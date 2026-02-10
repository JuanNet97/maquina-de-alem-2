import streamlit as st
from openai import OpenAI
import json

# --- 1. CONFIGURACIÓN VISUAL (ESTÉTICA COMPLETA) ---
st.set_page_config(page_title="La Máquina de Alem", page_icon="🇦🇷", layout="centered")

st.markdown("""
    <style>
    /* 1. FONDO Y ESTRUCTURA (Forzamos !important para anular modo oscuro) */
    .stApp { 
        background-color: #f4f4f4 !important; 
        border-top: 20px solid #D32F2F !important; 
    }
    
    /* 2. TIPOGRAFÍA */
    h1 { 
        color: #D32F2F !important; 
        font-family: 'Helvetica', sans-serif; 
        font-weight: 900; 
        text-transform: uppercase; 
        letter-spacing: -1px; 
        margin-bottom: 5px; 
    }
    
    /* Subtítulos y textos generales */
    h3, p, .stMarkdown { 
        font-family: 'Georgia', serif; 
        color: #333333 !important;
    }
    
    /* CAJA 1: LA FRASE RADICAL (Impacto - Recuadro Rojo) */
    .headline-box {
        background-color: #D32F2F !important;
        color: white !important;
        padding: 30px;
        text-align: center;
        font-family: 'Arial Black', sans-serif;
        font-size: 1.8rem;
        text-transform: uppercase;
        border-radius: 5px;
        margin-bottom: 25px;
        box-shadow: 0 5px 15px rgba(211, 47, 47, 0.3);
        line-height: 1.1;
        border: 2px solid #B71C1C !important;
    }

    /* CAJA 2: TESIS (Análisis - Recuadro Blanco) */
    .thesis-box {
        background-color: #fff !important;
        padding: 25px;
        border-left: 10px solid #212121 !important;
        font-family: 'Georgia', serif;
        color: #333 !important;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        font-size: 1.05rem;
        line-height: 1.6;
    }
    .thesis-label {
        font-size: 0.8rem;
        font-weight: 800;
        color: #9E9E9E !important;
        text-transform: uppercase;
        display: block;
        margin-bottom: 5px;
        letter-spacing: 2px;
    }
    .meme-name {
        color: #D32F2F !important;
        font-weight: 900;
        font-size: 1.4rem;
        text-transform: uppercase;
        display: block;
        margin-bottom: 10px;
    }
    
    /* CAJA 3: EVIDENCIA (Cita - Recuadro Gris) */
    .quote-box {
        background-color: #ECEFF1 !important;
        padding: 20px;
        font-style: italic;
        border-right: 8px solid #B71C1C !important;
        color: #37474F !important;
        margin-bottom: 25px;
        font-size: 1rem;
        border-radius: 5px;
    }
    .quote-author {
        text-align: right;
        font-weight: bold;
        color: #B71C1C !important;
        font-size: 0.9rem;
        margin-top: 10px;
        text-transform: uppercase;
        font-family: 'Helvetica', sans-serif;
    }

   /* BOTONES (Corrección de contraste) */
    .stButton > button { 
        background-color: #212121 !important; /* Fondo Negro */
        color: #FFFFFF !important; /* TEXTO BLANCO PURO OBLIGATORIO */
        border: 2px solid #212121 !important; 
        font-weight: 900 !important; 
        width: 100%; 
        padding: 15px; 
        font-size: 1.1rem;
        text-transform: uppercase; 
        transition: 0.3s; 
        border-radius: 5px;
    }
    
    /* Arreglo específico: A veces Streamlit usa etiquetas <p> dentro del botón */
    .stButton > button p {
        color: #FFFFFF !important; 
    }

    /* Estado Hover (Al pasar el mouse/dedo) */
    .stButton > button:hover { 
        background-color: #424242 !important; 
        color: #FFFFFF !important;
        border-color: #424242 !important;
        transform: translateY(-2px); 
    }
    
    /* Estado Focus/Active (Al hacer click) */
    .stButton > button:focus, .stButton > button:active {
        color: #FFFFFF !important;
        background-color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONEXIÓN CON OPENAI ---
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("⚠️ CRÍTICO: No se detectó la API Key. Configurala en 'Secrets'.")
    st.stop()

# --- 3. CARGA DE CONOCIMIENTO (SIN LÍMITES) ---
@st.cache_data
def cargar_conocimiento():
    try:
        with open("conocimiento.txt", "r", encoding="utf-8") as f:
            return f.read() 
    except FileNotFoundError:
        st.error("⚠️ Error: Falta el archivo 'conocimiento.txt'. Cárgalo en GitHub.")
        st.stop()

base_de_conocimiento = cargar_conocimiento()

# --- 4. INTERFAZ DE USUARIO ---

# --- B. CUERPO PRINCIPAL ---
st.title("/// LA MÁQUINA DE ALEM")
st.markdown("### ¿Qué dice el radicalismo sobre...")

st.info("""
**PROYECTO ACADÉMICO EXPERIMENTAL** Desarrollado en el marco de la investigación de Juan Ignacio Net como parte de su trabajo final de la **Maestría en Comunicación Política de la Universidad Austral**.

Esta API está alimentada exclusivamente por los resultados de la investigación sobre los discursos de los máximos referentes históricos de la Unión Cívica Radical.

⚙️ *El modelo se encuentra actualmente en fase de calibración.*
""")
with st.sidebar:
    st.header("Ficha Técnica")
    st.info("""
    **Autor:** Juan Ignacio Net
    **Maestría:** Comunicación Política (Univ. Austral)
    """)
    **Hipótesis de trabajo:**El radicalismo posee una estructura discursiva caracteristica que se reproduce a lo largo del tiempo con memes y significantes estables y versatiles*. ")

with st.expander("📘 Metodología", expanded=False):
    st.markdown("""
    Esta herramienta opera bajo la matriz teórica de la Tesis que consistio en el analísis de ocho discursos de referentes historicos de la UCR.
    **Procedimiento:**
    1.  **Detección:** Identifica cuál de los **Significantes** (categorías de análisis) se activa con el tema ingresado.
    2.  **Procesamiento:** Genera una postura doctrinaria (Rojo) y una justificación teórica (Blanco).
    3.  **Evidencia:** Rastrea citas textuales en el corpus de discursos cargado en el sistema (Gris).
    """)
tema_usuario = st.text_input("", placeholder="Ej: El veto a las universidades, los jubilados, la corrupción...")

col1, col2 = st.columns([0.65, 0.35])
with col1:
    boton = st.button("HACER HABLAR AL RADICALISMO")
with col2:
    generar_img = st.checkbox("Generar Meme", value=True)

# --- 6. LÓGICA DE PROCESAMIENTO (MODO EXTRACTIVO PURO) ---
# --- 6. LÓGICA DE PROCESAMIENTO (MODO TAXONOMÍA CIENTÍFICA) ---
if boton:
    if tema_usuario:
        with st.spinner("Procesando matriz de significantes..."):
            
            # 1. Definimos TU LISTA EXACTA como la "Constitución" del modelo
            lista_significantes = """
            1. "Ética Pública": Compromiso con la transparencia, honestidad y rechazo a la corrupción. (Ref: Alem, Illia, Alfonsín, De la Rúa, Manes).
            2. "Democracia": Defensa activa de las instituciones, participación popular y libertades civiles. (Ref: Alem, Yrigoyen, Illia, Alfonsín, Manes).
            3. "Juventud": Interpelación a la juventud como sujeto clave de transformación. (Ref: Alem, Alfonsín, Manes).
            4. "Reparación Nacional": Restaurar un orden social justo y democrático frente a injusticias. (Ref: Yrigoyen, Illia, Alfonsín, Manes).
            5. "Sacrificio": Compromiso ético y personal extremo por ideales políticos. (Ref: Alem, Yrigoyen, Alfonsín).
            6. "Unidad Nacional": Cohesión social y política frente a crisis graves. (Ref: Yrigoyen, Alfonsín, De la Rúa, Manes).
            7. "Justicia Social": Distribución equitativa de recursos y oportunidades. (Ref: Illia, Alfonsín, Manes).
            8. "Institucionalidad": Respeto a las instituciones, Constitución y legalidad republicana. (Ref: Alvear, Illia, Alfonsín, De la Rúa).
            9. "Constitucionalismo Ético": Legitimidad basada en la Constitución y valores éticos. (Ref: Illia, Alfonsín, De la Rúa).
            10. "Cambio / Renovación": Renovación frente a la corrupción, inmovilismo y decadencia. (Ref: Alem, Alfonsín, De la Rúa, Manes).
            """

           # --- PROMPT: TRADUCCIÓN SEMÁNTICA HISTÓRICA ---
            prompt_sistema = f"""
            Eres "La Máquina de Alem". Tu objetivo es la DIVULGACIÓN CIENTÍFICA de la Tesis de Maestría provista.
            
            TU BASE DE CONOCIMIENTO (Texto Fuente):
            {base_de_conocimiento}

            TUS CATEGORÍAS DE ANÁLISIS (USAR SOLO ESTAS 10):
            {lista_significantes}

            TU MISIÓN PARA EL TEMA: "{tema_usuario}"

            INSTRUCCIONES DE PROCESAMIENTO:

            PASO 1: CLASIFICACIÓN (El Cerebro)
            - Elige CUÁL de los 10 significantes aplica mejor. Usa el nombre exacto.

            PASO 2: REDACCIÓN POLÍTICA (Recuadro Rojo)
            - Redacta una sentencia política de **EXACTAMENTE 2 o 3 ORACIONES**.
            - Aplica la definición del Significante al tema actual con tono doctrinario.

            PASO 3: BÚSQUEDA SEMÁNTICA (La Clave del Análisis)
            - El tema del usuario es ACTUAL (ej: "Redes Sociales", "Veto Universitario").
            - El texto fuente es HISTÓRICO.
            - **ACCIÓN:** Genera mentalmente una lista de **Palabras Clave Históricas** relacionadas.
              * Ejemplo: Si el tema es "Veto Universitario", busca: "Reforma", "Educación", "Libre Pensamiento", "Autonomía".
              * Ejemplo: Si el tema es "Ajuste a Jubilados", busca: "Desprotegidos", "Solidaridad", "Derechos", "Ancianos".
            - Usa esas palabras clave para escanear el texto y encontrar la cita más pertinente.

            PASO 4: JUSTIFICACIÓN TEÓRICA (Recuadro Blanco)
            - Explica la relación: "¿Cómo se conecta el tema actual con las palabras clave históricas y el Significante elegido?".

            PASO 5: EVIDENCIA (Recuadro Gris)
            - Extrae el fragmento LITERAL encontrado gracias a la búsqueda semántica.
            - Si aun buscando por palabras clave NO encuentras nada relevante, devuelve "null".

            FORMATO JSON:
            {{
                "frase_radical": "Texto de 2 o 3 oraciones...",
                "nombre_meme": "NOMBRE EXACTO DEL SIGNIFICANTE",
                "explicacion_meme": "Justificación que mencione la conexión entre el tema y las palabras clave históricas...",
                "cita_historica": "Texto literal encontrado O null",
                "autor_cita": "Autor y año O null",
                "estilo_visual": "ÉPICA CALLEJERA, INSTITUCIONAL SOLEMNE o MODERNISMO ABSTRACTO",
                "prompt_meme": "Descripción visual"
            }}
            """

            try:
                # Temperatura 0.2: Rigor máximo para que respete la lista
                respuesta = client.chat.completions.create(
                    model="gpt-4o-mini", 
                    response_format={"type": "json_object"},
                    messages=[
                        {"role": "system", "content": prompt_sistema},
                        {"role": "user", "content": f"Tema: {tema_usuario}. Clasifica usando la lista cerrada."}
                    ],
                    temperature=0.2 
                )
                
                datos = json.loads(respuesta.choices[0].message.content)

                # --- OUTPUT VISUAL ---

                # 1. Línea Discursiva (Rojo)
                html_frase = f"""
                <div class="headline-box">
                    <p style="font-size: 1.3rem !important; line-height: 1.4 !important; font-weight: 700 !important; font-family: 'Georgia', serif !important; text-transform: none !important;">
                        "{datos['frase_radical']}"
                    </p>
                </div>
                """
                st.markdown(html_frase, unsafe_allow_html=True)

                # 2. Explicación del Significante (Blanco)
                html_tesis = f"""
                <div class="thesis-box">
                    <span style="font-size:0.8rem; font-weight:bold; color:#9E9E9E; display:block;">🧬 SIGNIFICANTE ACTIVADO (TESIS)</span>
                    <span style="color:#D32F2F; font-weight:900; font-size:1.4rem; text-transform:uppercase;">{datos['nombre_meme']}</span><br>
                    {datos['explicacion_meme']}
                </div>
                """
                st.markdown(html_tesis, unsafe_allow_html=True)

                # 3. Cita Histórica (Solo si es real)
                cita = datos.get('cita_historica')
                if cita and cita != "null" and len(cita) > 10:
                    html_cita = f"""
                    <div class="quote-box">
                        &laquo;{cita}&raquo;
                        <div style="text-align:right; font-weight:bold; color:#B71C1C; margin-top:5px;">&mdash; {datos.get('autor_cita', '')}</div>
                    </div>
                    """
                    st.markdown(html_cita, unsafe_allow_html=True)
                else:
                    # Mensaje de transparencia si no hay cita
                    st.caption("📝 *El archivo de tesis no contiene una cita textual directa para vincular este tema específico.*")

                # --- GENERACIÓN DE IMAGEN ---
                if generar_img:
                    st.write("---")
                    st.markdown("**📢 Propaganda Generada por la Máquina:**")
                    with st.spinner(f"Renderizando estética: {datos.get('estilo_visual', 'ÉPICA CALLEJERA')}..."):
                        
                        ESTILOS_UCR = {
                            "ÉPICA CALLEJERA": "Vintage political lithography poster (Argentina 1983), grainy paper texture. Massive crowd, white berets (boinas blancas), waving red and white UCR flags. Emotional.",
                            "INSTITUCIONAL SOLEMNE": "Brutalist architecture, imposing stone facade of Congress. UCR shield emblem (hammer and quill) engraved in marble. Serious, heavy.",
                            "MODERNISMO ABSTRACTO": "Contemporary Swiss design poster, minimalist typography. Abstract geometric deconstruction of UCR shield. Strict Red (#D32F2F) and White palette."
                        }
                        
                        estilo = ESTILOS_UCR.get(datos.get('estilo_visual'), ESTILOS_UCR["ÉPICA CALLEJERA"])
                        prompt_img = f"{estilo}. Scene: {datos['prompt_meme']}. Text: '{datos['nombre_meme']}'"
                        
                        try:
                            img_res = client.images.generate(model="dall-e-3", prompt=prompt_img, n=1, size="1024x1024", quality="hd", style="vivid")
                            st.image(img_res.data[0].url, caption=f"Estética: {datos.get('estilo_visual')}")
                        except Exception as e:
                            st.warning(f"Error imagen: {e}")

            except Exception as e:
                st.error(f"Error de sistema: {e}")

    else:
        st.warning("Por favor ingresá un tema para consultar a la Máquina.")








