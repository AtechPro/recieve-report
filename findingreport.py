from fpdf import FPDF
from fpdf.enums import XPos, YPos
from fpdf.fonts import FontFace
import json
import os
from PIL import Image

def get_record_by_no_or_wo(identifier):
    """Get record by No or WO (Work Order) number"""
    with open('extracted_data.json', 'r') as file:
        data = json.load(file)
    
    # First try to find by No
    for record in data['data']:
        if record.get('No') == str(identifier):
            return record
    
    # If not found by No, try to find by WO
    for record in data['data']:
        if record.get('WO ') == str(identifier):
            return record
    
    raise ValueError(f"No record found with No = {identifier} or WO = {identifier}")

def get_record_by_no(no_value):
    """Backward compatibility function - use get_record_by_no_or_wo instead"""
    return get_record_by_no_or_wo(no_value)

def load_valve_data(identifier, user_data=None, override_mode=False):
    """Load valve data from both valve_data.json (user-defined) and extracted_data.json (actual records)"""
    
    # Load user-defined data
    if user_data is None:
        try:
            with open('valve_data.json', 'r') as file:
                user_data = json.load(file)
        except FileNotFoundError:
            # Create default user data if file doesn't exist
            user_data = {
                'client_info': {
                    'client': 'PETRONAS CHEMICALS FERTILISER SABAH SDN BHD',
                    'project': 'VALVE MAINTENANCE PROJECT 2025',
                    'location': 'Sipitang',
                    'date_in': '01/01/2025'  # User can modify this date in dd/mm/yyyy format
                }
            }
    
    # Fetch the record by No or WO, but allow missing if override_mode
    if not override_mode:
        record = get_record_by_no_or_wo(identifier)
    else:
        try:
            record = get_record_by_no_or_wo(identifier)
        except Exception:
            record = {}  # Use empty record if not found in override mode
    
    def clean_value(value):
        """Clean NaN values and convert to empty string"""
        if value is None or value == 'nan' or value == 'NaT':
            return ''
        return str(value)
    
    # Combine user-defined data with extracted data, with full override for client_info fields
    def get_client_info_field(field, extracted_key=None, default=None):
        # Use user_data['client_info'][field] if present, else extracted data, else default
        if user_data and 'client_info' in user_data and field in user_data['client_info']:
            return clean_value(user_data['client_info'][field])
        if extracted_key and extracted_key in record:
            return clean_value(record.get(extracted_key))
        return clean_value(default)

    mapped_data = {
        'client_info': {
            'client': get_client_info_field('client', default='PETRONAS CHEMICALS FERTILISER SABAH SDN BHD'),
            'project': get_client_info_field('project', default='VALVE MAINTENANCE PROJECT 2025'),
            'doc_info': get_client_info_field('doc_info', extracted_key='Service Type'),
            'location': get_client_info_field('location', default='Sipitang'),
            'size_inlet': get_client_info_field('size_inlet', extracted_key='Inlet (Size)'),
            'inlet_rating': get_client_info_field('inlet_rating', extracted_key='Inlet (Rating)'),
            'inlet_type': get_client_info_field('inlet_type', extracted_key='Inlet (Type)'),
            'date_in': get_client_info_field('date_in'),
            'size_outlet': get_client_info_field('size_outlet', extracted_key='Outlet (Size)'),
            'outlet_rating': get_client_info_field('outlet_rating', extracted_key='Outlet (Rating)'),
            'outlet_type': get_client_info_field('outlet_type', extracted_key='Outlet (Type)'),
            'wo_number': get_client_info_field('wo_number', extracted_key='WO '),
            'manufacturer': get_client_info_field('manufacturer', extracted_key='Manufacturer'),
            'tag_no': get_client_info_field('tag_no', extracted_key='Tag Number (Valve No)'),
            'valve_type': get_client_info_field('valve_type', extracted_key='Type of Valve'),
            'valve_operated_type': get_client_info_field('valve_operated_type', extracted_key='Valve Operated Type'),
        },
        'stamp_info': {
            'stamp_path': user_data.get('stamp_info', {}).get('stamp_path', 'stamp/sao.png'),
            'prepared_name': user_data.get('stamp_info', {}).get('prepared_name', 'Sao Lip Zhou'),
            'date_value': user_data.get('stamp_info', {}).get('date_value', '')
        },
        'visual_inspection': user_data.get('visual_inspection') if user_data and user_data.get('visual_inspection') else [
            {"desc": "GENERAL APPEARANCE", "condition": "", "actions": "", "remarks": ""},
            {"desc": "NAMEPLATE", "condition": "", "actions": "", "remarks": ""}, # condition get from record 'nameplate'
            {"desc": "OVERALL FLANGE/CONNECTION CONDITION", "condition": "", "actions": "", "remarks": ""},
            {"desc": "BODY", "condition": "", "actions": "", "remarks": ""},
            {"desc": "BONNET", "condition": "", "actions": "", "remarks": ""},
            {"desc": "YOKE", "condition": "", "actions": "", "remarks": ""},
            {"desc": "DISC", "condition": "", "actions": "", "remarks": ""},
            {"desc": "SEAT", "condition": "", "actions": "", "remarks": ""},
            {"desc": "BONNET GASKET", "condition": "", "actions": "", "remarks": ""},
        ],
        'internal_inspection': user_data.get('internal_inspection') if user_data and user_data.get('internal_inspection') else [
            {"desc": "BODY", "condition": "", "actions": "", "remarks": ""},
            {"desc": "BONNET", "condition": "", "actions": "", "remarks": ""},
            {"desc": "YOKE", "condition": "", "actions": "", "remarks": ""},
            {"desc": "DISC", "condition": "", "actions": "", "remarks": ""},
            {"desc": "SEAT", "condition": "", "actions": "", "remarks": ""},
            {"desc": "BONNET GASKET", "condition": "", "actions": "", "remarks": ""},
            {"desc": "STEM", "condition": "", "actions": "", "remarks": ""},
            {"desc": "WHEEL NUT", "condition": "", "actions": "", "remarks": ""},
            {"desc": "PACKING", "condition": "", "actions": "", "remarks": ""},
            {"desc": "GLAND BUSHING", "condition": "", "actions": "", "remarks": ""},
            {"desc": "BACK SEAT", "condition": "", "actions": "", "remarks": ""},
            {"desc": "GLAND NUT", "condition": "", "actions": "", "remarks": ""},
        ],
        'detailed_pictures': user_data.get('detailed_pictures') if user_data and user_data.get('detailed_pictures') else [
            {"item": "ITEM 1", "finding": "", "proposed_action": "", "image_path_1": "goodvalve.png", "image_path_2": "goodvalve.png"},
            {"item": "ITEM 2", "finding": "", "proposed_action": "", "image_path_1": "goodvalve.png", "image_path_2": "goodvalve.png"},
            {"item": "ITEM 3", "finding": "", "proposed_action": "", "image_path_1": "goodvalve.png", "image_path_2": "goodvalve.png"}
        ],
        'pretest': user_data.get('pretest') if user_data and user_data.get('pretest') else {
            'type_test': '',
            'test_medium': '',
            'shell': {
                'pressure': '',
                'duration': '',
                'result_remarks': ''
            },
            'backseat': {
                'pressure': '',
                'duration': '',
                'result_remarks': ''
            },
            'seat': {
                'pressure': '',
                'duration': '',
                'result_remarks': ''
            },
            'test_accordance_to': ''
        },
        'comment': user_data.get('comment', '') if user_data else ''
    }
    
    return mapped_data

