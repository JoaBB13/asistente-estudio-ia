# Evaluación final del MVP

## Ejecución y alcance

Corrida del 15/11/2026, commit 15e7382e8c23eb2b2983bdc15a401004a8631db7.
20 casos: 16 respondibles y 4 no respondibles. Corpus: 697 diapositivas,
sin páginas vecinas añadidas; k=3. Preguntas y referencias no se incorporan
al índice ni se entregan como respuestas esperadas al generador.
TF-IDF se compara con embeddings en recuperación; la generación utiliza embeddings.

Registros originales: data/evaluacion/final_mvp_v1/. El paquete de revisión
revision_final_entrega_20261115T222021Z.json reúne configuración, casos,
contextos, salidas y huellas de los archivos originales. Se conserva fuera de Git.

## Configuración

- Recuperador: intfloat/multilingual-e5-small, revisión 614241f622f53c4eeff9890bdc4f31cfecc418b3.
- Generador: qwen3:4b-instruct-2507-q4_K_M.
- Digest: 0edcdef34593eac1aa2be9c7d06c432dcf81945adca5eca2f27662c18f168ba0.
- Ollama 0.40.16; Python 3.14.4; PyTorch 2.15.0+cpu; scikit-learn 1.9.1.
- Transformers 5.22.2; Sentence Transformers 6.2.0; NumPy 2.5.4.
- Temperatura 0; semilla 42; contexto 4096; salida máxima 512 tokens; 4 hilos; CPU.
- Tokenizador Qwen/Qwen3-4B-Instruct-2507: cdbee75f17c01a7cc42f958dc650907174af0554.
- Corpus SHA-256: 50eacef90daf99538ee6e78fa5a508a4444aad995bc72c91a60f4c0e573224a0.
- Preguntas SHA-256: 11676e3f0260abeca574da32a7386558ca8a6a37eb035992a8a83776efb2face.

El manifiesto contiene las huellas del código, opciones, instrucciones y
dependencias completas. Temperatura y semilla fijadas no garantizan identidad
de resultados entre hardware o versiones diferentes.

## Recuperación

| Medida | Embeddings | TF-IDF |
|---|---:|---:|
| Hit@3 | 15/16 (93,75 %) | 12/16 (75,00 %) |
| Cobertura completa de grupos | 1/1 (100 %) | 1/1 (100 %) |

Diferencia observada: 3 casos, o 18,75 puntos porcentuales de Hit@3.
No constituye una prueba de superioridad general con solo 16 casos respondibles.
Embeddings no recuperó la referencia esperada de FINAL-001. TF-IDF falló
en FINAL-003, FINAL-006, FINAL-008 y FINAL-016. Ambos cubrieron FINAL-013,
el único caso con grupos de evidencias requeridos.

FINAL-001 recuperó una definición alternativa pertinente. Se conserva como
fallo bajo las referencias fijadas; no se modificaron para mejorar el resultado.

## Generación: controles automáticos y comportamiento

- Estructura e identificadores comprobados: 19/20 (95 %).
- Salida inválida: 1/20 (5 %), FINAL-006, por evidencias repetidas.
- Preguntas respondibles: 15 respuestas emitidas y 1 salida inválida, sobre 16.
- Abstenciones totales en preguntas respondibles: 0/16. El fallo no se cuenta como abstención.
- Preguntas no respondibles: 4 abstenciones sobre 4 casos.
- Las 20 respuestas de la API finalizaron con stop; no hubo errores TF-IDF registrados.

El 95 % de controles aprobados no es exactitud de respuestas. FINAL-006 se
conserva como fallo de salida aunque su texto bruto incluya contenido útil.

## Tiempos

Sobre los 20 registros, búsqueda semántica y generación, incluidos los fallos:

- Media: 113.9 s por consulta.
- Mediana: 99.0 s.
- Mínimo: 66.41 s; máximo: 205.50 s.
- Suma de tiempos registrados del pipeline: 2278.90 s (37.98 min).

No incluyen la preparación inicial de índices, la búsqueda TF-IDF posterior
ni toda la escritura de archivos. No son el tiempo completo de pared de la corrida.

## Revisión asistida de respuestas

Revisión preliminar realizada con asistencia de ChatGPT a partir de los registros,
fuentes y criterios adjuntos. No equivale a una corrección humana independiente.
Los registros originales conservan revision_humana pendiente. No se aportó
evidencia de calibración entre dos integrantes; no se afirma que se haya realizado.

Los estados de criterios siguen su orden en cada caso. Se distinguen completitud,
respaldo y corrección conceptual. Las referencias de las 15 respuestas emitidas
apuntan a fuentes suministradas; ello no garantiza pertinencia de cada extracto
ni corrección conceptual. La cobertura parcial de FINAL-004 se describe abajo.

