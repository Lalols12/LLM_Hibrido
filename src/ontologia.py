from owlready2 import *
from owlready2 import OwlReadyInconsistentOntologyError

iri_base = "http://escom.ipn.mx/onto/math_assistant.owl"
onto = get_ontology(iri_base)

with onto:
    # Clases principales para representar los componentes matemáticos
    class ComponenteMatematico(Thing): pass
    class ConceptoTeorico(ComponenteMatematico): pass
    class OperacionCalculo(ComponenteMatematico): pass
    class MetodoSolucion(ComponenteMatematico): pass
    
    # Nuevas clases de control lógico para evitar alucinaciones
    class PropiedadFuncion(Thing): pass
    class FuncionContinua(PropiedadFuncion): pass
    class FuncionDiscontinua(PropiedadFuncion): 
        disjoint_with = [FuncionContinua] 

    # Propiedades de objeto para modelar relaciones lógicas y metodológicas
    class esRequisitoDe(ObjectProperty, TransitiveProperty):
        domain = [ComponenteMatematico]
        range  = [ComponenteMatematico]

    class seAplicaEn(ObjectProperty):
        domain = [MetodoSolucion]
        range  = [OperacionCalculo]

    class esResueltoPor(ObjectProperty):
        domain = [OperacionCalculo]
        range  = [MetodoSolucion]
        inverse_property = seAplicaEn

    class vaSeguidoDe(ObjectProperty):
        domain = [MetodoSolucion]
        range  = [MetodoSolucion]

    # Propiedades de datos para enriquecer la representación con información textual y alertas de control
    class expresionLatex(DataProperty):
        domain = [ComponenteMatematico]
        range  = [str]

    class explicacionSemantica(DataProperty):
        domain = [ComponenteMatematico]
        range  = [str]

    class advertenciaAlucinacion(DataProperty):
        domain = [MetodoSolucion]
        range  = [str]

    # Poblamos la ontología con conceptos, operaciones y métodos específicos del cálculo
    tfc = ConceptoTeorico("TeoremaFundamentalDelCalculo")
    integral_indefinida = OperacionCalculo("IntegralIndefinida")
    
    # Desglosamos los pasos de la Integración por Partes para el CoT
    paso_identificar_udv = MetodoSolucion("Paso1_Identificar_U_dV")
    paso_aplicar_formula = MetodoSolucion("Paso2_AplicarFormula")

    # Enlace lógico entre los conceptos y operaciones
    tfc.explicacionSemantica = ["Conecta la derivación con la integración, permitiendo evaluar integrales mediante la antiderivada."]
    
    paso_identificar_udv.explicacionSemantica = ["Elegir 'u' usando la regla ILATE y 'dv' como el resto del integrando."]
    paso_identificar_udv.expresionLatex = ["u = f(x), db = g'(x)dx"]
    paso_identificar_udv.advertenciaAlucinacion = ["No olvides calcular correctamente 'du' derivando y 'v' integrando; un error de signo aquí arruinará el CoT."]
    
    paso_aplicar_formula.expresionLatex = ["\\int u dv = u v - \\int v du"]
    
    # Definimos el orden secuencial del razonamiento
    paso_identificar_udv.vaSeguidoDe.append(paso_aplicar_formula)
    paso_aplicar_formula.seAplicaEn.append(integral_indefinida)

# Verificación de la consistencia lógica del grafo
print("[INFO] Ejecutando HermiT con la estructura enriquecida...")
with onto:
    try:
        sync_reasoner()
        print("[ÉXITO] Grafo consistente para producción.")
    except OwlReadyInconsistentOntologyError as e:
        print(f"[ERROR] Contradicción lógica detectada: {e}")

onto.save(file="ontologia_matematica_base.owl", format="rdfxml")