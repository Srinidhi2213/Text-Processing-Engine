import sys
import os
from src.engine import TextProcessingEngine

def main():
    SEP = "=" * 30
    MENU = (
        f"{SEP}\n"
        f"{'TEXT PROCESSING ENGINE'.center(30, ' ')}\n"
        f"{SEP}\n"
        "Enter 1 - Autocomplete\n"
        "Enter 2 - Pattern Search\n"
        "Enter 3 - Spell Correction\n"
        "Enter 0 - Quit\n"
        f"{SEP}"
    )
    print(MENU)

    engine = TextProcessingEngine()
    try:
        raw_src = sys.argv[1]
        corpus = engine.read_file(raw_src)
        engine.load_text(corpus, source_name=raw_src)
        src_name = os.path.basename(raw_src)
    except IndexError:
        raw_src = "corpus.txt"
        try:
            corpus = engine.read_file(raw_src)
            engine.load_text(corpus, source_name=raw_src)
            src_name = "corpus.txt"
        except FileNotFoundError:
            print("Error: 'corpus.txt' not found and no file provided via CLI arguments.")
            sys.exit(1)

    while True:
        try:
            choice_str = input("\n> Command: ").strip()
            if not choice_str:
                continue
            choice = int(choice_str)
        except ValueError:
            print("  Invalid input. Please enter a number.")
            continue
        
        if choice == 0:
            print("Session terminated!")
            break

        elif choice == 1:
            prefix = input("  Prefix: ").strip()
            suggestions = engine.autocomplete(prefix, 5)
            print(f"  Suggestions: {suggestions}")

        elif choice == 2:
            pattern = input("  Pattern: ").strip()
            search_results = engine.pattern_search(pattern)
            hits = search_results.get(src_name, [])
            print(f"  Hits at indices: {hits}")

        elif choice == 3:
            word = input("  Word: ").strip()
            suggestions = engine.correct(word, 3, 5)
            if suggestions:
                print(f"  Suggestions: {suggestions}")
            else:
                print("  Already Correct or no matches found!")

        else:
            print("  Invalid Option. Try 0, 1, 2, 3")

if __name__ == "__main__":
    main()