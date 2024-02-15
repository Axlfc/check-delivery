# check-delivery

## PDF Data Extraction Script
###Overview
This Python script is designed to extract product information from PDF files (specifically invoices or delivery notes) and present it in a structured format. The data extracted includes product description, quantity, unit price, and total amount. The script uses the PyPDF2 library for reading PDF files and performs text processing to parse the required information.

### Current Status
The script is functional but has some limitations and unhandled cases which are currently being worked on. It successfully processes most of the standard-format lines but may encounter issues with non-standard or unexpected formats.

### Known Issues
- Handling of Multiple Line Products: The script may not correctly handle products described over multiple lines.
- Quantity and Price Parsing: In some cases, the script struggles to accurately extract quantity and price, especially when the line format varies significantly.
- Special Characters Handling: The script currently replaces commas with dots for processing, which might not be accurate for all data formats.
- Serial Numbers: The script does not yet gather serial numbers for products with multiple serial numbers.

### Next Steps
- Improve Line Parsing Logic: Refine the logic for parsing lines to better handle variations in product descriptions and formats.
- Robust Error Handling: Implement more robust error handling to manage and log unexpected formats or parsing issues.
- Enhance Data Formatting: Work on improving the formatting of the output for better readability and consistency.
- Testing with Varied Data: Test the script with a wider range of PDF files to identify and fix format-specific issues.

### Usage
To use the script, put the PDF file in a new directory named ```deliveries``` you want to process. The script will read the file, extract the product information, and display it in a formatted output.

Contributions
Suggestions and contributions for improving this script are welcome. Please feel free to submit issues or pull requests for enhancements.
