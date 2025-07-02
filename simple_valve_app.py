from flask import Flask, render_template, request, send_file, send_from_directory
from openpyxl import load_workbook
import json
import os

app = Flask(__name__)

class MinimalExcelManager:
    def __init__(self, file_path='summary_project.xlsx'):
        self.file_path = file_path
        self.received_report_sheet = 'Received Report'  # Page 2
        self.vlookup_cell = 'T1'
    
    def get_available_reference_numbers(self):
        """Get reference numbers from extracted data"""
        try:
            with open('extracted_data.json', 'r') as f:
                data = json.load(f)
            
            # Get all "No" values (reference numbers)
            ref_numbers = []
            for record in data['data']:
                if record.get('No') and record['No'] != 'nan':
                    try:
                        ref_numbers.append(int(record['No']))
                    except:
                        pass
            
            return sorted(ref_numbers)
            
        except Exception as e:
            print(f"Error getting reference numbers: {e}")
            return []
    
    def set_reference_number(self, reference_number):
        """Set reference number in T1 cell - Excel VLOOKUP will handle the rest"""
        try:
            workbook = load_workbook(self.file_path)
            worksheet = workbook[self.received_report_sheet]
            
            # Set reference number in T1
            worksheet[self.vlookup_cell] = reference_number
            
            # Save workbook
            workbook.save(self.file_path)
            
            return True, f"Reference number {reference_number} set in {self.vlookup_cell}"
            
        except Exception as e:
            return False, f"Error setting reference number: {str(e)}"
    
    def get_client_info(self):
        """Get client info from D15, D16, D17"""
        try:
            workbook = load_workbook(self.file_path)
            worksheet = workbook[self.received_report_sheet]
            
            return {
                'client_name': worksheet['D15'].value,
                'project_name': worksheet['D16'].value,
                'location': worksheet['D17'].value
            }
            
        except Exception as e:
            print(f"Error getting client info: {e}")
            return {}
    
    def get_images(self):
        """Get images from specific cells"""
        try:
            workbook = load_workbook(self.file_path)
            worksheet = workbook[self.received_report_sheet]
            
            image_cells = {
                'A28': 'Receive Valve - Position A',
                'G28': 'Receive Valve - Position G', 
                'H28': 'Receive Valve - Position H',
                'F54': 'Detail - Inlet Connection',
                'F55': 'Detail - Defect Connection',
                'P54': 'Detail - Inlet Connection P',
                'P55': 'Detail - Inlet Connection P2'
            }
            
            images = []
            for cell_ref, caption in image_cells.items():
                cell = worksheet[cell_ref]
                if cell.value and hasattr(cell.value, 'image'):
                    # Save image to temp folder
                    temp_path = self.save_image_to_temp(cell.value.image, f"{cell_ref}.jpg")
                    if temp_path:
                        images.append({
                            'cell': cell_ref,
                            'caption': caption,
                            'path': temp_path
                        })
            
            return images
            
        except Exception as e:
            print(f"Error getting images: {e}")
            return []
    
    def save_image_to_temp(self, image_data, filename):
        """Save image to temp folder"""
        try:
            temp_dir = 'static/temp_images'
            os.makedirs(temp_dir, exist_ok=True)
            
            filepath = os.path.join(temp_dir, filename)
            
            if hasattr(image_data, 'read'):
                with open(filepath, 'wb') as f:
                    f.write(image_data.read())
            else:
                with open(filepath, 'wb') as f:
                    f.write(image_data)
            
            return filepath
            
        except Exception as e:
            print(f"Error saving image: {e}")
            return None

excel_manager = MinimalExcelManager()

@app.route('/')
def index():
    """Home page - select reference number"""
    ref_numbers = excel_manager.get_available_reference_numbers()
    return render_template('index.html', reference_numbers=ref_numbers)

@app.route('/valve/<int:reference_number>')
def view_valve(reference_number):
    """Set reference number and show valve info"""
    # Set reference number in T1
    success, message = excel_manager.set_reference_number(reference_number)
    
    if not success:
        return f"Error: {message}", 400
    
    # Get client info
    client_info = excel_manager.get_client_info()
    
    # Get images
    images = excel_manager.get_images()
    
    return render_template('valve.html', 
                         reference_number=reference_number,
                         client_info=client_info,
                         images=images,
                         message=message)

@app.route('/download_excel/<int:reference_number>')
def download_excel(reference_number):
    """Download Excel file with reference number set"""
    # Set reference number
    excel_manager.set_reference_number(reference_number)
    
    # Return Excel file
    return send_file(
        excel_manager.file_path,
        as_attachment=True,
        download_name=f"valve_report_{reference_number}.xlsx"
    )

if __name__ == '__main__':
    app.run(debug=True) 