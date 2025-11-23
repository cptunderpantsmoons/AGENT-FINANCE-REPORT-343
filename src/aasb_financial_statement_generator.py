import pandas as pd
import numpy as np
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.lib.colors import black, white
import os
from datetime import datetime

class AASBFinancialStatementGenerator:
    def __init__(self, entity_name, current_year, prior_year_data=None, notes_structure=None):
        self.entity_name = entity_name
        self.current_year = current_year
        self.prior_year = current_year - 1
        self.prior_year_data = prior_year_data or {}
        self.notes_structure = notes_structure or {}
        
        # Set up styles
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            alignment=TA_CENTER,
            spaceAfter=30
        )
        self.section_heading_style = ParagraphStyle(
            'SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceBefore=12,
            spaceAfter=6
        )
        self.normal_centered_style = ParagraphStyle(
            'NormalCentered',
            parent=self.styles['Normal'],
            alignment=TA_CENTER
        )
        self.right_align_style = ParagraphStyle(
            'RightAlign',
            parent=self.styles['Normal'],
            alignment=TA_RIGHT
        )
    
    def format_currency(self, amount):
        """Format currency values to nearest dollar"""
        if pd.isna(amount) or amount == 0:
            return "-"
        return f"${int(round(amount)):,}"
    
    def create_title_page(self):
        """Create the title page"""
        elements = []
        elements.append(Paragraph(f"Financial Statements", self.title_style))
        elements.append(Paragraph(f"{self.entity_name}", self.title_style))
        elements.append(Paragraph(f"For the Year Ended 30 June {self.current_year}", self.title_style))
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph(f"(Prepared in accordance with AASB standards applicable to non-reporting entities)", self.normal_centered_style))
        elements.append(PageBreak())
        return elements
    
    def create_contents_page(self, sections):
        """Create table of contents"""
        elements = []
        elements.append(Paragraph("Contents", self.section_heading_style))
        elements.append(Spacer(1, 0.2*inch))
        
        content_data = []
        for i, (section, page_num) in enumerate(sections.items(), 1):
            content_data.append([f"{i}. {section}", str(page_num)])
        
        table = Table(content_data, colWidths=[4*inch, 1*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(table)
        elements.append(PageBreak())
        return elements
    
    def create_income_statement(self, pl_data):
        """Create income statement"""
        elements = []
        elements.append(Paragraph("Statement of Profit or Loss and Other Comprehensive Income", self.section_heading_style))
        elements.append(Paragraph(f"For the year ended 30 June {self.current_year}", self.normal_centered_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Prepare income statement data
        income_data = [
            ["Revenue", "", self.format_currency(pl_data.get('revenue', 0)), self.format_currency(self.prior_year_data.get('revenue', 0))],
            ["Cost of Sales", "", f"({self.format_currency(abs(pl_data.get('cost_of_sales', 0)))})", f"({self.format_currency(abs(self.prior_year_data.get('cost_of_sales', 0)))})"],
            ["", "", "", ""],
            ["Gross Profit", "", self.format_currency(pl_data.get('gross_profit', 0)), self.format_currency(self.prior_year_data.get('gross_profit', 0))],
            ["", "", "", ""],
            ["Other Income", "", self.format_currency(pl_data.get('other_income', 0)), self.format_currency(self.prior_year_data.get('other_income', 0))],
            ["Distribution Costs", "", f"({self.format_currency(abs(pl_data.get('distribution_costs', 0)))})", f"({self.format_currency(abs(self.prior_year_data.get('distribution_costs', 0)))})"],
            ["Administrative Expenses", "", f"({self.format_currency(abs(pl_data.get('administrative_expenses', 0)))})", f"({self.format_currency(abs(self.prior_year_data.get('administrative_expenses', 0)))})"],
            ["Other Expenses", "", f"({self.format_currency(abs(pl_data.get('other_expenses', 0)))})", f"({self.format_currency(abs(self.prior_year_data.get('other_expenses', 0)))})"],
            ["", "", "", ""],
            ["Profit Before Tax", "", self.format_currency(pl_data.get('profit_before_tax', 0)), self.format_currency(self.prior_year_data.get('profit_before_tax', 0))],
            ["Income Tax Expense", "", f"({self.format_currency(abs(pl_data.get('income_tax_expense', 0)))})", f"({self.format_currency(abs(self.prior_year_data.get('income_tax_expense', 0)))})"],
            ["", "", "", ""],
            ["Profit/(Loss) for the Period", "", self.format_currency(pl_data.get('net_profit_loss', 0)), self.format_currency(self.prior_year_data.get('net_profit_loss', 0))],
            ["Other Comprehensive Income", "", "-", "-"],
            ["", "", "", ""],
            ["Total Comprehensive Income", "", self.format_currency(pl_data.get('net_profit_loss', 0)), self.format_currency(self.prior_year_data.get('net_profit_loss', 0))]
        ]
        
        table = Table(income_data, colWidths=[2.5*inch, 0.5*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('ALIGN', (2, 0), (3, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('LINEBELOW', (0, 2), (3, 2), 0.5, black),
            ('LINEBELOW', (0, 6), (3, 6), 0.5, black),
            ('LINEBELOW', (0, 10), (3, 10), 0.5, black),
            ('LINEBELOW', (0, 13), (3, 13), 0.5, black),
            ('LINEBELOW', (0, 16), (3, 16), 0.5, black),
            ('LINEBELOW', (0, 19), (3, 19), 0.5, black),
            ('LINEABOVE', (0, 0), (3, 0), 1, black),
            ('LINEBELOW', (0, -1), (3, -1), 1, black),
        ]))
        elements.append(table)
        elements.append(PageBreak())
        return elements
    
    def create_balance_sheet(self, bs_data):
        """Create balance sheet"""
        elements = []
        elements.append(Paragraph("Statement of Financial Position", self.section_heading_style))
        elements.append(Paragraph(f"As at 30 June {self.current_year}", self.normal_centered_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Assets section
        assets_data = [
            ["ASSETS", "", "", ""],
            ["Current Assets", "", "", ""],
            ["  Cash and Cash Equivalents", "", self.format_currency(bs_data.get('current_assets', {}).get('cash', 0)), self.format_currency(self.prior_year_data.get('current_assets', {}).get('cash', 0))],
            ["  Trade and Other Receivables", "", self.format_currency(bs_data.get('current_assets', {}).get('receivables', 0)), self.format_currency(self.prior_year_data.get('current_assets', {}).get('receivables', 0))],
            ["  Inventories", "", self.format_currency(bs_data.get('current_assets', {}).get('inventories', 0)), self.format_currency(self.prior_year_data.get('current_assets', {}).get('inventories', 0))],
            ["  Other Current Assets", "", self.format_currency(bs_data.get('current_assets', {}).get('other', 0)), self.format_currency(self.prior_year_data.get('current_assets', {}).get('other', 0))],
            ["", "", "", ""],
            ["Total Current Assets", "", self.format_currency(bs_data.get('total_current_assets', 0)), self.format_currency(self.prior_year_data.get('total_current_assets', 0))],
            ["", "", "", ""],
            ["Non-current Assets", "", "", ""],
            ["  Property, Plant and Equipment", "", self.format_currency(bs_data.get('non_current_assets', {}).get('ppe', 0)), self.format_currency(self.prior_year_data.get('non_current_assets', {}).get('ppe', 0))],
            ["  Intangible Assets", "", self.format_currency(bs_data.get('non_current_assets', {}).get('intangibles', 0)), self.format_currency(self.prior_year_data.get('non_current_assets', {}).get('intangibles', 0))],
            ["  Other Non-current Assets", "", self.format_currency(bs_data.get('non_current_assets', {}).get('other', 0)), self.format_currency(self.prior_year_data.get('non_current_assets', {}).get('other', 0))],
            ["", "", "", ""],
            ["Total Non-current Assets", "", self.format_currency(bs_data.get('total_non_current_assets', 0)), self.format_currency(self.prior_year_data.get('total_non_current_assets', 0))],
            ["", "", "", ""],
            ["TOTAL ASSETS", "", self.format_currency(bs_data.get('total_assets', 0)), self.format_currency(self.prior_year_data.get('total_assets', 0))]
        ]
        
        # Liabilities and Equity section
        liabilities_equity_data = [
            ["EQUITY AND LIABILITIES", "", "", ""],
            ["Current Liabilities", "", "", ""],
            ["  Trade and Other Payables", "", self.format_currency(bs_data.get('current_liabilities', {}).get('payables', 0)), self.format_currency(self.prior_year_data.get('current_liabilities', {}).get('payables', 0))],
            ["  Provisions", "", self.format_currency(bs_data.get('current_liabilities', {}).get('provisions', 0)), self.format_currency(self.prior_year_data.get('current_liabilities', {}).get('provisions', 0))],
            ["  Other Current Liabilities", "", self.format_currency(bs_data.get('current_liabilities', {}).get('other', 0)), self.format_currency(self.prior_year_data.get('current_liabilities', {}).get('other', 0))],
            ["", "", "", ""],
            ["Total Current Liabilities", "", self.format_currency(bs_data.get('total_current_liabilities', 0)), self.format_currency(self.prior_year_data.get('total_current_liabilities', 0))],
            ["", "", "", ""],
            ["Non-current Liabilities", "", "", ""],
            ["  Borrowings", "", self.format_currency(bs_data.get('non_current_liabilities', {}).get('borrowings', 0)), self.format_currency(self.prior_year_data.get('non_current_liabilities', {}).get('borrowings', 0))],
            ["  Provisions", "", self.format_currency(bs_data.get('non_current_liabilities', {}).get('provisions', 0)), self.format_currency(self.prior_year_data.get('non_current_liabilities', {}).get('provisions', 0))],
            ["  Other Non-current Liabilities", "", self.format_currency(bs_data.get('non_current_liabilities', {}).get('other', 0)), self.format_currency(self.prior_year_data.get('non_current_liabilities', {}).get('other', 0))],
            ["", "", "", ""],
            ["Total Non-current Liabilities", "", self.format_currency(bs_data.get('total_non_current_liabilities', 0)), self.format_currency(self.prior_year_data.get('total_non_current_liabilities', 0))],
            ["", "", "", ""],
            ["Total Liabilities", "", self.format_currency(bs_data.get('total_liabilities', 0)), self.format_currency(self.prior_year_data.get('total_liabilities', 0))],
            ["", "", "", ""],
            ["Equity", "", "", ""],
            ["  Share Capital", "", self.format_currency(bs_data.get('equity', {}).get('share_capital', 0)), self.format_currency(self.prior_year_data.get('equity', {}).get('share_capital', 0))],
            ["  Reserves", "", self.format_currency(bs_data.get('equity', {}).get('reserves', 0)), self.format_currency(self.prior_year_data.get('equity', {}).get('reserves', 0))],
            ["  Retained Earnings", "", self.format_currency(bs_data.get('equity', {}).get('retained_earnings', 0)), self.format_currency(self.prior_year_data.get('equity', {}).get('retained_earnings', 0))],
            ["", "", "", ""],
            ["Total Equity", "", self.format_currency(bs_data.get('total_equity', 0)), self.format_currency(self.prior_year_data.get('total_equity', 0))],
            ["", "", "", ""],
            ["TOTAL EQUITY AND LIABILITIES", "", self.format_currency(bs_data.get('total_liabilities_and_equity', 0)), self.format_currency(self.prior_year_data.get('total_liabilities_and_equity', 0))]
        ]
        
        # Combine assets and liabilities tables
        balance_sheet_data = assets_data + [["", "", "", ""]] + liabilities_equity_data
        
        table = Table(balance_sheet_data, colWidths=[2.5*inch, 0.5*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('ALIGN', (2, 0), (3, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('SPAN', (0, 0), (3, 0)),
            ('SPAN', (0, 1), (3, 1)),
            ('SPAN', (0, 8), (3, 8)),
            ('SPAN', (0, 10), (3, 10)),
            ('SPAN', (0, 17), (3, 17)),
            ('SPAN', (0, 20), (3, 20)),
            ('SPAN', (0, 24), (3, 24)),
            ('SPAN', (0, 26), (3, 26)),
            ('SPAN', (0, 30), (3, 30)),
            ('SPAN', (0, 33), (3, 33)),
            ('SPAN', (0, 37), (3, 37)),
            ('SPAN', (0, 41), (3, 41)),
            ('SPAN', (0, 43), (3, 43)),
            ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 24), (0, 24), 'Helvetica-Bold'),
            ('FONTNAME', (0, 41), (3, 41), 'Helvetica-Bold'),
            ('FONTNAME', (0, 43), (3, 43), 'Helvetica-Bold'),
            ('LINEBELOW', (0, 7), (3, 7), 0.5, black),
            ('LINEBELOW', (0, 16), (3, 16), 0.5, black),
            ('LINEBELOW', (0, 23), (3, 23), 0.5, black),
            ('LINEBELOW', (0, 29), (3, 29), 0.5, black),
            ('LINEBELOW', (0, 36), (3, 36), 0.5, black),
            ('LINEBELOW', (0, 40), (3, 40), 0.5, black),
            ('LINEABOVE', (0, 0), (3, 0), 1, black),
            ('LINEBELOW', (0, -1), (3, -1), 1, black),
        ]))
        elements.append(table)
        elements.append(PageBreak())
        return elements
    
    def create_notes(self, notes_data):
        """
        Create notes to the financial statements.
        Uses extracted structure from prior year PDF if available.
        """
        elements = []
        elements.append(Paragraph("Notes to the Financial Statements", self.section_heading_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # If we have extracted notes structure from prior year, use it
        if self.notes_structure:
            # Sort notes by number
            note_keys = sorted([k for k in self.notes_structure.keys() if k.startswith('note_')], 
                             key=lambda x: self.notes_structure[x]['number'])
            
            for note_key in note_keys:
                note = self.notes_structure[note_key]
                elements.append(Paragraph(f"{note['number']}. {note['heading']}", self.section_heading_style))
                
                # Use extracted content if available, otherwise use default
                if note.get('content'):
                    # Split content into paragraphs
                    for para in note['content'].split('\n'):
                        if para.strip():
                            elements.append(Paragraph(para.strip(), self.styles['Normal']))
                else:
                    # Default content based on note number
                    elements.append(Paragraph(self._get_default_note_content(note['number'], note['heading']), 
                                            self.styles['Normal']))
                
                elements.append(Spacer(1, 0.1*inch))
        else:
            # Fallback to default notes if structure not available
            # Note 1: Significant Accounting Policies
            elements.append(Paragraph("1. Significant accounting policies", self.section_heading_style))
            elements.append(Paragraph("Basis of preparation", self.styles['Normal']))
            elements.append(Paragraph("These financial statements have been prepared in accordance with Australian Accounting Standards Board (AASB) standards applicable to non-reporting entities. The financial statements comply with the recognition and measurement criteria of AASB 101 Presentation of Financial Statements, AASB 108 Accounting Policies, Changes in Accounting Estimates and Errors, and AASB 1048 Interpretation of Standards.", self.styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
            
            # Note 2: New accounting pronouncements
            elements.append(Paragraph("2. New accounting pronouncements", self.section_heading_style))
            elements.append(Paragraph("Not applicable.", self.styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
            
            # Note 3: Income tax
            elements.append(Paragraph("3. Income tax", self.section_heading_style))
            elements.append(Paragraph("No income tax expense has been recognised for the period as the entity has incurred losses and there is uncertainty regarding the availability of future taxable profits against which the temporary differences could be utilised.", self.styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
            
            # Additional standard notes
            elements.append(Paragraph("4. Property, plant and equipment", self.section_heading_style))
            elements.append(Paragraph("Additions during the period were $XX,XXX (prior year: $XX,XXX).", self.styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
            
            elements.append(Paragraph("5. Trade and other receivables", self.section_heading_style))
            elements.append(Paragraph("Trade receivables are measured at amortised cost using the effective interest method.", self.styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
            
            elements.append(Paragraph("6. Cash and cash equivalents", self.section_heading_style))
            elements.append(Paragraph("Cash and cash equivalents include cash on hand and deposits with banks.", self.styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
        
        elements.append(PageBreak())
        return elements
    
    def _get_default_note_content(self, note_number: int, note_heading: str) -> str:
        """Get default content for a note if not extracted from prior year."""
        defaults = {
            1: "These financial statements have been prepared in accordance with Australian Accounting Standards Board (AASB) standards applicable to non-reporting entities.",
            2: "Not applicable.",
            3: "No income tax expense has been recognised for the period as the entity has incurred losses and there is uncertainty regarding the availability of future taxable profits against which the temporary differences could be utilised.",
            4: "Property, plant and equipment are stated at cost less accumulated depreciation.",
            5: "Trade receivables are measured at amortised cost using the effective interest method.",
            6: "Cash and cash equivalents include cash on hand and deposits with banks.",
        }
        return defaults.get(note_number, f"Note {note_number}: {note_heading}")
    
    def create_directors_declaration(self, directors):
        """Create directors' declaration"""
        elements = []
        elements.append(Paragraph("Directors' Declaration", self.section_heading_style))
        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph("In accordance with section 295 of the Corporations Act 2001, the directors of the company declare that:", self.styles['Normal']))
        elements.append(Spacer(1, 0.1*inch))
        elements.append(Paragraph("1. The financial statements comply with Australian Accounting Standards and the Corporations Regulations 2001;", self.styles['Normal']))
        elements.append(Paragraph("2. The financial statements give a true and fair view of the company's financial position and performance; and", self.styles['Normal']))
        elements.append(Paragraph("3. There are reasonable grounds to believe that the company will be able to pay its debts as and when they become due and payable.", self.styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Director signatures
        for director in directors:
            elements.append(Paragraph(f"_______________________________    Date: 30 June {self.current_year}", self.styles['Normal']))
            elements.append(Paragraph(f"{director['name']}", self.styles['Normal']))
            elements.append(Paragraph(f"{director['title']}", self.styles['Normal']))
            elements.append(Spacer(1, 0.2*inch))
        
        elements.append(PageBreak())
        return elements
    
    def create_compilation_report(self, compiler):
        """Create independent compilation report"""
        elements = []
        elements.append(Paragraph("Independent Compilation Report", self.section_heading_style))
        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph("To the Directors of", self.styles['Normal']))
        elements.append(Paragraph(f"{self.entity_name}", self.styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph("I have compiled the accompanying financial statements from information provided by management. The financial statements have been prepared in accordance with AASB standards applicable to non-reporting entities.", self.styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph("The compilation has been undertaken in accordance with APES 205 Compilation Engagements. I have not audited, reviewed, or performed any other assurance work on the financial statements. Accordingly, I do not express an audit opinion, a review conclusion or any form of assurance conclusion on the financial statements.", self.styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph("_______________________________", self.styles['Normal']))
        elements.append(Paragraph(f"{compiler['name']}", self.styles['Normal']))
        elements.append(Paragraph(f"{compiler['title']}", self.styles['Normal']))
        elements.append(Paragraph(f"Date: 30 June {self.current_year}", self.styles['Normal']))
        return elements
    
    def generate_financial_statements(self, pl_data, bs_data, notes_data, directors, compiler):
        """Generate complete financial statements"""
        # Create document with page numbering
        filename = f"Financial Statements — {self.entity_name} — For the Year Ended 30 June {self.current_year}.pdf"
        
        # Custom page template for page numbers
        # ReportLab doesn't easily support "Page X of Y" without post-processing
        # We'll use a simpler approach with just page numbers
        page_num = [0]  # Use list to allow modification in nested function
        
        def add_page_number(canvas, doc):
            page_num[0] += 1
            canvas.saveState()
            canvas.setFont('Helvetica', 9)
            canvas.drawCentredString(4.25*inch, 0.75*inch, f"Page {page_num[0]}")
            canvas.restoreState()
        
        doc = SimpleDocTemplate(
            filename, 
            pagesize=A4, 
            topMargin=0.5*inch, 
            bottomMargin=0.75*inch,
            onFirstPage=add_page_number,
            onLaterPages=add_page_number
        )
        
        # Build document elements
        elements = []
        
        # Title page
        elements.extend(self.create_title_page())
        
        # Contents page (placeholder page numbers)
        sections = {
            "Statement of Profit or Loss and Other Comprehensive Income": 3,
            "Statement of Financial Position": 4,
            "Notes to the Financial Statements": 5,
            "Directors' Declaration": 8,
            "Independent Compilation Report": 9
        }
        elements.extend(self.create_contents_page(sections))
        
        # Income statement
        elements.extend(self.create_income_statement(pl_data))
        
        # Balance sheet
        elements.extend(self.create_balance_sheet(bs_data))
        
        # Notes
        elements.extend(self.create_notes(notes_data))
        
        # Directors' declaration
        elements.extend(self.create_directors_declaration(directors))
        
        # Compilation report
        elements.extend(self.create_compilation_report(compiler))
        
        # Build PDF
        doc.build(elements)
        
        # Update page numbers with total (requires re-reading PDF or using a different approach)
        # For now, we'll use a simpler approach - ReportLab doesn't easily support total pages
        # This is a limitation we can work around by post-processing or using a different library
        
        print(f"Financial statements generated: {filename}")
        return filename

# Example usage
if __name__ == "__main__":
    # Example data - in practice, this would come from Excel files
    entity_name = "Example Pty Ltd"
    current_year = 2025
    
    # Profit and Loss data
    pl_data = {
        'revenue': 1000000,
        'cost_of_sales': 400000,
        'gross_profit': 600000,
        'other_income': 50000,
        'distribution_costs': 150000,
        'administrative_expenses': 200000,
        'other_expenses': 25000,
        'profit_before_tax': 275000,
        'income_tax_expense': 0,  # Assuming no tax due to losses or other factors
        'net_profit_loss': 275000
    }
    
    # Balance Sheet data
    bs_data = {
        'current_assets': {
            'cash': 150000,
            'receivables': 200000,
            'inventories': 100000,
            'other': 50000
        },
        'total_current_assets': 500000,
        'non_current_assets': {
            'ppe': 800000,
            'intangibles': 100000,
            'other': 100000
        },
        'total_non_current_assets': 1000000,
        'total_assets': 1500000,
        'current_liabilities': {
            'payables': 150000,
            'provisions': 50000,
            'other': 100000
        },
        'total_current_liabilities': 300000,
        'non_current_liabilities': {
            'borrowings': 500000,
            'provisions': 100000,
            'other': 100000
        },
        'total_non_current_liabilities': 700000,
        'total_liabilities': 1000000,
        'equity': {
            'share_capital': 200000,
            'reserves': 0,
            'retained_earnings': 300000
        },
        'total_equity': 500000,
        'total_liabilities_and_equity': 1500000
    }
    
    # Notes data
    notes_data = {}
    
    # Directors information
    directors = [
        {'name': 'Matthew Warnken', 'title': 'Director'},
        {'name': 'Gary Wyatt', 'title': 'Director'},
        {'name': 'Julian Turecek', 'title': 'Director'}
    ]
    
    # Compiler information
    compiler = {
        'name': 'Allan Tuback',
        'title': 'Chief Financial Officer'
    }
    
    # Prior year data for comparatives
    prior_year_data = {
        'revenue': 950000,
        'cost_of_sales': 380000,
        'gross_profit': 570000,
        'other_income': 45000,
        'distribution_costs': 140000,
        'administrative_expenses': 190000,
        'other_expenses': 20000,
        'profit_before_tax': 260000,
        'income_tax_expense': 0,
        'net_profit_loss': 260000,
        'current_assets': {
            'cash': 120000,
            'receivables': 180000,
            'inventories': 90000,
            'other': 40000
        },
        'total_current_assets': 430000,
        'non_current_assets': {
            'ppe': 750000,
            'intangibles': 100000,
            'other': 90000
        },
        'total_non_current_assets': 940000,
        'total_assets': 1370000,
        'current_liabilities': {
            'payables': 140000,
            'provisions': 45000,
            'other': 90000
        },
        'total_current_liabilities': 275000,
        'non_current_liabilities': {
            'borrowings': 480000,
            'provisions': 95000,
            'other': 95000
        },
        'total_non_current_liabilities': 670000,
        'total_liabilities': 945000,
        'equity': {
            'share_capital': 200000,
            'reserves': 0,
            'retained_earnings': 25000  # Previous retained earnings
        },
        'total_equity': 425000,
        'total_liabilities_and_equity': 1370000
    }
    
    # Update retained earnings for current year
    bs_data['equity']['retained_earnings'] = prior_year_data['equity']['retained_earnings'] + pl_data['net_profit_loss']
    bs_data['total_equity'] = sum(bs_data['equity'].values())
    bs_data['total_liabilities_and_equity'] = bs_data['total_liabilities'] + bs_data['total_equity']
    
    # Create generator and generate statements
    generator = AASBFinancialStatementGenerator(entity_name, current_year, prior_year_data)
    filename = generator.generate_financial_statements(pl_data, bs_data, notes_data, directors, compiler)
    print(f"Generated financial statements: {filename}")