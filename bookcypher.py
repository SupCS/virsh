import tkinter as tk
from tkinter import messagebox, filedialog, ttk

class TritemiusCipher:
    def __init__(self, alphabet='абвгґдеєжзийіїклмнопрстуфхцчшщьюя'):
        self.alphabet_lower = alphabet
        self.alphabet_upper = alphabet.upper()
        self.alphabet_size = len(alphabet)

    def set_alphabet(self, alphabet):
        self.alphabet_lower = alphabet
        self.alphabet_upper = alphabet.upper()
        self.alphabet_size = len(alphabet)

    def validate_text(self, text):
        for char in text:
            if char.isalpha() and char not in self.alphabet_lower + self.alphabet_upper:
                raise ValueError("Текст містить недопустимі символи.")
        return text

    def linear_shift(self, position, A, B):
        return (A * position + B) % self.alphabet_size

    def nonlinear_shift(self, position, A, B, C):
        return (A * position**2 + B * position + C) % self.alphabet_size

    def keyword_shift(self, position, keyword):
        keyword = keyword.lower()
        return self.alphabet_lower.index(keyword[position % len(keyword)])

    def encrypt(self, text, method, key_params):
        text = self.validate_text(text)
        encrypted_text = ''
        for i, char in enumerate(text):
            if char in self.alphabet_lower:
                shift = self.calculate_shift(i, method, key_params)
                index = (self.alphabet_lower.index(char) + shift) % self.alphabet_size
                encrypted_text += self.alphabet_lower[index]
            elif char in self.alphabet_upper:
                shift = self.calculate_shift(i, method, key_params)
                index = (self.alphabet_upper.index(char) + shift) % self.alphabet_size
                encrypted_text += self.alphabet_upper[index]
            else:
                encrypted_text += char
        return encrypted_text

    def decrypt(self, text, method, key_params):
        text = self.validate_text(text)
        decrypted_text = ''
        for i, char in enumerate(text):
            if char in self.alphabet_lower:
                shift = self.calculate_shift(i, method, key_params)
                index = (self.alphabet_lower.index(char) - shift) % self.alphabet_size
                decrypted_text += self.alphabet_lower[index]
            elif char in self.alphabet_upper:
                shift = self.calculate_shift(i, method, key_params)
                index = (self.alphabet_upper.index(char) - shift) % self.alphabet_size
                decrypted_text += self.alphabet_upper[index]
            else:
                decrypted_text += char
        return decrypted_text

    def calculate_shift(self, position, method, key_params):
        if method == 'linear':
            A, B = key_params
            return self.linear_shift(position, A, B)
        elif method == 'nonlinear':
            A, B, C = key_params
            return self.nonlinear_shift(position, A, B, C)
        elif method == 'keyword':
            keyword = key_params[0]
            return self.keyword_shift(position, keyword)
        else:
            raise ValueError("Невідомий метод шифрування.")
        
class PoemCipher:
    def __init__(self):
        self.matrix = []
        self.rows = 0
        self.cols = 0

    def create_matrix(self, poem):
        """Створення матриці з вірша."""
        poem = poem.replace(" ", "").replace("\n", "")
        self.rows = len(poem) // 10
        self.cols = 10
        self.matrix = [poem[i:i + self.cols] for i in range(0, len(poem), self.cols)]
        if len(self.matrix[-1]) < self.cols:
            # Доповнюємо останній рядок пробілами, якщо він коротший за 10 символів
            self.matrix[-1] += " " * (self.cols - len(self.matrix[-1]))

    def encrypt(self, message):
        """Шифрування повідомлення через вірш."""
        cipher_text = []
        for char in message:
            char_lower = char.lower()  # Перетворюємо на нижній регістр
            for row_idx, row in enumerate(self.matrix):
                if char_lower in row:
                    col_idx = row.index(char_lower)
                    cipher_text.append(f"{row_idx+1}/{col_idx+1}")
                    break
        return ", ".join(cipher_text)

    def decrypt(self, cipher_text):
        """Розшифрування через координати."""
        message = []
        pairs = cipher_text.split(", ")
        for pair in pairs:
            row, col = map(int, pair.split("/"))
            decrypted_char = self.matrix[row-1][col-1]
            message.append(decrypted_char)
        return "".join(message)

class CryptoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Криптосистема")
        self.root.geometry("700x700")
        self.root.configure(bg="#f0f0f0")

        # Додавання меню
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Відкрити", command=self.open_file)
        file_menu.add_command(label="Зберегти", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Вийти", command=self.root.quit)

        edit_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Редагування", menu=edit_menu)
        edit_menu.add_command(label="Копіювати", command=self.copy_text)
        edit_menu.add_command(label="Вирізати", command=self.cut_text)
        edit_menu.add_command(label="Вставити", command=self.paste_text)

        # Додавання вкладок
        self.tab_control = ttk.Notebook(self.root)
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab1, text="Шифр Тритеміуса")
        self.tab_control.add(self.tab2, text="Книжковий шифр (вірш)")
        self.tab_control.pack(expand=1, fill="both")

        # Вкладка 1: Шифр Тритеміуса
        self.create_tritemius_tab()

        # Вкладка 2: Книжковий шифр
        self.create_book_cipher_tab()

    def create_tritemius_tab(self):
        # Інтерфейс для шифру Тритеміуса (залишився без змін)
        self.tritemius_cipher_ua = TritemiusCipher()  # Український алфавіт
        self.tritemius_cipher_en = TritemiusCipher(alphabet='abcdefghijklmnopqrstuvwxyz')  # Англійський алфавіт

        # Текстове поле для введення тексту
        text_frame = tk.Frame(self.tab1, pady=10, bg="#f0f0f0")
        text_frame.pack(fill="x")

        self.label = tk.Label(text_frame, text="Введіть текст для шифрування/розшифрування:",
                              font=("Arial", 12, "bold"), bg="#f0f0f0")
        self.label.pack(padx=20, pady=5)

        self.text_input_tritemius = tk.Text(text_frame, height=5, width=70, borderwidth=2, relief="solid")
        self.text_input_tritemius.pack(padx=10)

        # Вибір методу шифрування
        method_frame = tk.Frame(self.tab1, pady=10, bg="#f0f0f0")
        method_frame.pack(fill="x")

        self.method_label = tk.Label(method_frame, text="Оберіть метод шифрування:", font=("Arial", 10), bg="#f0f0f0")
        self.method_label.pack(side="left", padx=10)

        self.method_var = tk.StringVar(value="linear")
        self.linear_method = tk.Radiobutton(method_frame, text="Лінійний", variable=self.method_var, value="linear", bg="#f0f0f0", command=self.show_key_inputs)
        self.nonlinear_method = tk.Radiobutton(method_frame, text="Нелінійний", variable=self.method_var, value="nonlinear", bg="#f0f0f0", command=self.show_key_inputs)
        self.keyword_method = tk.Radiobutton(method_frame, text="Гасло", variable=self.method_var, value="keyword", bg="#f0f0f0", command=self.show_key_inputs)
        self.linear_method.pack(side="left")
        self.nonlinear_method.pack(side="left")
        self.keyword_method.pack(side="left")

        # Вибір мови
        language_frame = tk.Frame(self.tab1, pady=10, bg="#f0f0f0")
        language_frame.pack(fill="x")

        self.language_label = tk.Label(language_frame, text="Оберіть мову:", font=("Arial", 10), bg="#f0f0f0")
        self.language_label.pack(side="left", padx=10)

        self.language_var = tk.StringVar(value="ua")
        self.language_ua = tk.Radiobutton(language_frame, text="Українська", variable=self.language_var, value="ua", bg="#f0f0f0")
        self.language_en = tk.Radiobutton(language_frame, text="Англійська", variable=self.language_var, value="en", bg="#f0f0f0")
        self.language_ua.pack(side="left")
        self.language_en.pack(side="left")

        # Поля для введення ключів
        key_frame = tk.Frame(self.tab1, pady=10, bg="#f0f0f0")
        key_frame.pack(fill="x")

        self.key_label = tk.Label(key_frame, text="Введіть ключ шифрування:", font=("Arial", 10), bg="#f0f0f0")
        self.key_label.pack(side="left", padx=10)

        self.key_input_A = tk.Entry(key_frame, width=10, borderwidth=2, relief="solid")
        self.key_input_B = tk.Entry(key_frame, width=10, borderwidth=2, relief="solid")
        self.key_input_C = tk.Entry(key_frame, width=10, borderwidth=2, relief="solid")
        self.key_input_keyword = tk.Entry(key_frame, width=30, borderwidth=2, relief="solid")

        self.show_key_inputs()

        # Кнопки для шифрування і дешифрування
        button_frame = tk.Frame(self.tab1, pady=10, bg="#f0f0f0")
        button_frame.pack(fill="x")

        self.encrypt_button = tk.Button(button_frame, text="Зашифрувати", width=15, bg="#4CAF50", fg="white",
                                        font=("Arial", 10, "bold"), command=self.encrypt_text)
        self.encrypt_button.pack(side="left", padx=10)

        self.decrypt_button = tk.Button(button_frame, text="Розшифрувати", width=15, bg="#2196F3", fg="white",
                                        font=("Arial", 10, "bold"), command=self.decrypt_text)
        self.decrypt_button.pack(side="left", padx=10)

        self.about_button = tk.Button(button_frame, text="Про автора", width=15, bg="#9C27B0", fg="white",
                                      font=("Arial", 10, "bold"), command=self.show_about_info)
        self.about_button.pack(side="left", padx=10)

        # Поле для виведення результату
        result_frame = tk.Frame(self.tab1, pady=10, bg="#f0f0f0")
        result_frame.pack(fill="x")

        self.result_label_tritemius = tk.Label(result_frame, text="Результат:", font=("Arial", 12, "bold"), bg="#f0f0f0")
        self.result_label_tritemius.pack(anchor="w", padx=10)

        self.result_output_tritemius = tk.Text(result_frame, height=10, width=70, borderwidth=2, relief="solid")
        self.result_output_tritemius.pack(padx=10)

    def show_key_inputs(self):
        method = self.method_var.get()
        self.key_input_A.pack_forget()
        self.key_input_B.pack_forget()
        self.key_input_C.pack_forget()
        self.key_input_keyword.pack_forget()

        if method == "linear":
            self.key_input_A.pack(side="left", padx=5)
            self.key_input_B.pack(side="left", padx=5)
        elif method == "nonlinear":
            self.key_input_A.pack(side="left", padx=5)
            self.key_input_B.pack(side="left", padx=5)
            self.key_input_C.pack(side="left", padx=5)
        elif method == "keyword":
            self.key_input_keyword.pack(side="left", padx=5)

    def parse_key(self):
        method = self.method_var.get()

        if method == "linear":
            try:
                A = int(self.key_input_A.get().strip())
                B = int(self.key_input_B.get().strip())
                return method, (A, B)
            except ValueError:
                raise ValueError("Невірний формат ключа для лінійного шифрування. Використовуйте два числа.")
        elif method == "nonlinear":
            try:
                A = int(self.key_input_A.get().strip())
                B = int(self.key_input_B.get().strip())
                C = int(self.key_input_C.get().strip())
                return method, (A, B, C)
            except ValueError:
                raise ValueError("Невірний формат ключа для нелінійного шифрування. Використовуйте три числа.")
        elif method == "keyword":
            keyword = self.key_input_keyword.get().strip()
            if not keyword:
                raise ValueError("Гасло не може бути порожнім.")
            return method, (keyword,)
        else:
            raise ValueError("Невідомий метод шифрування.")

    def encrypt_text(self):
        text = self.text_input_tritemius.get("1.0", tk.END).strip()
        language = self.language_var.get()

        if language == "ua":
            cipher = self.tritemius_cipher_ua
        else:
            cipher = self.tritemius_cipher_en

        try:
            method, key_params = self.parse_key()
            encrypted_text = cipher.encrypt(text, method, key_params)
            self.result_output_tritemius.delete("1.0", tk.END)
            self.result_output_tritemius.insert(tk.END, encrypted_text)
        except ValueError as e:
            messagebox.showerror("Помилка", str(e))

    def decrypt_text(self):
        text = self.text_input_tritemius.get("1.0", tk.END).strip()
        language = self.language_var.get()

        if language == "ua":
            cipher = self.tritemius_cipher_ua
        else:
            cipher = self.tritemius_cipher_en

        try:
            method, key_params = self.parse_key()
            decrypted_text = cipher.decrypt(text, method, key_params)
            self.result_output_tritemius.delete("1.0", tk.END)
            self.result_output_tritemius.insert(tk.END, decrypted_text)
        except ValueError as e:
            messagebox.showerror("Помилка", str(e))

    def create_book_cipher_tab(self):
        # Поле для вибору вірша
        poem_label = tk.Label(self.tab2, text="Введіть вірш, який буде використано як ключ шифрування:", 
                            font=("Arial", 12, "bold"), bg="#f0f0f0")
        poem_label.pack(pady=10)

        self.poem_input = tk.Text(self.tab2, height=5, width=70, borderwidth=2, relief="solid")
        self.poem_input.pack(padx=10, pady=5)

        # Поле для тексту, який потрібно зашифрувати/розшифрувати
        message_label = tk.Label(self.tab2, text="Введіть текст для шифрування/розшифрування:",
                                font=("Arial", 12, "bold"), bg="#f0f0f0")
        message_label.pack(pady=10)

        self.message_input = tk.Text(self.tab2, height=5, width=70, borderwidth=2, relief="solid")
        self.message_input.pack(padx=10, pady=5)

        # Кнопки для шифрування і дешифрування
        button_frame = tk.Frame(self.tab2, pady=10, bg="#f0f0f0")
        button_frame.pack(fill="x")

        encrypt_button = tk.Button(button_frame, text="Зашифрувати", width=15, bg="#4CAF50", fg="white",
                                font=("Arial", 10, "bold"), command=self.encrypt_poem)
        encrypt_button.pack(side="left", padx=10)

        decrypt_button = tk.Button(button_frame, text="Розшифрувати", width=15, bg="#2196F3", fg="white",
                                font=("Arial", 10, "bold"), command=self.decrypt_poem)
        decrypt_button.pack(side="left", padx=10)

        # Поле для виведення результату
        result_label = tk.Label(self.tab2, text="Результат:", font=("Arial", 12, "bold"), bg="#f0f0f0")
        result_label.pack(anchor="w", padx=10)

        self.result_output_book_cipher = tk.Text(self.tab2, height=10, width=70, borderwidth=2, relief="solid")
        self.result_output_book_cipher.pack(padx=10, pady=5)

        self.poem_cipher = PoemCipher()  # Ініціалізуємо шифр вірша

    def encrypt_poem(self):
        poem = self.poem_input.get("1.0", tk.END).strip()
        message = self.message_input.get("1.0", tk.END).strip()

        if not poem or not message:
            messagebox.showerror("Помилка", "Введіть вірш і повідомлення для шифрування.")
            return

        self.poem_cipher.create_matrix(poem)
        encrypted_text = self.poem_cipher.encrypt(message)
        
        self.result_output_book_cipher.delete("1.0", tk.END)
        self.result_output_book_cipher.insert(tk.END, encrypted_text)

    def decrypt_poem(self):
        poem = self.poem_input.get("1.0", tk.END).strip()
        cipher_text = self.message_input.get("1.0", tk.END).strip()

        if not poem or not cipher_text:
            messagebox.showerror("Помилка", "Введіть вірш і шифр для розшифрування.")
            return

        self.poem_cipher.create_matrix(poem)
        decrypted_text = self.poem_cipher.decrypt(cipher_text)
        
        self.result_output_book_cipher.delete("1.0", tk.END)
        self.result_output_book_cipher.insert(tk.END, decrypted_text)

    # Меню - копіювання, вставка і вирізання
    def copy_text(self):
        try:
            widget = self.root.focus_get()
            if isinstance(widget, tk.Text):
                widget.event_generate("<<Copy>>")
        except tk.TclError:
            messagebox.showerror("Помилка", "Немає виділеного тексту для копіювання.")

    def cut_text(self):
        try:
            widget = self.root.focus_get()
            if isinstance(widget, tk.Text):
                widget.event_generate("<<Cut>>")
        except tk.TclError:
            messagebox.showerror("Помилка", "Немає виділеного тексту для вирізання.")

    def paste_text(self):
        try:
            widget = self.root.focus_get()
            if isinstance(widget, tk.Text):
                widget.event_generate("<<Paste>>")
        except tk.TclError:
            messagebox.showerror("Помилка", "Буфер обміну порожній або недоступний.")

    def show_about_info(self):
        messagebox.showinfo("Про розробника", "Розробник: Дмитро Аспарян ТВ-11\nКриптосистема на основі шифру Тритеміуса")

    def save_file(self):
        content = self.result_output_tritemius.get("1.0", tk.END).strip()
        if not content:
            messagebox.showerror("Помилка", "Немає тексту для збереження.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            messagebox.showinfo("Успіх", "Файл успішно збережено.")

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            self.text_input_tritemius.delete("1.0", tk.END)
            self.text_input_tritemius.insert(tk.END, content)


if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoGUI(root)
    root.mainloop()