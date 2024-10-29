"""Main module for the Streamlit app"""

import csv

import streamlit as st

from word import Direction, Position, Word
from grid import display_grid

# Load the crossword puzzle


def read_data(file_path: str) -> list[Word]:
    """Read the crossword puzzle data."""
    words = []
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:

            position = Position(int(row[0]), int(row[1]))
            direction = Direction(1 if row[2] == "Across" else 2)

            word = Word(position, direction, row[4], row[5], int(row[3]))
            words.append(word)

    words.sort(key=lambda x: x.number)
    return words


# Define a function to update the grid based on submitted inputs
def submit_all_answers(inputs: dict[Word, str]) -> int:
    """Update the grid based on the submitted answers."""

    score = 0
    for word, user_input in inputs.items():
        # Validate input length

        if user_input == word.word:
            score += len(word.word)

        if user_input and len(user_input) == len(word.word):
            for i, char in enumerate(user_input):
                if word.direction == Direction.ACROSS:
                    st.session_state["entries"][word.position.row][
                        word.position.col + i
                    ].add(char.title())
                else:
                    st.session_state["entries"][word.position.row + i][
                        word.position.col
                    ].add(char.title())
        elif user_input:
            st.warning(
                f"Answer for '{word.display_clue}' must be {len(word.word)} characters long."
            )

        return score


def main():
    """Main function for the Streamlit app."""

    st.title("APH Crossword Puzzle")

    st.markdown(
        "Welcome to the APH Crossword Puzzle! Enter your answers in the grid below. "
        "You can submit your answers all at once by clicking the 'Submit' button at the bottom of the page. "
        "You can also revise your answers as many times as you like and your score will be updated accordingly. "
        "Good luck!"
    )

    puzzle = read_data("crossword_clues.csv")

    num_grid_rows = max(
        word.position.row + word.length
        for word in puzzle
        if word.direction == Direction.DOWN
    )
    num_grid_cols = max(
        word.position.col + word.length
        for word in puzzle
        if word.direction == Direction.ACROSS
    )

    if "entries" not in st.session_state:
        st.session_state["entries"] = [
            [set() for _ in range(num_grid_cols)] for _ in range(num_grid_rows)
        ]

    display_grid(puzzle, num_grid_rows, num_grid_cols)

    inputs = {}

    st.markdown("## Clues")
    st.write("Enter your answers below:")

    for word in puzzle:
        inputs[word] = st.text_input(f"{word.display_clue}", key=word.number)

    # Single submit button to update all answers
    if st.button("Submit"):
        st.session_state["entries"] = [
            [set() for _ in range(num_grid_cols)] for _ in range(num_grid_rows)
        ]
        score = submit_all_answers(inputs)
        st.rerun()  # Rerun the app to update the displayed grid

    else:
        score = 0

    st.markdown(f"## Current Score: {score} / {len(puzzle)}")


if __name__ == "__main__":
    main()
