# Evaluación inicial de generación con Qwen 2.5 3B

## Configuración

- Modelo: qwen2.5:3b-instruct-q4_K_M.
- Conjunto: 40 preguntas de desarrollo.
- Recuperación: resultados previamente guardados de embeddings.
- Se conservaron los fragmentos y su orden de recuperación.
- Las respuestas de referencia no se enviaron al modelo.
- El conjunto final no se utilizó.

La configuración detallada, las huellas de los archivos y el digest
del modelo están en data/evaluacion/generacion_3b_v1/configuracion.json.
Los registros individuales se guardaron en esa misma carpeta.
La carpeta data está excluida de Git.

## Resultados operativos

| Resultado | Casos |
| --- | ---: |
| Estructura y extractos comprobados | 17 |
| Salida rechazada por extracto no literal | 17 |
| Error de preparación por límite de entrada | 6 |
| Total registrado | 40 |

De los 40 casos, 34 llegaron a generar una salida.

Entre las 17 salidas que pasaron los controles automáticos,
el programa derivó 12 respuestas y 5 abstenciones.
Estos conteos no miden corrección ni abstención acertada.

## Limitaciones observadas

- DEV-002 y DEV-014 omitieron explicar el cálculo del MAE.
- DEV-004 no explicó suficientemente en qué consiste la alineación.
- DEV-036 y DEV-039 devolvieron una referencia como información
  faltante, sin explicar adecuadamente la ausencia del dato.
- Los errores de extractos requieren distinguir reformulaciones,
  omisiones, referencias incorrectas e invenciones.
- El límite de 3000 bytes pertenece a la implementación.
  No es un conteo de tokens ni un límite demostrado del modelo.
- Los errores técnicos y las salidas rechazadas no se cuentan
  como abstenciones correctas.
- La coincidencia literal no garantiza que una afirmación esté
  respaldada semánticamente ni que responda toda la pregunta.

## Estado

Prototipo experimental con revisión humana pendiente.
No se considera validada la generación de respuestas.

Antes de una nueva evaluación se revisarán el presupuesto de
contexto, la representación de las evidencias y los controles.
Esta ejecución se conservará sin sobrescribir sus resultados.