class PDF(FPDF):
    FONT_FAMILY = 'helvetica'
    FONT_SIZE = 6
    HEADER_FONT_SIZE = 8
    RECEIVED_FONT_SIZE = 7

    def __init__(self, data, selected_services=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.valve_data = data
        self.selected_services = selected_services or []

    def header(self):
        # Two-column header: logo and wrapped title
        self.set_font(self.FONT_FAMILY, 'B', 8)
        logo_width = 30
        title_width = 160
        line_height = 8
        y_start = self.get_y()
        
        # Logo area dimensions
        logo_area_width = logo_width
        logo_area_height = line_height * 4
        
        # Calculate logo position to center it in the allocated area
        logo_x = self.get_x()
        logo_y = y_start
        
        # Try to load and display the logo with aspect ratio preservation
        logo_path = 'petronas.png'
        if os.path.exists(logo_path):
            # Get image dimensions to calculate aspect ratio
            from PIL import Image
            try:
                with Image.open(logo_path) as img:
                    img_width, img_height = img.size
                    aspect_ratio = img_width / img_height
                    
                    # Calculate dimensions that fit within the allocated area
                    if aspect_ratio > 1:  # Landscape
                        logo_display_width = logo_area_width - 2  # Leave small margin
                        logo_display_height = logo_display_width / aspect_ratio
                    else:  # Portrait or square
                        logo_display_height = logo_area_height - 2  # Leave small margin
                        logo_display_width = logo_display_height * aspect_ratio
                    
                    # Center the logo in the allocated area
                    logo_x_offset = logo_x + (logo_area_width - logo_display_width) / 2
                    logo_y_offset = logo_y + (logo_area_height - logo_display_height) / 2
                    
                    # Draw the logo
                    self.image(logo_path, x=logo_x_offset, y=logo_y_offset, w=logo_display_width, h=logo_display_height)
                    
            except Exception as e:
                print(f"Error loading logo: {e}")
                # Fallback to placeholder if logo loading fails
                self.cell(logo_width, line_height * 4, '[LOGO]', border=1, align='C')
        else:
            # Fallback to placeholder if logo file doesn't exist
            self.cell(logo_width, line_height * 4, '[LOGO]', border=1, align='C')
        
        # Draw border around logo area for visual reference
        self.rect(logo_x, logo_y, logo_area_width, logo_area_height)
        
        # Title section
        self.set_xy(logo_x + logo_area_width, y_start)
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

        # Add client information as part of the header
        data = self.valve_data['client_info']
        self.set_font(self.FONT_FAMILY, '', self.FONT_SIZE)
        col_widths = [30, 80, 40, 14, 20, 20, 23, 23]
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

        # Add service information as part of the header
        # Get selected_services from valve_data if available
        selected_services = getattr(self, 'selected_services', [])
        self.service_info(selected_services)


    def service_info(self, selected_services=None):
        if selected_services is None:
            selected_services = []
        
        self.set_font(self.FONT_FAMILY, '', self.FONT_SIZE)
        col_widths = [30, 20, 40, 20, 40, 20, 50, 30]
        with self.table(col_widths=col_widths, line_height=4) as table:
            row = table.row()
            row.cell('INSITU TESTING')
            row.cell('/' if 'insitu_testing' in selected_services else '', align='C') # checkbox for INSITU TESTING
            row.cell('SERVICE & REPAIR')
            row.cell('/' if 'service_repair' in selected_services else '', align='C') # checkbox for SERVICE & REPAIR
            row.cell('TESTING ONLY')
            row.cell('/' if 'testing_only' in selected_services else '', align='C') # checkbox for TESTING ONLY
            row.cell('REPLACE NEW VALVE')
            row.cell('/' if 'replace_new_valve' in selected_services else '', align='C') # checkbox for REPLACE NEW VALVE 
    
    def visual_inspection(self):
        self.set_font(self.FONT_FAMILY, '', self.FONT_SIZE)
        col_widths = [64, 62, 62, 62] # =190

        grey = (128, 128, 128)
        headings_style = FontFace(emphasis="B", fill_color=grey)
        with self.table(col_widths=col_widths, line_height=4, headings_style=headings_style) as table:
            row = table.row()
            row.cell('AS RECEIVED VISUAL INSPECTION (EXTERNAL)', align='C', colspan=4)
            row = table.row()
            row.cell('DESCRIPTION', align='C')
            row.cell('CONDITION', align='C')
            row.cell('ACTIONS', align='C')
            row.cell('REMARKS', align='C')
            
            # Use mapped data for parts
            parts = self.valve_data.get('visual_inspection', [])
            for part in parts:
                row = table.row()
                row.cell(part.get('desc', ''), align='L')
                row.cell(part.get('condition', ''), align='C')
                row.cell(part.get('actions', ''), align='C')
                row.cell(part.get('remarks', ''), align='C')

    def pretest(self):
        self.set_font(self.FONT_FAMILY, '', self.FONT_SIZE)
        col_widths = [10,45,45,45,45]  # 4 columns, total 190mm
        grey = (128, 128, 128)
        headings_style = FontFace(emphasis="B", fill_color=grey)
        
        # Get pretest data from mapped data
        pretest_data = self.valve_data.get('pretest', {})
        
        with self.table(col_widths=col_widths, line_height=4, headings_style=headings_style) as table:
            row = table.row()
            row.cell('PRE-TEST (HYDROTEST/LEAKED TEST)', align='C', colspan=5)
            row = table.row()
            row.cell('TYPE TEST', align='C', colspan=2)
            row.cell(pretest_data.get('type_test', ''), align='C')
            row.cell('TEST MEDIUM', align='C')
            row.cell(pretest_data.get('test_medium', ''), align='C')
            row = table.row()
            row.cell('DESCRIPTION', align='C', colspan=2)
            row.cell('PRESSURE', align='C')
            row.cell('DURATION', align='C')
            row.cell('RESULT & REMARKS', align='C')
            row = table.row()
            row.cell('A', align='C')
            row.cell('SHELL', align='C')
            row.cell(pretest_data.get('shell', {}).get('pressure', ''), align='C')
            row.cell(pretest_data.get('shell', {}).get('duration', ''), align='C')
            row.cell(pretest_data.get('shell', {}).get('result_remarks', ''), align='C')
            row = table.row()
            row.cell('B', align='C')
            row.cell('BACKSEAT', align='C')
            row.cell(pretest_data.get('backseat', {}).get('pressure', ''), align='C')
            row.cell(pretest_data.get('backseat', {}).get('duration', ''), align='C')
            row.cell(pretest_data.get('backseat', {}).get('result_remarks', ''), align='C')
            row = table.row()
            row.cell('C', align='C')
            row.cell('SEAT', align='C')
            row.cell(pretest_data.get('seat', {}).get('pressure', ''), align='C')
            row.cell(pretest_data.get('seat', {}).get('duration', ''), align='C')
            row.cell(pretest_data.get('seat', {}).get('result_remarks', ''), align='C')
            row = table.row()
            row.cell('TEST ACCORDANCE TO', align='C', colspan=2)
            row.cell(pretest_data.get('test_accordance_to', ''), align='C', colspan=3)


    def additonal_comment(self):
        comment = self.valve_data.get('comment', '')
        self.set_font(self.FONT_FAMILY, '', self.FONT_SIZE)
        x = self.get_x()
        y = self.get_y()
        width = 190
        height = 50  # Adjust as needed

        # Draw the rectangle
        self.rect(x, y, width, height)

        # Set position just inside the top-left of the box
        self.set_xy(x + 1, y + 1)
        self.set_font(self.FONT_FAMILY, 'B', self.FONT_SIZE)  # Bold for label
        self.cell(0, 7, 'ADDITIONAL COMMENT:', ln=1)

        # Now write the comment, a bit lower inside the box
        self.set_font(self.FONT_FAMILY, '', self.FONT_SIZE)  # Regular for comment
        self.set_x(x + 2)
        self.multi_cell(width - 8, 5, comment, 0, 'J')  # Justified alignment

        # Move Y to the bottom of the box for spacing after
        self.set_xy(x, y + height)
        self.ln(30)


    def internal_inspection(self):
        self.set_font(self.FONT_FAMILY, '', self.FONT_SIZE)
        col_widths = [64, 62, 62, 62]  # 4 columns, total 190mm
        grey = (128, 128, 128)
        headings_style = FontFace(emphasis="B", fill_color=grey)
        with self.table(col_widths=col_widths, line_height=4, headings_style=headings_style) as table:
            row = table.row()
            row.cell('INTERNAL PARTS INSPECTION', align='C', colspan=4)
            row = table.row()
            self.set_font(self.FONT_FAMILY, 'B', self.FONT_SIZE)
            row.cell('DESCRIPTION', align='C')
            row.cell('CONDITION', align='C')
            row.cell('ACTIONS', align='C')
            row.cell('REMARKS', align='C')
            self.set_font(self.FONT_FAMILY, '', self.FONT_SIZE)
            # Use mapped data for parts
            parts = self.valve_data.get('internal_inspection', [])
            for part in parts:
                row = table.row()
                row.cell(part.get('desc', ''), align='L')
                row.cell(part.get('condition', ''), align='C')
                row.cell(part.get('actions', ''), align='C')
                row.cell(part.get('remarks', ''), align='C')
    
    def detailed_picture(self):
        self.set_font(self.FONT_FAMILY, '', self.FONT_SIZE)
        col_widths = [95, 47.5, 47.5]
        line_height = 3
        image_height = 35

        grey = (128, 128, 128)
        headings_style = FontFace(emphasis="B", fill_color=grey)
        # Table header (full width)
        with self.table(col_widths=col_widths, line_height=4, headings_style=headings_style) as table:
            row = table.row()
            row.cell('DETAILS PICTURE/MAJOR DEFECT ', align='C', colspan=3)

        # Section header row (drawn manually for perfect alignment)
        x_start = self.l_margin
        y_start = self.get_y()
        self.set_xy(x_start, y_start)
        self.set_font(self.FONT_FAMILY, 'B', self.FONT_SIZE)
        self.cell(col_widths[0], line_height * 2, 'ITEM:', border=1, align='C')
        self.cell(col_widths[1], line_height * 2, 'FINDING', border=1, align='C')
        self.cell(col_widths[2], line_height * 2, 'DESCRIPTION OF SERVICES', border=1, align='C')
        self.ln(line_height * 2)
        self.set_font(self.FONT_FAMILY, '', self.FONT_SIZE)

        detailed_pictures = self.valve_data.get('detailed_pictures', [])
        for i, picture_data in enumerate(detailed_pictures):
            finding = picture_data.get('finding', '')
            proposed_action = picture_data.get('proposed_action', '')
            image_path_1 = picture_data.get('image_path_1', '')
            image_path_2 = picture_data.get('image_path_2', '')

            # Calculate required height for each cell
            y_start = self.get_y()
            x_start = self.l_margin
            self.set_xy(x_start, y_start)
            finding_height = self.get_string_height(col_widths[1], finding, line_height)
            action_height = self.get_string_height(col_widths[2], proposed_action, line_height)
            row_height = max(finding_height, action_height, image_height)

            # Page break if needed
            if self.get_y() + row_height > self.page_break_trigger:
                self.add_page()
                y_start = self.get_y()

            # Draw image cell (first column)
            self.set_xy(x_start, y_start)
            self.cell(col_widths[0], row_height, '', border=1)
            # Draw images if any
            image_x = x_start + 2
            image_y = y_start + 2
            uploaded_images = []
            if image_path_1 and image_path_1 != 'goodvalve.png' and os.path.exists(image_path_1):
                uploaded_images.append(image_path_1)
            if image_path_2 and image_path_2 != 'goodvalve.png' and os.path.exists(image_path_2):
                uploaded_images.append(image_path_2)
            for idx, img_path in enumerate(uploaded_images):
                if idx == 0:
                    self.image(img_path, x=image_x, y=image_y, w=40, h=30)
                elif idx == 1:
                    self.image(img_path, x=image_x + 45, y=image_y, w=40, h=30)

            # Draw finding cell (second column)
            self.set_xy(x_start + col_widths[0], y_start)
            self.multi_cell(col_widths[1], line_height, finding, border=0, align='L')
            y_after_finding = self.get_y()
            if y_after_finding < y_start + row_height:
                self.set_xy(x_start + col_widths[0], y_after_finding)
                self.cell(col_widths[1], y_start + row_height - y_after_finding, '', border=0)
            self.rect(x_start + col_widths[0], y_start, col_widths[1], row_height)

            # Draw proposed_action cell (third column)
            self.set_xy(x_start + col_widths[0] + col_widths[1], y_start)
            self.multi_cell(col_widths[2], line_height, proposed_action, border=0, align='L')
            y_after_action = self.get_y()
            if y_after_action < y_start + row_height:
                self.set_xy(x_start + col_widths[0] + col_widths[1], y_after_action)
                self.cell(col_widths[2], y_start + row_height - y_after_action, '', border=0)
            self.rect(x_start + col_widths[0] + col_widths[1], y_start, col_widths[2], row_height)

            # Move to the start of the next row
            self.set_y(y_start + row_height)

    def get_string_height(self, w, txt, line_height):
        # Helper to calculate the height a multicell would take
        if not txt:
            return line_height
        # Split by newlines first
        lines = txt.split('\n')
        total_lines = 0
        for line in lines:
            # Estimate number of lines for this chunk
            str_width = self.get_string_width(line)
            n_lines = max(1, int(str_width / w) + 1)
            total_lines += n_lines
        return total_lines * line_height

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

            sig_height = 30
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



    def stamp(self, stamp_path=None, prepared_name=None, date_value=None):
        stamp_data = self.valve_data.get('stamp_info', {})
        
        stamp_path = stamp_path or stamp_data.get('stamp_path')
        prepared_name = prepared_name or stamp_data.get('prepared_name')
        date_value = date_value or stamp_data.get('date_value')

        current_x = self.get_x()
        current_y = self.get_y()
        
        sig_width = 63.33
        sig_height = 30

        stamp_x = current_x + 10  # Small offset from left edge
        stamp_y = current_y - sig_height + 2   # Position within signature box
        
        # Position name and date text
        name_x = current_x + 15
        name_y = current_y - 15  # Near bottom of signature box
        date_x = current_x + 15
        date_y = current_y - 8   # Near bottom of signature box
        
        if stamp_path and os.path.exists(stamp_path):
            try:
                with Image.open(stamp_path) as img:
                    img_width, img_height = img.size
                    aspect_ratio = img_width / img_height

                    # Always fix the height, scale width to maintain aspect ratio
                    stamp_height = 15  # mm
                    stamp_width = stamp_height * aspect_ratio

                    self.image(stamp_path, x=stamp_x, y=stamp_y, w=stamp_width, h=stamp_height)
            except Exception as e:
                print(f"Error loading stamp image: {e}")
                self.image(stamp_path, x=stamp_x, y=stamp_y, w=15, h=15)
        else:
            print("Stamp image not found")

        # Position text in the first column of signature block
        if prepared_name:
            self.set_xy(name_x, name_y)
            self.set_font(self.FONT_FAMILY, 'B', self.FONT_SIZE)
            self.cell(sig_width - 4, 5, prepared_name, align='L')
        
        if date_value:
            self.set_xy(date_x, date_y)
            self.cell(sig_width - 4, 5, date_value, align='L')

def generate_pdf(identifier, user_data=None, stamp_selection=None, date_value=None, selected_services=None, override_mode=False):
    valve_data = load_valve_data(identifier, user_data, override_mode=override_mode)
    pdf = PDF(valve_data, selected_services=selected_services, format='A4')
    print('FPDF units: millimeters (mm) by default for A4 size 210x297mm')
    pdf.add_page()
    # Service info is now part of the header, so no need to call service_info() separately
    pdf.visual_inspection()
    pdf.internal_inspection()
    pdf.pretest()
    pdf.additonal_comment()
    
    pdf.detailed_picture()
    pdf.signature_block()
    
    # Map stamp selection to stamp path and prepared name
    stamp_mapping = {
        'SAO': {
            'stamp_path': 'stamp/sao.png',
            'prepared_name': 'Sao Lip Zhou'
        }
    }
    
    if stamp_selection and stamp_selection in stamp_mapping:
        stamp_info = stamp_mapping[stamp_selection]
        pdf.stamp(stamp_info['stamp_path'], stamp_info['prepared_name'], date_value)
    else:
        pass

    # Create generated_pdfs directory if it doesn't exist
    os.makedirs('generated_pdfs', exist_ok=True)
    
    # Determine if identifier is a No or WO for filename
    if not override_mode:
        record = get_record_by_no_or_wo(identifier)
        if record.get('No') == str(identifier):
            output_filename = f'Finding_report_No_{identifier}.pdf'
            print(f'PDF report "{output_filename}" created successfully for No = {identifier}.')
        else:
            output_filename = f'Finding_report_WO_{identifier}.pdf'
            print(f'PDF report "{output_filename}" created successfully for WO = {identifier}.')
    else:
        output_filename = f'Finding_report_Manual_{identifier}.pdf'
        print(f'PDF report "{output_filename}" created successfully in override/manual mode for identifier = {identifier}.')
    
    output_path = os.path.join('generated_pdfs', output_filename)
    pdf.output(output_path)
    
    return output_filename


if __name__ == "__main__":
    # Example identifier (replace with a valid No or WO from your extracted_data.json)
    identifier = "1"  # Change as needed
    # Optionally, you can provide user_data, image_files, received_valve_images, stamp_selection, date_value, selected_services
    try:
        # Example user_data with comment
        user_data = {
            'client_info': {
                'client': 'PETRONAS CHEMICALS FERTILISER SABAH SDN BHD',
                'project': 'VALVE MAINTENANCE PROJECT 2025',
                'location': 'Sipitang',
                'date_in': '01/01/2025'
            },
            'comment': (
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean vitae massa mi. "
                "Pellentesque a pulvinar purus. Curabitur vehicula ultrices enim, eget suscipit ante venenatis quis. "
                "Ut ullamcorper, arcu porta ultrices ultrices, mi tellus consequat ipsum, ut tempor nunc ante eget risus. "
                "Praesent iaculis pellentesque est, ut pretium arcu pellentesque eu. Morbi quis hendrerit diam, posuere placerat turpis. "
                "Etiam ac neque eget nulla dapibus vehicula a nec augue. Vestibulum in finibus dolor. Pellentesque vel nunc dolor. "
                "Sed dignissim dui quis mattis laoreet. Aliquam fringilla feugiat leo vitae pulvinar. Curabitur dictum erat ex. "
                "Proin aliquam leo nunc, eu viverra erat ultrices vel. Duis est lacus, efficitur at blandit eu, iaculis a nulla. "
                "Aenean convallis nisl sit amet dui pellentesque dictum. In vehicula eros quis felis ornare, vitae luctus odio aliquam. "
                "Vestibulum sodales nisl eu mi dapibus, sit amet feugiat ex tempus. In ut suscipit orci. Integer interdum id tellus quis dapibus. "
                "Sed tempor neque at pulvinar tristique. Nunc gravida, odio vel ultricies rutrum, ex odio tristique libero, at ultrices ligula felis at turpis. "
                "Sed mollis nibh nisl, a tempus lacus rhoncus vitae. Etiam tincidunt augue sit amet massa sodales, et vulputate ex malesuada. "
                "Duis non nibh augue. Nullam cursus iaculis enim, at fringilla erat venenatis at."
                "Sed dignissim dui quis mattis laoreet. Aliquam fringilla feugiat leo vitae pulvinar. Curabitur dictum erat ex. "
            )
        }
        output_filename = generate_pdf(
            identifier=identifier,
            user_data=user_data,
            stamp_selection="SAO",
            date_value="01/01/2025",
            selected_services=["insitu_testing", "service_repair"]
        )
        print(f"Test PDF generated: {output_filename}")
    except Exception as e:
        print(f"Test failed: {e}") 