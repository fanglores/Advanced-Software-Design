This is an individual programming and design analysis task for two weeks.

Please submit solutions to the Project submit form. No video or slides are needed.

You are asked to practice design methods to solve classical software design problems using Java8+ or Python3.

Problem A. Key Word in Context (KWIC)
For problem description see https://en.wikipedia.org/wiki/Key_Word_in_Context 

Problem B. Eight Queens (8Q)
For problem description see https://en.wikipedia.org/wiki/Eight_queens_puzzle 

Method 1. Abstract Data Types
This is similar to object-oriented design method, use any of the approaches to identify classes and provide rationale for eliciting them.

Method 2. Main/Subroutine with stepwise refinement (also Shared Data)
See Parnas paper for description of the method. Try to follow the steps of the procedure as closely as possible.

Method 3. Pipes-and-filters
See Garlan and Shaw paper for description of the method. 
Most of the time you would implement this as a set of independent programs connected using primitive data pipes. There should be no direct invocations between modules / programs.

Method 4. Implicit invocation (event-driven)
See Garlan and Shaw paper for description of the method.
In general, any asynchronous or event-driven programming framework will help. 
A simpler solution could employ the Observer/Listener pattern instead of direct invocations.

What to do:  
1. Apply any of the methods to solve Problem A and any other method to solve Problem B. A total of two implementations.
2. Compare your solution to problems A and B with the solutions by two of your teammates (or classmates if less than three in a team) who applied different methods. 
3. Use the following checklist: 
  a) in which case it is easier to change the implementation algorithm in each of the modules? 
  b) in which solution it is easier (= seemingly less effort) to change data representation  
  c) in which solution it is easier to add additional functions to the modules
  d) which solution is seemingly more performant?
  e) if you are asked to implement a similar program, which of the solutions would you reuse?

Show the results as a table. Justify and explain the comparison.


Try to combine your results into a single table for all methods. Put the table in markdown to the repository

You get +1 individual point for solving two tasks at step 1. and another +1 point for comparing solutions at step 2.

Please put your individual solution to the team project repository and submit a direct link to the solution. Supply a readme along with the solution on how to run it and a sample input if needed.

References:
1. "On the criteria to be used in decomposing systems into modules" by D L Parnas
2. "An Introduction to Software Architecture" by David Garlan and Mary Shaw
