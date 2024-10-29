"""Module with functions for crossword puzzle grid."""

import streamlit as st

from word import Position, Word

html_table = '<div style="display: table;">'
html_row = '<div style="display: table-row">'
html_end = "</div>"


def html_cell(number: str = "", entry: str = ""):
    """Return the HTML for a table cell."""
    return f'<div style="width: 60px; height: 60px; display: table-cell; border: 1px solid white"> {number} {entry} </div>'


def html_blocked_cell():
    """Return the HTML for a blocked table cell."""
    return '<div style="width: 60px; height: 60px; display: table-cell; border: 1px solid white; background-color: white">  </div>'


def display_grid(puzzle: list[Word], num_grid_rows: int, num_grid_cols: int):

    valid_cells = list(word.cells for word in puzzle)
    valid_cells = [cell for sublist in valid_cells for cell in sublist]

    string = ""
    string += html_table
    for row in range(num_grid_rows):
        string += html_row
        for col in range(num_grid_cols):
            pos = Position(row, col)
            if pos in valid_cells:
                entry = ", ".join(st.session_state["entries"][row][col])
                if pos in [word.position for word in puzzle]:
                    word = [word for word in puzzle if word.position == pos][0]
                    string += html_cell(word.number, entry)
                else:
                    string += html_cell("", entry)
            else:
                string += html_blocked_cell()
        string += html_end
    string += html_end

    st.write(string, unsafe_allow_html=True)