import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

def readCSV(filepath):
    df = pd.read_csv(filepath, delimiter=';', dtype=str)  # Alle Spalten als Strings lesen
    return df

def filterCSV(df, filters):
    # Nur Filter anwenden, die sowohl eine Spalte als auch einen Wert haben
    filters = {col: val for col, val in filters.items() if col and val}
    
    if not filters:
        return pd.DataFrame()  # Leeres DataFrame zurückgeben, wenn keine gültigen Filter vorhanden sind
    
    condition = pd.Series([True] * len(df))
    for column, value in filters.items():
        condition &= df[column].str.lower() == value.lower()
        
    filteredDF = df[condition]
    selectDF = filteredDF[['Vorname']]
    return selectDF

def saveCSV(df, filepath):
    df.to_csv(filepath, index=False)

def open_file_dialog():
    filepath = filedialog.askopenfilename()
    if filepath:
        entry_filepath.delete(0, tk.END)
        entry_filepath.insert(0, filepath)

def save_file_dialog():
    filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if filepath:
        return filepath
    return None

def filter_and_save():
    filepath = entry_filepath.get()
    filters = {
        entry_column1.get(): entry_value1.get(),
        entry_column2.get(): entry_value2.get(),
        entry_column3.get(): entry_value3.get()
    }

    if not filepath:
        messagebox.showwarning("Eingabefehler", "Bitte eine CSV-Datei auswählen")
        return

    if not any(filters.values()):
        messagebox.showwarning("Eingabefehler", "Bitte mindestens einen Wert für die Filterung angeben")
        return

    try:
        df = readCSV(filepath)
    except Exception as e:
        messagebox.showerror("Fehler beim Lesen der Datei", str(e))
        return

    try:
        result_df = filterCSV(df, filters)
        if result_df.empty:
            messagebox.showinfo("Keine Ergebnisse", "Es wurden keine übereinstimmenden Datensätze gefunden.")
            return
    except KeyError as e:
        messagebox.showerror("Fehler", f"Spalte '{e.args[0]}' nicht gefunden")
        return

    save_path = save_file_dialog()
    if save_path:
        try:
            saveCSV(result_df, save_path)
            messagebox.showinfo("Erfolg", f"Gefilterte Daten erfolgreich in '{save_path}' gespeichert")
        except Exception as e:
            messagebox.showerror("Fehler beim Speichern der Datei", str(e))

# GUI erstellen
root = tk.Tk()
root.title("CSV-Filter")

# Dateiauswahl
label_filepath = tk.Label(root, text="CSV-Datei:")
label_filepath.grid(row=0, column=0, padx=10, pady=10)
entry_filepath = tk.Entry(root, width=50)
entry_filepath.grid(row=0, column=1, padx=10, pady=10)
button_browse = tk.Button(root, text="Durchsuchen", command=open_file_dialog)
button_browse.grid(row=0, column=2, padx=10, pady=10)

# Spalte 1
label_column1 = tk.Label(root, text="Spalte 1:")
label_column1.grid(row=1, column=0, padx=10, pady=10)
entry_column1 = tk.Entry(root, width=50)
entry_column1.grid(row=1, column=1, padx=10, pady=10)

# Wert 1
label_value1 = tk.Label(root, text="Wert 1:")
label_value1.grid(row=2, column=0, padx=10, pady=10)
entry_value1 = tk.Entry(root, width=50)
entry_value1.grid(row=2, column=1, padx=10, pady=10)

# Spalte 2
label_column2 = tk.Label(root, text="Spalte 2:")
label_column2.grid(row=3, column=0, padx=10, pady=10)
entry_column2 = tk.Entry(root, width=50)
entry_column2.grid(row=3, column=1, padx=10, pady=10)

# Wert 2
label_value2 = tk.Label(root, text="Wert 2:")
label_value2.grid(row=4, column=0, padx=10, pady=10)
entry_value2 = tk.Entry(root, width=50)
entry_value2.grid(row=4, column=1, padx=10, pady=10)

# Spalte 3
label_column3 = tk.Label(root, text="Spalte 3:")
label_column3.grid(row=5, column=0, padx=10, pady=10)
entry_column3 = tk.Entry(root, width=50)
entry_column3.grid(row=5, column=1, padx=10, pady=10)

# Wert 3
label_value3 = tk.Label(root, text="Wert 3:")
label_value3.grid(row=6, column=0, padx=10, pady=10)
entry_value3 = tk.Entry(root, width=50)
entry_value3.grid(row=6, column=1, padx=10, pady=10)

# Filter- und Speichern-Button
button_filter = tk.Button(root, text="Filtern und Speichern", command=filter_and_save)
button_filter.grid(row=7, column=0, columnspan=3, pady=20)

root.mainloop()
