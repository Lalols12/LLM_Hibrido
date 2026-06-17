from owlready2 import *
import os

# Definimos la ruta local de la ontología mapeada en tu estructura
RUTA_ONTOLOGIA = os.path.join(os.path.dirname(__file__), "..", "data", "ontologia_matematica_base.owl")

print("[INFO] Cargando ontología localmente...")
onto = get_ontology(f"file://{os.path.abspath(RUTA_ONTOLOGIA)}").load()

with onto:
    sync_reasoner()

def construir_prompt_guiado(problema_texto, operacion_target="IntegralIndefinida"):
    
    operacion = onto[operacion_target]
    
    if not operacion:
        return f"Problema: {problema_texto}\nSolución:", {}
        
    # Inicializamos el diccionario que servirá para cumplir la petición del doctor (Logs)
    log_reglas = {
        "operacion_detectada": operacion_target,
        "metodos_autorizados": [],
        "advertencias_aplicadas": []
    }
    
    contexto_ontologico = "Sigue estrictamente estas reglas axiomáticas para resolver el problema:\n"
    
    # HermiT resuelve la propiedad inversa aquí
    for metodo in operacion.esResueltoPor:
        log_reglas["metodos_autorizados"].append(metodo.name)
        contexto_ontologico += f"- Método Autorizado: {metodo.name}\n"
        
        if metodo.explicacionSemantica:
            contexto_ontologico += f"  Descripción: {metodo.explicacionSemantica[0]}\n"
        if metodo.expresionLatex:
            contexto_ontologico += f"  Fórmula Formal LaTeX: {metodo.expresionLatex[0]}\n"
        if metodo.advertenciaAlucinacion:
            log_reglas["advertencias_aplicadas"].append(metodo.advertenciaAlucinacion[0])
            contexto_ontologico += f"  [RESTRICCIÓN CRÍTICA]: {metodo.advertenciaAlucinacion[0]}\n"
            
        if metodo.vaSeguidoDe:
            for siguiente in metodo.vaSeguidoDe:
                contexto_ontologico += f"  - Paso Siguiente Obligatorio: Ejecutar {siguiente.name}\n"

    prompt_completo = f"""<|im_start|>system
Eres un Asistente Matemático de Alta Precisión. 
{contexto_ontologico}
Genera tu respuesta desglosando tu razonamiento paso a paso.<|im_end|>
<|im_start|>user
Resuelve el siguiente problema: {problema_texto}<|im_end|>
<|im_start|>assistant
Pensamiento:\n"""
    
    return prompt_completo, log_reglas