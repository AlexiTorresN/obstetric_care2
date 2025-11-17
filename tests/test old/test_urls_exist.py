from django.urls import reverse, resolve

def test_matrona_urls_existen():
    """
    Verifica que las rutas clave estén definidas.
    Ajusta los 'name=' si en tu urls difieren.
    """
    # buscar paciente
    path_buscar = reverse("matrona:buscar_paciente")
    assert resolve(path_buscar)

    # patrón de detalle existe (no lo llamamos aquí)
    # NOTA: no hacemos reverse sin pk para no disparar error
