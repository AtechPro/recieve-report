from recievedreport import generate_pdf

if __name__ == "__main__":
    # Test function to generate PDF with all available PNG images
    def test_pdf_generation():
        """Test PDF generation with all available PNG images"""
        import glob
        
        # Find all PNG images in the current directory and subdirectories
        png_files = glob.glob("*.png") + glob.glob("**/*.png", recursive=True)
        
        print(f"Found {len(png_files)} PNG files:")
        for png_file in png_files:
            print(f"  - {png_file}")
        
        # Create test image mappings
        image_files = {}
        received_valve_images = []
        
        # Map specific images to their positions if they exist
        if 'goodvalve.png' in png_files:
            image_files['inlet_connection'] = 'goodvalve.png'
        if 'badvalve.png' in png_files:
            image_files['outlet_connection'] = 'badvalve.png'
        if 'image.png' in png_files:
            image_files['defect_connection'] = 'image.png'
        if 'petronas.png' in png_files:
            # petronas.png is used in header, not in detailed pictures
            pass
        
        # Add all PNG files as received valve images (up to 3)
        for i, png_file in enumerate(png_files[:3]):
            if png_file not in ['petronas.png', 'stamp/sao.png']:  # Exclude header and stamp images
                received_valve_images.append(png_file)
        
        print(f"\nUsing {len(image_files)} images for detailed pictures:")
        for key, value in image_files.items():
            print(f"  - {key}: {value}")
        
        print(f"\nUsing {len(received_valve_images)} images for received valve condition:")
        for img in received_valve_images:
            print(f"  - {img}")
        
        # Test with a sample identifier (you can change this)
        test_identifier = "1"  # Try with No = 1
        
        try:
            # Generate the PDF
            output_filename = generate_pdf(
                identifier=test_identifier,
                user_data=None,  # Use default user data
                image_files=image_files,
                received_valve_images=received_valve_images,
                stamp_selection='SAO',  # Use SAO stamp
                date_value='7/7/2027'  # Use test date
            )
            
            print(f"\n✅ PDF generated successfully: {output_filename}")
            print(f"📁 Check the 'generated_pdfs' folder for the output file")
            
        except Exception as e:
            print(f"\n❌ Error generating PDF: {e}")
            print("Make sure you have:")
            print("1. extracted_data.json file with valve records")
            print("2. PNG images in the current directory")
            print("3. All required dependencies installed")
    
    # Run the test
    test_pdf_generation()