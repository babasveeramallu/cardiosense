from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing, Line, Circle, Rect
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF
from datetime import datetime
import io
import os

def create_ecg_waveform(width=500, height=180, st_elevation=0.0, t_wave=0.3):
    """Generate ECG waveform drawing with dynamic values"""
    drawing = Drawing(width, height)
    
    # Background
    drawing.add(Rect(0, 0, width, height, fillColor=colors.HexColor('#1e293b'), strokeColor=None))
    
    # Grid background
    for i in range(0, int(width), 20):
        drawing.add(Line(i, 0, i, height, strokeColor=colors.HexColor('#374151'), strokeWidth=0.5))
    for i in range(0, int(height), 20):
        drawing.add(Line(0, i, width, i, strokeColor=colors.HexColor('#374151'), strokeWidth=0.5))
    
    # ECG waveform - draw multiple heartbeats
    baseline = height / 2
    beat_width = 120
    
    for beat in range(3):
        x_offset = 20 + (beat * beat_width)
        
        # P wave
        p_points = []
        for i in range(15):
            x = x_offset + i
            y = baseline - 15 * (i/15) * ((15-i)/15) * 4
            p_points.append((x, y))
        for i in range(len(p_points)-1):
            drawing.add(Line(p_points[i][0], p_points[i][1], p_points[i+1][0], p_points[i+1][1], 
                           strokeColor=colors.HexColor('#10b981'), strokeWidth=2.5))
        
        x = x_offset + 20
        
        # PR segment
        drawing.add(Line(x, baseline, x+15, baseline, strokeColor=colors.HexColor('#10b981'), strokeWidth=2.5))
        x += 15
        
        # QRS complex
        # Q wave
        drawing.add(Line(x, baseline, x+3, baseline+8, strokeColor=colors.HexColor('#10b981'), strokeWidth=2.5))
        x += 3
        # R wave (tall spike)
        drawing.add(Line(x, baseline+8, x+5, baseline-55, strokeColor=colors.HexColor('#10b981'), strokeWidth=2.5))
        x += 5
        # S wave
        drawing.add(Line(x, baseline-55, x+3, baseline+10, strokeColor=colors.HexColor('#10b981'), strokeWidth=2.5))
        x += 3
        drawing.add(Line(x, baseline+10, x+3, baseline, strokeColor=colors.HexColor('#10b981'), strokeWidth=2.5))
        x += 3
        
        # ST segment (shows elevation for heart attack)
        st_y = baseline + (st_elevation * 100)
        drawing.add(Line(x, baseline, x+25, st_y, strokeColor=colors.HexColor('#ef4444' if st_elevation > 0.1 else '#10b981'), strokeWidth=2.5))
        x += 25
        
        # T wave
        t_points = []
        for i in range(25):
            tx = x + i
            ty = st_y - (t_wave * 60) * (i/25) * ((25-i)/25) * 4
            t_points.append((tx, ty))
        for i in range(len(t_points)-1):
            drawing.add(Line(t_points[i][0], t_points[i][1], t_points[i+1][0], t_points[i+1][1], 
                           strokeColor=colors.HexColor('#10b981'), strokeWidth=2.5))
        
        x += 25
        
        # Return to baseline
        drawing.add(Line(x, t_points[-1][1], x+10, baseline, strokeColor=colors.HexColor('#10b981'), strokeWidth=2.5))
    
    return drawing

def create_vitals_chart(report_data):
    """Generate vitals bar chart"""
    drawing = Drawing(500, 200)
    chart = VerticalBarChart()
    chart.x = 50
    chart.y = 50
    chart.height = 125
    chart.width = 400
    
    # Data for average vitals
    chart.data = [
        [report_data['averages']['heart_rate'], 
         report_data['averages']['oxygen_saturation'],
         report_data['averages']['temperature'] * 10,  # Scale for visibility
         report_data['averages']['risk_score'] * 5]  # Scale for visibility
    ]
    
    chart.categoryAxis.categoryNames = ['Heart Rate\n(bpm)', 'SpO2\n(%)', 'Temp\n(°C x10)', 'Risk Score\n(x5)']
    chart.bars[0].fillColor = colors.HexColor('#3b82f6')
    chart.valueAxis.valueMin = 0
    chart.valueAxis.valueMax = 120
    
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
    
    # Logo
    logo_path = os.path.join(os.path.dirname(__file__), 'logo.png')
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=2.5*inch, height=1*inch)
        logo.hAlign = 'CENTER'
        elements.append(logo)
        elements.append(Spacer(1, 0.2*inch))
    else:
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
    
    # Vitals Chart
    vitals_chart_title = Paragraph("<b>Average Vitals Visualization</b>", styles['Heading2'])
    elements.append(vitals_chart_title)
    elements.append(Spacer(1, 0.1*inch))
    
    vitals_chart = create_vitals_chart(report_data)
    elements.append(vitals_chart)
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
