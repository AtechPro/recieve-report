# Valve Report Generator

A comprehensive web-based system for generating professional valve inspection and service reports with image support, Excel data integration, and PDF management.

## 🚀 Features

### **Core Functionality**
- **Web-based Interface**: Modern, responsive web application built with Flask
- **Dual Report Types**: Service Reports and Received Reports with different layouts
- **Excel Data Integration**: Upload Excel files or use existing extracted data
- **Professional PDF Generation**: Clean, structured reports with company branding
- **Image Management**: Upload, preview, and delete images with drag-and-drop support
- **PDF Management**: View, download, and delete generated PDFs

### **Advanced Features**
- **Multiple Image Support**: Upload up to 3 "AS RECEIVED VALVE" images + 4 detailed images
- **Service Options**: Select multiple service types (In-situ Testing, Service & Repair, Testing Only, Replace New Valve)
- **Custom Client Information**: Override default values with custom client data
- **Stamp System**: Add digital stamps with prepared by information and dates
- **Mobile Responsive**: Works seamlessly on desktop and mobile devices
- **Real-time Preview**: Image previews with delete functionality
- **Auto-cleanup**: Automatic cleanup of temporary files after PDF generation

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Modern web browser (Chrome, Firefox, Safari, Edge)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd valverec
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Prepare Data Files
Ensure you have the following files in your project directory:
- `extracted_data.json` (will be created when you upload Excel)
- `petronas.png` (company logo)
- `stamp/sao.png` (stamp image)

## 🚀 Quick Start

### 1. Start the Application
```bash
python recweb.py
```

### 2. Access the Web Interface
Open your browser and navigate to:
```
http://localhost:5300
```

### 3. Generate Your First Report
1. **Upload Excel Data**: Upload your valve data Excel file or use existing data
2. **Enter Work Order**: Search by Work Order (WO) number
3. **Upload Images**: Add valve images (optional)
4. **Customize Information**: Modify client details if needed
5. **Generate PDF**: Click "Generate PDF" to create your report

## 📊 Report Types

### Service Report (`servicerep.py`)
- **Visual Inspection**: Internal parts inspection table
- **Internal Inspection**: Detailed component inspection
- **Service Options**: Multiple service type selections
- **Professional Layout**: Clean, structured format

### Received Report (`recievedreport.py`)
- **Transportation Details**: Transport mode, packaging, received by
- **Valve Condition**: Overall condition assessment
- **Detailed Pictures**: 4-image grid layout
- **AS Received Images**: Up to 3 valve condition images

## 🖼️ Image Management

### Supported Image Types
- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)

### Image Features
- **Drag & Drop**: Easy image upload
- **Real-time Preview**: See images before PDF generation
- **Delete Functionality**: Remove uploaded images with red × button
- **Mobile Camera**: Take photos directly on mobile devices
- **Auto-cleanup**: Temporary images removed after PDF generation

### Image Categories
1. **AS RECEIVED VALVE Images** (up to 3)
   - Overall valve condition photos
   - Before-service documentation

2. **Detailed Images** (4 specific types)
   - Inlet Connection
   - Outlet Connection
   - Defect Connection (if any)
   - Defect on Body (if any)

## 📁 File Management

### Generated PDFs
- **View**: Open PDFs directly in browser
- **Download**: Download PDFs to your device
- **Delete**: Remove unwanted PDFs with confirmation
- **List**: Browse all generated reports

### Data Files
- **Excel Upload**: Upload new valve data
- **Existing Data**: Use previously extracted data
- **Auto-extraction**: Excel data automatically converted to JSON

## 🎨 Customization

### Client Information
Customize the following fields:
- Client Name
- Project Name
- Location
- Date In
- Transport Mode
- Transport By
- Packaging
- Received By
- Inlet/Outlet Types
- Connection Conditions
- Valve Body Condition
- Overall Valve Condition

### Service Options
Select multiple service types:
- ✅ In-situ Testing
- ✅ Service & Repair
- ✅ Testing Only
- ✅ Replace New Valve

### Stamp System
- **Digital Stamps**: Add prepared by information
- **Date Stamps**: Include generation dates
- **Customizable**: Modify stamp details

## 🔧 Configuration

### Environment Variables
Create a `.env` file for custom configuration:
```env
FLASK_ENV=development
UPLOAD_FOLDER=static/temp_images
PDF_FOLDER=generated_pdfs
```

