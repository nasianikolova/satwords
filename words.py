import tkinter as tk
from tkinter import messagebox
from user import User
from wordrequests import DBRequests
import random


try:
    connectedUser = User.get_connectedUser()
    if not connectedUser:
        raise ValueError("Connected user is not defined.")
except Exception as e:
    messagebox.showerror("Error", f"Could not fetch connected user: {e}")
    connectedUser = None

try:
    word_requests = DBRequests()
except Exception as e:
    messagebox.showerror("Error", f"Database connection failed: {e}")
    word_requests = None

word_data = []

WORDS_PER_PAGE = 5
current_exam_page = 0
exam_page_data = []

# === Core Functions ===
def load_words_from_db():
    if not word_requests or not connectedUser:
        messagebox.showerror("Error", "Database or user not properly initialized.")
        return
    try:
        word_data.clear()
        rows = word_requests.fetch_words(connectedUser)
        word_data.extend(rows)
        display_page()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load words: {e}")

def display_page():
    vocab_listbox.delete(0, tk.END)
    for row in word_data:
        fail_count = row.get('fails', 0)
        if fail_count > 0:
            vocab_listbox.insert(tk.END, f"{row['word']} - {row['translation']} (Failed {fail_count}x)")
        else:
            vocab_listbox.insert(tk.END, f"{row['word']} - {row['translation']}")


def add_word():
    if not word_requests or not connectedUser:
        return
    word = word_entry.get()
    translation = translation_entry.get()
    sentence = sentence_entry.get()
    if word and translation and sentence:
        try:
            word_requests.insert_word(connectedUser, word, translation, sentence)
            load_words_from_db()
            word_entry.delete(0, tk.END)
            translation_entry.delete(0, tk.END)
            sentence_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to insert word: {e}")
    else:
        messagebox.showwarning("Warning", "Fill in all fields.")

def delete_selected_word():
    if not word_requests:
        return
    selection = vocab_listbox.curselection()
    if selection:
        index = selection[0]
        word_uuid = word_data[index]['uuid']
        try:
            word_requests.delete_word(word_uuid)
            load_words_from_db()
            sentence_label.config(text="")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete word: {e}")

def on_vocab_select(event):
    selection = vocab_listbox.curselection()
    if selection:
        index = selection[0]
        sentence = word_data[index]['sentence']
        sentence_label.config(text=f"Example: {sentence}")

def show_vocabulary_page():
    main_menu_frame.pack_forget()
    exam_frame.pack_forget()
    vocab_frame.pack()
    load_words_from_db()

def show_exam_page():
    global current_exam_page
    main_menu_frame.pack_forget()
    vocab_frame.pack_forget()
    exam_frame.pack()
    load_words_from_db()
    current_exam_page = 0


def back():
    window.destroy()
    import login

def show_last_20():
    global exam_page_data
    exam_page_data = word_data[-20:]
    messagebox.showinfo("Words Selected", f"{len(exam_page_data)} words loaded: Last 20")

def show_previous_20():
    global exam_page_data
    exam_page_data = word_data[:20]
    messagebox.showinfo("Words Selected", f"{len(exam_page_data)} words loaded: Previous 20")

def show_failed_words():
    global exam_page_data
    exam_page_data = [w for w in word_data if w.get('fails', 0) > 0]
    vocab_listbox.delete(0, tk.END)
    for row in exam_page_data:
        vocab_listbox.insert(tk.END, f"{row['word']} - {row['translation']} (Failed {row['fails']}x)")
    messagebox.showinfo("Words Selected", f"{len(exam_page_data)} failed words loaded")


def show_random_words():
    global exam_page_data
    exam_page_data = random.sample(word_data, min(20, len(word_data)))
    messagebox.showinfo("Words Selected", f"{len(exam_page_data)} random words loaded")

def change_exam_page(delta):
    global current_exam_page
    max_page = (len(word_data) + WORDS_PER_PAGE - 1) // WORDS_PER_PAGE
    if 0 <= current_exam_page + delta < max_page:
        current_exam_page += delta



def start_quiz():
    if not word_requests:
        return
    selected = exam_page_data
    if not selected:
        messagebox.showinfo("Quiz", "No words loaded for quiz. Please select words using the buttons.")
        return


    quiz_frame = tk.Toplevel()
    quiz_frame.title("Quiz")
    quiz_frame.geometry("400x300")

    score = {"correct": 0, "total": len(selected)}
    current = {"index": 0}
    wrong_answers = []

    def next_question():
        for widget in quiz_frame.winfo_children():
            widget.destroy()

        if current["index"] >= score["total"]:
            tk.Label(quiz_frame, text="Quiz Complete!", font=("Arial", 16)).pack(pady=10)
            tk.Label(quiz_frame, text=f"Correct: {score['correct']} / {score['total']}", font=("Arial", 14)).pack(pady=10)
            if wrong_answers:
                tk.Label(quiz_frame, text="Wrong Answers:", font=("Arial", 13)).pack(pady=10)
                for word, translation in wrong_answers:
                    tk.Label(quiz_frame, text=f"{word} → {translation}", fg="red").pack()
            tk.Button(quiz_frame, text="Close", command=quiz_frame.destroy).pack(pady=10)
            return

        entry = selected[current["index"]]
        tk.Label(quiz_frame, text=f"Translate: {entry['word']}").pack(pady=10)
        answer_entry = tk.Entry(quiz_frame)
        answer_entry.pack()

        def check_answer():
            answer = answer_entry.get().strip().lower()
            correct = entry['translation'].strip().lower()
            try:
                if answer == correct:
                    score["correct"] += 1
                    word_requests.reset_fail(entry["uuid"])
                else:
                    wrong_answers.append((entry['word'], entry['translation']))
                    word_requests.increment_fail(entry["uuid"])
            except Exception as e:
                messagebox.showerror("Error", f"Error updating fail count: {e}")
            current["index"] += 1
            next_question()

        tk.Button(quiz_frame, text="Submit", command=check_answer).pack(pady=5)

    next_question()

window = tk.Tk()
window.title("Words")
window.geometry("600x500")
window.resizable(False, False)
window.configure(bg='#4F93B8')


# Main Menu
main_menu_frame = tk.Frame(window, bg='#4F93B8')
main_menu_frame.pack()
tk.Label(main_menu_frame, text="Choose section", font=("Arial", 17)).pack(pady=20)
tk.Button(main_menu_frame, text="Vocabulary Page", width=15, padx=20, pady=15, command=show_vocabulary_page, font=("Arial", 15)).pack(pady=12)
tk.Button(main_menu_frame, text="Exam Page", width=15, padx=20, pady=15, command=show_exam_page, font=("Arial", 15)).pack(pady=12)
tk.Button(main_menu_frame, text="Disconnect", width=15, padx=20, pady=15, command=back, font=("Arial", 15)).pack(pady=12)

# Vocabulary Page
vocab_frame = tk.Frame(window)
tk.Label(vocab_frame, text="Vocabulary", font=("Arial", 14)).pack(pady=10)
vocab_listbox = tk.Listbox(vocab_frame, width=50)
vocab_listbox.pack()
vocab_listbox.bind("<<ListboxSelect>>", on_vocab_select)
sentence_label = tk.Label(vocab_frame, text="", wraplength=500)
sentence_label.pack(pady=5)

tk.Label(vocab_frame, text="Word:").pack()
word_entry = tk.Entry(vocab_frame)
word_entry.pack()
tk.Label(vocab_frame, text="Translation:").pack()
translation_entry = tk.Entry(vocab_frame)
translation_entry.pack()
tk.Label(vocab_frame, text="Sentence:").pack()
sentence_entry = tk.Entry(vocab_frame)
sentence_entry.pack()
tk.Button(vocab_frame, text="Add New Word", command=add_word).pack(pady=5)
tk.Button(vocab_frame, text="Delete Selected Word", command=delete_selected_word).pack(pady=5)
tk.Button(vocab_frame, text="Back to Menu", command=lambda: [vocab_frame.pack_forget(), main_menu_frame.pack()]).pack(pady=5)

# Exam Page
# Exam Page
# === Exam Page ===
exam_frame = tk.Frame(window, bg='#4F93B8')
tk.Label(exam_frame, text="Exam Page", font=("Arial", 17), bg='#4F93B8').pack(pady=10)
tk.Label(exam_frame, text="Choose words:", font=("Arial", 14), bg='#4F93B8').pack(pady=5)

exam_nav_frame = tk.Frame(exam_frame, bg='#4F93B8')
exam_nav_frame.pack(pady=10)

tk.Button(exam_nav_frame, text="Last 20", command=show_last_20).pack(side=tk.LEFT, padx=5)
tk.Button(exam_nav_frame, text="Previous 20", command=show_previous_20).pack(side=tk.LEFT, padx=5)
tk.Button(exam_nav_frame, text="Failed", command=show_failed_words).pack(side=tk.LEFT, padx=5)
tk.Button(exam_nav_frame, text="Random", command=show_random_words).pack(side=tk.LEFT, padx=5)
tk.Button(exam_frame, text="Start Quiz", command=start_quiz, font=("Arial", 15), padx=20, pady=10).pack(pady=10)

tk.Button(exam_frame, text="Back to Menu", command=lambda: [exam_frame.pack_forget(), main_menu_frame.pack()], font=("Arial", 15)).pack(pady=10)


# === Start the main loop ===
window.mainloop()
