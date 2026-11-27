from assistant.privacy import mask


def test_masks_email_cpf_and_enrollment():
    text = "Sou Ana, matrícula 512345, cpf 123.456.789-09, email ana@alu.ufc.br. Qual o prazo?"
    masked = mask(text)
    assert "512345" not in masked and "123.456.789-09" not in masked and "ana@alu.ufc.br" not in masked
    assert "[matrícula]" in masked and "[cpf]" in masked and "[email]" in masked


def test_keeps_years_and_article_numbers():
    assert mask("O Art. 12 vale desde 2016?") == "O Art. 12 vale desde 2016?"
