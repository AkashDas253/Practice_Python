from flashcard_core import add_flashcard, review_flashcards, load_flashcards, save_flashcards
from datetime import datetime, timedelta

def menu_add_flashcard():
	question = input('Enter question: ')
	answer = input('Enter answer: ')
	tags = input('Enter tags (comma separated): ').split(',')
	tags = [t.strip() for t in tags if t.strip()]
	add_flashcard(question, answer, tags)

def menu_review_all():
	review_flashcards()

def menu_review_by_tag():
	tag = input('Enter tag to review: ').strip()
	review_flashcards(tag)

def menu_ai_suggested_flashcard():
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
		print('No cards to suggest for review!')
		return
	def card_score(card):
		if card['last_reviewed'] is None:
			return (card['interval'], float('inf'))
		try:
			last = datetime.strptime(card['last_reviewed'], '%Y-%m-%d %H:%M:%S')
		except Exception:
			last = datetime.strptime(card['last_reviewed'], '%Y-%m-%d')
		hours_since = (now - last).total_seconds() / 3600
		return (card['interval'], hours_since)
	suggested = min(due_cards, key=card_score)
	print('\nAI-Suggested Flashcard:')
	print(f"Q: {suggested['question']}")
	print(f"Tags: {', '.join(suggested.get('tags', []))}")
	input('Press Enter to see the answer...')
	print(f"A: {suggested['answer']}")
	correct = input('Did you get it right? (y/n): ').strip().lower()
	if correct == 'y':
		suggested['interval'] = min(suggested['interval'] * 2, 24)
	else:
		suggested['interval'] = 1
	suggested['last_reviewed'] = now.strftime('%Y-%m-%d %H:%M:%S')
	save_flashcards(cards)
	print('Review complete!')

def main_menu():
	while True:
		print('\nAI-Powered Flashcards')
		print('Intervals are now in hours (cards can be due multiple times per day).')
		print('1. Review all due flashcards')
		print('2. AI-suggested flashcard')
		print('3. Add flashcard')
		print('4. Review by tag')
		print('5. Exit')
		choice = input('Choose an option: ')
		if choice == '1':
			menu_review_all()
		elif choice == '2':
			menu_ai_suggested_flashcard()
		elif choice == '3':
			menu_add_flashcard()
		elif choice == '4':
			menu_review_by_tag()
		elif choice == '5':
			break
		else:
			print('Invalid choice!')

if __name__ == '__main__':
	main_menu()
