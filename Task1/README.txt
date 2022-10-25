Task1 
For this assignment, you will be implementing a solver for the Hua Rong Dao sliding puzzle game. Hua Rong Dao is a sliding puzzle that is popular in China. Check out the following page for some background story on the puzzle and an English description of the rules. http://chinesepuzzles.org/huarong-pass-sliding-block-puzzle/

You will implement two search algorithms: A* search and Depth-first search.

Two Heuristic Functions for A* Search If we want A* search to find an optimal solution, we need to provide it with an admissible heuristic function. You will implement two admissible heuristic functions for A* search.

You will first implement the Manhattan distance heuristic, the simplest admissible heuristic function for this problem. Suppose that we relax the problem such that the pieces can overlap. Given this relaxation, we can solve the puzzle by moving the 2x2 piece over the other pieces towards the goal. The cost of this solution would be the Manhattan distance between the 2x2 piece and the bottom opening. For example, for the most classic initial configuration, the heuristic value is 3.

Next, propose another advanced heuristic function that is admissible but dominates the Manhattan distance heuristic. Implement this heuristic function. Explain why this heuristic function is admissible and dominates the Manhattan distance heuristic.
