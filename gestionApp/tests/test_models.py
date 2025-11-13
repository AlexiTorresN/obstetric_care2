from django.test import TestCase
from django.core.exceptions import ValidationError
from gestionApp.models import Persona, Paciente
from datetime import date

class PersonaModelTest(TestCase):
    def setUp(self):
        self.persona_data = {
            'Rut': '12345678-9',
            'Nombre': 'Juan',
            'Apellido_Paterno': 'Pérez',
            'Apellido_Materno': 'González',
            'Fecha_nacimiento': date(1990, 1, 1),
            'Sexo': 'Masculino',
        }
    
    def test_crear_persona_valida(self):
        """Test que una persona se crea correctamente"""
        persona = Persona.objects.create(**self.persona_data)
        self.assertEqual(persona.Nombre, 'Juan')
        self.assertEqual(persona.Rut, '12345678-9')
    
    def test_rut_invalido(self):
        """Test que un RUT inválido lanza excepción"""
        self.persona_data['Rut'] = '11111111-1'
        with self.assertRaises(ValidationError):
            persona = Persona(**self.persona_data)
            persona.full_clean()
    
    def test_calcular_edad(self):
        """Test del método calcular_edad"""
        persona = Persona.objects.create(**self.persona_data)
        edad = persona.calcular_edad()
        self.assertIsInstance(edad, int)
        self.assertGreater(edad, 0)

class PacienteModelTest(TestCase):
    def test_crear_paciente(self):
        """Test creación de paciente"""
        persona = Persona.objects.create(
            Rut='12345678-9',
            Nombre='María',
            Apellido_Paterno='López',
            Apellido_Materno='Silva',
            Fecha_nacimiento=date(1995, 5, 15),
            Sexo='Femenino'
        )
        
        paciente = Paciente.objects.create(
            persona=persona,
            GrupoSanguineo='O+',
            Alergias='Ninguna'
        )
        
        self.assertEqual(paciente.persona.Nombre, 'María')
        self.assertEqual(paciente.GrupoSanguineo, 'O+')