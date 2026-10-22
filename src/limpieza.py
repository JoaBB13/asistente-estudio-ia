"""Limpieza conservadora del texto extraído de las diapositivas."""

import re


PIE_DOCENTE = re.compile(
    r"^\s*©\s*gonzalezhalexis@gmail\.com\s*©\s*$",
    flags=re.IGNORECASE,
)

LIGADURAS = str.maketrans({
    "ﬁ": "fi",
    "ﬂ": "fl",
    "ﬀ": "ff",
    "ﬃ": "ffi",
    "ﬄ": "ffl",
})


def limpiar_texto(texto):
    """Limpia espacios y el pie conocido, conservando líneas y símbolos."""
    texto = texto.translate(LIGADURAS)
    texto = texto.replace("\r\n", "\n").replace("\r", "\n")
    texto = texto.replace("\u00a0", " ")

    lineas = []

    for linea in texto.splitlines():
        if PIE_DOCENTE.fullmatch(linea):
            continue

        linea = re.sub(r"[ \t]+", " ", linea).strip()
        lineas.append(linea)

    limpio = "\n".join(lineas)
    limpio = re.sub(r"\n{3,}", "\n\n", limpio)

    return limpio.strip()
