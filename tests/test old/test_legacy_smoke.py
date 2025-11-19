import pytest
from django.db import connections

@pytest.mark.django_db
def test_legacy_query_no_revienta():
    """
    La conexión 'legacy' existe y una consulta simple no explota.
    No exigimos cantidad: puede devolver 0..n filas.
    """
    assert "legacy" in connections.databases

    from legacyApp.models import ControlesPrevios
    qs = ControlesPrevios.objects.using("legacy").all()[:1]
    assert qs is not None