### File Structure
```
valverec/
├── recweb.py                 # Main Flask application
├── servicerep.py            # Service report generator
├── recievedreport.py        # Received report generator
├── extract_excel_to_json.py # Excel data extractor
├── templates/
│   └── index.html           # Web interface
├── static/
│   ├── temp_images/         # Temporary uploaded images
│   └── temp_excel/          # Temporary Excel files
├── generated_pdfs/          # Generated PDF reports
├── stamp/                   # Stamp images
└── requirements.txt         # Python dependencies
```

## 🐳 Docker Support

### Build and Run with Docker
```bash
# Build the Docker image
docker build -t valve-report-generator .

# Run the container
docker run -p 5300:5300 valve-report-generator
```

## 📱 Mobile Support

### Mobile Features
- **Responsive Design**: Optimized for mobile screens
- **Touch-friendly**: Large buttons and touch targets
- **Camera Integration**: Take photos directly with device camera
- **Mobile Upload**: Easy file selection on mobile devices

### Mobile Workflow
1. Open web app on mobile browser
2. Upload Excel data or use existing
3. Enter Work Order number
4. Tap image fields to take photos
5. Generate PDF report
6. Download or view generated report

## 🔍 API Endpoints

### Core Endpoints
- `GET /` - Main web interface
- `POST /upload-excel` - Upload Excel data
- `POST /upload-image` - Upload valve images
- `POST /generate` - Generate PDF report
- `GET /list-pdfs` - List generated PDFs
- `GET /download-pdf/<filename>` - Download PDF
- `GET /view-pdf/<filename>` - View PDF in browser
- `DELETE /delete-pdf/<filename>` - Delete PDF
- `POST /cleanup-temp` - Clean temporary files

### Data Endpoints
- `GET /available-no` - Get available Work Order numbers

## 🛡️ Security Features

### File Upload Security
- **File Type Validation**: Only allowed image types
- **Secure Filenames**: Prevents path traversal attacks
- **Size Limits**: Prevents large file uploads
- **Auto-cleanup**: Temporary files automatically removed

### PDF Management Security
- **Filename Validation**: Prevents directory traversal
- **Confirmation Dialogs**: Prevents accidental deletions
- **Error Handling**: Graceful error management

## 🐛 Troubleshooting

### Common Issues

**1. Port Already in Use**
```bash
# Change port in recweb.py
app.run(debug=True, port=5301, host='0.0.0.0')
```

**2. Missing Dependencies**
```bash
pip install -r requirements.txt
```

**3. Excel Upload Fails**
- Ensure Excel file is .xlsx or .xls format
- Check file is not corrupted
- Verify file permissions

**4. Image Upload Issues**
- Check image format (JPG, PNG, GIF)
- Ensure image file is not corrupted
- Verify file size is reasonable

**5. PDF Generation Errors**
- Check Work Order number exists in data
- Verify all required fields are filled
- Check server logs for detailed errors

### Debug Mode
Enable debug mode for detailed error messages:
```python
app.run(debug=True, port=5300, host='0.0.0.0')
```

## 📈 Performance Tips

### Optimization
- **Image Compression**: Compress images before upload
- **Batch Processing**: Generate multiple reports efficiently
- **Cleanup**: Regularly clean temporary files
- **Browser Cache**: Clear browser cache if issues occur

### Best Practices
- **Regular Backups**: Backup generated PDFs
- **Data Validation**: Verify Excel data before upload
- **Image Quality**: Use high-quality images for better reports
- **File Management**: Regularly delete old PDFs

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Style
- Follow PEP 8 Python style guide
- Add comments for complex logic
- Include error handling
- Write descriptive commit messages

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Getting Help
- **Documentation**: Check this README first
- **Issues**: Report bugs via GitHub Issues
- **Questions**: Ask questions in GitHub Discussions

### Contact
For support or questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the code comments

## 🔄 Version History

### v2.0.0 (Current)
- ✅ Web-based interface
- ✅ Image upload and management
- ✅ PDF generation and management
- ✅ Excel data integration
- ✅ Mobile responsive design
- ✅ Delete functionality for images and PDFs
- ✅ Professional report layouts

### v1.0.0
- ✅ Basic PDF generation
- ✅ Simple report templates
- ✅ Image support

---

**Made with ❤️ for professional valve inspection reporting** 