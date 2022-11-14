# Snake Hunt: A Multiplayer Web Game with Python
## John Bernardin, Jaffar Alzeidi, Sean Britt, Katrina Janeczko

### Description
A multiplayer snake game. Each player controls a snake. Each snake must avoid colliding with itself and other snakes, and consume pellets to grow. There will be a leaderboard which keeps track of the lengths of the snakes in-game. Upon starting the game, each player enters a name to distinguish themselves from other players. When two snakes collide, the larger snake consumes the smaller snake and gains a portion of its length. Food pellets are of random colors. When a snake consumes a pellet, its color changes to match that of the pellet that it consumed.

### Links:
* Katrina's Original Proof of Concept GitHub Repo: https://github.com/katrinajaneczko/snake-game
* Project Proposal Doc: https://docs.google.com/document/d/1Yl-RqufEqbRA9tiASvdXXW6PVBQkL_xODWGyHY7tYbM/edit?usp=sharing
* Vision Statement Doc: https://docs.google.com/document/d/1s-oI0ZeV8gtgRm2gVKJcQJro9EUkMLNex4oKgRsP6x0/edit?usp=sharing
* Four Personas Doc: https://docs.google.com/document/d/1Wj0bjpiVvBNf44rSyA2jAdtV-C6_LgCzSFIdO1QHEFA/edit?usp=sharing
* Project Board: https://github.com/orgs/cis3296f22/projects/97/views/1
* Canvas Project Scrum Assignment: https://templeu.instructure.com/courses/111775/assignments/1684194?module_item_id=4334499
* Canvas Final Project Assignment: https://templeu.instructure.com/courses/111775/assignments/1684177
* Final Project Slideshow: https://docs.google.com/presentation/d/1NVaFhOVlrwaS7WHmIXqEa2vlAmIVo0nabkphQpIDJ8U/edit?usp=sharing

![Snake hunt screenshot](/mockup.png)

# How to run
On Windows and Mac:
1. Download `server.exe` (Windows) or `server` (Mac) from the latest release, this will now be called the server executable
2. Download `client.exe` (Windows) or `client` (Mac) from the latest release, this will now be called the client executable
3. Open the server executable. Ignore the warning messages, you can trust us!
4. A terminal will pop up, **note the IP and port number**.
5. Open the client executable, also ignore warning messages.
6. A terminal will pop up prompting an input for IP, enter the IP found at step 4
7. Enter port number found at step 4
8. Repeat 5 - 7 to connect multiple clients (from a single computer, you can open multiple terminals and open the client executable in each terminal)

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

# Troubleshooting on Mac
When downloading the executable snake-hunt from GitHub, your Mac may give you the error message: `“snake-hunt” can't be opened because Apple cannot check it for malicious software.` 

To run the executable, do the following:
1. Click `OK` on the error message.
2. Choose the `Apple menu`  > `System Preferences` > `Security & Privacy` > `General`.
3. If the lock at the bottom left is locked , click it to unlock the preference panel. You may need to enter your password.
3. Next to the message beginning with `"client"` or `"server"` was blocked, click `Allow Anyway`.
4. Now, in your terminal, cd into your Downloads folder (or wherever you downloaded the executable to) and type the command `./client` and/or `./server`. 
5. It may tell you `permission denied: ./client` and/or `./server`. In this case, you must change the permissions of the file by typing `chmod 755 server` (or `chmod 755 client`). Now you can type `./client` or `./server` and it will begin to run.

# How to contribute
Follow this project board to know the latest status of the project: [https://github.com/orgs/cis3296f22/projects/97](https://github.com/orgs/cis3296f22/projects/97)  
