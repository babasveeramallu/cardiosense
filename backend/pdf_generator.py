from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing, Line, Circle
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics import renderPDF
from datetime import datetime
import io

def create_ecg_waveform(width=400, height=150):
    """Generate ECG waveform drawing"""
    drawing = Drawing(width, height)
    
    # Grid background
    for i in range(0, int(width), 20):
        drawing.add(Line(i, 0, i, height, strokeColor=colors.lightgrey, strokeWidth=0.5))
    for i in range(0, int(height), 20):
        drawing.add(Line(0, i, width, i, strokeColor=colors.lightgrey, strokeWidth=0.5))
    
    # ECG waveform
    baseline = height / 2
    x = 20
    
    # P wave
    drawing.add(Line(x, baseline, x+15, baseline-20, strokeColor=colors.red, strokeWidth=2))
    drawing.add(Line(x+15, baseline-20, x+30, baseline, strokeColor=colors.red, strokeWidth=2))
    x += 40
    
    # QRS complex
    drawing.add(Line(x, baseline, x+5, baseline+10, strokeColor=colors.red, strokeWidth=2))  # Q
    drawing.add(Line(x+5, baseline+10, x+10, baseline-60, strokeColor=colors.red, strokeWidth=2))  # R
    drawing.add(Line(x+10, baseline-60, x+15, baseline+15, strokeColor=colors.red, strokeWidth=2))  # S
    drawing.add(Line(x+15, baseline+15, x+20, baseline, strokeColor=colors.red, strokeWidth=2))
    x += 30
    
    # ST segment
    drawing.add(Line(x, baseline, x+40, baseline, strokeColor=colors.red, strokeWidth=2))
    x += 40
    
    # T wave
    drawing.add(Line(x, baseline, x+20, baseline-30, strokeColor=colors.red, strokeWidth=2))
    drawing.add(Line(x+20, baseline-30, x+40, baseline, strokeColor=colors.red, strokeWidth=2))
    
    return drawing

def create_vitals_chart(history_data):
    """Generate vitals trend chart"""
    drawing = Drawing(400, 200)
    chart = HorizontalLineChart()
    chart.x = 50
    chart.y = 50
    chart.height = 125
    chart.width = 300
    
    # Sample data (last 10 readings)
    chart.data = [
        [hr['heart_rate'] for hr in history_data[-10:]],
        [hr['oxygen_saturation'] for hr in history_data[-10:]]
    ]
    
    chart.lines[0].strokeColor = colors.blue
    chart.lines[1].strokeColor = colors.green
    chart.lines[0].strokeWidth = 2
    chart.lines[1].strokeWidth = 2
    
    drawing.add(chart)
    return drawing

