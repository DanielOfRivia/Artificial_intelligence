In this assignment you will be creating a CSP solver for the domain of Battleship Solitaire puzzles. This will require you to encode these puzzles as a constraint satisfaction problem (CSP), implement the CSP solver, and use that to solve the puzzles we provide.

There are 8 possible characters for this section of the input file:

‘0’ (zero) represents no hint for that square
‘S’ represents a submarine,
‘W’ represents water
‘L’ represents the left end of a horizontal ship,
‘R’ represents the right end of a horizontal ship,
‘T’ represents the top end of a vertical ship, 
‘B’ represents the bottom end of a vertical ship, and
'M' represents a middle segment of a ship (horizontal or vertical).

To run the battle.py script provide two arguments from the command line: the names of the input and output files.

python3 battle.py <input file> <output file>

To validate the script follow the instructions inside battle_validate.py file
