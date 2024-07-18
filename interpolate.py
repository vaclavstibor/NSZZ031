import fitz  # PyMuPDF

def set_interpolate_false(pdf_path, output_path):
    # Open the PDF
    doc = fitz.open(pdf_path)
    
    # Iterate through pages
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        # Iterate through images
        image_list = page.get_images(full=True)
        for img_index, img_info in enumerate(image_list):
            xref = img_info[0]
            # Get the image dictionary
            img_dict = doc.xref_get_key(xref, 'dict')
            # Modify the 'Interpolate' key
            if "/Interpolate" in img_dict:
                doc.xref_set_key(xref, "Interpolate", "false")
    
    # Save the modified PDF
    doc.save(output_path)
    doc.close()

# Example usage
input_pdf = "/Users/stiborv/Documents/2324/ZS2324/NPRG045/better-thesis-master/img/semi-supervised-1.pdf"
output_pdf = "/Users/stiborv/Documents/2324/ZS2324/NPRG045/better-thesis-master/img/semi-supervised-2.pdf"
set_interpolate_false(input_pdf, output_pdf)
