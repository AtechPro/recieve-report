import servicerep

if __name__ == "__main__":
    # Example identifier (replace with a valid No or WO from your extracted_data.json)
    identifier = "1"  # Change as needed
    # Optionally, you can provide user_data, image_files, received_valve_images, stamp_selection, date_value, selected_services
    try:
        output_filename = servicerep.generate_pdf(
            identifier=identifier,
            user_data=None,
            image_files=None,
            received_valve_images=None,
            stamp_selection="SAO",
            date_value="01/01/2025",
            selected_services=["insitu_testing", "service_repair"]
        )
        print(f"Test PDF generated: {output_filename}")
    except Exception as e:
        print(f"Test failed: {e}") 