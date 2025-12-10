from gtts import gTTS
from PyPDF2 import PdfReader
def pdf_to_text (pdf_file):
    text=""
    with open(pdf_file,'rb') as f:
        reader=PdfReader(f)
        for page_num in range(len(reader.pages)):
            page=reader.pages[page_num]
            text += page.extract_text()
    return text
pdf_file="./the lump of gold.pdf"
output_audio_file="./outputfile.mp3"
def text_to_audio(text,output_file):
    tts=gTTS(text)
    tts.save(output_audio_file)
text=pdf_to_text(pdf_file)

text_to_audio(text,output_audio_file)
print("Conversion complete. Audio saved to",output_audio_file)