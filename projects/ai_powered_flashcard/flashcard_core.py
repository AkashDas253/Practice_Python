import json
import os
from datetime import datetime, timedelta

FLASHCARDS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flashcards.json')

def load_flashcards():
    if not os.path.exists(FLASHCARDS_FILE):
        return []
    with open(FLASHCARDS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_flashcards(cards):
    with open(FLASHCARDS_FILE, 'w', encoding='utf-8') as f:
        json.dump(cards, f, indent=2)

def add_flashcard(question, answer, tags):
    cards = load_flashcards()
    cards.append({
        'question': question,
        'answer': answer,
        'tags': tags,
        'last_reviewed': None,
        'interval': 1,  # interval in hours
    })
    save_flashcards(cards)
    print('Flashcard added!')

def review_flashcards(tag=None):
    cards = load_flashcards()
    now = datetime.now()
    due_cards = []
    tag_normalized = tag.strip().lower() if tag else None
    for card in cards:
        card_tags = [t.strip().lower() for t in card.get('tags', [])]
        if tag_normalized and tag_normalized not in card_tags:
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
    for idx, card in enumerate(due_cards, 1):
        print(f"\nCard {idx} of {len(due_cards)}")
        print(f"Q: {card['question']}")
        print(f"Tags: {', '.join(card.get('tags', []))}")
        input('Press Enter to see the answer...')
        print(f"A: {card['answer']}")
        correct = input('Did you get it right? (y/n): ').strip().lower()
        if correct == 'y':
            card['interval'] = min(card['interval'] * 2, 24)  # max 24 hours
        else:
            card['interval'] = 1
        card['last_reviewed'] = now.strftime('%Y-%m-%d %H:%M:%S')
    save_flashcards(cards)
    print('Review session complete!')
