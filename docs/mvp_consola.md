# MVP de consola: estado de integración

Se integraron la recuperación semántica por multilingual-e5-small
y la generación local con qwen3:4b-instruct-2507-q4_K_M.

## Ejecución

Para preparar otra computadora, seguir [Instalación del MVP](instalacion_mvp.md).

Con el entorno virtual activo, los datos preparados, el modelo
instalado en Ollama y el tokenizador disponible en la caché:

    python src/consola_asistente.py

Para realizar una consulta y terminar:

    python src/consola_asistente.py --pregunta "¿Qué representa el MAE?"

La consola conserva el índice durante la sesión.
Cada consulta se registra en data/evaluacion/sesiones_mvp/.
Los registros incluyen fuentes, configuración, huellas y tiempos.

## Verificación inicial

- 25 pruebas automáticas aprobadas.
- Consulta real sobre significado y cálculo del MAE:
  incluyó el valor absoluto y el promedio.
- Referencia recuperada: 10 - Regresión.pdf, página 27.
- Preparación del índice: 37,74 segundos.
- Tiempo de consulta: 80,57 segundos.

El piloto previo de Qwen3 también se abstuvo ante la fecha del examen
y ante el resultado desconocido del proyecto.

## Limitaciones

Estos casos no constituyen una validación completa del asistente.
Las comprobaciones estructurales no garantizan corrección semántica.
El rendimiento observado depende del equipo y de su memoria disponible.
La evaluación ampliada de generación está pendiente de revisión humana.
El conjunto final se ejecutó el 15/11/2026. Consultar
[Resultados finales y revisión asistida](resultados_final_mvp.md).
