from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # Title (smaller font)
        self.set_font('Arial', 'B', 8)
        self.cell(0, 5, 'PROVISION FOR MECHANICAL VALVE IN SITU PACKING', ln=1, align='C')
        self.cell(0, 5, 'REPLACEMENT, MECHANICAL VALVE OVERHAULING, AUTOMATIC', ln=1, align='C')
        self.cell(0, 5, 'RECIRCULATORY VALVE (ARV) SERVICING, AND MOV\'S GEARBOX', ln=1, align='C')
        self.cell(0, 5, 'SERVICING FOR PCFS TA2025', ln=1, align='C')
        self.ln(2)
        # Received Report
        self.set_font('Arial', 'B', 7)
        self.cell(0, 5, 'RECEIVED REPORT', ln=1, align='C')
        self.ln(1)

    def table(self, data):
        self.set_font('Arial', '', 5)
        col_widths = [15, 30, 15, 15, 15, 15, 15]  # 50% of previous widths
        for row in data:
            for i, item in enumerate(row):
                self.cell(col_widths[i], 4, str(item), border=1)
            self.ln(4)

pdf = PDF()
pdf.add_page()

# Table data (fill with your actual data)
data = [
    ['CLIENT', 'PETRONAS CHEMICALS FERTILISER SABAH SDN BHD', '', '', '', '', ''],
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
