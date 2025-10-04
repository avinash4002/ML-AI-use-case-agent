from fpdf import FPDF
from datetime import datetime

# A custom PDF class to handle headers and footers
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'AI/ML Research Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

# Helper function to write text with proper encoding and line breaks
def write_text(pdf, text, size=11, style=''):
    pdf.set_font("Arial", style, size)
    # Encode to latin-1, replacing unsupported characters
    clean_text = text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 5, clean_text)
    pdf.ln(3)

def create_pdf(company_name, overview, use_cases):
    """Generates a professionally formatted PDF report in memory."""
    pdf = PDF()
    pdf.add_page()
    
    # --- Title Section ---
    pdf.set_font("Arial", 'B', 24)
    pdf.cell(0, 10, company_name, 0, 1, 'C')
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1, 'C')
    pdf.ln(10)

    # --- Overview Section ---
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Company Overview", 'B', 1) # 'B' adds a bottom border
    pdf.ln(5)
    write_text(pdf, overview)

    # --- Use Cases Section ---
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Top 5 AI/ML Use Cases", 'B', 1)
    pdf.ln(5)

    for i, case in enumerate(use_cases):
        # Use Case Title
        pdf.set_font("Arial", 'B', 14)
        pdf.multi_cell(0, 7, f"{i+1}. {case['heading']}")
        pdf.ln(2)
        
        # Description
        write_text(pdf, case['description'], style='I') # Italic for description
        
        # Implementation Steps
        pdf.set_font("Arial", 'B', 12)
        pdf.multi_cell(0, 5, "Implementation Steps:")
        for step in case.get('implementation_steps', []):
             # Replaced the special bullet character with a standard hyphen
             write_text(pdf, f"  -  {step.replace('**', '')}")
        
        # Resources
        pdf.set_font("Arial", 'B', 12)
        pdf.multi_cell(0, 5, "Suggested Resources:")
        
        # Datasets
        pdf.set_text_color(0, 0, 139) # Dark Blue for links
        if case['datasets']:
            for ds in case['datasets']:
                # Replaced the special bullet character with a standard hyphen
                write_text(pdf, f"  - [Dataset] {ds['title']}: {ds['url']}", size=10)
        
        # Repositories
        if case['repos']:
            for repo in case['repos']:
                # Replaced the special bullet character with a standard hyphen
                write_text(pdf, f"  - [Repo] {repo['name']} (Stars: {repo['stars']}): {repo['url']}", size=10)
            
        # Papers
        if case['papers']:
            for paper in case['papers']:
                # Replaced the special bullet character with a standard hyphen
                write_text(pdf, f"  - [Paper] {paper['title']}: {paper['url']}", size=10)
        
        pdf.set_text_color(0, 0, 0) # Reset text color
        pdf.ln(10)

    # Return PDF content as bytes
    return pdf.output(dest='S').encode('latin-1')

