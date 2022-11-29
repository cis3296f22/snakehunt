# Snake Hunt: A Multiplayer Web Game with Python
### John Bernardin, Jaffar Alzeidi, Sean Britt, Katrina Janeczko

## Description
A multiplayer snake game. Each player controls a snake. Each snake must avoid colliding with itself and other snakes, and consume pellets to grow. A leaderboard keeps track of the lengths of the snakes in game. Upon starting the game, each player enters a name to distinguish themselves from other players. When a snake consumes a pellet, it adds a block of that color to its body. Music and sound effects play as a player navigates its snake around the board, whose borders wrap around and whose center remains the player's snake. 
<img width="495" alt="Screen Shot 2022-11-28 at 10 28 21 PM" src="https://user-images.githubusercontent.com/73796086/204431645-88d2bb55-bf96-46f3-ba13-0d6410ddb9f7.png">

## How to run
On Windows and Mac:
1. Download `server.exe` (Windows) or `server` (Mac) from the latest release, this will now be called the server executable
2. Download `client.exe` (Windows) or `client` (Mac) from the latest release, this will now be called the client executable
3. Open the server executable. Ignore the warning messages, you can trust us!
4. A terminal will pop up, **note the IP and port number**. 
<img width="513" alt="Screen Shot 2022-11-28 at 10 29 57 PM" src="https://user-images.githubusercontent.com/73796086/204432021-766e6d84-a402-4d1a-aa87-980c201fd56e.png">
5. Open the client executable, also ignore warning messages.
6. A terminal will pop up prompting an input for IP, enter the IP found at step 4
7. Enter port number found at step 4
<img width="509" alt="Screen Shot 2022-11-28 at 10 32 54 PM" src="https://user-images.githubusercontent.com/73796086/204432284-3cb7724f-4dfa-471e-8a6a-f3e946a2170d.png">
8. A window will pop up prompting for a name. Enter a name under 32 characters and press `Play` to begin gameplay from your client!
<img width="276" alt="Screen Shot 2022-11-28 at 10 38 40 PM" src="https://user-images.githubusercontent.com/73796086/204432857-ce3d15e2-60de-4f1a-b143-33095cd75727.png">
9. Repeat 5 - 8 to connect multiple clients (from a single computer, you can open multiple terminals and open the client executable in each terminal)
10. To exit the game from the client, cick the red `x` in the upper left corner. To shut down the server, type 'exit' in the terminal.

## Alternate way to run
Alternatively, if you do not want to download an executable for Windows or Mac, or if you use Linux,

* Install Python (https://www.python.org/downloads/) (preferably version 3.7 or newer)
* Install Pygame (https://www.pygame.org/wiki/GettingStarted)
* Clone this repo
* Open a terminal
* Navigate to the cloned repo's root directory
* Enter the command `python server.py` (or `python3 server.py` depending on your Python version)
* Enter the command `python client.py` (or `python3 client.py` depending on your Python version)
* Follow steps 4-8 from the Windows and Mac instructions above. 

You now have a working copy of the game!

## Troubleshooting on Mac
When downloading the executable snake-hunt from GitHub, your Mac may give you the error message: `“snake-hunt” can't be opened because Apple cannot check it for malicious software.` 

To run the executable, do the following:
1. Click `OK` on the error message.
2. Choose the `Apple menu`  > `System Preferences` > `Security & Privacy` > `General`.
3. If the lock at the bottom left is locked , click it to unlock the preference panel. You may need to enter your password.
3. Next to the message beginning with `"client"` or `"server"` was blocked, click `Allow Anyway`.
4. Now, in your terminal, cd into your Downloads folder (or wherever you downloaded the executable to) and type the command `./client` and/or `./server`. 
5. It may tell you `permission denied: ./client` and/or `./server`. In this case, you must change the permissions of the file by typing `chmod 755 server` (or `chmod 755 client`). Now you can type `./client` or `./server` and it will begin to run.
6. If you are still having trouble, you may need to follow the instructions for cloning the repository and running the code directly from the terminal.

## How to play
* Use the Up/Down/Left/Right arrow keys to navigate the snake
* Use your computer's volume controls to turn the sound up or down

## How to contribute
Follow this project board to know the latest status of the project: [https://github.com/orgs/cis3296f22/projects/97](https://github.com/orgs/cis3296f22/projects/97)  
