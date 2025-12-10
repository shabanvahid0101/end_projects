from textblob import TextBlob
try:
    text=input("please insert text:")
    blob = TextBlob(text)
    corrected_blob=blob.correct()
except Exception as e:
    print(f"An error occurred: {e}")

print(f"this is first text: {text}\n")
print(f"this is later corrected text: {corrected_blob}")