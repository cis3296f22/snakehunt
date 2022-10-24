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
On Windows:
Download snake-hunt.exe from the dist folder. Your antivirus software and Windows Defender may give you warnings about downloading the executable, but just ignore them. 

On Mac:
Download snake-hunt.exe from the snakehunt_mac folder. 

Alternatively, if you do not want to download an executable for Windows or Mac, or if you use Linux,

* Install Python (https://www.python.org/downloads/) (preferably version 3.7 or newer)
* Install Pygame (https://www.pygame.org/wiki/GettingStarted)
* Clone this repo
* Open a terminal
* Navigate to the cloned repo's root directory
* Enter the command `python snake-hunt.py` (or `python3 snake-hunt.py` depending on your Python version)

You now have a working copy of the game!

# Troubleshooting on Mac
When downloading the executable snake-hunt from GitHub, your Mac may give you the error message: “snake-hunt” can't be opened because Apple cannot check it for malicious software. 

To run the executable, do the following:
1. Click OK on the error message.
2. Choose the Apple menu  > System Preferences > Security & Privacy > General.
3. If the lock at the bottom left is locked , click it to unlock the preference panel. You may need to enter your password.
3.  Next to the message beginning with "snake-hunt" was blocked, click Allow Anyway.
4. Now, in your terminal, cd into your Downloads folder (or wherever you downloaded the executable to) and type the command ./snake-hunt. 
5. It may tell you permission denied: ./snake-hunt. In this case, you must change the permissions of the file by typing chmod 755 snake-hunt. Now you can type ./snake-hunt and it will begin to run.
6. It takes about 15 seconds to start up. Wait until a window pops up, and now you can play Snake Hunt by using the arrow keys to move!

# How to contribute
Follow this project board to know the latest status of the project: [https://github.com/orgs/cis3296f22/projects/97](https://github.com/orgs/cis3296f22/projects/97)  
