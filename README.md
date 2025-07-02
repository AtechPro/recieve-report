# Valve Report PDF Template

A comprehensive FPDF template for generating professional valve inspection reports with image support.

## Features

- **Professional Layout**: Clean, structured PDF reports with headers and footers
- **Image Support**: Add single images or multiple images in grid layouts
- **Cover Pages**: Professional cover pages with titles and dates
- **Data Tables**: Structured tables for valve information and inspection results
- **Recommendations Section**: Numbered list for recommendations
- **Signature Section**: Professional signature area for inspectors
- **Auto-scaling Images**: Images automatically scale to fit page dimensions
- **Multiple Image Layouts**: Support for single images and grid layouts

## Installation

The template uses the following dependencies (already in your `requirements.txt`):

```bash
fpdf2==2.8.3
Pillow
```

## Quick Start

### Basic Usage

```python
from valvereport import ValveReportPDF

# Create a new PDF
pdf = ValveReportPDF()

# Add cover page
pdf.add_cover_page(
    title="Valve Inspection Report",
    subtitle="Valve #V-001",
    date="December 15, 2024"
)

# Add valve information
valve_data = {
    "Valve ID": "V-001",
    "Type": "Gate Valve",
    "Size": "8 inch",
    "Material": "Carbon Steel"
}
pdf.add_valve_info_section(valve_data)

# Save the PDF
pdf.output("my_report.pdf")
```

### Adding Images

```python
# Add a single image with caption
pdf.add_image_section("valve_photo.jpg", "Front view of valve V-001")

# Add multiple images in a grid
image_paths = ["valve1.jpg", "valve2.jpg", "valve3.jpg"]
captions = ["Front view", "Side view", "Internal components"]
pdf.add_multiple_images(image_paths, captions)
```

## Template Methods

### Core Methods

- `add_cover_page(title, subtitle, date)`: Add a professional cover page
- `add_valve_info_section(valve_data)`: Add valve information in a table format
- `add_inspection_results(results_data)`: Add inspection results in a table
- `add_recommendations(recommendations)`: Add numbered recommendations
- `add_signature_section(inspector_name, date)`: Add signature section

### Image Methods

- `add_image_section(image_path, caption, max_width, max_height)`: Add single image
- `add_multiple_images(image_paths, captions, images_per_row)`: Add multiple images in grid

## Example Reports

Run the example script to see the template in action:

```bash
python example_usage.py
```

This will generate:
- `basic_valve_report.pdf`: Basic report without images
- `valve_report_with_images.pdf`: Report with sample data
- `image_demo_report.pdf`: Demonstration of image features

## Data Formats

### Valve Data Dictionary
```python
valve_data = {
    "Valve ID": "V-001",
    "Type": "Gate Valve",
    "Size": "8 inch",
    "Material": "Carbon Steel",
    "Location": "Pump Station A",
    "Installation Date": "2020-03-15",
    "Last Inspection": "2023-06-20"
}
```

### Inspection Results List
```python
results_data = [
    {
        "test_type": "Visual Inspection",
        "result": "Pass",
        "status": "Good",
        "notes": "No visible damage"
    },
    {
        "test_type": "Pressure Test",
        "result": "Pass",
        "status": "Good",
        "notes": "Holds 150 PSI"
    }
]
```

### Recommendations List
```python
recommendations = [
    "Continue regular maintenance schedule",
    "Monitor for any signs of wear or corrosion",
    "Schedule next inspection within 12 months"
]
```

## Image Support

### Supported Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- BMP (.bmp)
- TIFF (.tiff)

### Image Features
- **Auto-scaling**: Images automatically scale to fit page dimensions
- **Centering**: Single images are centered on the page
- **Grid Layout**: Multiple images arranged in configurable grid
- **Captions**: Optional captions for each image
- **Page Breaks**: Automatic page breaks for multiple images

### Image Sizing
- **Single Images**: Maximum 180x200 mm (configurable)
- **Grid Images**: Automatically sized for grid layout
- **Aspect Ratio**: Maintains original aspect ratio

## Customization

### Fonts and Styling
The template uses Arial font family with different sizes:
- Title: 24pt Bold
- Section Headers: 14pt Bold
- Table Headers: 10pt Bold
- Body Text: 10pt Regular
- Captions: 10pt Italic

### Page Layout
- **Page Size**: A4 (210x297 mm)
- **Margins**: 15mm auto page break
- **Headers**: "Valve Inspection Report" on each page
- **Footers**: Page numbers

### Colors
- **Text**: Black
- **Tables**: Black borders
- **Lines**: Black signature lines

## Advanced Usage

### Custom Page Headers
```python
class CustomValveReportPDF(ValveReportPDF):
    def header(self):
        # Custom header implementation
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Custom Valve Report', 0, 1, 'C')
```

### Adding Custom Sections
```python
def add_custom_section(self, title, content):
    self.add_page()
    self.set_font('Arial', 'B', 14)
    self.cell(0, 10, title, 0, 1, 'L')
    self.ln(5)
    
    self.set_font('Arial', '', 11)
    self.multi_cell(0, 8, content)
```

## Troubleshooting

### Common Issues

1. **Image not found**: Ensure image path is correct and file exists
2. **Font issues**: Arial font should be available on most systems
3. **Page breaks**: Adjust `max_width` and `max_height` for better image placement
4. **Memory issues**: For large images, consider resizing before adding to PDF

### Error Handling
The template includes error handling for:
- Missing image files
- Invalid image formats
- File permission issues

## License

This template is provided as-is for valve inspection reporting purposes.

## Support

For issues or questions about the template, check the example usage and ensure all dependencies are properly installed. 