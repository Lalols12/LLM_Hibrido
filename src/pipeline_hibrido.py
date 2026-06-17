from owlready2 import *
import os
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_ONTOLOGIA = os.path.join(BASE_DIR, "data", "ontologia_matematica_base.owl")
RUTA_LOGS = os.path.join(BASE_DIR, "logs")

print("[INFO] Inicializando Pipeline Híbrido...")
onto = get_ontology(f"file://{os.path.abspath(RUTA_ONTOLOGIA)}").load()

with onto:
    sync_reasoner()

def construir_prompt_guiado(problema_texto, operacion_target="IntegralIndefinida"):
    """
    Interroga la ontología, construye el prompt para Qwen y genera un log de auditoría.
    """
    operacion = onto[operacion_target]
    
    log_auditoria = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "problema_recibido": problema_texto,
        "clase_operacion": operacion_target,
        "inferencias_hermit": {
            "metodos_descubiertos_por_inversa": [],
            "dependencias_transitivas_requisito": []
        },
        "restricciones_inyectadas": {
            "formulas_latex": [],
            "alertas_alucinacion": []
        }
    }
    
    if not operacion:
        return f"Problema: {problema_texto}\nSolución:", log_auditoria

    for metodo in operacion.esResueltoPor:
        log_auditoria["inferencias_hermit"]["metodos_descubiertos_por_inversa"].append(metodo.name)
        
        if metodo.expresionLatex:
            log_auditoria["restricciones_inyectadas"]["formulas_latex"].append(metodo.expresionLatex[0])
        if metodo.advertenciaAlucinacion:
            log_auditoria["restricciones_inyectadas"]["alertas_alucinacion"].append(metodo.advertenciaAlucinacion[0])
            

    if hasattr(operacion, "esRequisitoDe"):
        for req in onto.ComponenteMatematico.instances():
            if operacion in req.esRequisitoDe:
                log_auditoria["inferencias_hermit"]["dependencias_transitivas_requisito"].append(req.name)

    contexto = "Sigue estrictamente estas reglas axiomáticas:\n"
    for m in log_auditoria["inferencias_hermit"]["metodos_descubiertos_por_inversa"]:
        contexto += f"- Método Autorizado: {m}\n"
    for f in log_auditoria["restricciones_inyectadas"]["formulas_latex"]:
        contexto += f"  Fórmula LaTeX: {f}\n"
    for a in log_auditoria["restricciones_inyectadas"]["alertas_alucinacion"]:
        contexto += f"  [CRÍTICO]: {a}\n"

    prompt_completo = f"""<|im_start|>system
Eres un Asistente Matemático de Alta Precisión. 
{contexto}
Genera tu respuesta desglosando tu razonamiento paso a paso.<|im_end|>
<|im_start|>user
Resuelve el siguiente problema: {problema_texto}<|im_end|>
<|im_start|>assistant
Pensamiento:\n"""
    
    # 4. Guardar de forma persistente el Log en la carpeta logs/
    nombre_log = f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    ruta_final_log = os.path.join(RUTA_LOGS, nombre_log)
    
    with open(ruta_final_log, "w", encoding="utf-8") as f:
        json.dump(log_auditoria, f, indent=4, ensure_ascii=False)
        
    print(f"[LOG GUARDADO]: {nombre_log}")
    
    return prompt_completo