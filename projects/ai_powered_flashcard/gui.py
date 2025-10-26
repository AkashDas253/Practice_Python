import tkinter as tk
from tkinter import messagebox, simpledialog
from flashcard_core import add_flashcard, review_flashcards, load_flashcards, save_flashcards
from datetime import datetime, timedelta

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title('AI Powered Flashcard')
        self.menu_frame = tk.Frame(root)
        self.menu_frame.pack(padx=10, pady=10)
        tk.Label(self.menu_frame, text='AI Powered Flashcard', font=('Arial', 16)).pack(pady=5)
        tk.Button(self.menu_frame, text='Review All Due Flashcards', command=self.review_all).pack(fill='x', pady=2)
        tk.Button(self.menu_frame, text='Review AI-Suggested Flashcard', command=self.ai_suggested).pack(fill='x', pady=2)
        tk.Button(self.menu_frame, text='Add New Flashcard', command=self.add_flashcard).pack(fill='x', pady=2)
        tk.Button(self.menu_frame, text='Review Flashcards by Tag', command=self.review_by_tag).pack(fill='x', pady=2)
        tk.Button(self.menu_frame, text='Exit', command=self.root.quit).pack(fill='x', pady=2)

    def add_flashcard(self):
        question = simpledialog.askstring('Add Flashcard', 'Enter question:')
        if not question:
            return
        answer = simpledialog.askstring('Add Flashcard', 'Enter answer:')
        if not answer:
            return
        tags = simpledialog.askstring('Add Flashcard', 'Enter tags (comma separated):')
        tags = [t.strip() for t in tags.split(',')] if tags else []
        add_flashcard(question, answer, tags)
        messagebox.showinfo('Success', 'Flashcard added!')

    def review_all(self):
        cards = load_flashcards()
        now = datetime.now()
        due_cards = []
        for card in cards:
            if card['last_reviewed'] is None:
                due_cards.append(card)
            else:
                try:
                    last = datetime.strptime(card['last_reviewed'], '%Y-%m-%d %H:%M:%S')
                except Exception:
                    last = datetime.strptime(card['last_reviewed'], '%Y-%m-%d')
                if now >= last + timedelta(hours=card['interval']):
                    due_cards.append(card)
        if not due_cards:
            messagebox.showinfo('Review', 'No cards to review!')
            return
        for card in due_cards:
            self.review_card(card, cards)

    def review_by_tag(self):
        tag = simpledialog.askstring('Review by Tag', 'Enter tag:')
        if not tag:
            return
        cards = load_flashcards()
        now = datetime.now()
        due_cards = []
        for card in cards:
            card_tags = [t.strip().lower() for t in card.get('tags', [])]
            if tag.strip().lower() not in card_tags:
                continue
            if card['last_reviewed'] is None:
                due_cards.append(card)
            else:
                try:
                    last = datetime.strptime(card['last_reviewed'], '%Y-%m-%d %H:%M:%S')
                except Exception:
                    last = datetime.strptime(card['last_reviewed'], '%Y-%m-%d')
                if now >= last + timedelta(hours=card['interval']):
                    due_cards.append(card)
        if not due_cards:
            messagebox.showinfo('Review', 'No cards to review for this tag!')
            return
        for card in due_cards:
            self.review_card(card, cards)

    def ai_suggested(self):
        cards = load_flashcards()
        now = datetime.now()
        due_cards = []
        for card in cards:
            if card['last_reviewed'] is None:
                due_cards.append(card)
            else:
                try:
                    last = datetime.strptime(card['last_reviewed'], '%Y-%m-%d %H:%M:%S')
                except Exception:
                    last = datetime.strptime(card['last_reviewed'], '%Y-%m-%d')
                if now >= last + timedelta(hours=card['interval']):
                    due_cards.append(card)
        if not due_cards:
            messagebox.showinfo('AI Suggestion', 'No cards to suggest!')
            return
        def card_score(card):
            if card['last_reviewed'] is None:
                return (card.get('interval', 1), float('inf'))
            try:
                last = datetime.strptime(card['last_reviewed'], '%Y-%m-%d %H:%M:%S')
            except Exception:
                last = datetime.strptime(card['last_reviewed'], '%Y-%m-%d')
            hours_since = (now - last).total_seconds() / 3600
            return (card.get('interval', 1), hours_since, -card.get('score', 0))
        suggested = min(due_cards, key=card_score)
        self.review_card(suggested, cards)

    def review_card(self, card, cards):
        q = f"Q: {card['question']}\nTags: {', '.join(card.get('tags', []))}"
        messagebox.showinfo('Review', q)
        a = f"A: {card['answer']}"
        messagebox.showinfo('Answer', a)
        correct = messagebox.askyesno('Result', 'Did you get it right?')
        now = datetime.now()
        if correct:
            card['interval'] = min(card['interval'] * 2, 24)
            card['score'] = card.get('score', 0) - 1
        else:
            card['interval'] = 1
            card['score'] = card.get('score', 0) + 1
        card['last_reviewed'] = now.strftime('%Y-%m-%d %H:%M:%S')
        save_flashcards(cards)

if __name__ == '__main__':
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()
