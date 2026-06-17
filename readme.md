# Asistente Matemático Híbrido (Neuro-Simbólico)

Este proyecto implementa una arquitectura de **IA Neuro-Simbólica**. El sistema combina la robustez lingüística y la capacidad de desglose de razonamiento de **Qwen2.5-Math-7B** con el rigor lógico e infalible de una ontología matemática en **OWL** gestionada mediante `owlready2` y el motor de inferencia **HermiT**.

## Estructura del Proyecto

El repositorio sigue un estándar de desarrollo modular y limpio:

```text
LLM_Hibrido/
│
├── data/           # Almacenamiento de grafos semánticos e información del dominio (.owl)
├── logs/           # Registros de ejecución y trazas de auditoría de reglas utilizadas
├── src/            # Código fuente del Prompt Builder e integraciones del sistema
│   ├── ontologia.py
│   └── pipeline_hibrido.py
├── README.md       # Documentación e instrucciones generales del proyecto
└── requirements.txt# Dependencias de software necesarias para el entorno local

```

## Instrucciones de Instalación y Configuración

Sigue estos pasos para desplegar y probar el entorno de forma local

### 1. Clonar el repositorio

Abre tu terminal y ejecuta:

```bash
git clone [https://github.com/Lalols12/LLM_Hibrido.git](https://github.com/Lalols12/LLM_Hibrido.git)
cd LLM_Hibrido
```
## Instalar dependencias del sistema

Asegúrate de contar con Python instalado y ejecuta este comando para instalar los requerimientos:

```bash
pip install -r requirements.txt
```

## Inicializar la Ontología

Ejecuta el constructor local de la ontología para invocar al razonador HermiT y materializar el grafo semántico en su carpeta destino:

```bash
Ejecuta el constructor local de la ontología para invocar al razonador HermiT y materializar el grafo semántico en su carpeta destino:
```

