import sys
import pikepdf

def embed_file_in_pdf(pdf_path, file_to_embed, embedded_file_name):
    try:
        pdf = pikepdf.Pdf.open(pdf_path)
    
        with open(file_to_embed, 'rb') as f:
            file_data = f.read()
        
        embedded_file = pdf.make_stream(file_data)
        embedded_file["/Type"] = "/EmbeddedFile"
        
        filespec = pikepdf.Dictionary({
            "/Type": "/Filespec",
            "/F": embedded_file_name,
            "/EF": pikepdf.Dictionary({
                "/F": embedded_file
            })
        })
        
        if "/Names" not in pdf.Root:
            pdf.Root["/Names"] = pikepdf.Dictionary()
        
        if "/EmbeddedFiles" not in pdf.Root["/Names"]:
            pdf.Root["/Names"]["/EmbeddedFiles"] = pikepdf.Dictionary({
                "/Names": pikepdf.Array()
            })
        
        embedded_files = pdf.Root["/Names"]["/EmbeddedFiles"]["/Names"]
        embedded_files.append(pikepdf.String(embedded_file_name))
        embedded_files.append(filespec) 
        
        output_path = f"embedded_{pdf_path}"
        pdf.save(output_path)
        print(f"File successfully embedded! Output saved as: {output_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python embed_file_in_pdf.py <PDF_File> <File_to_Embed> <Embedded_File_Name>")
    else:
        pdf_path = sys.argv[1]
        file_to_embed = sys.argv[2]
        embedded_file_name = sys.argv[3]
        embed_file_in_pdf(pdf_path, file_to_embed, embedded_file_name)
