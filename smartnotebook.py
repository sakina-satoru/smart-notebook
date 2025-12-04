import os
import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext

# --- Setup folders ---
NOTES_DIR = "notes"
os.makedirs(NOTES_DIR, exist_ok=True)

# --- Main App ---
class SmartNotebook:
    def __init__(self, root):
        self.root = root
        root.title("Smart Notebook ✨")
        root.geometry("700x700")

        # Gradient background
        self.canvas = tk.Canvas(root, width=700, height=700)
        self.canvas.pack(fill="both", expand=True)
        self.draw_gradient("#ffcfcf", "white")

        # Header
        self.canvas.create_text(350, 60, text="Smart Notebook", font=("Segoe UI", 28, "bold"), fill="#ff496c")
        self.canvas.create_text(600, 680, text="made by Sakina", font=("Segoe UI", 12, "italic"), fill="#ff7290")

        # Buttons
        btn_y = 150
        btn_gap = 60

        self.add_btn("Add Note", self.add_note, btn_y)
        self.add_btn("Edit Notes", self.edit_notes, btn_y + btn_gap)
        self.add_btn("Delete Note", self.delete_note, btn_y + 2*btn_gap)
        self.add_btn("Today's Notes", self.show_today_notes, btn_y + 3*btn_gap)
        self.add_btn("Search Notes", self.search_notes, btn_y + 4*btn_gap)
        self.add_btn("Stats", self.show_stats, btn_y + 5*btn_gap)
        self.add_btn("Export All", self.export_all_notes, btn_y + 6*btn_gap)
        self.add_btn("Exit", root.quit, btn_y + 7*btn_gap)

    def add_btn(self, text, command, y):
        b = tk.Button(self.root, text=text, command=command,
                      font=("Segoe UI", 14, "bold"), bg="white", fg="#ff4b6e",
                      width=20)
        self.canvas.create_window(350, y, window=b)

    def draw_gradient(self, color1, color2):
        for i in range(700):
            ratio = i / 700
            r1, g1, b1 = self.hex_to_rgb(color1)
            r2, g2, b2 = self.hex_to_rgb(color2)
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.canvas.create_line(0, i, 700, i, fill=color)

    def hex_to_rgb(self, hex_code):
        hex_code = hex_code.lstrip('#')
        return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

    # --- Features ---
    def add_note(self):
        note = simpledialog.askstring("New Note", "Write your note:")
        if not note:
            return

        today = datetime.date.today().isoformat()
        file_path = os.path.join(NOTES_DIR, f"{today}_notes.txt")

        with open(file_path, "a", encoding="utf-8") as f:
            f.write(note + "\n")

        messagebox.showinfo("Saved", f"Note saved to {today}_notes.txt ✨")

    def edit_notes(self):
        today = datetime.date.today().isoformat()
        file_path = os.path.join(NOTES_DIR, f"{today}_notes.txt")

        if not os.path.exists(file_path):
            messagebox.showinfo("None", "No notes today yet!")
            return

        editor = tk.Toplevel(self.root)
        editor.title("Edit Today's Notes")
        editor.geometry("600x500")

        text_area = scrolledtext.ScrolledText(editor, font=("Segoe UI", 12))
        text_area.pack(fill="both", expand=True)

        with open(file_path, "r", encoding="utf-8") as f:
            text_area.insert("1.0", f.read())

        def save():
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text_area.get("1.0", "end"))
            editor.destroy()
            messagebox.showinfo("Updated", "Notes updated!")

        tk.Button(editor, text="Save", command=save, bg="#ffb6c1").pack()

    def delete_note(self):
        today = datetime.date.today().isoformat()
        file_path = os.path.join(NOTES_DIR, f"{today}_notes.txt")

        if not os.path.exists(file_path):
            messagebox.showinfo("None", "No notes today!")
            return

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        delete_window = tk.Toplevel(self.root)
        delete_window.title("Delete Note")
        delete_window.geometry("500x400")

        lb = tk.Listbox(delete_window, font=("Segoe UI", 12))
        lb.pack(fill="both", expand=True)

        for line in lines:
            lb.insert("end", line.strip())

        def delete_selected():
            sel = lb.curselection()
            if not sel:
                return
            index = sel[0]
            lines.pop(index)
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(lines)
            lb.delete(index)

        tk.Button(delete_window, text="Delete Selected", command=delete_selected,
                  bg="#ff8ca9").pack()

    def show_today_notes(self):
        today = datetime.date.today().isoformat()
        file_path = os.path.join(NOTES_DIR, f"{today}_notes.txt")

        if not os.path.exists(file_path):
            messagebox.showinfo("None", "No notes today!")
            return

        viewer = tk.Toplevel(self.root)
        viewer.title("Today's Notes")
        viewer.geometry("600x500")

        text_area = scrolledtext.ScrolledText(viewer, font=("Segoe UI", 12))
        text_area.pack(fill="both", expand=True)

        with open(file_path, "r", encoding="utf-8") as f:
            text_area.insert("1.0", f.read())

    def search_notes(self):
        keyword = simpledialog.askstring("Search", "Enter keyword:")
        if not keyword:
            return

        matches = []

        for file in os.listdir(NOTES_DIR):
            if file.endswith(".txt"):
                path = os.path.join(NOTES_DIR, file)
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        if keyword.lower() in line.lower():
                            matches.append((file, line.strip()))

        if not matches:
            messagebox.showinfo("None", "No matches found.")
            return

        result = tk.Toplevel(self.root)
        result.title("Search Results")
        result.geometry("600x500")

        text_area = scrolledtext.ScrolledText(result, font=("Segoe UI", 12))
        text_area.pack(fill="both", expand=True)

        for file, line in matches:
            text_area.insert("end", f"{file} → {line}\n")

    def show_stats(self):
        total = 0
        words = {}

        for file in os.listdir(NOTES_DIR):
            if file.endswith(".txt"):
                path = os.path.join(NOTES_DIR, file)
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        total += 1
                        for w in line.split():
                            w = w.lower()
                            words[w] = words.get(w, 0) + 1

        most_used = max(words, key=words.get) if words else "None"

        messagebox.showinfo("Stats", f"Total notes: {total}\nMost used word: {most_used}")

    def export_all_notes(self):
        export_path = os.path.join(NOTES_DIR, "all_notes.txt")

        with open(export_path, "w", encoding="utf-8") as out:
            for file in os.listdir(NOTES_DIR):
                if file.endswith(".txt"):
                    out.write(f"--- {file} ---\n")
                    with open(os.path.join(NOTES_DIR, file), "r", encoding="utf-8") as f:
                        out.write(f.read() + "\n")

        messagebox.showinfo("Exported", "All notes exported to all_notes.txt ✨")

# --- Run ---
root = tk.Tk()
app = SmartNotebook(root)
root.mainloop()
