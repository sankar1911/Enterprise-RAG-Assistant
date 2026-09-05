def create_chunks(pages, file_name):
    chunks = []
    chunk_id = 0
    for page in pages:
        page_number = page["page_number"]
        text = page["text"]
        paragraphs = [paragraph.strip().replace("\n", " ")
            for paragraph in text.split("\n\n")if paragraph.strip()]
        
        for paragraph in paragraphs:
            if page_number == 1:
                department = "hr"
            elif page_number == 2:
                department = "security"
            else:
                department = "it"
            chunk = {
                "chunk_id": chunk_id,
                "text": paragraph,
                "file_name": file_name,
                "page_number": page_number,
                "department": department
            }
            chunks.append(chunk)
            chunk_id += 1
    return chunks