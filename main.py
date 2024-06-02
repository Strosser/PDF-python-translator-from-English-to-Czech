import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
from ttkbootstrap import Style
from PyPDF2 import PdfReader
from googletrans import Translator
import os

def translate_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if not file_path:
        return

    try:
        reader = PdfReader(file_path)
        num_pages = len(reader.pages)

        translator = Translator()

        text_box.delete(1.0, tk.END)

        global translated_content
        translated_content = ""

        for p in range(num_pages):
            page = reader.pages[p]
            text = page.extract_text()

            if text is not None and text.strip() != "":
                try:
                    translated_text = translator.translate(text, src='en', dest='cs').text #here you can setup source and destination language

                    formatted_text = f"--- Page {p + 1} ---\n\n{translated_text}\n\n\n"
                    text_box.insert(tk.END, formatted_text)
                    translated_content += formatted_text

                except Exception as e:
                    error_text = f"Translation error on page {p + 1}: {e}\n\n\n"
                    text_box.insert(tk.END, error_text)
                    translated_content += error_text
            else:
                empty_text = f"Page {p + 1} is empty or could not extract text.\n\n\n"
                text_box.insert(tk.END, empty_text)
                translated_content += empty_text

            progress_bar['value'] += 1
            root.update_idletasks()

        progress_bar.pack_forget()

    except Exception as e:
        error_text = f"An error occurred: {e}\n\n\n"
        text_box.insert(tk.END, error_text)
        translated_content += error_text

def save_to_file():
    if not translated_content:
        messagebox.showwarning("Warning", "No translated content to save.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if not file_path:
        return

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(translated_content)
        messagebox.showinfo("Success", "Translated text saved successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving the file: {e}")

root = tk.Tk()
root.title("PDF Translator")

style = Style(theme='litera')

frame = ttk.Frame(root, padding="10")
frame.pack(fill=tk.BOTH, expand=True)

translate_button = ttk.Button(frame, text="Upload and Translate PDF", command=translate_pdf, style="TButton")
translate_button.pack(pady=10)

save_button = ttk.Button(frame, text="Save Translated Text to .txt", command=save_to_file, style="TButton")
save_button.pack(pady=10)

text_box = ScrolledText(frame, wrap=tk.WORD, width=100, height=30, font=("Helvetica", 14))
text_box.pack(pady=10, fill=tk.BOTH, expand=True)

progress_bar = ttk.Progressbar(frame, orient=tk.HORIZONTAL, mode='determinate')

translated_content = ""

root.mainloop()
