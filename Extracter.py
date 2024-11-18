#pip install pikepdf 
import pikepdf
import os
import sys

def extract_files_with_incremental_names(pdf_path, output_dir):
    try:
        pdf = pikepdf.Pdf.open(pdf_path)
        embedded_files = pdf.Root.get("/Names", {}).get("/EmbeddedFiles", {}).get("/Names", [])
        
        if len(embedded_files) == 0:
            print(f"No embedded files found in {pdf_path}.")
            return
        
        os.makedirs(output_dir, exist_ok=True)
        
        for i in range(0, len(embedded_files), 2):
            name = str(embedded_files[i]) 
            file_spec = embedded_files[i + 1]
            file_stream = file_spec["/EF"]["/F"]
            
            output_file_path = os.path.join(output_dir, f"{(i // 2) + 1}")
            
            with open(output_file_path, 'wb') as f:
                f.write(file_stream.read_bytes())
            
            print(f"File {i // 2 + 1} extracted successfully! Saved as: {output_file_path}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_files_with_incremental_names.py <PDF_File>")
    else:
        pdf_path = sys.argv[1]
        output_dir = "extractedFiles"
        
        extract_files_with_incremental_names(pdf_path, output_dir)
