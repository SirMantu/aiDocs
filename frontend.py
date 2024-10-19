import tkinter as tk
import json
from datetime import datetime
from tkinter import filedialog

# Funktion zum Speichern der Daten
def save_data():
    vorname = vorname_entry.get()
    nachname = nachname_entry.get()
    
    if not vorname or not nachname:
        print("Vorname und Nachname müssen angegeben werden.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{vorname}_{nachname}_{timestamp}.json"
    
    data = {
        "vorname": vorname,
        "nachname": nachname,
        "geschlecht": geschlecht_var.get(),
        "arzt": arzt_entry.get(),
        "notizen": text_box.get("1.0", tk.END),
        "diagnose": diagnose_box.get("1.0", tk.END),
        "arztbrief": arztbrief_box.get("1.0", tk.END),
        "chatgpt_ausgabe": chatgpt_box.get("1.0", tk.END)
    }
    
    with open(filename, 'w') as file:
        json.dump(data, file)
    print(f"Daten gespeichert in: {filename}")

# Funktion zum Laden der Daten
def load_data():
    file_path = filedialog.askopenfilename(
        title="Wähle eine Datei aus",
        filetypes=[("JSON Dateien", "*.json")]
    )
    
    if not file_path:
        return

    with open(file_path, 'r') as file:
        data = json.load(file)
        vorname_entry.delete(0, tk.END)
        vorname_entry.insert(0, data.get("vorname", ""))
        nachname_entry.delete(0, tk.END)
        nachname_entry.insert(0, data.get("nachname", ""))
        geschlecht_var.set(data.get("geschlecht", "Frau"))
        arzt_entry.delete(0, tk.END)
        arzt_entry.insert(0, data.get("arzt", ""))
        text_box.delete("1.0", tk.END)
        text_box.insert("1.0", data.get("notizen", ""))
        diagnose_box.delete("1.0", tk.END)
        diagnose_box.insert("1.0", data.get("diagnose", "Diagnose Notizen hier einfügen"))
        diagnose_box.config(fg="grey")  # Setze graue Schrift für Diagnose-Box
        chatgpt_box.delete("1.0", tk.END)
        chatgpt_box.insert("1.0", data.get("chatgpt_ausgabe", "Ausgabe von ChatGPD"))
        chatgpt_box.config(fg="grey")  # Setze graue Schrift für ChatGPT-Box

# Funktion, um Platzhaltertext bei Fokus zu entfernen
def on_focus_in(event, widget, default_text):
    if widget.get("1.0", tk.END).strip() == default_text:
        widget.delete("1.0", tk.END)
        widget.config(fg="black")

# Funktion, um Platzhaltertext bei Fokusverlust wieder einzufügen
def on_focus_out(event, widget, default_text):
    if not widget.get("1.0", tk.END).strip():
        widget.insert("1.0", default_text)
        widget.config(fg="grey")

# Funktion, um die Diagnoseinformationen zu sammeln und in die ChatGPT-Box zu schreiben
def collect_input_for_diagnosis():
    # Texte aus den Textboxen sammeln
    arztbrief_text = arztbrief_box.get("1.0", tk.END).strip()
    diagnose_text = diagnose_box.get("1.0", tk.END).strip()
    
    # Vorname, Nachname und Geschlecht sammeln
    vorname = vorname_entry.get().strip()
    nachname = nachname_entry.get().strip()
    geschlecht = geschlecht_var.get()
    
    # Behandelnder Arzt sammeln
    arzt_name = arzt_entry.get().strip()

    # String für die Diagnose zusammensetzen
    diagnose_info = (
        f"{arztbrief_text}\n\n{diagnose_text}\n\n"
        f"Informationen über den Patient:\n"
        f"Geschlecht: {geschlecht}\n"
        f"Vorname: {vorname}\n"
        f"Nachname: {nachname}\n\n"
        f"Behandelnder Arzt: {arzt_name}"
    )
    
    # Den zusammengesetzten Text in die chatgpt_box schreiben
    chatgpt_box.delete("1.0", tk.END)  # Vorherigen Text löschen
    chatgpt_box.insert("1.0", diagnose_info)
    chatgpt_box.config(fg="black")  # Textfarbe schwarz setzen, falls es vorher grau war
    print(diagnose_info)  # Optional: Zur Kontrolle in der Konsole ausgeben

# Hauptfenster erstellen
root = tk.Tk()
root.title("Patienteninformation")

# Textbox für Arztbrief
arztbrief_box = tk.Text(root, height=5, width=80)
arztbrief_box.grid(row=0, column=0, columnspan=2)
arztbrief_box.insert("1.0", "Schreibe einen Arztbrief mit den folgenden Diagnose Notizen")

# Textbox für Notizen
text_box = tk.Text(root, height=10, width=80)
text_box.grid(row=1, column=0, columnspan=2)

# Textbox für Diagnose mit grauem Platzhaltertext
diagnose_box = tk.Text(root, height=10, width=80, fg="grey")
diagnose_box.grid(row=2, column=0, columnspan=2)
diagnose_box.insert("1.0", "Diagnose Notizen hier einfügen")
diagnose_box.bind("<FocusIn>", lambda event: on_focus_in(event, diagnose_box, "Diagnose Notizen hier einfügen"))
diagnose_box.bind("<FocusOut>", lambda event: on_focus_out(event, diagnose_box, "Diagnose Notizen hier einfügen"))

# Textbox für ChatGPT-Ausgabe mit grauem Platzhaltertext
chatgpt_box = tk.Text(root, height=5, width=80, fg="grey")
chatgpt_box.grid(row=3, column=0, columnspan=2)
chatgpt_box.insert("1.0", "Ausgabe von ChatGPD")
chatgpt_box.bind("<FocusIn>", lambda event: on_focus_in(event, chatgpt_box, "Ausgabe von ChatGPD"))
chatgpt_box.bind("<FocusOut>", lambda event: on_focus_out(event, chatgpt_box, "Ausgabe von ChatGPD"))

# Vorname
tk.Label(root, text="Vorname").grid(row=4, column=0)
vorname_entry = tk.Entry(root)
vorname_entry.grid(row=4, column=0, columnspan=2)

# Nachname
tk.Label(root, text="Nachname").grid(row=5, column=0)
nachname_entry = tk.Entry(root)
nachname_entry.grid(row=5, column=0, columnspan=2)

# Geschlecht
tk.Label(root, text="Geschlecht").grid(row=6, column=0)
geschlecht_var = tk.StringVar(value="Frau")
tk.Radiobutton(root, text="Frau", variable=geschlecht_var, value="Frau").grid(row=6, column=1, padx=10)
tk.Radiobutton(root, text="Mann", variable=geschlecht_var, value="Mann").grid(row=6, column=2, padx=10)
tk.Radiobutton(root, text="Divers", variable=geschlecht_var, value="Divers").grid(row=6, column=3, padx=10)

# Behandelnder Arzt
tk.Label(root, text="Behandelnder Arzt").grid(row=7, column=0)
arzt_entry = tk.Entry(root)
arzt_entry.grid(row=7, column=0, columnspan=2)

# Speichern-Button
save_button = tk.Button(root, text="Daten speichern", command=save_data)
save_button.grid(row=8, column=0)

# Laden-Button
load_button = tk.Button(root, text="Daten laden", command=load_data)
load_button.grid(row=8, column=1)

# Diagnose-Button
diagnose_button = tk.Button(root, text="Diagnose", command=collect_input_for_diagnosis)
diagnose_button.grid(row=8, column=2)

# Hauptschleife starten
root.mainloop()
