import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library - Личная кинотека")
        self.root.geometry("800x500")

        self.movies = []
        self.load_data()

        # Поля ввода
        tk.Label(root, text="Название:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.title_entry = tk.Entry(root, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Жанр:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.genre_entry = tk.Entry(root, width=20)
        self.genre_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(root, text="Год выпуска:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.year_entry = tk.Entry(root, width=10)
        self.year_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(root, text="Рейтинг (0-10):").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.rating_entry = tk.Entry(root, width=5)
        self.rating_entry.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        # Кнопки
        tk.Button(root, text="Добавить фильм", command=self.add_movie).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(root, text="Очистить фильтры", command=self.clear_filters).grid(row=2, column=2, columnspan=2, pady=10)

        # Фильтры
        tk.Label(root, text="Фильтр по жанру:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.filter_genre_entry = tk.Entry(root, width=20)
        self.filter_genre_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.filter_genre_entry.bind("<KeyRelease>", lambda e: self.filter_movies())

        tk.Label(root, text="Фильтр по году:").grid(row=3, column=2, padx=5, pady=5, sticky="e")
        self.filter_year_entry = tk.Entry(root, width=10)
        self.filter_year_entry.grid(row=3, column=3, padx=5, pady=5, sticky="w")
        self.filter_year_entry.bind("<KeyRelease>", lambda e: self.filter_movies())

        # Таблица
        self.tree = ttk.Treeview(root, columns=("Название", "Жанр", "Год", "Рейтинг"), show="headings")
        self.tree.heading("Название", text="Название")
        self.tree.heading("Жанр", text="Жанр")
        self.tree.heading("Год", text="Год")
        self.tree.heading("Рейтинг", text="Рейтинг")
        self.tree.column("Название", width=250)
        self.tree.column("Жанр", width=150)
        self.tree.column("Год", width=80)
        self.tree.column("Рейтинг", width=80)
        self.tree.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Прокрутка
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=4, column=4, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        root.grid_rowconfigure(4, weight=1)
        root.grid_columnconfigure(0, weight=1)

        self.refresh_table()

    def load_data(self):
        if os.path.exists("movies.json"):
            with open("movies.json", "r", encoding="utf-8") as f:
                self.movies = json.load(f)

    def save_data(self):
        with open("movies.json", "w", encoding="utf-8") as f:
            json.dump(self.movies, f, indent=4, ensure_ascii=False)

    def add_movie(self):
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year_str = self.year_entry.get().strip()
        rating_str = self.rating_entry.get().strip()

        if not title or not genre or not year_str or not rating_str:
            messagebox.showerror("Ошибка", "Все поля обязательны для заполнения")
            return

        # Проверка года
        if not year_str.isdigit():
            messagebox.showerror("Ошибка", "Год должен быть числом")
            return
        year = int(year_str)
        if year < 1888 or year > 2030:
            messagebox.showerror("Ошибка", "Год должен быть между 1888 и 2030")
            return

        # Проверка рейтинга
        try:
            rating = float(rating_str)
            if rating < 0 or rating > 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10")
            return

        movie = {
            "title": title,
            "genre": genre,
            "year": year,
            "rating": rating
        }
        self.movies.append(movie)
        self.save_data()
        self.clear_entries()
        self.refresh_table()
        messagebox.showinfo("Успех", f"Фильм \"{title}\" добавлен!")

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)

    def filter_movies(self):
        genre_filter = self.filter_genre_entry.get().strip().lower()
        year_filter = self.filter_year_entry.get().strip()
        self.refresh_table(genre_filter, year_filter)

    def refresh_table(self, genre_filter="", year_filter=""):
        # Очищаем таблицу
        for row in self.tree.get_children():
            self.tree.delete(row)

        for movie in self.movies:
            # Фильтрация по жанру
            if genre_filter and genre_filter not in movie["genre"].lower():
                continue
            # Фильтрация по году
            if year_filter:
                try:
                    if int(movie["year"]) != int(year_filter):
                        continue
                except ValueError:
                    pass  # Если фильтр не число, игнорируем

            self.tree.insert("", tk.END, values=(
                movie["title"],
                movie["genre"],
                movie["year"],
                movie["rating"]
            ))

    def clear_filters(self):
        self.filter_genre_entry.delete(0, tk.END)
        self.filter_year_entry.delete(0, tk.END)
        self.refresh_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()
