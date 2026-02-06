import streamlit as st
from openai import OpenAI
import json

# --- 1. CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="La Máquina de Alem", page_icon="🇦🇷", layout="centered")

st.markdown("""
    <style>
    /* Estética General */
    .stApp { background-color: #f4f4f4; border-top: 20px solid #D32F2F; }
    
    /* Título Principal */
    h1 { color: #D32F2F; font-family: 'Helvetica', sans-serif; font-weight: 900; text-transform: uppercase; letter-spacing: -1px; margin-bottom: 0px; }
    
    /* CAJA 1: LA FRASE RADICAL (Impacto) */
    .headline-box {
        background-color: #D32F2F;
        color: white;
        padding: 25px;
        text-align: center;
        font-family: 'Arial Black', sans-serif;
        font-size: 1.6rem;
        text-transform: uppercase;
        border-radius: 4px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        line-height: 1.2;
    }

    /* CAJA 2: EL MEME DE LA TESIS (Teoría) */
    .thesis-box {
        background-color: #fff;
        padding: 20px;
        border-left: 8px solid #212121; /* Negro UCR */
        font-family: 'Georgia', serif;
        color: #333;
        margin-bottom: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .thesis-label {
        font-size: 0.85rem;
        font-weight: bold;
        color: #757575;
        text-transform: uppercase;
        display: block;
        margin-bottom: 10px;
        letter-spacing: 1px;
    }
    .meme-name {
        color: #D32F2F;
        font-weight: 900;
        font-size: 1.2rem;
        text-transform: uppercase;
    }
    
    /* CAJA 3: EVIDENCIA (Cita) */
    .quote-box {
        background-color: #eceff1;
        padding: 15px;
        font-style: italic;
        border-right: 6px solid #B71C1C;
        color: #455a64;
        margin-bottom: 20px;
        font-size: 0.95rem;
    }
    .quote-author {
        text-align: right;
        font-weight: bold;
        color: #B71C1C;
        font-size: 0.8rem;
        margin-top: 5px;
        text-transform: uppercase;
    }

    /* Botón */
    .stButton>button { background-color: #212121; color: white; border: none; font-weight: bold; width: 100%; padding: 12px; text-transform: uppercase; transition: 0.3s; }
    .stButton>button:hover { background-color: #424242; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONEXIÓN ---
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    st.error("⚠️ Error: Falta API Key.")
    st.stop()

# --- 3. CARGA DE CONOCIMIENTO ---
@st.cache_data
def cargar_conocimiento():
    try:
        with open("conocimiento.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        st.error("⚠️ Error: Falta 'conocimiento.txt'.")
        st.stop()

base_de_conocimiento = cargar_conocimiento()

# --- 4. INTERFAZ ---

st.title("/// LA MÁQUINA DE ALEM")
st.markdown("### ¿Qué dice el radicalismo sobre...?")

st.info("Ingresá el tema sobre el que el partido guarda silencio. La máquina recuperará la voz histórica.")

tema_usuario = st.text_input("", placeholder="Ej: El veto a las universidades, la crisis económica...")

col1, col2 = st.columns([0.65, 0.35])
with col1:
    boton = st.button("HACER HABLAR AL RADICALISMO")
with col2:
    generar_img = st.checkbox("Generar Meme", value=True)

# --- 5. PROCESAMIENTO ---
if boton:
    if tema_usuario:
        with st.spinner("Consultando Tesis y Archivo..."):
            
            # PROMPT CORREGIDO (Sin "Protocolos")
            prompt = f"""
            Eres "La Máquina de Alem". Tu cerebro es esta Tesis y Discursos:
            --- INICIO TEXTO ---
            {base_de_conocimiento}
            --- FIN TEXTO ---

            TAREA:
            El usuario pregunta sobre: "{tema_usuario}".
            
            INSTRUCCIONES CLAVE:
            1. No hables de "protocolos activados" ni lenguaje robótico.
            2. Identifica cuál es el "Meme" o "Significante" de la tesis que aplica (ej: La Reparación, La Intransigencia, El Rezo Laico, La Ética, etc.).

            FORMATO JSON OBLIGATORIO:
            1. "frase_radical": Una sentencia política contundente, estilo slogan, sobre el tema.
            2. "nombre_meme": SOLO el nombre del concepto de la tesis (ej: "LA REPARACIÓN").
            3. "explicacion_meme": Breve justificación teórica de por qué aplica este concepto.
            4. "cita_historica": Cita textual del archivo.
            5. "autor_cita": Autor y año.
            6. "prompt_meme": Descripción visual para DALL-E (Poster político rojo y blanco).
            """

            try:
                # 1. GPT piensa
                respuesta = client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    response_format={"type": "json_object"},
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": tema_usuario}
                    ],
                    temperature=0.5
                )
                
                datos = json.loads(respuesta.choices[0].message.content)

                # 2. OUTPUT 1: La Frase
                st.markdown(f"""
                <div class="headline-box">
                    "{datos['frase_radical']}"
                </div>
                """, unsafe_allow_html=True)

                # 3. OUTPUT 2: El Meme / Significante (Limpio)
                st.markdown(f"""
                <div class="thesis-box">
                    <span class="thesis-label">🧬 MEME / SIGNIFICANTE DE LA TESIS</span>
                    <span class="meme-name">{datos['nombre_meme']}</span><br>
                    {datos['explicacion_meme']}
                </div>
                """, unsafe_allow_html=True)

                # 4. OUTPUT 3: La Cita
                st.markdown(f"""
                <div class="quote-box">
                    «{datos['cita_historica']}»
                    <div class="quote-author">— {datos['autor_cita']}</div>
                </div>
                """, unsafe_allow_html=True)

                # 5. OUTPUT 4: El Meme Visual
                if generar_img:
                    st.write("**Representación Gráfica:**")
                    with st.spinner("Generando imagen..."):
                        try:
                            img = client.images.generate(
                                model="dall-e-3",
                                prompt=f"Political poster graphic design, {datos['prompt_meme']}, text in Spanish: '{datos['frase_radical']}', colors red white and black, propaganda style.",
                                n=1,
                                size="1024x1024"
                            )
                            st.image(img.data[0].url, caption=f"Concepto: {datos['frase_radical']}")
                        except Exception as e:
                            st.warning(f"No se pudo generar imagen: {e}")

            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Escribí un tema.")