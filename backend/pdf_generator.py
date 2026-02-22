from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
from datetime import datetime
import io

def generate_pdf_report(report_data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title = Paragraph("<b>CardioSense AI - Cardiac Monitoring Report</b>", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    # Report date
    date_text = Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
    elements.append(date_text)
    elements.append(Spacer(1, 0.3*inch))
    
    # Summary section
    summary_title = Paragraph("<b>Summary</b>", styles['Heading2'])
    elements.append(summary_title)
    elements.append(Spacer(1, 0.1*inch))
    
    summary_data = [
        ['Total Readings', str(report_data['total_readings'])],
        ['Average Heart Rate', f"{report_data['averages']['heart_rate']} bpm"],
        ['Average Blood Pressure', report_data['averages']['blood_pressure']],
        ['Average SpO2', f"{report_data['averages']['oxygen_saturation']}%"],
        ['Average Temperature', f"{report_data['averages']['temperature']}°C"],
        ['Average Risk Score', str(report_data['averages']['risk_score'])]
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Risk distribution
    risk_title = Paragraph("<b>Risk Distribution</b>", styles['Heading2'])
    elements.append(risk_title)
    elements.append(Spacer(1, 0.1*inch))
    
    risk_data = [['Risk Level', 'Count']]
    for level, count in report_data['risk_distribution'].items():
        risk_data.append([level, str(count)])
    
    risk_table = Table(risk_data, colWidths=[3*inch, 3*inch])
    risk_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(risk_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Highest risk event
    highest_title = Paragraph("<b>Highest Risk Event</b>", styles['Heading2'])
    elements.append(highest_title)
    elements.append(Spacer(1, 0.1*inch))
    
    highest_text = Paragraph(
        f"Score: {report_data['highest_risk']['score']}<br/>"
        f"Time: {report_data['highest_risk']['timestamp']}",
        styles['Normal']
    )
    elements.append(highest_text)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer
