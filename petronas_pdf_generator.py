from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # Two-column header: logo (placeholder) and title
        self.set_font('Arial', 'B', 8)
        # Set column widths
        logo_width = 30
        title_width = 160
        shared_height = 28  # Shared height for both logo and title

        # Logo placeholder (left cell)
        self.cell(logo_width, shared_height, '[LOGO]', border=1, align='C')

        # Title (right cell, multi-line, vertically centered)
        x = self.get_x()
        y = self.get_y()
        title = ('PROVISION FOR MECHANICAL VALVE IN SITU PACKING\n'
                 'REPLACEMENT, MECHANICAL VALVE OVERHAULING, AUTOMATIC\n'
                 "RECIRCULATORY VALVE (ARV) SERVICING, AND MOV'S GEARBOX\n"
                 'SERVICING FOR PCFS TA2025')
        # Draw a cell for the border, then print the text inside
        self.multi_cell(title_width, shared_height / 4, title, border=0, align='C')
        # Draw the border for the title cell
        self.rect(x, y, title_width, shared_height)
        self.ln(shared_height)

        # Received Report
        self.set_font('Arial', 'B', 7)
        self.cell(0, 5, 'RECEIVED REPORT', ln=1, align='C')
        self.ln(1)

    def table(self, data):
        self.set_font('Arial', '', 5)
        col_widths = [15, 60, 15, 15, 15, 15, 15]  # 50% of previous widths
        for row in data:
            for i, item in enumerate(row):
                self.cell(col_widths[i], 4, str(item), border=1)
            self.ln(4)

pdf = PDF()
pdf.add_page()

# Table data (fill with your actual data)
data = [
    ['CLIENT', 'PETRONAS CHEMICALS FERTILISER SABAH SDN BHD'],
    ['PROJECT', 'VALVE MAINTENANCE/REPAIR', 'DOC NO', '', '', '', ''],
    ['LOCATION', 'SIPITANG SABAH', 'SIZE INLET', '0', 'RATING', '0', 'INLET TYPE'],
    ['DATE IN', '1/0/1900', 'SIZE OUTLET', '8', 'RATING', '600', 'OUTLET TYPE'],
    ['WO', '81799204', 'MANUFACTURER', 'GATE VALVE', '', '', ''],
    ['TAG NO', '1/0/1900', 'TYPE OF VALVE', '52', '', '', ''],
    ['', '', 'VALVE OPERATED TYPE', 'PK VALVE', '', '', ''],
    ['INSITU TESTING', 'SERVICE & REPAIR', '', 'TESTING ONLY', 'REPLACE NEW VALVE', '', ''],
]

pdf.table(data)

pdf.output('generated_report.pdf')
