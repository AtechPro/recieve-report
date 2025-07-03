from fpdf import FPDF
from fpdf.enums import XPos, YPos
from fpdf.fonts import FontFace
import json

def load_valve_data():
    with open('valve_data.json', 'r') as file:
        return json.load(file)

class PDF(FPDF):
    FONT_FAMILY = 'helvetica'
    FONT_SIZE = 6
    HEADER_FONT_SIZE = 8
    RECEIVED_FONT_SIZE = 7

    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.valve_data = data

    def header(self):
        # Two-column header: logo (placeholder) and wrapped title
        self.set_font(self.FONT_FAMILY, 'B', 8)
        logo_width = 30
        title_width = 160
        line_height = 8
        y_start = self.get_y()
        self.cell(logo_width, line_height * 4, '[LOGO]', border=1, align='C')
        self.set_xy(self.get_x(), y_start)
        title = 'PROVISION FOR MECHANICAL VALVE IN SITU PACKING\nREPLACEMENT, MECHANICAL VALVE OVERHAULING, AUTOMATIC\nRECIRCULATORY VALVE (ARV) SERVICING, AND MOV\'S GEARBOX\nSERVICING FOR PCFS TA2025'
        self.multi_cell(title_width, line_height, title, border=1, align='C')
        self.set_y(y_start + line_height * 4)

        grey = (128, 128, 128)
        headings_style = FontFace(emphasis="B", fill_color=grey)

        self.set_font(self.FONT_FAMILY, 'B', self.RECEIVED_FONT_SIZE)
        col_widths = [190]
        with self.table(col_widths=col_widths, line_height=5, headings_style=headings_style) as table:
            row = table.row()
            row.cell('RECEIVED REPORT', align='C')

    def client_info(self):
        data = self.valve_data['client_info']
        self.set_font(self.FONT_FAMILY, '', self.FONT_SIZE)
        col_widths = [30, 80, 40, 10, 20, 10, 25, 35]
        with self.table(col_widths=col_widths, line_height=4) as table:
            row = table.row()
            row.cell('CLIENT')
            row.cell(data['client'], colspan=7)

            row = table.row()
            row.cell('PROJECT')
            row.cell(data['project'])
            row.cell('DOC NO')
            row.cell(data['doc_info'], colspan=5)

            row = table.row()
            row.cell('LOCATION')
            row.cell(data['location'])
            row.cell('SIZE INLET')
            row.cell(data['size_inlet'])
            row.cell('RATING', align='C')
            row.cell(data['inlet_rating'])
            row.cell('INLET TYPE')
            row.cell(data['inlet_type'], align='C')

            row = table.row()
            row.cell('DATE IN')
            row.cell(data['date_in'])
            row.cell('SIZE OUTLET')
            row.cell(data['size_outlet'])
            row.cell('RATING', align='C')
            row.cell(data['outlet_rating'])
            row.cell('OUTLET TYPE')
            row.cell(data['outlet_type'], align='C')

            row = table.row()
            row.cell('WO')
            row.cell(data['wo_number'])
            row.cell('MANUFACTURER')
            row.cell(data['manufacturer'], colspan=5)

            row = table.row()
            row.cell('TAG NO')
            row.cell(data['tag_no'])
            row.cell('TYPE OF VALVE')
            row.cell(data['valve_type'], colspan=5)

            row = table.row()
            row.cell('')
            row.cell('')
            row.cell('VALVE OPERATED TYPE')
            row.cell(data['valve_operated_type'], colspan=5)

    def service_info(self):
        self.set_font(self.FONT_FAMILY, '', self.FONT_SIZE)
        col_widths = [30, 20, 40, 20, 40, 20, 50, 30]
        with self.table(col_widths=col_widths, line_height=4) as table:
            row = table.row()
            row.cell('INSITU TESTING')
            row.cell('')
            row.cell('SERVICE & REPAIR')
            row.cell('')
            row.cell('TESTING ONLY')
            row.cell('')
            row.cell('REPLACE NEW VALVE')
            row.cell('')

    def transportation_details(self):
        data = self.valve_data['transportation_details']
        self.set_font(self.FONT_FAMILY, '', self.FONT_SIZE)
        col_widths = [30, 80, 40, 20, 20, 20, 30, 10]
        grey = (128, 128, 128)
        headings_style = FontFace(emphasis="B", fill_color=grey)

        with self.table(col_widths=col_widths, line_height=4, headings_style=headings_style) as table:
            row = table.row()
            row.cell('TRANSPORTATION DETAILS', colspan=8, align='C')

            row = table.row()
            row.cell('TRANSPORT MODE')
            row.cell(data['transport_mode'])
            row.cell('PACKAGING')
            row.cell(data['packaging'], colspan=5)

            row = table.row()
            row.cell('TRANSPORT BY')
            row.cell(data['transport_by'])
            row.cell('RECIEVED BY')
            row.cell(data['received_by'], colspan=5)

            row = table.row()
            row.cell('COMMENT ON TRANSPORTATION IF ANY', colspan=2)
            row.cell(data['transport_comment'], colspan=6)

    def received_info_and_condition(self):
        data = self.valve_data['received_valve_condition']
        self.set_font(self.FONT_FAMILY, '', self.FONT_SIZE)
        col_widths = [63.33, 63.33, 63.33]
        box_height = 40

        x = self.get_x()
        y = self.get_y()

        self.rect(x, y, sum(col_widths), box_height)

        self.set_xy(x, y)
        self.set_font(self.FONT_FAMILY, 'B', self.FONT_SIZE)
        self.cell(0, 5, 'AS RECEIVED VALVE:', align='L')
        
        image_width = 55
        image_height = 30
        margin = 4
        y_offset = 8
        
        for i in range(3):
            image_x = x + margin + (i * (image_width + margin))
            self.image('image.png', x=image_x, y=y + y_offset, w=image_width, h=image_height)

        self.set_xy(x, y + box_height)
        self.set_font(self.FONT_FAMILY, '', self.FONT_SIZE)
        grey = (128, 128, 128)
        headings_style = FontFace(emphasis="B", fill_color=grey)

        col_widths = [47.5, 47.5, 47.5, 47.5]

        with self.table(col_widths=col_widths, line_height=4, headings_style=headings_style) as table:
            row = table.row()
            row.cell('AS RECEIVED VALVE CONDITION', colspan=4, align='C')

            row = table.row()
            row.cell('INLET CONNECTION TYPE')
            row.cell(data['inlet_connection_type'])
            row.cell('OUTLET CONNECTION TYPE')
            row.cell(data['outlet_connection_type'])

            row = table.row()
            row.cell('NAMEPLATE')
            row.cell(data['nameplate'])
            row.cell('TAG NUMBER/PLATE')
            row.cell(data['tag_number'])

            row = table.row()
            row.cell('INLET CONNECTION CONDITION')
            row.cell(data['inlet_connection_condition'])
            row.cell('OUTLET CONNECTION CONDITION')
            row.cell(data['outlet_connection_condition'])

            row = table.row()
            row.cell('CONNECTION MAJOR DEFECT/DAMAGE')
            row.cell(data['connection_major_defect'])
            row.cell('')
            row.cell('')

            row = table.row()
            row.cell('VALVE BODY CONDITION')
            row.cell(data['valve_body_condition'])
            row.cell('MAJOR DEFECT ON BODY')
            row.cell(data['major_defect_body'])

    def valve_condition(self, extra_height=8):
        data = self.valve_data['overall_condition']
        self.set_font(self.FONT_FAMILY, 'B', self.FONT_SIZE)
        col_widths = [190]

        grey = (128, 128, 128)
        headings_style = FontFace(emphasis="B", fill_color=grey)

        with self.table(col_widths=col_widths, line_height=4, headings_style=headings_style) as table:
            row = table.row()
            row.cell('OVERALL VALVE CONDITION', colspan=1, align='C')
        self.cell(190, extra_height, data['description'], border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        
        with self.table(col_widths=col_widths, line_height=4, headings_style=headings_style) as table:
            row = table.row()
            row.cell('DETAILED PICTURE', colspan=1, align='C')

    def detailed_picture(self):
        self.set_font(self.FONT_FAMILY, '', self.FONT_SIZE)
        col_widths = [47.5, 47.5, 47.5, 47.5]
        img_width = col_widths[1] - 10
        
        with self.table(col_widths=col_widths, line_height=30) as table:
            row = table.row()
            row.cell('INLET CONNECTION')
            row.cell(img='image.png', img_fill_width=False)
            row.cell('OUTLET CONNECTION')
            row.cell(img='image.png', img_fill_width=False)
            
            row = table.row()
            row.cell('DEFECT CONNECTION  (IF ANY)')
            row.cell(img='image.png', img_fill_width=False)
            row.cell('DEFECT ON BODY (IF ANY)')
            row.cell(img='image.png', img_fill_width=False)

    def signature_block(self, date_value=""):
        self.set_font(self.FONT_FAMILY, 'B', self.FONT_SIZE)
        col_widths = [63.33, 63.33, 63.33]
        table_width = sum(col_widths)
        x_start = self.get_x()
        y_start = self.get_y()
        grey = (128, 128, 128)
        headings_style = FontFace(emphasis="B", fill_color=grey)

        with self.table(col_widths=col_widths, line_height=5, headings_style=headings_style) as table:
            row = table.row()
            row.cell('PREPARED BY', align='C')
            row.cell('CLIENT REPRESENTATIVE', align='C')
            row.cell('APPROVED BY', align='C')

        sig_height = 40
        y_sig = self.get_y()
        self.rect(x_start, y_sig, table_width, sig_height)

        for i in range(1, len(col_widths)):
            x = x_start + sum(col_widths[:i])
            self.line(x, y_sig, x, y_sig + sig_height)

        label_x_offsets = [x_start + 2, x_start + col_widths[0] + 2, x_start + col_widths[0] + col_widths[1] + 2]
        label_y_name = y_sig + sig_height - 15
        label_y_date = y_sig + sig_height - 8

        for x in label_x_offsets:
            self.set_xy(x, label_y_name)
            self.cell(0, 5, "NAME:")
            self.set_xy(x, label_y_date)
            self.cell(0, 5, "DATE:")

        self.set_y(y_sig + sig_height)

def generate_pdf():
    valve_data = load_valve_data()
    pdf = PDF(valve_data, format='A4')
    print('FPDF units: millimeters (mm) by default for A4 size 210x297mm')
    pdf.add_page()

    pdf.client_info()
    pdf.service_info()
    pdf.transportation_details()
    pdf.received_info_and_condition()
    pdf.valve_condition()
    pdf.detailed_picture()
    pdf.signature_block()

    pdf.output('generated_report.pdf')
    print('PDF report "generated_report.pdf" created successfully.')

if __name__ == "__main__":
    generate_pdf()
