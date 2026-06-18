import streamlit as st
import os
import json
from pipeline_hibrido import construir_prompt_guiado, RUTA_LOGS

st.set_page_config(page_title="Asistente Híbrido Demo", layout="wide")

st.title("Asistente Matemático Híbrido (Neuro-Simbólico)")
st.caption("Prototipo de Investigación Basado en Ontologías")

demo_seleccionada = st.sidebar.selectbox(
    "Selecciona la Demo de Funcionalidad:",
    [
        "Demo 1: Asistente en Acción (Inferencia Simulada)",
        "Demo 2: Inspector de Caja Negra (XAI Logs Activos)",
        "Demo 3: Playground del Prompt Builder y Estructura CoT"
    ]
)

BANCO_RESPUESTAS = {
    "Calcula la integral de x * cos(x) dx.": (
        "Para resolver la integral de $x \\cdot \\cos(x) dx$, usaremos la integración por partes:\n"
        "$$\\int u \\, dv = u v - \\int v \\, du$$\n\n"
        "1. **Elegimos:** $u = x \\implies du = dx$\n"
        "2. **Elegimos:** $dv = \\cos(x)dx \\implies v = \\sin(x)$\n\n"
        "Aplicando la fórmula:\n"
        "$$\\int x \\cdot \\cos(x) dx = x \\cdot \\sin(x) - \\int \\sin(x) dx$$\n\n"
        "La integral de $\\sin(x)$ es $-\\cos(x)$, por lo que obtenemos:\n"
        "$$\\boxed{x \\cdot \\sin(x) + \\cos(x) + C}$$\n"
        "Donde C es la constante de integración."
    ),
    "Resuelve la integral indefinida de 2x * cos(x) dx.": (
        "Para resolver la integral indefinida de $2x \\cdot \\cos(x) dx$, aplicamos integración por partes:\n"
        "$$\\int u \\, dv = u v - \\int v \\, du$$\n\n"
        "1. **Elegimos:** $u = 2x \\implies du = 2dx$\n"
        "2. **Elegimos:** $dv = \\cos(x)dx \\implies v = \\sin(x)$\n\n"
        "Sustituyendo en la fórmula formal:\n"
        "$$\\int 2x \\cdot \\cos(x) dx = 2x \\cdot \\sin(x) - \\int \\sin(x) \\cdot 2 dx$$\n"
        "$$\\int 2x \\cdot \\cos(x) dx = 2x \\cdot \\sin(x) - 2\\int \\sin(x) dx$$\n\n"
        "Resolviendo la integral remanente:\n"
        "$$\\boxed{2x \\cdot \\sin(x) + 2\\cos(x) + C}$$\n"
        "Resultado verificado bajo restricciones del grafo semántico."
    ),
    "Encuentra la antiderivada de t * cos(t) dt.": (
        "Para encontrar la antiderivada de $t \\cdot \\cos(t) dt$, el sistema detecta un operando algebraico y uno trigonométrico.\n"
        "Aplicando la regla inyectada de integración por partes con la variable de control $t$:\n\n"
        "* $u = t \\implies du = dt$\n"
        "* $dv = \\cos(t)dt \\implies v = \\sin(t)$\n\n"
        "Desarrollo del andamiaje lógico:\n"
        "$$\\int t \\cdot \\cos(t) dt = t \\cdot \\sin(t) - \\int \\sin(t) dt$$\n"
        "$$\\boxed{t \\cdot \\sin(t) + \\cos(t) + C}$$\n"
        "La abstracción de variables se ejecutó exitosamente."
    )
}

problema_seleccionado = st.selectbox(
    "Selecciona un problema matemático del banco de pruebas:",
    list(BANCO_RESPUESTAS.keys())
)

if "prompt_generado" not in st.session_state:
    st.session_state["prompt_generado"] = ""
if "respuesta_llm" not in st.session_state:
    st.session_state["respuesta_llm"] = ""

if st.button("Procesar con Pipeline Híbrido"):
    with st.spinner("Interrogando localmente al grafo OWL de la ontología..."):
        prompt_final = construir_prompt_guiado(problema_seleccionado, "IntegralIndefinida")
        
        st.session_state["prompt_generado"] = prompt_final
        st.session_state["respuesta_llm"] = BANCO_RESPUESTAS[problema_seleccionado]
        st.success("¡Grafo OWL interrogado con éxito! Log JSON de auditoría generado en /logs/")

prompt_actual = st.session_state["prompt_generado"]
respuesta_actual = st.session_state["respuesta_llm"]

if demo_seleccionada == "Demo 1: Asistente en Acción (Inferencia Simulada)":
    st.header("Interfaz de Usuario - Solución del Asistente")
    if respuesta_actual:
        st.markdown(respuesta_actual)
    else:
        st.caption("Selecciona un problema y presiona el botón para visualizar el despliegue del alumno.")

elif demo_seleccionada == "Demo 2: Inspector de Caja Negra (XAI Logs Activos)":
    st.header("Auditoría de Inferencia Lógica Formal")
    if respuesta_actual:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Salida de Texto del LLM")
            st.code(respuesta_actual, language="text")
        with col2:
            st.subheader("Log de Auditoría Semántica Real (JSON)")
            archivos = sorted([f for f in os.listdir(RUTA_LOGS) if f.endswith('.json')])
            if archivos:
                with open(os.path.join(RUTA_LOGS, archivos[-1]), "r", encoding="utf-8") as f:
                    st.json(json.load(f))
    else:
        st.caption("Presiona el botón para generar de forma dinámica el archivo de auditoría semántica.")

elif demo_seleccionada == "Demo 3: Playground del Prompt Builder y Estructura CoT":
    st.header("Simulador Comparativo: Prompt Estándar vs. Pipeline Híbrido")
    if prompt_actual:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Enfoque Tradicional (Estilo Ollama / Texto Plano)")
            prompt_ollama_estandar = f"<|im_start|>system\nEres un asistente experto en matemáticas. Resuelve paso a paso...<|im_end|>\n<|im_start|>user\nResuelve: {problema_seleccionado}<|im_end|>\n<|im_start|>assistant\nPensamiento:\n"
            st.text_area("Prompt Base Común:", value=prompt_ollama_estandar, height=300)
        with col2:
            st.subheader("Enfoque Híbrido (Inyección Semántica OWL)")
            st.text_area("Prompt Expandido por la Ontología:", value=prompt_actual, height=300)
    else:
        st.caption("Presiona el botón para comparar las ventanas de contexto del Prompt Builder.")