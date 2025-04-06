from fpdf import FPDF

def export_summary_to_pdf(summary_text, filename='summary.pdf'):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in summary_text.split('\n'):
        pdf.cell(200, 10, txt=line, ln=True)
    filepath = f"static/{filename}"
    pdf.output(filepath)
    return filepath
