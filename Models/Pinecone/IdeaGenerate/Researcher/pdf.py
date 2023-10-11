import PyPDF2
import json

def extract_paragraphs_from_pdf(pdf_file):
    """
    [
        {
            "id":id,
            "content": content,
            "page_number" page_number
        }
    ]
    """
    paragraphs = []
    try:
        with open(pdf_file, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)

            for page_number in range(num_pages):
                page = pdf_reader.pages[page_number]
                content = page.extract_text()
                content = content.replace('\n', ' ')  # Replace newlines with spaces

                # Split the content into paragraphs based on double line breaks
                raw_paragraphs = content.split('\n\n')

                # Create a dictionary for each paragraph and add it to the list
                for paragraph_id, raw_paragraph in enumerate(raw_paragraphs):
                    paragraph = {
                        'id': paragraph_id + 1,  # Add 1 to start the IDs from 1
                        'content': raw_paragraph.strip(),  # Remove leading/trailing whitespace
                        'page_number': page_number + 1  # Add 1 to start the page numbers from 1
                    }
                    paragraphs.append(paragraph)
        

        return paragraphs
    except Exception as e:
        print(e)
        return paragraphs

# # Example usage:
# pdf_file_path = 'example.pdf'
# result = extract_paragraphs_from_pdf(pdf_file_path)

# # Save the result as JSON
# json_file_path = 'pdf-result.json'
# with open(json_file_path, 'w') as json_file:
#     json.dump(result, json_file)

# print("JSON file saved successfully.")
