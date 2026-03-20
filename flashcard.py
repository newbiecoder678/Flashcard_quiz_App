import json
import os
import random
import sys


CARDS_FILE = "cards.json"


def load_cards():
    """Load flashcards from JSON file."""
    if not os.path.exists(CARDS_FILE):
        return []
    with open(CARDS_FILE, "r") as f:
        return json.load(f)


def save_cards(cards):
    """Save flashcards to JSON file."""
    with open(CARDS_FILE, "w") as f:
        json.dump(cards, f, indent=2)


def add_card(cards):
    """Add a new flashcard."""
    print("\n--- Add a New Flashcard ---")
    question = input("Question: ").strip()
    if not question:
        print("Question cannot be empty.")
        return
    answer = input("Answer: ").strip()
    if not answer:
        print("Answer cannot be empty.")
        return
    cards.append({"question": question, "answer": answer, "correct": 0, "attempts": 0})
    save_cards(cards)
    print("✓ Flashcard added!")


def list_cards(cards):
    """List all flashcards."""
    if not cards:
        print("\nNo flashcards yet. Add some first!")
        return
    print(f"\n--- Your Flashcards ({len(cards)} total) ---")
    for i, card in enumerate(cards, 1):
        accuracy = (
            f"{int(card['correct'] / card['attempts'] * 100)}%"
            if card["attempts"] > 0
            else "N/A"
        )
        print(f"{i}. Q: {card['question']}")
        print(f"   A: {card['answer']}  |  Accuracy: {accuracy}")
        print()


def delete_card(cards):
    """Delete a flashcard by number."""
    if not cards:
        print("\nNo flashcards to delete.")
        return
    list_cards(cards)
    try:
        choice = int(input("Enter card number to delete (0 to cancel): "))
        if choice == 0:
            return
        if 1 <= choice <= len(cards):
            removed = cards.pop(choice - 1)
            save_cards(cards)
            print(f"✓ Deleted: \"{removed['question']}\"")
        else:
            print("Invalid number.")
    except ValueError:
        print("Please enter a valid number.")


def quiz(cards):
    """Run a quiz session."""
    if not cards:
        print("\nNo flashcards yet. Add some first!")
        return

    print("\n--- Quiz Mode ---")
    print(f"Cards available: {len(cards)}")
    try:
        n = input(f"How many cards to quiz on? (1-{len(cards)}, Enter for all): ").strip()
        if n == "":
            n = len(cards)
        else:
            n = int(n)
            if not (1 <= n <= len(cards)):
                print("Invalid number.")
                return
    except ValueError:
        print("Please enter a valid number.")
        return

    deck = random.sample(cards, n)
    correct_count = 0

    print("\nType your answer and press Enter. Press Ctrl+C to quit early.\n")

    try:
        for i, card in enumerate(deck, 1):
            print(f"Card {i}/{n}")
            print(f"Q: {card['question']}")
            user_answer = input("Your answer: ").strip()

            # Find and update the original card
            for c in cards:
                if c["question"] == card["question"]:
                    c["attempts"] += 1
                    if user_answer.lower() == card["answer"].lower():
                        print("✓ Correct!\n")
                        correct_count += 1
                        c["correct"] += 1
                    else:
                        print(f"✗ Incorrect. The answer was: {card['answer']}\n")
                    break

    except KeyboardInterrupt:
        print("\n\nQuiz interrupted.")

    save_cards(cards)
    print(f"--- Quiz Complete ---")
    print(f"Score: {correct_count}/{n}  ({int(correct_count / n * 100)}%)")

    if correct_count == n:
        print("Perfect score! Amazing work!")
    elif correct_count >= n * 0.8:
        print("Great job! Keep it up!")
    elif correct_count >= n * 0.5:
        print("Good effort! Keep practicing!")
    else:
        print("Keep studying — you'll get there!")


def reset_stats(cards):
    """Reset all card statistics."""
    if not cards:
        print("\nNo flashcards to reset.")
        return
    confirm = input("\nReset all stats? This cannot be undone. (yes/no): ").strip().lower()
    if confirm == "yes":
        for card in cards:
            card["correct"] = 0
            card["attempts"] = 0
        save_cards(cards)
        print("✓ All stats reset.")
    else:
        print("Cancelled.")


def main():
    print("╔══════════════════════════════╗")
    print("║     CS50 Flashcard Quiz      ║")
    print("╚══════════════════════════════╝")

    cards = load_cards()

    while True:
        print("\nWhat would you like to do?")
        print("  1. Start Quiz")
        print("  2. Add Flashcard")
        print("  3. View All Cards")
        print("  4. Delete a Card")
        print("  5. Reset Stats")
        print("  6. Quit")

        choice = input("\nEnter choice (1-6): ").strip()

        if choice == "1":
            quiz(cards)
        elif choice == "2":
            add_card(cards)
        elif choice == "3":
            list_cards(cards)
        elif choice == "4":
            delete_card(cards)
        elif choice == "5":
            reset_stats(cards)
        elif choice == "6":
            print("\nGoodbye! Keep studying! ")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter 1–6.")


if __name__ == "__main__":
    main()
