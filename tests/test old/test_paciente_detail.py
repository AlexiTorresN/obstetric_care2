import pytest
from datetime import date
from django.urls import reverse
from gestionApp.models import Persona, Paciente


def _first_valid_choice(model, field_name):
    """
    Devuelve la primera clave válida de choices para el campo dado.
    Evita claves vacías o de placeholder.
    """
    field = model._meta.get_field(field_name)
    choices = list(field.choices or [])
    # Filtra placeholders y vacíos
    keys = [k for (k, _v) in choices if k not in ("", None, "Seleccione", "SELECCIONE")]
    if not keys:
        # Si no hay choices, retorna un fallback común
        return None
    return keys[0]


@pytest.mark.django_db
def test_paciente_detail_render_publico(client):
    """
    La vista de detalle renderiza y muestra el panel LEGACY.
    """
    persona = Persona.objects.create(
        Rut="16293109-1",
        Nombre="Ana",
        Apellido_Paterno="Silva",
        Apellido_Materno="Rivas",
        Sexo="F",
        Fecha_nacimiento=date(1987, 5, 12),
        Telefono="+56900000000",
        Email="ana@example.com",
        Direccion="Pasaje Real 1234",
    )

    # Obtener valores válidos desde los choices reales del modelo
    estado_civil_val = _first_valid_choice(Paciente, "Estado_civil")
    previcion_val = _first_valid_choice(Paciente, "Previcion")

    paciente = Paciente.objects.create(
        persona=persona,
        Edad=38,
        Estado_civil=estado_civil_val,
        Previcion=previcion_val,
    )
    url = reverse("matrona:detalle_paciente", args=[paciente.pk])
    r = client.get(url)

    assert r.status_code == 200
    # Si tu template incluye este texto del panel LEGACY:
    assert b"Controles de Rutina Previos (LEGACY)" in r.content

