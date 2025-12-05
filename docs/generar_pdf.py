#!/usr/bin/env python3
"""
Script para generar PDF de los manuales técnico y del usuario
Requiere: pip install reportlab markdown pillow
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import markdown
from pathlib import Path

class ManualPDFGenerator:
    """Generador de PDFs para manuales"""
    
    def __init__(self, output_dir="./docs"):
        self.output_dir = output_dir
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup de estilos personalizados"""
        self.styles.add(ParagraphStyle(
            name='Title',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='Heading2Custom',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2563eb'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='BodyCustom',
            parent=self.styles['BodyText'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=12
        ))
    
    def generate_technical_manual(self):
        """Generar PDF del manual técnico"""
        output_path = os.path.join(self.output_dir, "manual_tecnico.pdf")
        
        story = []
        
        # Portada
        story.append(Spacer(1, 2 * inch))
        story.append(Paragraph(
            "SIA-R News Engine",
            self.styles['Title']
        ))
        story.append(Spacer(1, 0.3 * inch))
        story.append(Paragraph(
            "Manual Técnico",
            self.styles['Heading1']
        ))
        story.append(Spacer(1, 0.5 * inch))
        story.append(Paragraph(
            "Sistema Automatizado de Redacción, Auditoría y Publicación",
            self.styles['Normal']
        ))
        story.append(Spacer(1, 1 * inch))
        story.append(Paragraph(
            f"<b>Versión:</b> 1.0.0<br/><b>Fecha:</b> {datetime.now().strftime('%d de %B de %Y')}<br/><b>Autor:</b> SIA-R Team",
            self.styles['Normal']
        ))
        
        story.append(PageBreak())
        
        # Tabla de contenidos
        story.append(Paragraph("Tabla de Contenidos", self.styles['Heading1']))
        story.append(Spacer(1, 0.2 * inch))
        
        toc_items = [
            "1. Arquitectura del Sistema",
            "2. Instalación",
            "3. Configuración",
            "4. Pipeline de Procesamiento",
            "5. Modelos de Datos",
            "6. Endpoints de API",
            "7. Taxonomía Adaptativa",
            "8. Seguridad",
            "9. Troubleshooting"
        ]
        
        for item in toc_items:
            story.append(Paragraph(item, self.styles['Normal']))
            story.append(Spacer(1, 0.1 * inch))
        
        story.append(PageBreak())
        
        # Contenido
        story.append(Paragraph("1. Arquitectura del Sistema", self.styles['Heading1']))
        story.append(Spacer(1, 0.2 * inch))
        
        arch_text = """
        SIA-R utiliza una arquitectura modular basada en:
        <br/><br/>
        <b>Frontend:</b> Cliente HTTP (web o mobile)<br/>
        <b>API:</b> Flask con REST endpoints<br/>
        <b>Services:</b> Módulos de procesamiento especializados<br/>
        <b>Pipeline:</b> Orquestador de flujos<br/>
        <b>Storage:</b> SQLAlchemy + PostgreSQL/SQLite<br/>
        <b>External:</b> OpenAI API, WordPress REST API
        """
        story.append(Paragraph(arch_text, self.styles['BodyCustom']))
        
        story.append(PageBreak())
        
        # Instalación
        story.append(Paragraph("2. Instalación", self.styles['Heading1']))
        story.append(Spacer(1, 0.2 * inch))
        
        install_text = """
        <b>Requisitos Previos:</b><br/>
        • Python 3.10+<br/>
        • pip (gestor de paquetes)<br/>
        • git<br/>
        • Docker (opcional)<br/>
        <br/>
        <b>Pasos:</b><br/>
        1. Clonar repositorio<br/>
        2. Crear entorno virtual<br/>
        3. Instalar dependencias<br/>
        4. Configurar .env<br/>
        5. Inicializar base de datos<br/>
        6. Ejecutar aplicación
        """
        story.append(Paragraph(install_text, self.styles['BodyCustom']))
        
        story.append(PageBreak())
        
        # Pipeline
        story.append(Paragraph("4. Pipeline de Procesamiento", self.styles['Heading1']))
        story.append(Spacer(1, 0.2 * inch))
        
        pipeline_text = """
        El pipeline SIA-R consiste de 10 etapas secuenciales:
        <br/><br/>
        <b>[1] Cleaner:</b> Limpieza y normalización<br/>
        <b>[2] Tagger:</b> Extracción de metadatos (LLM)<br/>
        <b>[3] Auditor:</b> Auditoría de calidad (LLM)<br/>
        <b>[4] Fact Checker:</b> Verificación de hechos<br/>
        <b>[5] Verifier:</b> Verificación de coherencia<br/>
        <b>[6] Humanizer:</b> Humanización de texto<br/>
        <b>[7] SEO Optimizer:</b> Optimización para buscadores<br/>
        <b>[8] Taxonomy Normalizer:</b> Normalización de categorías<br/>
        <b>[9] Planner:</b> Planificación de publicación<br/>
        <b>[10] AutoLearn:</b> Aprendizaje automático
        """
        story.append(Paragraph(pipeline_text, self.styles['BodyCustom']))
        
        # Generar PDF
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        doc.build(story)
        print(f"✓ Manual técnico generado: {output_path}")
        return output_path
    
    def generate_user_manual(self):
        """Generar PDF del manual del usuario"""
        output_path = os.path.join(self.output_dir, "manual_usuario.pdf")
        
        story = []
        
        # Portada
        story.append(Spacer(1, 2 * inch))
        story.append(Paragraph(
            "SIA-R News Engine",
            self.styles['Title']
        ))
        story.append(Spacer(1, 0.3 * inch))
        story.append(Paragraph(
            "Manual del Usuario",
            self.styles['Heading1']
        ))
        story.append(Spacer(1, 0.5 * inch))
        story.append(Paragraph(
            "Guía Rápida para Redactores y Publicadores",
            self.styles['Normal']
        ))
        story.append(Spacer(1, 1 * inch))
        story.append(Paragraph(
            f"<b>Versión:</b> 1.0.0<br/><b>Fecha:</b> {datetime.now().strftime('%d de %B de %Y')}",
            self.styles['Normal']
        ))
        
        story.append(PageBreak())
        
        # Tabla de contenidos
        story.append(Paragraph("Tabla de Contenidos", self.styles['Heading1']))
        story.append(Spacer(1, 0.2 * inch))
        
        toc_items = [
            "1. ¿Qué es SIA-R?",
            "2. Inicio Rápido en 5 Pasos",
            "3. Flujo Completo de Uso",
            "4. Ejemplos de Uso",
            "5. Tips y Mejores Prácticas",
            "6. Entender los Avisos",
            "7. Preguntas Frecuentes",
            "8. Cheatsheet de Comandos"
        ]
        
        for item in toc_items:
            story.append(Paragraph(item, self.styles['Normal']))
            story.append(Spacer(1, 0.1 * inch))
        
        story.append(PageBreak())
        
        # Contenido
        story.append(Paragraph("1. ¿Qué es SIA-R?", self.styles['Heading1']))
        story.append(Spacer(1, 0.2 * inch))
        
        what_is_text = """
        SIA-R es un asistente inteligente de IA que:
        <br/><br/>
        ✓ Mejora automáticamente la calidad de tus artículos<br/>
        ✓ Optimiza para motores de búsqueda (SEO)<br/>
        ✓ Verifica hechos automáticamente<br/>
        ✓ Publica directamente en WordPress<br/>
        ✓ Aprende de tus patrones de publicación
        """
        story.append(Paragraph(what_is_text, self.styles['BodyCustom']))
        
        story.append(PageBreak())
        
        # Inicio rápido
        story.append(Paragraph("2. Inicio Rápido en 5 Pasos", self.styles['Heading1']))
        story.append(Spacer(1, 0.2 * inch))
        
        quick_text = """
        <b>Paso 1: Acceder</b><br/>
        Abrir navegador en http://localhost:8000
        <br/><br/>
        <b>Paso 2: Iniciar Sesión</b><br/>
        Usar tu email y contraseña
        <br/><br/>
        <b>Paso 3: Preparar Artículo</b><br/>
        Tener listo título y contenido
        <br/><br/>
        <b>Paso 4: Enviar para Procesamiento</b><br/>
        Hacer POST a /api/pipeline/run
        <br/><br/>
        <b>Paso 5: Revisar y Publicar</b><br/>
        Verificar calidad y publicar en WordPress
        """
        story.append(Paragraph(quick_text, self.styles['BodyCustom']))
        
        story.append(PageBreak())
        
        # Mejores prácticas
        story.append(Paragraph("5. Tips y Mejores Prácticas", self.styles['Heading1']))
        story.append(Spacer(1, 0.2 * inch))
        
        tips_text = """
        <b>Haz ESTO:</b><br/>
        ✓ Escribe en tu estilo natural<br/>
        ✓ Incluye hechos específicos<br/>
        ✓ Estructura clara con párrafos cortos<br/>
        ✓ Revisa siempre el resultado<br/>
        ✓ Usa categorías consistentes
        <br/><br/>
        <b>Evita ESTO:</b><br/>
        ✗ Copiar y pegar sin verificar<br/>
        ✗ Afirmaciones sin fundamento<br/>
        ✗ Artículos muy cortos<br/>
        ✗ Información contradictoria<br/>
        ✗ Enlaces spam
        """
        story.append(Paragraph(tips_text, self.styles['BodyCustom']))
        
        # Generar PDF
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        doc.build(story)
        print(f"✓ Manual del usuario generado: {output_path}")
        return output_path
    
    def generate_all(self):
        """Generar todos los PDFs"""
        print("Generando PDFs de manuales...")
        print("-" * 50)
        
        technical = self.generate_technical_manual()
        user = self.generate_user_manual()
        
        print("-" * 50)
        print("✓ Manuales generados exitosamente")
        print(f"  • {technical}")
        print(f"  • {user}")

if __name__ == "__main__":
    # Asegurar que la carpeta docs existe
    docs_dir = Path("./docs")
    docs_dir.mkdir(exist_ok=True)
    
    generator = ManualPDFGenerator(output_dir="./docs")
    generator.generate_all()