def generate_pdf_report(report_data, patient_name="John Doe", patient_age=45):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch)
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#3b82f6'),
        spaceAfter=30,
        alignment=1  # Center
    )
    
    # Logo placeholder (text-based)
    logo_text = Paragraph(
        "<b>❤️ CardioSense AI</b>",
        ParagraphStyle('Logo', parent=styles['Title'], fontSize=28, textColor=colors.HexColor('#ef4444'), alignment=1)
    )
    elements.append(logo_text)
    elements.append(Spacer(1, 0.2*inch))
    
    # Title
    title = Paragraph("<b>Cardiac Monitoring Report</b>", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.1*inch))
    
    # Report metadata
    date_text = Paragraph(
        f"<b>Report Generated:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
        styles['Normal']
    )
    elements.append(date_text)
    elements.append(Spacer(1, 0.3*inch))
    
    # Patient Information Section
    patient_title = Paragraph("<b>Patient Information</b>", styles['Heading2'])
    elements.append(patient_title)
    elements.append(Spacer(1, 0.1*inch))
    
    patient_data = [
        ['Patient Name:', patient_name],
        ['Age:', f'{patient_age} years'],
        ['Report ID:', f'CS-{datetime.now().strftime("%Y%m%d-%H%M%S")}']
    ]
    
    patient_table = Table(patient_data, colWidths=[2*inch, 4*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e5e7eb')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    elements.append(patient_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Monitoring Summary
    summary_title = Paragraph("<b>Monitoring Summary</b>", styles['Heading2'])
    elements.append(summary_title)
    elements.append(Spacer(1, 0.1*inch))
    
    summary_data = [
        ['Metric', 'Value'],
        ['Total Readings', str(report_data['total_readings'])],
        ['Average Heart Rate', f"{report_data['averages']['heart_rate']} bpm"],
        ['Average Blood Pressure', report_data['averages']['blood_pressure']],
        ['Average SpO2', f"{report_data['averages']['oxygen_saturation']}%"],
        ['Average Temperature', f"{report_data['averages']['temperature']}°C"],
        ['Average Risk Score', str(report_data['averages']['risk_score'])]
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f3f4f6')),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # ECG Waveform
    ecg_title = Paragraph("<b>ECG Waveform Analysis</b>", styles['Heading2'])
    elements.append(ecg_title)
    elements.append(Spacer(1, 0.1*inch))
    
    ecg_drawing = create_ecg_waveform()
    elements.append(ecg_drawing)
    elements.append(Spacer(1, 0.1*inch))
    
    ecg_params = [
        ['ECG Parameter', 'Value', 'Normal Range'],
        ['P Wave Duration', '0.08 s', '0.06-0.11 s'],
        ['PR Interval', '0.16 s', '0.12-0.20 s'],
        ['QRS Duration', '0.09 s', '0.06-0.10 s'],
        ['QT Interval', '0.40 s', '0.36-0.44 s'],
        ['T Wave Amplitude', '0.3 mV', '0.1-0.5 mV'],
        ['ST Segment', '0.0 mV', '-0.05 to 0.1 mV']
    ]
    
    ecg_table = Table(ecg_params, colWidths=[2*inch, 2*inch, 2*inch])
    ecg_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f3f4f6')),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    elements.append(ecg_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Risk Distribution
    risk_title = Paragraph("<b>Risk Assessment Distribution</b>", styles['Heading2'])
    elements.append(risk_title)
    elements.append(Spacer(1, 0.1*inch))
    
    risk_data = [['Risk Level', 'Count', 'Percentage']]
    total = report_data['total_readings']
    for level, count in report_data['risk_distribution'].items():
        percentage = (count / total * 100) if total > 0 else 0
        risk_data.append([level, str(count), f'{percentage:.1f}%'])
    
    risk_table = Table(risk_data, colWidths=[2*inch, 2*inch, 2*inch])
    risk_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f59e0b')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fef3c7')),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    elements.append(risk_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Highest Risk Event
    highest_title = Paragraph("<b>⚠️ Highest Risk Event</b>", styles['Heading2'])
    elements.append(highest_title)
    elements.append(Spacer(1, 0.1*inch))
    
    highest_data = [
        ['Risk Score', str(report_data['highest_risk']['score'])],
        ['Timestamp', report_data['highest_risk']['timestamp']],
        ['Status', 'CRITICAL' if report_data['highest_risk']['score'] >= 15 else 'HIGH' if report_data['highest_risk']['score'] >= 8 else 'MODERATE']
    ]
    
    highest_table = Table(highest_data, colWidths=[2*inch, 4*inch])
    highest_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#fee2e2')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.red)
    ]))
    elements.append(highest_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Footer
    footer = Paragraph(
        "<i>This report is generated by CardioSense AI for monitoring purposes only. "
        "Consult a healthcare professional for medical advice.</i>",
        ParagraphStyle('Footer', parent=styles['Normal'], fontSize=9, textColor=colors.grey, alignment=1)
    )
    elements.append(Spacer(1, 0.5*inch))
    elements.append(footer)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer
