from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # Two-column header: logo (placeholder) and wrapped title (safe multi_cell usage)
        self.set_font('Arial', 'B', 8)
        logo_width = 30
        title_width = 160
        line_height = 5
        # Save starting y
        y_start = self.get_y()
        # Logo placeholder (left cell, fixed height)
        self.cell(logo_width, line_height * 4, '[LOGO]', border=1, align='C')
        # Move to the right for the title
        self.set_xy(self.get_x(), y_start)
        title = 'PROVISION FOR MECHANICAL VALVE IN SITU PACKING\nREPLACEMENT, MECHANICAL VALVE OVERHAULING, AUTOMATIC\nRECIRCULATORY VALVE (ARV) SERVICING, AND MOV\'S GEARBOX\nSERVICING FOR PCFS TA2025'
        self.multi_cell(title_width, line_height, title, border=1, align='C')
        # Move cursor below the header
        self.set_y(y_start + line_height * 4)
        # Received Report
        self.set_font('Arial', 'B', 7)
        # 'RECEIVED REPORT' as a table row
        self.cell(190, 7, 'RECEIVED REPORT', border=1, ln=1, align='C')

    def table(self, data):
        self.set_font('Arial', '', 5)
        col_widths = [15, 60, 15, 15, 15, 15, 15]  # 50% of previous widths
        for row in data:
            for i, item in enumerate(row):
                self.cell(col_widths[i], 4, str(item), border=1)
            self.ln(4)

pdf = PDF(format='A4')  # Explicitly set A4 size (210 x 297 mm by default)
print('FPDF units: millimeters (mm) by default for A4 size 210x297mm')
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
