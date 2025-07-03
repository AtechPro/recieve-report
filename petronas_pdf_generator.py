from fpdf import FPDF
from fpdf.enums import XPos, YPos
from fpdf.fonts import FontFace # Import FontFace

class PDF(FPDF):
    FONT_FAMILY = 'helvetica'
    FONT_SIZE = 6
    HEADER_FONT_SIZE = 8
    RECEIVED_FONT_SIZE = 7

    def header(self):
        # Two-column header: logo (placeholder) and wrapped title (safe multi_cell usage)
        self.set_font(self.FONT_FAMILY, 'B', 8)
        logo_width = 30
        title_width = 160
        line_height = 8
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

        grey = (128, 128, 128)
        # Create a FontFace style for table headings
        headings_style = FontFace(emphasis="B",  fill_color=grey) # Changed emphasis to "B" for bold

        # Received Report as a table with colored heading
        self.set_font(self.FONT_FAMILY, 'B', self.RECEIVED_FONT_SIZE)
        col_widths = [190]  # Full width single column
        # Apply the headings_style to the table
        with self.table(col_widths=col_widths, line_height=5, headings_style=headings_style) as table:
            row = table.row()
            # Removed is_heading=True as it's not supported by row.cell()
            row.cell('RECEIVED REPORT', align='C')

    def client_info(self):
        self.set_font(self.FONT_FAMILY, '', self.FONT_SIZE)
        # Define column widths (adjust as needed)
        col_widths = [30, 80, 40, 20, 20, 20, 30, 10]
        with self.table(col_widths=col_widths, line_height=4) as table:
            # Row 1: CLIENT (colspan=1), PETRONAS... (colspan=7)
            row = table.row()
            row.cell('CLIENT')
            row.cell('PETRONAS CHEMICALS FERTILISER SABAH SDN BHD', colspan=7) # data

            # Row 2: PROJECT, VALVE..., DOC NO, Gear Box..., (colspan as needed)
            row = table.row()
            row.cell('PROJECT')
            row.cell('VALVE MAINTENANCE/REPAIR') #data
            row.cell('DOC NO')
            row.cell('Gear Box Servicing & Valve Packing Replacement', colspan=5) #data

            # Row 3: LOCATION, SIPITANG..., SIZE INLET, 0, RATING, 0, INLET TYPE, 20
            row = table.row()
            row.cell('LOCATION')
            row.cell('SIPITANG SABAH') #data
            row.cell('SIZE INLET')
            row.cell('0') #data
            row.cell('RATING')
            row.cell('0') #data
            row.cell('INLET TYPE')
            row.cell('20') #data

            # Row 4: DATE IN, YES, SIZE OUTLET, 20, RATING, 300, OUTLET TYPE, 0
            row = table.row()
            row.cell('DATE IN')
            row.cell('YES') #data
            row.cell('SIZE OUTLET')
            row.cell('20') #data
            row.cell('RATING')
            row.cell('300') #data
            row.cell('OUTLET TYPE')
            row.cell('0') #data

            # Row 5: WO, 81620164, MANUFACTURER, MOV, (rest empty)
            row = table.row()
            row.cell('WO')
            row.cell('81620164') #data
            row.cell('MANUFACTURER')
            row.cell('MOV', colspan=5) #data

            # Row 6: TAG NO, 1/0/1900, TYPE OF VALVE, 14, (rest empty)
            row = table.row()
            row.cell('TAG NO')
            row.cell('M237-19MOV-002') #data
            row.cell('TYPE OF VALVE')
            row.cell('14', colspan=5) #data

            # Row 7: (empty), VALVE OPERATED TYPE, SAMBO, (rest empty)
            row = table.row()
            row.cell('')
            row.cell('') #data
            row.cell('VALVE OPERATED TYPE')
            row.cell('SAMBO', colspan=5) #data

    def service_info(self):
        self.set_font(self.FONT_FAMILY, '', self.FONT_SIZE)
        # 8 columns: label, box, label, box, label, box, label, box
        col_widths = [30, 20, 40, 20, 40, 20, 50, 30] # total 250
        with self.table(col_widths=col_widths, line_height=4) as table:
            row = table.row()
            row.cell('INSITU TESTING')
            row.cell('')  # empty cell for checkbox
            row.cell('SERVICE & REPAIR')
            row.cell('')  # empty cell for checkbox
            row.cell('TESTING ONLY')
            row.cell('')  # empty cell for checkbox
            row.cell('REPLACE NEW VALVE')
            row.cell('')  # empty cell for checkbox

    def transportation_details(self):
        self.set_font(self.FONT_FAMILY, '', self.FONT_SIZE)
        col_widths = [30, 80, 40, 20, 20, 20, 30, 10]
        grey = (128, 128, 128)
        headings_style = FontFace(emphasis="B",  fill_color=grey)

        with self.table(col_widths=col_widths, line_height=4, headings_style=headings_style) as table:
            row = table.row()
            # Removed is_heading=True
            row.cell('TRANSPORTATION DETAILS', colspan=8, align='C')

            row = table.row()
            row.cell('TRANSPORT MODE')
            row.cell('lorry') #data
            row.cell('PACKAGING')
            row.cell('wooden box', colspan=5) #data

            row = table.row()
            row.cell('TRANSPORT BY')
            row.cell('petronas') #data
            row.cell('RECIEVED BY')
            row.cell('petronas', colspan=5) #data

            row = table.row()
            row.cell('COMMENT ON TRANSPORTATION IF ANY', colspan=2)
            row.cell('broken on the wooden box', colspan=6) #data

    def received_info_and_condition(self):
        self.set_font(self.FONT_FAMILY, '', self.FONT_SIZE)
        # Adjust to 3 equal columns for images
        col_widths = [63.33, 63.33, 63.33]  # 190/3 for equal image spaces
        box_height = 40  # or whatever height you want

        # Save current position
        x = self.get_x()
        y = self.get_y()

        # Draw the big box (spanning all columns)
        self.rect(x, y, sum(col_widths), box_height)

        # Place the label at the top-left inside the box
        self.set_xy(x, y)
        self.set_font(self.FONT_FAMILY, 'B', self.FONT_SIZE)
        self.cell(0, 5, 'AS RECEIVED VALVE:', align='L')
        
        # Calculate dimensions for images
        image_width = 55  # Width for each image
        image_height = 30  # Height for each image
        margin = 4  # Margin between images
        y_offset = 8  # Space from title to images
        
        # Place three images side by side
        for i in range(3):
            image_x = x + margin + (i * (image_width + margin))
            self.image('image.png', x=image_x, y=y + y_offset, w=image_width, h=image_height)

        # Move cursor to the bottom of the box
        self.set_xy(x, y + box_height)
        self.set_font(self.FONT_FAMILY, '', self.FONT_SIZE)
        grey = (128, 128, 128)
        headings_style = FontFace(emphasis="B",  fill_color=grey)

        col_widths = [47.5, 47.5, 47.5, 47.5]

        # Now continue with the table for the condition
        with self.table(col_widths=col_widths, line_height=4, headings_style=headings_style) as table:
            row = table.row()
            # Removed is_heading=True
            row.cell('AS RECEIVED VALVE CONDITION', colspan=4, align='C')
            # Data rows
            row = table.row()
            row.cell('INLET CONNECTION TYPE')
            row.cell('20') #data
            row.cell('OUTLET CONNECTION TYPE')
            row.cell('0') #data

            row = table.row()
            row.cell('NAMEPLATE')
            row.cell('M237-14MOV-002') #data
            row.cell('TAG NUMBER/PLATE')
            row.cell('0') #data

            row = table.row()
            row.cell('INLET CONNECTION CONDITION')
            row.cell('300') #data
            row.cell('OUTLET CONNECTION CONDITION')
            row.cell('0') #data

            row = table.row()
            row.cell('CONNECTION MAJOR DEFECT/DAMAGE')
            row.cell('0') #data
            row.cell('')
            row.cell('')

            row = table.row()
            row.cell('VALVE BODY CONDITION')
            row.cell('0') #data
            row.cell('MAJOR DEFECT ON BODY')
            row.cell('0') #data

    def valve_condition(self, extra_height=8):
        self.set_font(self.FONT_FAMILY, 'B', self.FONT_SIZE)
        col_widths = [190]

        # Define colors for headings
        blue = (0, 0, 255)
        grey = (128, 128, 128)
        headings_style = FontFace(emphasis="B",  fill_color=grey)

        with self.table(col_widths=col_widths, line_height=4, headings_style=headings_style) as table:
            row = table.row()
            # Removed is_heading=True
            row.cell('OVERALL VALVE CONDITION', colspan=1, align='C')
        # Add extra space after the table
        self.cell(190, extra_height, 'Little Scratch on the Valves Body, No Major Defect', border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C') #data
        with self.table(col_widths=col_widths, line_height=4, headings_style=headings_style) as table:
            row = table.row()
            # Removed is_heading=True
            row.cell('DETAILED PICTURE', colspan=1, align='C')

    def detailed_picture(self):
        self.set_font(self.FONT_FAMILY, '', self.FONT_SIZE)
        col_widths = [47.5, 47.5, 47.5, 47.5]
        with self.table(col_widths=col_widths, line_height=30) as table:
            row = table.row()
            row.cell('INLET CONNECTION')
            row.cell(img='image.png')  # Insert image in cell
            row.cell('OUTLET CONNECTION')
            row.cell(img='image.png')  # Insert image in cell
            
            row = table.row()
            row.cell('DEFECT CONNECTION  (IF ANY)')
            row.cell(img='image.png')  # Insert image in cell
            row.cell('DEFECT ON BODY (IF ANY)')
            row.cell(img='image.png')  # Insert image in cell

    def signature_block(self, date_value=""):
        self.set_font(self.FONT_FAMILY, 'B', self.FONT_SIZE)
        col_widths = [63.33, 63.33, 63.33]
        table_width = sum(col_widths)
        x_start = self.get_x()
        y_start = self.get_y()
        grey = (128, 128, 128)
        headings_style = FontFace(emphasis="B",  fill_color=grey)

        # 1. Draw header row as a table
        with self.table(col_widths=col_widths, line_height=5, headings_style=headings_style) as table:
            row = table.row()
            # Removed is_heading=True
            row.cell('PREPARED BY', align='C')
            # Removed is_heading=True
            row.cell('CLIENT REPRESENTATIVE', align='C')
            # Removed is_heading=True
            row.cell('APPROVED BY', align='C')

        # 2. Draw the big signature area rectangle (no horizontal lines inside)
        sig_height = 40  # Adjust as needed
        y_sig = self.get_y()
        self.rect(x_start, y_sig, table_width, sig_height)

        # 3. Draw vertical lines to divide columns
        for i in range(1, len(col_widths)):
            x = x_start + sum(col_widths[:i])
            self.line(x, y_sig, x, y_sig + sig_height)

        # 4. Place NAME: and DATE: labels near the bottom of each column
        label_x_offsets = [x_start + 2, x_start + col_widths[0] + 2, x_start + col_widths[0] + col_widths[1] + 2]
        label_y_name = y_sig + sig_height - 15  # 15mm from the bottom
        label_y_date = y_sig + sig_height - 8   # 8mm from the bottom

        for x in label_x_offsets:
            self.set_xy(x, label_y_name)
            self.cell(0, 5, "NAME:")
            self.set_xy(x, label_y_date)
            self.cell(0, 5, "DATE:")

        # Move cursor to the bottom of the signature block for next content
        self.set_y(y_sig + sig_height)

pdf = PDF(format='A4')  # Explicitly set A4 size (210 x 297 mm by default)
print('FPDF units: millimeters (mm) by default for A4 size 210x297mm')
pdf.add_page()

# Call the client_info method to display the client information
pdf.client_info()
pdf.service_info()
pdf.transportation_details()
pdf.received_info_and_condition()
pdf.valve_condition()
pdf.detailed_picture()
pdf.signature_block()


pdf.output('generated_report.pdf')
print('PDF report "generated_report.pdf" created successfully.')
