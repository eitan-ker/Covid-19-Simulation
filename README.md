# Covid-19-Simulation

A simulation of a disease outbreak. The simulation allows the user to input parameters such as the number of people, the number of healthy individuals, the number of sick individuals, the number of recovering individuals, the percentage of infection for healthy individuals, the percentage of infection for recovering individuals, and the number of sick iterations.

The simulation creates a GUI using the Pygame library and prompts the user to enter the input parameters. Once the parameters are entered, the simulation runs and displays the progress of the disease outbreak in a graphical form.

The code initializes several variables and Pygame Rect objects to define the position and dimensions of various GUI elements such as input boxes and buttons. The code uses the Pygame event loop to handle user input events such as mouse clicks and keyboard input.

The code also performs error checking to ensure that the user enters valid input parameters. If the user enters invalid parameters, the simulation displays an error message and prompts the user to try again.

**The Game** class has a constructor that initializes various parameters, such as the size of the grid, the probability of an infected cell spreading the disease to its neighbors, etc. The make_sections() method creates a grid and updates it to the display screen. The update() method is responsible for updating the status of each cell of the grid according to the rules of the simulation. For instance, healthy cells might get infected, or cells infected for too long might recover.

**The Grid** class contains information about the cells of the grid. It is responsible for creating the grid and initializing its cells. There are several helper functions inside the Grid class, such as add_sick_cell(), which updates the number of infected cells in the grid, or make_shuffled_list(), which creates a shuffled list of cell states.

**The Cell** Class defines the properties and behavior of a cell. The class has instance-level attributes that represent the state of the cell, its color, and its location on a grid. The class also has methods that allow the cell to change its state, calculate its neighbors, and count the number of generations it has been in its current state.
