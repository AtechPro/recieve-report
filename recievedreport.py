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
    """Load valve data from both valve_data.json (user-defined) and extracted_data.json (actual records), with optional override mode."""
    
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
    record = None
    if not override_mode:
        record = get_record_by_no_or_wo(identifier)
    else:
        try:
            record = get_record_by_no_or_wo(identifier)
        except Exception:
            # In override mode, allow missing record
            record = {}
    
    def clean_value(value):
        """Clean NaN values and convert to empty string"""
        if value is None or value == 'nan' or value == 'NaT':
            return ''
        return str(value)

    # Helper to get value with override logic
    def get_field(user_key, record_key, section='client_info'):
        if override_mode:
            # Always prefer user_data if present, else fallback to record
            val = user_data.get(section, {}).get(user_key)
            if val is not None and val != '':
                return val
            return clean_value(record.get(record_key))
        else:
            # Current behavior: user_data overrides only if present, else fallback
            return user_data.get(section, {}).get(user_key, clean_value(record.get(record_key)))

    mapped_data = {
        'client_info': {
            'client': get_field('client', 'Client'),
            'project': get_field('project', 'Project'),
            'doc_info': get_field('doc_info', 'Service Type'),
            'location': get_field('location', 'Location'),
            'size_inlet': get_field('size_inlet', 'Inlet (Size)'),
            'inlet_rating': get_field('inlet_rating', 'Inlet (Rating)'),
            'inlet_type': get_field('inlet_type', 'Inlet (Type)'),
            'date_in': get_field('date_in', 'Date In'),
            'size_outlet': get_field('size_outlet', 'Outlet (Size)'),
            'outlet_rating': get_field('outlet_rating', 'Outlet (Rating)'),
            'outlet_type': get_field('outlet_type', 'Outlet (Type)'),
            'wo_number': get_field('wo_number', 'WO '),
            'manufacturer': get_field('manufacturer', 'Manufacturer'),
            'tag_no': get_field('tag_no', 'Tag Number (Valve No)'),
            'valve_type': get_field('valve_type', 'Type of Valve'),
            'valve_operated_type': get_field('valve_operated_type', 'Valve Operated Type')
        },
        'transportation_details': {
            'transport_mode': get_field('transport_mode', 'Transport Mode'),
            'packaging': get_field('packaging', 'Packaging '),
            'transport_by': get_field('transport_by', 'Transport By'),
            'received_by': get_field('received_by', 'Received By'),
            'transport_comment': get_field('transport_comment', 'TRANSPORTATION (COMMENT)')
        },
        'received_valve_condition': {
            'inlet_connection_type': get_field('inlet_type', 'Inlet (Type)'),
            'outlet_connection_type': get_field('outlet_type', 'Outlet (Type)'),
            'nameplate': get_field('tag_no', 'Tag Number (Valve No)'),
            'tag_number': get_field('tag_no', 'Tag Number (Valve No)'),
            'inlet_connection_condition': get_field('inlet_connection_condition', 'Inlet Connection Condition'),
            'outlet_connection_condition': get_field('outlet_connection_condition', 'Outlet Connection Condition'),
            'connection_major_defect': get_field('connection_major_damage', ' Connection Major Damage'),
            'valve_body_condition': get_field('valve_body_condition', 'Valve Body Condition'),
            'major_defect_body': get_field('major_defect_on_body', 'Major Defect on Body')
        },
        'overall_condition': {
            'description': get_field('overall_valve_condition', 'Overall Valve Condition')
        },
        'stamp_info': {
            # Always use user_data['stamp_info'] if present, else fallback to defaults
            'stamp_path': user_data.get('stamp_info', {}).get('stamp_path', 'stamp/sao.png'),
            'prepared_name': user_data.get('stamp_info', {}).get('prepared_name', 'Sao Lip Zhou'),
            'date_value': user_data.get('stamp_info', {}).get('date_value', '')
        }
    }
    
    return mapped_data

