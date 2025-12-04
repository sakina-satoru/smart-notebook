import os
import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext, filedialog
import zipfile

# ---------------------------------------------------
# Ensure notes folder exists
# ---------------------------------------------------
categories = ["school", "personal", "ideas", "journal"]
for cat in categories:
    if not os.path.exists(f"notes/{cat}"):
        os.makedirs(f"notes/{cat}")

# ---------------------------------------------------
# Gradient Background
# ---------------------------------------------------
def draw_gradient(canvas, color1, color2):
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    r1, g1, b1 = canvas.winfo_rgb(color1)
    r2, g2, b2 = canvas.winfo_rgb(color2)
    r1 >>= 8; g1 >>= 8; b1 >>= 8
    r2 >>= 8; g2 >>= 8; b2 >>= 8
    for i in range(height):
        r = int(r1 + (r2 - r1) * (i / height))
        g = int(g1 + (g2 - g1) * (i / height))
        b = int(b1 + (b2 - b1) * (i / height))
        color = f"#{r:02x}{g:02x}{b:02x}"
        canvas.create_line(0, i, width, i, fill=color)

# ---------------------------------------------------
# App Class
# ---------------------------------------------------
class SmartNotebookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Notebook by Sakina")
        self.root.geometry("650x750")

        # Canvas for gradient
        self.canvas = tk.Canvas(root, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.redraw_gradient)

        # Title
        self.title_label = tk.Label(root, text="Smart Notebook 🧠", bg="#ffcfcf",
                                    fg="white", font=("Segoe UI", 22, "bold"))
        self.canvas.create_window(325, 60, window=self.title_label)

        # Buttons
        self.add_button = tk.Button(root, text="➕ Add Note", command=self.add_note,
                                    bg="white", fg="#ff8aa6", font=("Segoe UI", 14, "bold"), width=25)
        self.canvas.create_window(325, 150, window=self.add_button)

        self.edit_button = tk.Button(root, text="✏️ Edit Notes", command=self.edit_notes,
                                     bg="white", fg="#ff8aa6", font=("Segoe UI", 14, "bold"), width=25)
        self.canvas.create_window(325, 220, window=self.edit_button)

        self.delete_button = tk.Button(root, text="🗑️ Delete Note", command=self.delete_note,
                                       bg="white", fg="#ff8aa6", font=("Segoe UI", 14, "bold"), width=25)
        self.canvas.create_window(325, 290, window=self.delete_button)

        self.search_button = tk.Button(root, text="🔍 Search Notes", command=self.search_notes,
                                       bg="white", fg="#ff8aa6", font=("Segoe UI", 14, "bold"), width=25)
        self.canvas.create_window(325, 360, window=self.search_button)

        self.today_button = tk.Button(root, text="📅 Today’s Notes", command=self.today_notes,
                                      bg="white", fg="#ff8aa6", font=("Segoe UI", 14, "bold"), width=25)
        self.canvas.create_window(325, 430, window=self.today_button)

        self.stats_button = tk.Button(root, text="📊 Notebook Stats", command=self.show_stats,
                                      bg="white", fg="#ff8aa6", font=("Segoe UI", 14, "bold"), width=25)
        self.canvas.create_window(325, 500, window=self.stats_button)

        self.export_button = tk.Button(root, text="📤 Export All Notes", command=self.export_all,
                                       bg="white", fg="#ff8aa6", font=("Segoe UI", 14, "bold"), width=25)
        self.canvas.create_window(325, 570, window=self.export_button)

        self.exit_button = tk.Button(root, text="🚪 Exit", command=self.exit_app,
                                     bg="white", fg="#ff8aa6", font=("Segoe UI", 14, "bold"), width=25)
        self.canvas.create_window(325, 640, window=self.exit_button)

        # Signature
        self.signature = tk.Label(root, text="made by Sakina", bg="#ffcfcf",
                                  fg="white", font=("Segoe UI", 10, "italic"))
        self.canvas.create_window(620, 720, window=self.signature, anchor="se")

    def redraw_gradient(self, event):
        self.canvas.delete("all")
        draw_gradient(self.canvas, "#ffcfcf", "#ffffff")
        # redraw widgets
        self.canvas.create_window(325, 60, window=self.title_label)
        self.canvas.create_window(325, 150, window=self.add_button)
        self.canvas.create_window(325, 220, window=self.edit_button)
        self.canvas.create_window(325, 290, window=self.delete_button)
        self.canvas.create_window(325, 360, window=self.search_button)
        self.canvas.create_window(325, 430, window=self.today_button)
        self.canvas.create_window(325, 500, window=self.stats_button)
        self.canvas.create_window(325, 570, window=self.export_button)
        self.canvas.create_window(325, 640, window=self.exit_button)
        self.canvas.create_window(620, 720, window=self.signature, anchor="se")

    # ---------------------------------------------------
    # Add Note
    # ---------------------------------------------------
    def add_note(self):
        note = simpledialog.askstring("Add Note", "Write your note here:")
        if not note:
            return

        # Timestamp
        now = datetime.datetime.now().strftime("%H:%M")
        note_text = f"[{now}] {note}"

        # Choose category
        category = simpledialog.askstring("Category",
                                          f"Choose category ({', '.join(categories)}):")
        if category not in categories:
            messagebox.showerror("Error", f"Invalid category! Saving to 'personal'.")
            category = "personal"

        today = datetime.date.today().strftime("%Y-%m-%d")
        filename = f"notes/{category}/{today}_notes.txt"

        with open(filename, "a", encoding="utf-8") as f:
            f.write(note_text + "\n")

        messagebox.showinfo("Saved 💗", f"Note saved in {filename}")

    # ---------------------------------------------------
    # Edit Notes
    # ---------------------------------------------------
    def edit_notes(self):
        category = simpledialog.askstring("Category", f"Choose category ({', '.join(categories)}):")
        if category not in categories:
            messagebox.showerror("Error", "Invalid category")
            return

        file_list = [f for f in os.listdir(f"notes/{category}") if f.endswith(".txt")]
        if not file_list:
            messagebox.showinfo("No Notes", "No note files in this category.")
            return

        file_choice = simpledialog.askstring("Select File", f"Choose file:\n{', '.join(file_list)}")
        if file_choice not in file_list:
            messagebox.showerror("Error", "Invalid file selected")
            return

        path = f"notes/{category}/{file_choice}"
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        edit_win = tk.Toplevel(self.root)
        edit_win.title(f"Editing {file_choice}")
        text_area = scrolledtext.ScrolledText(edit_win, width=70, height=20)
        text_area.pack(padx=10, pady=10)
        text_area.insert(tk.END, content)

        def save_changes():
            with open(path, "w", encoding="utf-8") as f:
                f.write(text_area.get("1.0", tk.END).strip())
            messagebox.showinfo("Saved 💗", "Changes saved successfully!")

        save_btn = tk.Button(edit_win, text="Save Changes", command=save_changes, bg="#ffcfcf")
        save_btn.pack(pady=10)

    # ---------------------------------------------------
    # Delete Note
    # ---------------------------------------------------
    def delete_note(self):
        category = simpledialog.askstring("Category", f"Choose category ({', '.join(categories)}):")
        if category not in categories:
            messagebox.showerror("Error", "Invalid category")
            return

        file_list = [f for f in os.listdir(f"notes/{category}") if f.endswith(".txt")]
        if not file_list:
            messagebox.showinfo("No Notes", "No note files in this category.")
            return

        file_choice = simpledialog.askstring("Select File", f"Choose file:\n{', '.join(file_list)}")
        if file_choice not in file_list:
            messagebox.showerror("Error", "Invalid file selected")
            return

        path = f"notes/{category}/{file_choice}"
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        line_text = "\n".join([f"{i+1}. {l.strip()}" for i, l in enumerate(lines)])
        line_num = simpledialog.askinteger("Delete Line", f"Select line number to delete:\n{line_text}")
        if not line_num or line_num < 1 or line_num > len(lines):
            messagebox.showerror("Error", "Invalid line number")
            return

        del lines[line_num - 1]
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(lines)

        messagebox.showinfo("Deleted ❌", f"Line {line_num} deleted successfully!")

    # ---------------------------------------------------
    # Search Notes
    # ---------------------------------------------------
    def search_notes(self):
        keyword = simpledialog.askstring("Search", "Enter keyword:")
        if not keyword:
            return

        results = ""
        date_filter = simpledialog.askstring("Filter by Date (optional)", "Enter date YYYY-MM-DD or leave blank:")
        for cat in categories:
            folder = f"notes/{cat}"
            for file in os.listdir(folder):
                if file.endswith(".txt") and (not date_filter or date_filter in file):
                    with open(f"{folder}/{file}", "r", encoding="utf-8") as f:
                        for line in f:
                            if keyword.lower() in line.lower():
                                results += f"{cat}/{file}: {line}"

        if not results:
            messagebox.showinfo("No Results 😪", "No matching notes found.")
        else:
            result_win = tk.Toplevel(self.root)
            result_win.title("Search Results 🎯")
            text_area = scrolledtext.ScrolledText(result_win, width=70, height=25)
            text_area.pack(padx=10, pady=10)
            text_area.insert(tk.END, results)

    # ---------------------------------------------------
    # Today's Notes
    # ---------------------------------------------------
    def today_notes(self):
        today = datetime.date.today().strftime("%Y-%m-%d")
        results = ""
        for cat in categories:
            folder = f"notes/{cat}"
            for file in os.listdir(folder):
                if file.endswith(f"{today}_notes.txt"):
                    with open(f"{folder}/{file}", "r", encoding="utf-8") as f:
                        for line in f:
                            results += f"{cat}/{file}: {line}"

        if not results:
            messagebox.showinfo("No Notes Today 😪", "No notes found for today.")
        else:
            result_win = tk.Toplevel(self.root)
            result_win.title("Today's Notes 📅")
            text_area = scrolledtext.ScrolledText(result_win, width=70, height=25)
            text_area.pack(padx=10, pady=10)
            text_area.insert(tk.END, results)

    # ---------------------------------------------------
    # Notebook Stats
    # ---------------------------------------------------
    def show_stats(self):
        total_notes = 0
        word_count = {}
        for cat in categories:
            folder = f"notes/{cat}"
            for file in os.listdir(folder):
                if file.endswith(".txt"):
                    with open(f"{folder}/{file}", "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        total_notes += len(lines)
                        for line in lines:
                            for word in line.split():
                                word = word.strip("#.,!?").lower()
                                if word:
                                    word_count[word] = word_count.get(word, 0) + 1
        most_used = max(word_count, key=word_count.get) if word_count else "N/A"
        messagebox.showinfo("Stats 📊",
                            f"Total Notes: {total_notes}\nMost Used Word: {most_used}")

    # ---------------------------------------------------
    # Export All Notes
    # ---------------------------------------------------
    def export_all(self):
        export_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                   filetypes=[("Text Files", "*.txt")],
                                                   title="Export All Notes")
        if not export_path:
            return

        all_notes = ""
        for cat in categories:
            folder = f"notes/{cat}"
            for file in os.listdir(folder):
                if file.endswith(".txt"):
                    with open(f"{folder}/{file}", "r", encoding="utf-8") as f:
                        all_notes += f"--- {cat}/{file} ---\n"
                        all_notes += f.read() + "\n\n"

        with open(export_path, "w", encoding="utf-8") as f:
            f.write(all_notes)

        messagebox.showinfo("Exported 📤", f"All notes exported to {export_path}")

    # ---------------------------------------------------
    # Exit App with Backup
    # ---------------------------------------------------
    def exit_app(self):
        backup_name = f"backup_{datetime.date.today().strftime('%Y-%m-%d')}.zip"
        with zipfile.ZipFile(backup_name, 'w') as zipf:
            for cat in categories:
                folder = f"notes/{cat}"
                for file in os.listdir(folder):
                    zipf.write(f"{folder}/{file}")
        messagebox.showinfo("Goodbye 💗", f"Backup created: {backup_name}\nNotes saved successfully!")
        self.root.destroy()

# ---------------------------------------------------
# Run App
# ---------------------------------------------------
root = tk.Tk()
app = SmartNotebookApp(root)
root.mainloop()
