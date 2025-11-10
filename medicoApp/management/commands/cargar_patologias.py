# ============================================
# UBICACIÓN: medicoApp/management/commands/cargar_patologias.py
# ============================================

from django.core.management.base import BaseCommand
from django.db import transaction
from medicoApp.models import Patologias


class Command(BaseCommand):
    help = 'Carga catálogo de patologías obstétricas predefinidas y las ACTIVA automáticamente'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                patologias_data = [
                    {
                        'codigo_cie10': 'O10.0',
                        'nombre': 'Hipertensión Preexistente',
                        'descripcion': 'Presión arterial elevada diagnosticada antes del embarazo o antes de las 20 semanas de gestación.',
                        'nivel_de_riesgo': 'Alto',
                        'protocolo_seguimiento': '''Control semanal de presión arterial
- Monitoreo de proteinuria
- Control de peso
- Evaluación de edemas
- Ultrasonografía doppler cada 4 semanas
- Consulta con cardiólogo si PA > 160/110'''
                    },
                    {
                        'codigo_cie10': 'O24.0',
                        'nombre': 'Diabetes Gestacional',
                        'descripcion': 'Intolerancia a la glucosa que se desarrolla durante el embarazo.',
                        'nivel_de_riesgo': 'Alto',
                        'protocolo_seguimiento': '''Control glicémico diario
- Dieta balanceada supervisada por nutricionista
- Control prenatal cada 2 semanas
- Monitoreo fetal semanal desde las 32 semanas
- Evaluación de crecimiento fetal mensual
- Preparación para posible inducción a las 38-39 semanas'''
                    },
                    {
                        'codigo_cie10': 'O14.0',
                        'nombre': 'Preeclampsia Leve',
                        'descripcion': 'Hipertensión con proteinuria después de las 20 semanas de gestación sin signos de severidad.',
                        'nivel_de_riesgo': 'Alto',
                        'protocolo_seguimiento': '''Hospitalización para evaluación inicial
- Control de PA cada 4 horas
- Análisis de proteinuria 24 horas
- Perfil bioquímico completo semanal
- Evaluación de bienestar fetal diario
- Preparación para parto si aparecen signos de severidad'''
                    },
                    {
                        'codigo_cie10': 'O14.1',
                        'nombre': 'Preeclampsia Severa',
                        'descripcion': 'Hipertensión con proteinuria y uno o más criterios de severidad.',
                        'nivel_de_riesgo': 'Critico',
                        'protocolo_seguimiento': '''Hospitalización INMEDIATA
- Sulfato de magnesio profiláctico
- Control PA continuo
- Monitoreo fetal continuo
- Laboratorios cada 12-24 horas
- Maduración pulmonar si < 34 semanas
- Interrupción del embarazo según protocolo'''
                    },
                    {
                        'codigo_cie10': 'O42.0',
                        'nombre': 'Rotura Prematura de Membranas',
                        'descripcion': 'Ruptura de membranas antes del inicio del trabajo de parto.',
                        'nivel_de_riesgo': 'Medio',
                        'protocolo_seguimiento': '''Hospitalización
- Reposo absoluto
- Antibióticos profilácticos
- Corticoides si < 34 semanas
- Monitoreo de signos de infección
- Temperatura cada 4 horas
- Evaluación de FCF cada 8 horas'''
                    },
                    {
                        'codigo_cie10': 'O60.0',
                        'nombre': 'Trabajo de Parto Prematuro',
                        'descripcion': 'Contracciones regulares con cambios cervicales antes de las 37 semanas.',
                        'nivel_de_riesgo': 'Alto',
                        'protocolo_seguimiento': '''Hospitalización
- Tocolíticos según protocolo
- Corticoides para maduración pulmonar
- Sulfato de magnesio neuroprotección si < 32 semanas
- Monitoreo continuo de contracciones y FCF
- Evaluación cervical frecuente'''
                    },
                    {
                        'codigo_cie10': 'O36.3',
                        'nombre': 'Restricción del Crecimiento Intrauterino',
                        'descripcion': 'Peso fetal estimado por debajo del percentil 10 para la edad gestacional.',
                        'nivel_de_riesgo': 'Alto',
                        'protocolo_seguimiento': '''Evaluación doppler semanal
- Perfil biofísico 2 veces por semana
- Control de movimientos fetales
- Ultrasonografía de crecimiento cada 2 semanas
- Evaluación de líquido amniótico
- Hospitalización si deterioro'''
                    },
                    {
                        'codigo_cie10': 'O36.5',
                        'nombre': 'Anemia en el Embarazo',
                        'descripcion': 'Hemoglobina < 11 g/dL en el primer trimestre o < 10.5 g/dL en segundo/tercer trimestre.',
                        'nivel_de_riesgo': 'Bajo',
                        'protocolo_seguimiento': '''Suplementación con hierro y ácido fólico
- Control de hemograma mensual
- Evaluación de adherencia al tratamiento
- Investigar causa de anemia
- Derivar a hematología si Hb < 7 g/dL
- Considerar transfusión si Hb < 7 g/dL'''
                    },
                    {
                        'codigo_cie10': 'O44.0',
                        'nombre': 'Placenta Previa',
                        'descripcion': 'Implantación de la placenta en el segmento inferior uterino cubriendo el orificio cervical interno.',
                        'nivel_de_riesgo': 'Critico',
                        'protocolo_seguimiento': '''REPOSO ABSOLUTO - Sin tacto vaginal
- Hospitalización si sangrado
- Ultrasonografía cada 4 semanas
- Corticoides a las 34 semanas
- Preparación para cesárea electiva 36-37 semanas
- Banco de sangre disponible'''
                    },
                    {
                        'codigo_cie10': 'O68.0',
                        'nombre': 'Sufrimiento Fetal Agudo',
                        'descripcion': 'Alteraciones en la frecuencia cardíaca fetal que indican compromiso fetal.',
                        'nivel_de_riesgo': 'Critico',
                        'protocolo_seguimiento': '''Monitoreo fetal continuo
- Reposición de líquidos IV
- Oxígeno materno
- Cambios de posición materna
- Preparación para parto de emergencia
- Equipo neonatal en alerta'''
                    }
                ]

                patologias_creadas = 0
                patologias_existentes = 0

                self.stdout.write(self.style.WARNING('\n📋 Iniciando carga de patologías obstétricas...'))

                for data in patologias_data:
                    patologia, created = Patologias.objects.get_or_create(
                        codigo_cie_10=data['codigo_cie10'],
                        defaults={
                            'nombre': data['nombre'],
                            'descripcion': data['descripcion'],
                            'nivel_de_riesgo': data['nivel_de_riesgo'],
                            'protocolo_seguimiento': data['protocolo_seguimiento'],
                            'estado': True
                        }
                    )

                    if created:
                        patologias_creadas += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'  ✅ Creada y ACTIVADA: {data["codigo_cie10"]} - {data["nombre"]}'
                            )
                        )
                    else:
                        if not patologia.estado:
                            patologia.estado = True
                            patologia.save()
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f'  ✓ Activada: {data["codigo_cie10"]} - {data["nombre"]}'
                                )
                            )
                            patologias_creadas += 1
                        else:
                            patologias_existentes += 1
                            self.stdout.write(
                                self.style.WARNING(
                                    f'  ⚠️  Ya existe y está activa: {data["codigo_cie10"]} - {data["nombre"]}'
                                )
                            )

                self.stdout.write(
                    self.style.SUCCESS(
                        f'\n✅ PROCESO COMPLETADO'
                    )
                )
                self.stdout.write(f'  📊 Patologías creadas y activadas: {patologias_creadas}')
                self.stdout.write(f'  📊 Patologías ya existentes: {patologias_existentes}')
                self.stdout.write(f'  📊 Total en catálogo: {Patologias.objects.count()}')
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  ✅ Patologías activas disponibles: {Patologias.objects.filter(estado=True).count()}'
                    )
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'\n❌ Error al cargar patologías: {str(e)}')
            )
            raise