from fpdf import FPDF
from datetime import datetime

# Helper function to write text and handle multi-line content
def write_text(pdf, text):
    # Set to a regular font for body text
    pdf.set_font("Arial", size=11)
    # Use multi_cell for automatic line breaking
    pdf.multi_cell(0, 5, text.encode('latin-1', 'replace').decode('latin-1'))
    pdf.ln(5)

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'AI/ML Research Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf(company_name, overview, use_cases):
    """
    Generates a PDF report in memory and returns its content as bytes.
    """
    pdf = PDF()
    pdf.add_page()
    
    # --- Title ---
    pdf.set_font("Arial", 'B', 24)
    pdf.cell(0, 10, company_name, 0, 1, 'C')
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1, 'C')
    pdf.ln(10)

    # --- Overview ---
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Company Overview", 0, 1)
    write_text(pdf, overview)

    # --- Use Cases ---
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Top 5 AI/ML Use Cases", 0, 1)

    for case in use_cases:
        pdf.set_font("Arial", 'B', 14)
        pdf.multi_cell(0, 7, f"Use Case: {case['heading']}")
        pdf.ln(2)
        
        pdf.set_font("Arial", 'B', 12)
        pdf.multi_cell(0, 5, "Description")
        write_text(pdf, case['description'])
        
        pdf.set_font("Arial", 'B', 12)
        pdf.multi_cell(0, 5, "Implementation Steps")
        for step in case.get('implementation_steps', []):
             # Clean up markdown bolding for the PDF
             write_text(pdf, f"- {step.replace('**', '')}")
        
        # --- Resources Section ---
        pdf.set_font("Arial", 'B', 12)
        pdf.multi_cell(0, 5, "Suggested Resources")
        
        # Datasets
        pdf.set_font("Arial", 'B', 11)
        pdf.multi_cell(0, 5, "Datasets (from Kaggle):")
        if case['datasets']:
            for ds in case['datasets']:
                write_text(pdf, f"- {ds['title']}: {ds['url']}")
        else:
            write_text(pdf, "No relevant datasets found.")

        # Repositories
        pdf.set_font("Arial", 'B', 11)
        pdf.multi_cell(0, 5, "Repositories (from GitHub):")
        if case['repos']:
            for repo in case['repos']:
                write_text(pdf, f"- {repo['name']} (Stars: {repo['stars']}): {repo['url']}")
        else:
            write_text(pdf, "No relevant repositories found.")
            
        # Papers
        pdf.set_font("Arial", 'B', 11)
        pdf.multi_cell(0, 5, "Research Papers (from ArXiv):")
        if case['papers']:
            for paper in case['papers']:
                write_text(pdf, f"- {paper['title']}: {paper['url']}")
        else:
            write_text(pdf, "No relevant research papers found.")
            
        pdf.ln(10) # Add space between use cases

    # Generate the PDF content in memory as bytes
    return pdf.output(dest='S').encode('latin-1')