| Caso | Criterios: valoración propuesta | Respaldo contextual | Observación |
|---|---|---|---|
| FINAL-001 | Parcial / No cumple / Parcial | Completo | Definición alternativa respaldada por Fundamentos p.13; omite algoritmos y no expresa explícitamente todos los criterios. Es el fallo de Hit@3 de embeddings, aunque sus fuentes aportan una definición pertinente. |
| FINAL-002 | Cumple / Cumple | Completo | Iniciación en Ciencia de Datos y uso durante el curso. |
| FINAL-003 | Parcial / Cumple / Cumple | Completo | Repite una formulación absoluta del material sobre outliers y errores; debería decir que pueden indicar problemas. Contiene el error de redacción adecu-than. |
| FINAL-004 | Cumple / Parcial | Parcial | Explica que el dato no existe; añade que fue intencionalmente omitido. Esa intención no está establecida en la fuente. |
| FINAL-005 | Cumple / Cumple | Completo | Una variable y descripción de sus características. |
| FINAL-006 | No evaluable: salida rechazada | No evaluable como respuesta entregada | El validador rechazó evidencias repetidas. No es abstención y no se rescata el texto bruto para contarlo como respuesta exitosa. |
| FINAL-007 | Cumple / Cumple | Completo | Peso dividido por altura al cuadrado. |
| FINAL-008 | Cumple / Cumple | Completo a nivel de página | Raíz y expansión por niveles; orden de profundidad debe entenderse como profundidad creciente, no DFS. Los extractos seleccionados enfatizan la cola; la página completa contiene el orden. |
| FINAL-009 | Cumple / Cumple | Completo | Estados posibles, aceptación de cambios, energía y temperatura presentes en el contexto. |
| FINAL-010 | Cumple / Parcial | Completo | Reproduce la explicación del material; conviene explicitar que la estabilidad se compara al cambiar las muestras de entrenamiento. |
| FINAL-011 | Cumple / Cumple / Cumple | Completo | Estimación de parámetros, predicción e inferencia. |
| FINAL-012 | Cumple / Cumple / Cumple | Completo | Descartar el canal intermedio y consecuencias perceptuales. |
| FINAL-013 | Cumple / Cumple / Cumple | Completo | Distingue folds y MAE de ambas iteraciones; añade la primera sin inventar resultados numéricos. Cubre los dos grupos requeridos. |
| FINAL-014 | Cumple / Cumple / Cumple | Completo | Raíz del MSE, unidad original e interpretación. |
| FINAL-015 | Cumple / Cumple / Cumple / Cumple | Completo | Repite los cuatro pasos. La frase final de la fuente sobre atribuir el efecto al azar requiere cautela: no rechazar H0 no demuestra esa explicación. |
| FINAL-016 | No cumple / Cumple | Completo | Repite la imprecisión del material: dependencia lineal no equivale a correlación perfecta entre todos los pares. Eliminar siempre una columna no es una regla universal. |
| FINAL-017 | Cumple / Cumple / Cumple | No aplica | Abstención pertinente: no inventa el porcentaje de Age ni convierte rangos generales en resultados del dataset. |
| FINAL-018 | Cumple / Cumple / Cumple | No aplica | Abstención pertinente: no inventa temperatura ni enfriamiento ni usa max_steps como esos parámetros. |
| FINAL-019 | Cumple / Cumple / Cumple | No aplica | Abstención pertinente frente al contexto enviado; no inventa RMSE. La ausencia señalada se limita al contexto, no a todo el corpus. |
| FINAL-020 | Cumple / Cumple / Cumple | No aplica | Abstención pertinente: no inventa horario de biblioteca. |

Las cuatro abstenciones se consideran pertinentes en esta revisión asistida:
4/4 (100 %), pendiente de confirmación humana. El denominador es pequeño:
cada caso representa 25 puntos porcentuales.

No se define a posteriori una nota global ni se afirma haber alcanzado la meta
de 80 % de respuestas aceptables. La guía original separa dimensiones y no
establece una regla única para combinarlas.

## Limitaciones y discrepancias con el material

Una fuente puede respaldar una frase y a la vez contener una simplificación
conceptual. FINAL-003, FINAL-015 y FINAL-016 muestran este riesgo; no se atribuyen
automáticamente esas imprecisiones solo al modelo.

- Los outliers pueden ser errores, variación aleatoria o hallazgos relevantes:
  [NIST, detección de outliers](https://www.itl.nist.gov/div898/handbook/eda/section3/eda35h.htm).
- No rechazar H0 indica insuficiencia de evidencia para rechazarla; no demuestra
  que el efecto provenga del azar:
  [NIST, pruebas de hipótesis](https://www.itl.nist.gov/div898/handbook/eda/section3/eda35.htm).
- Eliminar una categoría depende del modelo y del problema de colinealidad;
  puede introducir sesgo en otros modelos:
  [scikit-learn, OneHotEncoder](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html).

Estas fuentes se usaron para revisar resultados, no se incorporaron al contexto
del asistente ni modifican la corrida registrada.

El recuperador truncó un fragmento de 543 a 512 tokens, como en desarrollo,
conservando el texto original para mostrarlo. Las entradas del generador cabían
según la estimación de la plantilla HF (máximo 1526 de 3328 tokens presupuestados);
esto no demuestra equivalencia exacta con la plantilla de Ollama.

No se cubren OCR ni información exclusivamente visual. Se evaluó una sola
asignatura, un conjunto manual pequeño y una ejecución por caso, en CPU.
El tiempo de respuesta y la calidad pueden variar entre equipos y ejecuciones.

## Cierre de revisión del equipo

Pendiente: registrar nombres y fecha de los revisores, acuerdos o desacuerdos
con esta propuesta y las valoraciones definitivas según criterios_respuestas.md.
No modificar las respuestas originales ni repetir solo los casos fallidos.
Si la confirmación humana no se completa antes de entregar, declarar este estado.