def load_stamp_mapping(json_path='stamp_mapping.json'):
    """Load the stamp mapping from a JSON file."""
    try:
        with open(json_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading stamp mapping: {e}")
        return {}

class PDF(FPDF):
    FONT_FAMILY = 'helvetica'
    FONT_SIZE = 6
    HEADER_FONT_SIZE = 8
    RECEIVED_FONT_SIZE = 7

    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.valve_data = data

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

    def client_info(self):
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

    def received_info_and_condition(self, received_valve_images=None):
        data = self.valve_data['received_valve_condition']
        self.set_font(self.FONT_FAMILY, '', self.FONT_SIZE)
        col_widths = [63.33, 63.33, 63.33]
        box_height = 38

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
        
        # Use uploaded images if provided, otherwise use default images
        if received_valve_images and len(received_valve_images) > 0:
            image_files = received_valve_images
        else:
            image_files = []
        
        # Display up to 3 images
        for i in range(min(3, len(image_files))):
            image_file = image_files[i]
            if image_file and os.path.exists(image_file):
                image_x = x + margin + (i * (image_width + margin))
                self.image(image_file, x=image_x, y=y + y_offset, w=image_width, h=image_height)

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

    def detailed_picture(self, image_files=None):
        self.set_font(self.FONT_FAMILY, '', self.FONT_SIZE)
        col_widths = [47.5, 47.5, 47.5, 47.5]
        row_height = 33
        margin = 1  # mm gap from cell borders
        image_width = col_widths[1] - 2 * margin
        image_height = row_height - 2 * margin

        # Draw the table and get the starting x/y
        x_start = self.get_x()
        y_start = self.get_y()

        with self.table(col_widths=col_widths, line_height=row_height) as table:
            row = table.row()
            row.cell('INLET CONNECTION')
            row.cell('')  # image cell
            row.cell('OUTLET CONNECTION')
            row.cell('')  # image cell

            row = table.row()
            row.cell('DEFECT CONNECTION  (IF ANY)')
            row.cell('')  # image cell
            row.cell('DEFECT ON BODY (IF ANY)')
            row.cell('')  # image cell

        # Define image positions and their corresponding keys
        image_positions = {
            'inlet_connection': {
                'x': x_start + col_widths[0] + margin,
                'y': y_start + margin,
                'w': image_width,
                'h': image_height
            },
            'outlet_connection': {
                'x': x_start + col_widths[0] + col_widths[1] + col_widths[2] + margin,
                'y': y_start + margin,
                'w': image_width,
                'h': image_height
            },
            'defect_connection': {
                'x': x_start + col_widths[0] + margin,
                'y': y_start + row_height + margin,
                'w': image_width,
                'h': image_height
            },
            'defect_body': {
                'x': x_start + col_widths[0] + col_widths[1] + col_widths[2] + margin,
                'y': y_start + row_height + margin,
                'w': image_width,
                'h': image_height
            }
        }

        # Debug print for image_files
        print('DEBUG: image_files received in detailed_picture:', image_files)
        if image_files:
            for image_key, image_path in image_files.items():
                print(f'DEBUG: Checking {image_key}: {image_path}, exists: {os.path.exists(image_path)}')
                if image_key in image_positions and os.path.exists(image_path):
                    pos = image_positions[image_key]
                    self.image(image_path, x=pos['x'], y=pos['y'], w=pos['w'], h=pos['h'])

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

        sig_height = 28
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
        sig_height = 28

        stamp_x = current_x + 10  # Small offset from left edge
        stamp_y = current_y - sig_height + 1   # Position within signature box
        
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


def generate_pdf(identifier, user_data=None, image_files=None, received_valve_images=None, stamp_selection=None, date_value=None, selected_services=None, override_mode=False):
    valve_data = load_valve_data(identifier, user_data, override_mode=override_mode)
    pdf = PDF(valve_data, format='A4')
    print('FPDF units: millimeters (mm) by default for A4 size 210x297mm')
    pdf.add_page()

    pdf.client_info()
    pdf.service_info(selected_services)
    pdf.transportation_details()
    pdf.received_info_and_condition(received_valve_images)
    pdf.valve_condition()
    pdf.detailed_picture(image_files)
    pdf.signature_block()
    
    # Load stamp mapping from JSON
    stamp_mapping = load_stamp_mapping()
    
    if stamp_selection and stamp_selection in stamp_mapping:
        stamp_info = stamp_mapping[stamp_selection]
        pdf.stamp(stamp_info['stamp_path'], stamp_info['prepared_name'], date_value)
    else:
        pass

    # Create generated_pdfs directory if it doesn't exist
    os.makedirs('generated_pdfs', exist_ok=True)
    
    # Determine output filename
    if override_mode:
        output_filename = f'Recieved_report_Manual_{identifier}.pdf'
        print(f'PDF report "{output_filename}" created successfully in override/manual mode for identifier = {identifier}.')
    else:
        record = get_record_by_no_or_wo(identifier)
        if record.get('No') == str(identifier):
            output_filename = f'Recieved_report_No_{identifier}.pdf'
            print(f'PDF report "{output_filename}" created successfully for No = {identifier}.')
        else:
            output_filename = f'Recieved_report_WO_{identifier}.pdf'
            print(f'PDF report "{output_filename}" created successfully for WO = {identifier}.')
    
    output_path = os.path.join('generated_pdfs', output_filename)
    pdf.output(output_path)
    
    return output_filename
