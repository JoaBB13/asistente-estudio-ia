# Criterios de revisión manual de respuestas

## Propósito

Aplicar reglas comunes para evaluar las respuestas del asistente.

Esta guía complementa `evaluacion.md`. No modifica las métricas
de recuperación ni define una nota global.

Las respuestas de referencia sirven como orientación conceptual:
no se exige repetirlas literalmente.

## Material necesario

Para revisar cada respuesta se conservarán:

- Identificador de la ejecución y del caso.
- Pregunta y respuesta completa del asistente.
- Fragmentos recuperados, en su orden original.
- Contexto efectivamente enviado al generador.
- Citas devueltas por el asistente.
- Respuesta de referencia y criterios del caso.
- Versiones del corpus, preguntas y configuración.
- Nombre del evaluador.

El contexto añadido mediante páginas vecinas se distingue de los
fragmentos originalmente recuperados.

Las respuestas de referencia y los criterios de evaluación no se
incluyen en el contexto enviado al generador.

## 1. Cumplimiento de criterios

Para cada elemento de `criterios_respuesta`, registrar:

- Cumple: expresa correctamente el contenido requerido.
- Parcial: expresa una parte, pero omite otra necesaria.
- No cumple: lo omite, lo contradice o lo explica incorrectamente.

Anotar una justificación breve para los estados parcial y no cumple.

Informar cuántos criterios cumple de los exigidos en ese caso.
No asignar automáticamente medio punto a los criterios parciales.

En preguntas no respondibles, aplicar los criterios específicos
de abstención definidos en el caso.

## 2. Corrección conceptual

Clasificar las afirmaciones sustantivas de la respuesta:

- Sin errores detectados.
- Con errores: registrar la afirmación y explicar el problema.
- No evaluable: no hay una respuesta sustantiva que corregir.

Una omisión afecta la completitud; no implica por sí sola que
lo expresado sea falso.

Una abstención total no se cuenta como respuesta conceptualmente
correcta a una pregunta respondible.

Si se detecta un posible error en la respuesta de referencia o
en la diapositiva, registrar la discrepancia para revisión.
No penalizar automáticamente una formulación científicamente correcta
por no repetir una simplificación del material.

## 3. Respaldo en el contexto

Comprobar si las afirmaciones están sustentadas por el contexto
que realmente recibió el generador:

- Completo: todas las afirmaciones sustantivas están respaldadas.
- Parcial: algunas están respaldadas y otras no.
- Ausente: ninguna está respaldada.
- No aplica: abstención sin afirmaciones sustantivas sobre el tema.

Una afirmación puede ser correcta por conocimiento general y aun así
no estar respaldada por el contexto disponible.

Registrar los agregados no respaldados, aunque parezcan plausibles.

## 4. Calidad de las citas

Revisar por separado:

### Validez de la referencia

Para cada cita, comprobar que el documento y la página existen.
Si incluye un identificador de fragmento, debe coincidir con ellos.

### Pertinencia

Comprobar que la página citada respalda la afirmación a la que
está asociada. Compartir palabras o tema no es suficiente.

### Cobertura

Comprobar que las afirmaciones que requieren respaldo tienen
citas adecuadas:

- Completa.
- Parcial.
- Ausente.
- No aplica: abstención sin afirmaciones que requieran citas.

Una respuesta informativa sin citas tiene cobertura ausente,
aunque su contenido sea correcto.

Una abstención correcta no necesita inventar una cita para justificar
que falta información. Si incluye explicaciones adicionales sobre
el tema, esas afirmaciones sí deben revisarse.

## 5. Abstención

Registrar el comportamiento observado:

- Responde.
- Se abstiene totalmente.
- Responde una parte y declara que falta información para otra.
- Salida vacía o error técnico.

Para preguntas no respondibles, la abstención es correcta si:

1. Reconoce que el material disponible no permite obtener el dato.
2. No inventa ese dato.
3. No atribuye resultados de otros ejemplos al caso consultado.

Responder con información relacionada sin reconocer que falta
el dato solicitado no cuenta como abstención correcta.

Para preguntas respondibles, registrar las abstenciones totales
incorrectas y las abstenciones parciales injustificadas.

Una salida vacía o un error técnico no es una abstención correcta.
Los fallos técnicos se registran y reportan; no se eliminan
silenciosamente de los resultados.

## 6. Ejemplos de calibración

Los siguientes ejemplos son hipotéticos y pertenecen al conjunto
de desarrollo. No son resultados medidos del asistente.

### DEV-002: error absoluto medio

Respuesta hipotética:

"El MAE mide la magnitud promedio del error."

Revisión:

- Describe la interpretación.
- Omite cómo se calcula a partir de los residuos.
- Lo expresado puede ser correcto, pero la respuesta está incompleta.
- Si no incluye citas, su cobertura de citas es ausente.

Respuesta hipotética:

"El MAE se calcula promediando los residuos al cuadrado."

Revisión:

- Contiene un error conceptual.
- No cumple el criterio de cálculo mediante valores absolutos.

### DEV-008: chi-cuadrado frente a ANOVA

Una respuesta que solo explica chi-cuadrado queda incompleta,
aunque esa explicación sea correcta.

Si se recuperó únicamente su evidencia, puede haber acierto
en Hit@3 sin cobertura completa de los grupos requeridos.

El acierto de recuperación no demuestra por sí solo que la
respuesta generada sea correcta y completa.

### DEV-011: fecha y horario del examen final

Respuesta hipotética:

"No encuentro la fecha ni el horario en el material disponible."

Revisión:

- Es una abstención correcta.
- No necesita una cita inventada.

Respuesta hipotética:

"No figura en el material, pero probablemente sea el viernes a las 18."

Revisión:

- No es una abstención correcta.
- Introduce una fecha y un horario sin respaldo.

## 7. Acuerdo entre evaluadores

Antes de evaluar el conjunto final:

1. Elegir algunas respuestas de desarrollo.
2. Hacer que dos integrantes las revisen por separado.
3. Comparar los juicios y discutir diferencias.
4. Aclarar las reglas que generen ambigüedad.
5. Fijar la guía antes de la evaluación final.

Conservar los juicios iniciales y la resolución de desacuerdos.

Cuando sea posible, ocultar el nombre del método durante la
corrección para reducir preferencias por una implementación.

## 8. Registro y reporte

Cada revisión debe incluir:

- Caso y ejecución.
- Evaluador.
- Estado de cada criterio.
- Errores conceptuales detectados.
- Respaldo en el contexto.
- Validez, pertinencia y cobertura de citas.
- Comportamiento de abstención.
- Observaciones y desacuerdos.

No combinar automáticamente estas dimensiones en una única nota.

Informar cantidades absolutas y denominadores. Distinguir
resultados de desarrollo de resultados finales y separar las
preguntas base de sus reformulaciones.