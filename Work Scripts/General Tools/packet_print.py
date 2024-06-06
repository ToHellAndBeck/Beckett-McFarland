import os
import comtypes.client

def print_word_file(file_path):
    try:
        word = comtypes.client.CreateObject("Word.Application")
        word.Visible = False

        doc = word.Documents.Open(os.path.abspath(file_path), Visible=False)
        doc.PrintOut()

        doc.Close(False)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        word.Quit()



if __name__ == "__main__":
    file_path = r"C:\Users\beckett.mcfarland\Documents\Cable Label Packet Master (Personal).docx"  # Replace with the path to your Word document
    print_word_file(file_path)
