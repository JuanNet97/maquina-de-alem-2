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
    
    /* CAJA 1: LA FRASE RADICAL (Impacto) */
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

    /* CAJA 2: TESIS (Análisis) */
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
    
    /* CAJA 3: EVIDENCIA (Cita) */
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

# --- 2. CONEXIÓN CON OPENAI ---
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("⚠️ CRÍTICO: No se detectó la API Key. Configurala en 'Secrets'.")
    st.stop()

# --- 3. CARGA DE CONOCIMIENTO (CEREBRO) ---
@st.cache_data
def cargar_conocimiento():
    try:
        with open("conocimiento.txt", "r", encoding="utf-8") as f:
            # Leemos el archivo. Si es GIGANTE (libros enteros), cortamos en 80k caracteres
            # para no saturar la memoria de contexto, pero mantenemos la calidad.
            texto = f.read()
            return texto[:80000] 
    except FileNotFoundError:
        st.error("⚠️ Error: Falta el archivo 'conocimiento.txt'. Cárgalo en GitHub.")
        st.stop()

base_de_conocimiento = cargar_conocimiento()

# --- 4. INTERFAZ DE USUARIO ---

st.title("/// LA MÁQUINA DE ALEM")
st.markdown("### ¿Qué dice el radicalismo sobre...")

st.info("Esta IA está alimentada por la **Tesis de Maestría en Comunicación Política de Juan Ignacio Net** y el **Archivo Histórico de la UCR**. Recuperá la voz del partido.")

tema_usuario = st.text_input("", placeholder="Ej: El veto a las universidades, los jubilados, la corrupción...")

col1, col2 = st.columns([0.65, 0.35])
with col1:
    boton = st.button("HACER HABLAR AL RADICALISMO")
with col2:
    generar_img = st.checkbox("Generar Meme", value=True)

# --- 5. LÓGICA DE PROCESAMIENTO ---
if boton:
    if tema_usuario:
        with st.spinner("Analizando protocolos de la Tesis y Discursos Históricos..."):
            
            # --- EL PROMPT MAESTRO (Volvimos a la versión detallada) ---
            prompt_sistema = f"""
            Eres "La Máquina de Alem", la conciencia histórica y digital de la Unión Cívica Radical.
            
            TU CEREBRO (Base de Conocimiento):
            --- INICIO TEXTO ---
            {base_de_conocimiento}
            --- FIN TEXTO ---

            TU MISIÓN:
            El usuario ingresa un tema actual sobre el cual el partido guarda silencio.
            Tú debes responder basándote EXCLUSIVAMENTE en la teoría de la Tesis (latencia, reparación, ética, institucionalidad) y los discursos históricos provistos.

            REGLAS DE RAZONAMIENTO:
            1. **No inventes fechas:** Extrae el año y autor EXACTO del encabezado de los discursos en el texto provisto.
            2. **Identifica el Significante:** Usa los conceptos de la tesis (ej: "La Reparación", "La Intransigencia", "El Rezo Laico", "La Ética Pública").
            3. **Estilo:** Sé contundente, irónico si es necesario, y épico. Habla como la historia juzgando al presente.

            FORMATO DE SALIDA (JSON Puro):
            1. "frase_radical": Una sentencia política breve y poderosa sobre el tema (Slogan).
            2. "nombre_meme": El nombre exacto del concepto de la tesis que aplica.
            3. "explicacion_meme": Explicación de por qué este concepto teórico resuelve esta crisis.
            4. "cita_historica": Una cita textual del archivo que funcione como evidencia.
            5. "autor_cita": Autor y Año (ej: "Leandro N. Alem, 1896").
            6. "prompt_meme": Descripción visual para un poster de propaganda política.
            """

            try:
                # VOLVEMOS AL MODELO TURBO (Mejor calidad de razonamiento)
                respuesta = client.chat.completions.create(
                    model="gpt-4o-mini", 
                    response_format={"type": "json_object"},
                    messages=[
                        {"role": "system", "content": prompt_sistema},
                        {"role": "user", "content": f"El tema es: {tema_usuario}"}
                    ],
                    temperature=0.6 # Un poco más de creatividad para la frase
                )
                
                datos = json.loads(respuesta.choices[0].message.content)

                # --- MOSTRAR RESULTADOS ---
                
                # 1. LA FRASE (Headline)
                st.markdown(f"""
                <div class="headline-box">
                    "{datos['frase_radical']}"
                </div>
                """, unsafe_allow_html=True)

                # 2. EL SIGNIFICANTE (Tesis)
                st.markdown(f"""
                <div class="thesis-box">
                    <span class="thesis-label">🧬 SIGNIFICANTE ACTIVADO (TESIS)</span>
                    <span class="meme-name">{datos['nombre_meme']}</span>
                    {datos['explicacion_meme']}
                </div>
                """, unsafe_allow_html=True)

                # 3. LA EVIDENCIA (Archivo)
                st.markdown(f"""
                <div class="quote-box">
                    «{datos['cita_historica']}»
                    <div class="quote-author">— {datos['autor_cita']}</div>
                </div>
                """, unsafe_allow_html=True)

                # 4. EL MEME (Imagen con Simbología)
                if generar_img:
                    st.write("---")
                    st.markdown("**📢 Propaganda Generada por la Máquina:**")
                    with st.spinner("Inyectando simbología partidaria en DALL-E..."):
                        
                        # INYECCIÓN DE SÍMBOLOS UCR (Hardcoded para asegurar estética)
                        simbologia_obligatoria = "Argentine Radical Civic Union aesthetics, white berets (boinas blancas), red and white flags, vintage propaganda poster style, high contrast red/white/black palette"
                        
                        # Armamos el prompt final sumando lo que imaginó la IA + los símbolos obligatorios
                        prompt_final_imagen = f"{simbologia_obligatoria}. {datos['prompt_meme']}. Text in Spanish: '{datos['frase_radical']}'"
                        
                        try:
                            img_res = client.images.generate(
                                model="dall-e-3",
                                prompt=prompt_final_imagen,
                                n=1,
                                size="1024x1024",
                                quality="standard"
                            )
                            st.image(img_res.data[0].url, caption=f"Concepto Visual: {datos['frase_radical']}")
                        except Exception as e:
                            st.warning(f"No se pudo generar la imagen (Posible error de API o contenido): {e}")

            except Exception as e:
                # Si falla por Rate Limit (el error 429), le avisamos amablemente al usuario
                if "429" in str(e):
                    st.error("🚦 La Máquina está saturada (Límite de velocidad de OpenAI). Esperá 1 minuto y probá de nuevo.")


