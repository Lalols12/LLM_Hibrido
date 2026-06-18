import streamlit as st
import os
import json
import requests
from pipeline_hibrido import construir_prompt_guiado, RUTA_LOGS

st.set_page_config(page_title="Asistente Híbrido Demo", layout="wide")

st.title("Asistente Matemático Híbrido (Neuro-Simbólico)")
st.caption("Prototipo de Investigación Basado en Ontologías")

demo_seleccionada = st.sidebar.selectbox(
    "Selecciona la Demo de Funcionalidad:",
    [
        "Demo 1: Asistente en Acción (Inferencia Real Qwen)",
        "Demo 2: Inspector de Caja Negra (Logs)",
        "Demo 3: Playground del Prompt Builder y Estructura CoT"
    ]
)

problema_input = st.text_input("Ingresa el problema matemático de control:", "Calcula la integral de x * cos(x) dx.")

if st.button("Procesar"):
    with st.spinner("Interrogando al grafo OWL y procesando inferencia en el servidor..."):
        prompt_final = construir_prompt_guiado(problema_input, "IntegralIndefinida")
        st.session_state["prompt_generado"] = prompt_final
        
        URL_SERVIDOR_COLAB = "https://poem-rind-impure.ngrok-free.dev/generate"
        
        try:
            payload = {"prompt": prompt_final}
            respuesta_api = requests.post(URL_SERVIDOR_COLAB, json=payload, timeout=45)
            if respuesta_api.status_code == 200:
                st.session_state["respuesta_llm"] = respuesta_api.json().get("text", "")
                st.success("¡Inferencia y auditoría semántica completadas con éxito!")
            else:
                st.session_state["respuesta_llm"] = "Error: El servidor en Colab devolvió un estado inválido."
        except Exception as e:
            st.session_state["respuesta_llm"] = "[MODO SIMULACIÓN LOCAL]: Para resolver la integral de x * cos(x) dx, aplicando la fórmula de partes inyectada, el resultado es x * sin(x) + cos(x) + C."
            st.warning("No se detectó un servidor Colab activo. Se desplegó una respuesta simulada de control.")

respuesta_actual = st.session_state.get("respuesta_llm", "Presiona el botón de arriba para procesar el problema.")
prompt_actual = st.session_state.get("prompt_generado", "Presiona el botón de arriba para construir el prompt.")

if demo_seleccionada == "Demo 1: Asistente en Acción":
    st.header("Interfaz de Usuario - Solución del Asistente")
    st.info("Esta vista emula lo que el alumno visualiza en producción.")
    st.markdown(f"**Resultado:**\n\n{respuesta_actual}")

elif demo_seleccionada == "Demo 2: Inspector de Caja Negra (Logs)":
    st.header("Auditoría de Inferencia Lógica Formal")
    st.info("Esta vista genera y despliega el registro JSON de auditoría inmediatamente tras presionar procesar.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Salida de Texto del LLM")
        st.code(respuesta_actual, language="text")
    with col2:
        st.subheader("Log de Auditoría Semántica (JSON)")
        archivos = sorted([f for f in os.listdir(RUTA_LOGS) if f.endswith('.json')])
        if archivos:
            with open(os.path.join(RUTA_LOGS, archivos[-1]), "r", encoding="utf-8") as f:
                st.json(json.load(f))
        else:
            st.caption("El archivo JSON aparecerá aquí en cuanto se presione el botón de procesamiento.")

elif demo_seleccionada == "Demo 3: Playground del Prompt Builder y Estructura CoT":
    st.header("Simulador Comparativo: Prompt Estándar vs. Pipeline Híbrido (Neuro-Simbólico)")
    st.info("Compara visualmente cómo cambia la ventana de contexto que recibe el modelo al pasar de una instrucción tradicional a una guiada por ontologías.")
    
    prompt_completo = st.session_state.get("prompt_generado", "Presiona el botón 'Procesar' para construir el prompt.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Enfoque Tradicional (Estilo Ollama / Texto Plano)")
        st.caption("Instrucciones genéricas basadas en lenguaje natural. Alta probabilidad de desvíos lógicos.")
        
        prompt_ollama_estandar = f"""<|im_start|>system
Eres un asistente experto en matemáticas. Por favor, resuelve los problemas que te pida el usuario de forma detallada, explicando paso a paso tu razonamiento (Chain-of-Thought) y utilizando notación LaTeX para las fórmulas.<|im_end|>
<|im_start|>user
Resuelve el siguiente problema: {problema_input}<|im_end|>
<|im_start|>assistant
Pensamiento:\n"""
        
        st.text_area("Prompt Base Común (Sin restricciones formales):", value=prompt_ollama_estandar, height=350)
        st.markdown("""
        **Características de este prompt:**
        * Confía ciegamente en la **memoria estadística** del modelo.
        * No hay control sintáctico sobre qué fórmulas específicas usar.
        * El andamiaje *Chain-of-Thought* es libre; el LLM puede inventar axiomas intermedios si "suenan probables".
        """)

    with col2:
        st.subheader("Enfoque Híbrido (Inyección Semántica OWL)")
        st.caption("Instrucciones dinámicas gobernadas por el razonador HermiT. Contención probabilística estricta.")
        
        st.text_area("Prompt Expandido y Auditado por la Ontología:", value=prompt_completo, height=350)
        st.markdown("""
        **Mejoras inyectadas por tu arquitectura:**
        * **Restricción de Vocabulario:** Se le imponen explícitamente los métodos autorizados deducidos por el grafo.
        * **Rieles Sintácticos:** Se le provee la fórmula exacta en LaTeX extraída de las propiedades de la ontología.
        * **Escudo de Contención:** Inyecta de forma dinámica alertas de alucinación específicas para el tipo de operando analizado.
        """)