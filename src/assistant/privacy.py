"""Mask personal data in a question before it reaches a model or a log (BR5)."""

import re

EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
CPF = re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b")
ENROLLMENT = re.compile(r"\b\d{6,}\b")


def mask(text: str) -> str:
    text = EMAIL.sub("[email]", text)
    text = CPF.sub("[cpf]", text)
    return ENROLLMENT.sub("[matrícula]", text)
