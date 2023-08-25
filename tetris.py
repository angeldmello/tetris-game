# 900x900
import csv
import pickle
import time
from tkinter import *
from PIL import ImageTk, Image
from tkinter import Label
from tkinter import ttk
from random import shuffle
from copy import copy
 

class Game:
    def __init__(self):
        self.root = Tk()
        self.root.title("Tetris")
        self.root.geometry("900x900")
        self.root.configure(bg="#151d36")
        self.root.grid()
        self.pressed = "False"
        self.root.bind(
            "<KeyPress>", lambda event="<KeyPress>": Game.KeyPress(self, event)
        )
        self.root.bind(
            "<KeyRelease>", lambda event="<KeyRelease>": Game.KeyRelease(self, event)
        )  # Key binding defined in KeyPress and KeyRelease functions
        self.tetronimoes = {
            "shape1": {
                "index": [[0, 3], [0, 4], [0, 5], [0, 6]],
                "color": "#c4f1f5",
            },  # I-Block, Light Blue
            "shape2": {
                "index": [[1, 4], [1, 5], [1, 6], [0, 4]],
                "color": "#347deb",
            },  # J-Block, Medium Blue
            "shape3": {
                "index": [[1, 4], [1, 5], [1, 6], [0, 6]],
                "color": "#f58d4c",
            },  # L-Block, Orange
            "shape4": {
                "index": [[1, 4], [1, 5], [1, 6], [0, 5]],
                "color": "#cb94eb",
            },  # T-Block, Lavender
            "shape5": {
                "index": [[0, 4], [1, 5], [0, 5], [1, 6]],
                "color": "#e65369",
            },  # Z-Block, Red
            "shape6": {
                "index": [[0, 6], [1, 5], [1, 4], [0, 5]],
                "color": "#b4f0a8",
            },  # S-Block, Green
            "shape7": {
                "index": [[0, 5], [0, 6], [1, 5], [1, 6]],
                "color": "#ffee80",
            },  # O-Block, Yellow
        }

        self.gridFrame = Frame(bg="White")
        self.gameGrid = (
            list()
        )  # Gameplay takes place in a square grid containing labels as shapes
        for i in range(19):
            self.gameGrid.append([])
            for x in range(10):
                self.gameGrid[i].append("")
                self.gameGrid[i][x] = Label(
                    self.gridFrame, height=2, width=4, bg="#151d36", bd=2
                )
                self.gameGrid[i][x].grid(row=i, column=x, padx=1, pady=1)
                self.gameGrid[i][x].occupied = "False"
        self.gridFrame.place(x=240)
        self.nextLabel = Label(
            font="Calibri 20 bold", text="NEXT", bg="#151d36", fg="White"
        )
        self.nextLabel.place(x=760, y=0)
        self.scoreLabel = Label(
            font="Calibri 20 bold", text="SCORE:", bg="#151d36", fg="White"
        )
        self.scoreLabel.place(x=740, y=500)
        self.gameScore = Label(
            font="Calibri 20 bold", text="0", bg="#151d36", fg="White"
        )
        self.gameScore.place(x=740, y=530)
        self.nextFrame = Frame(bg="White")
        self.nextShapeGrid = list()  # Creating a grid for the next shape
        for i in range(4):
            self.nextShapeGrid.append([])
            for x in range(4):
                self.nextShapeGrid[i].append("")
                self.nextShapeGrid[i][x] = Label(
                    self.nextFrame, height=2, width=4, bg="#151d36", bd=2
                )
                self.nextShapeGrid[i][x].grid(row=i, column=x, padx=1, pady=1)
        self.nextFrame.place(x=900, y=0)
        self.rowsCleared = 0  # Number of rows cleared
        self.gameGrid.reverse
        self.level = 1  # Difficulty level
        Game.levelUp(self)

        self.levelLabel = Label(
            font="Calibri 20 bold",
            text="Level: " + str(self.level),
            bg="#151d36",
            fg="White",
        )
        self.levelLabel.place(x=40, y=500)
        self.rowsClearedlabel = Label(
            font="Calibri 20 bold",
            text="Lines Cleared: " + str(self.rowsCleared),
            bg="#151d36",
            fg="White",
        )
        self.rowsClearedlabel.place(x=40, y=400)

        self.combo = 0  # Score combos for clearing lines
        self.score = 0
        self.speed = "Slow"
        self.interrupt = "False"
        self.holding = "False"  # Checks if a shape is currently being held
        self.running = "False"  # Stops mainloop from running more than once
        self.shapeDrop = "False"  # If a shape is currently falling
        self.direction = "None"
        self.time = self.gameTime
        self.clean = "N"
        self.endReached = "False"  # Chekcs if the top of the grid has been reached
        self.cpressed = "False"  # Checks whether the c key is currently being pressed
        self.bossPressed = False
        self.paused = False
        self.indexlist = list()  # Creating a list to choose shapes

        self.frame = Frame(self.root, width=900, height=900)
        self.nextFrame.place(x=700, y=50)
        self.saveButton = Button(
            self.root, text="Save Game", width="9", height="3", command=self.saveGame
        )
        self.saveButton.place(x=20, y=20)
        self.loadButton = Button(
            self.root, text="Load Game", width="9", height="3", command=self.loadGame
        )
        self.loadButton.place(x=130, y=20)
        self.myCanvas = Canvas(self.root, bg="white", height=900, width=870)

        Game.nextShape(self)
        Game.regSpeed(self)
        self.root.mainloop()

    def levelUp(self):
        # Increases speed after every level
        if self.level == 1:
            self.gameTime = 1000
        elif self.level > 1:
            self.gameTime = 500
        elif self.level > 2:
            self.gameTime = 250
        elif self.level > 3:
            self.gameTime = 200

    def regSpeed(self):
        self.speed = "Slow"
        if self.endReached == "False" and self.time != int(self.gameTime / 10):
            Game.freeFall(self)
            Game.scoreAndLineClear(self)
            self.running = "True"
            self.time = copy(self.gameTime)
            self.root.after(self.time, Game.regSpeed, self)
        else:
            self.running = "False"

    def highSpeed(self):
        self.speed = "Medium"
        if self.endReached == "False" and self.time != self.gameTime:
            Game.freeFall(self)
            Game.scoreAndLineClear(self)
            self.time = int(copy(self.gameTime) / 10)
            self.root.after(self.time, Game.highSpeed, self)

    def scoreAndLineClear(self):
        totalamount = 0
        lines = 0
        if self.endReached == "False":
            for i in range(19):
                amount = 0
                for x in range(10):
                    if self.gameGrid[i][x].occupied == "True":
                        amount += 1
                        totalamount += 1
                    elif self.gameGrid[i][x].occupied == "Player":
                        found = "N"
                        for z in range(4):
                            if len(self.playing) == 4:
                                if i == self.playing[z][0] and x == self.playing[z][1]:
                                    found = "Y"
                        if found == "N":
                            self.gameGrid[i][x].occupied = "False"
                            self.gameGrid[i][x].configure(bg="#151d36")
                        self.clean = "N"

                if amount == 10:
                    totalamount -= 10
                    lines += 1
                    self.rowsCleared += 1
                    self.rowsClearedlabel.configure(
                        text="Rows Cleared: " + str(self.rowsCleared)
                    )
                    for z in range(10):
                        self.gameGrid[i][z].configure(bg="#151d36")
                        self.gameGrid[i][z].occupied = "False"

                    # Removing cleared line and lowering the above line
                    for a in range(i):
                        for b in range(10):
                            lower = i - a
                            if self.gameGrid[lower][b].occupied == "True":
                                colour = self.gameGrid[lower][b]["bg"]
                                self.gameGrid[lower][b].configure(bg="#151d36")
                                self.gameGrid[lower][b].occupied = "False"
                                self.gameGrid[lower + 1][b].occupied = "True"
                                self.gameGrid[lower + 1][b].configure(bg=colour)
                    # Level increases for every row cleared
                    if self.rowsCleared > 2 and self.rowsCleared != 0:
                        self.level += 1
                        self.levelLabel.configure(text="Level: " + str(self.level))
                        Game.levelUp(self)
            # Scoring mechanism adds 150, 250, 350, ... points for every 1, 2, 3, ... lines cleared respectively
            if self.shapeDrop == "False":
                if lines > 0:
                    self.combo += 1
                else:
                    self.combo = 0
                if lines > 0:
                    clearpoints = [
                        0,
                        100,
                        200,
                        300,
                        400,
                        500,
                        600,
                    ]  # 1 row, 2 rows, 3 rows, 4 rows is the bonus for amount of rows clear at once
                    pointstoadd = clearpoints[self.rowsCleared]
                    pointstoadd += copy(self.combo) * 50
                    print(pointstoadd)
                    self.gameScore.configure(
                        text=str(int(self.gameScore["text"]) + pointstoadd)
                    )

    def nextShape(self):
        # Selects a shape from shuffled list
        for a in range(4):
            for b in range(4):
                self.nextShapeGrid[a][b].configure(bg="#151d36")
        if len(self.indexlist) == 0:
            self.indexlist = [1, 2, 3, 4, 5, 6, 7]
            shuffle(self.indexlist)
        if self.interrupt == "False":
            self.nextshapecopy = self.indexlist[
                0
            ]  # A copy of the nextshape to be used for getting held shapes
            self.nextshape = self.indexlist[0]
            del self.indexlist[0]
        else:
            self.nextshape = self.nextshapecopy
            self.interrupt = "False"
        shape = "shape" + str(self.nextshape)
        # Displays next shape on nextShapeGrid
        for z in range(4):
            if self.endReached == "False":
                i = copy(self.tetronimoes[shape]["index"][z][0])
                x = copy(self.tetronimoes[shape]["index"][z][1])
                self.color = self.tetronimoes[shape]["color"]
                self.nextShapeGrid[i + 1][x - 4].configure(bg=self.color)

    def freeFall(self):
        if self.endReached == "False":
            if self.shapeDrop == "False":
                self.shape = self.nextshape
                Game.nextShape(self)
                self.playing = list()
                self.shapeDrop = "True"
                shape = "shape" + str(self.shape)
                for z in range(4):
                    if self.endReached == "False":
                        self.playing.append(copy(self.tetronimoes[shape]["index"][z]))
                        i = copy(self.tetronimoes[shape]["index"][z][0])
                        x = copy(self.tetronimoes[shape]["index"][z][1])
                        self.color = self.tetronimoes[shape]["color"]
                        self.gameGrid[i][x].configure(bg=self.color)
                        if self.gameGrid[i][x].occupied == "True":
                            if self.endReached == "False":
                                self.endReached = "True"
                                global finalScore
                                finalScore = int((self.gameScore["text"]))
                                print(finalScore)
                                with open(
                                    "/Users/angeldmello/GitRepos/COMP16321-Labs_t37525ad/COMP16321-Labs_t37525ad/score.csv",
                                    "a",
                                ) as fobj:
                                    fobj.write(str(finalScore) + "\n")
                                fobj.close()
                                self.endScreen()
                        else:
                            self.gameGrid[i][x].occupied = "Player"
            else:
                verf = 0
                for z in range(4):
                    if len(self.playing) == 4:
                        i = self.playing[z][0]
                        x = self.playing[z][1]
                        if i < 18:
                            if self.gameGrid[i + 1][x].occupied != "True":
                                verf += 1

                if verf == 4:
                    if self.speed == "Medium":
                        multiplier = 1
                    elif self.speed == "Fast":
                        multiplier = 2
                    else:
                        multiplier = 0
                    pointstoadd = int((copy(self.level) + 1) / 2) * multiplier
                    self.gameScore.configure(
                        text=str(int(self.gameScore["text"]) + pointstoadd)
                    )

                tempValues = list()
                for z in range(4):
                    if len(self.playing) == 4:
                        i = self.playing[z][0]
                        x = self.playing[z][1]
                        if verf != 4:
                            self.shapeDrop = "False"
                            self.gameGrid[i][x].occupied = "True"
                            self.gameGrid[i][x].configure(bg=self.color)
                            if self.time == 1:
                                self.time = copy(self.gameTime)
                        else:
                            tempValues.append([i + 1, x])
                            self.gameGrid[i][x].occupied = "False"
                            self.gameGrid[i][x].configure(bg="#151d36")

                for z in range(len(tempValues)):
                    if len(self.playing) == 4:
                        self.playing[z] = tempValues[z]
                        i = self.playing[z][0]
                        x = self.playing[z][1]
                        self.gameGrid[i][x].configure(bg=self.color)
                        self.gameGrid[i][x].occupied = "Player"

    def move(self):
        if self.direction == "Left":
            changePos = -1
        else:
            changePos = 1
        if self.shapeDrop == "True":
            verf = 0
            for z in range(4):
                i = self.playing[z][0]
                x = self.playing[z][1]
                if x + changePos >= 0 and x + changePos <= 9:
                    if self.gameGrid[i][x + changePos].occupied != "True":
                        verf += 1

            tempValues = list()
            if verf == 4:
                for z in range(4):
                    i = self.playing[z][0]
                    x = self.playing[z][1]
                    tempValues.append([i, x + changePos])
                    self.gameGrid[i][x].occupied = "False"
                    self.gameGrid[i][x].configure(bg="#151d36")

            for z in range(len(tempValues)):
                self.playing[z] = tempValues[z]
                i = self.playing[z][0]
                x = self.playing[z][1]
                self.gameGrid[i][x].configure(bg=self.color)
                self.gameGrid[i][x].occupied = "Player"
        Game.scoreAndLineClear(self)

    def hold(self):
        # Cheatcode that clears and changes the current shape when c is pressed
        if self.holding == "True":
            self.nextshape = self.holdshape
            self.interrupt = "True"
        self.holding = "True"  # Put shape into hold box
        for z in range(len(self.playing)):
            self.gameGrid[self.playing[z][0]][self.playing[z][1]].configure(
                bg="#151d36"
            )
            self.gameGrid[self.playing[z][0]][self.playing[z][1]].occupied = "False"
        self.shapeDrop = "False"
        self.holdshape = copy(self.shape)
        shape = "shape" + str(copy(self.holdshape))
        for z in range(4):
            if self.endReached == "False":
                i = copy(self.tetronimoes[shape]["index"][z][0])
                x = copy(self.tetronimoes[shape]["index"][z][1])
                self.color = self.tetronimoes[shape]["color"]

    def saveGame(self):
        self.lastSave = []
        self.gridSave = []
        # Gets list of bg colors for every label in GameGrid
        for i in range(19):
            for x in range(10):
                self.filledBlocks = self.gameGrid[i][x]["bg"]
                self.gridSave.append(self.filledBlocks)
        chunk_size = 10
        self.gridList = [
            self.gridSave[i : i + chunk_size]
            for i in range(0, len(self.gridSave), chunk_size)
        ]

        # Gets list of important game information
        self.lastSave.append(self.score)
        self.lastSave.append(self.level)
        self.lastSave.append(self.rowsCleared)
        self.lastSave.append(self.gameTime)
        self.currentGrid = copy(self.gameGrid)

        # Stores serialized data
        with open("savedData.pickle", "wb") as saveData:
            pickle.dump(self.lastSave, saveData)
            pickle.dump(self.gridList, saveData)

    def loadGame(self):
        # Loads serialized data
        with open("savedData.pickle", "br") as loadData:
            loadedData = pickle.load(loadData)

        # Clears allblocks on the game grid
        for i in range(19):
            for x in range(10):
                self.gameGrid[i][x].configure(bg="#151d36")
        time.sleep(1)

        # Recreates loaded blocks on the game grid
        for i in range(19):
            for x in range(10):
                self.gameGrid[i][x].configure(bg=str(self.gridList[i][x]))

        self.score = loadedData[0]
        self.level = loadedData[1]
        self.rowsCleared = loadedData[2]
        self.gameTime = loadedData[3]

    def bossKey(self):
        # Press B to display and release Boss Key window
        self.bossPressed = not self.bossPressed
        if self.bossPressed == True:
            self.frame.place(x=0, y=0)
            image1 = Image.open(
                "/Users/angeldmello/GitRepos/COMP16321-Labs_t37525ad/COMP16321-Labs_t37525ad/stockmarket.jpg"
            )
            test = ImageTk.PhotoImage(image1)
            label1 = Label(self.frame, image=test)
            label1.image = test
            label1.place(x=0, y=-2)
            self.saveButton.place(x=900, y=900)
            self.loadButton.place(x=900, y=900)
        elif self.bossPressed == False:
            self.frame.place(x=900, y=900)
            self.saveButton.place(x=20, y=20)
            self.loadButton.place(x=130, y=20)
            
    def pause(self):
        # Press P to pause and unpause the game
        self.paused = not self.paused
        if self.paused == True:
            self.time = 0
            self.gameTime = 0
            self.frame2 = Frame(self.root, width=300, height=280)
            self.frame2.place(x=310, y=200)
            image2 = Image.open(
                "/Users/angeldmello/GitRepos/COMP16321-Labs_t37525ad/COMP16321-Labs_t37525ad/pause.jpeg"
            )
            test = ImageTk.PhotoImage(image2)
            label2 = Label(self.frame2, image=test)
            label2.image = test
            label2.place(x=-3, y=-3)
        elif self.paused == False:
            self.frame2.place(x=900, y=900)
            self.running = "True"
            self.root.after(self.time, Game.regSpeed, self)
            self.levelUp()
            self.speed = "Slow"

    def endScreen(self):
        # Canvas creates an ending screen after the game is over
        self.myCanvas.pack()
        self.image = PhotoImage(
            file="/Users/angeldmello/GitRepos/COMP16321-Labs_t37525ad/COMP16321-Labs_t37525ad/background.png"
        )
        self.myCanvas.create_image(0, 0, image=self.image, anchor="nw")
        buttonfont = 15
        self.quitButton = Button(
            self.myCanvas,
            text="Quit Game",
            font=("Calibri 22 bold", buttonfont),
            width="12",
            height="4",
            command=quit,
        )
        quitGame = self.myCanvas.create_window(
            440, 400, anchor=N, window=self.quitButton
        )
        textFont = 64
        scoreFont = 50
        widget = Label(
            self.myCanvas,
            text="Your Score:",
            font=("Calibri 22 bold", textFont),
            fg="white",
            bg="#151d36",
        )
        makeLabel = self.myCanvas.create_window(440, 110, window=widget)
        scoreText = str(finalScore)
        scoreWidget = Label(
            self.myCanvas,
            text=scoreText,
            font=("Calibri 22 bold", scoreFont),
            fg="white",
            bg="#151d36",
        )
        makeScore = self.myCanvas.create_window(440, 198, window=scoreWidget)
        self.playButton = Button(
            self.myCanvas,
            text="Play Again",
            font=("Calibri 22 bold", buttonfont),
            width="12",
            height="4",
            command=start,
        )
        playAgain = self.myCanvas.create_window(
            440, 300, anchor=N, window=self.playButton
        )

    def quit(self):
        # Closes the window on quitting the game
        self.root.destroy()

    def KeyPress(self, event):
        # Defines key press for movements, cheats, pause and boss key
        if self.pressed == "False":
            key = event.keysym
            self.pressed = "True"
            if self.time != 1:
                if key == "Left":
                    self.direction = "Left"
                    Game.move(self)

                elif key == "Right":
                    self.direction = "Right"
                    Game.move(self)

                # Increases speed of shape movement to go faster
                elif (
                    key == "Down"
                    and self.time != int(self.gameTime / 10)
                    and self.time != 1
                ):
                    self.time = int(copy(self.gameTime) / 10)
                    Game.highSpeed(self)

                elif key == "Up":
                    self.time = 1
                    while self.time == 1:
                        self.speed = "Fast"
                        Game.freeFall(self)
                        Game.scoreAndLineClear(self)

                # Cheatcode when c is pressed
                elif (
                    (key == "c" or key == "C")
                    and self.cpressed == "False"
                    and self.shapeDrop == "True"
                ):
                    self.cpressed = "True"
                    Game.hold(self)

                elif key == "p" or key == "P":
                    Game.pause(self)

                elif key == "b" or key == "B":
                    Game.bossKey(self)

    def KeyRelease(self, event):
        self.pressed = "False"
        key = event.keysym

        # Changes speed to regular if Down key is not pressed
        if key == "Down":
            self.time = copy(self.gameTime)
            if self.running == "False":
                Game.regSpeed(self)

        # Allows cheatcode to take place consecutively
        elif key == "c" or key == "C":
            self.cpressed = "False"


class StartUp:
    def __init__(self):
        # Creating a home page that includes the name input, play button, leaderboard
        self.window = Tk()
        self.window.geometry("870x900")
        self.window.title("Tetris Homepage")
        self.window["bg"] = "#151d36"

        self.framew = Frame(self.window, width=900, height=900)
        image3 = Image.open(
            "/Users/angeldmello/GitRepos/COMP16321-Labs_t37525ad/COMP16321-Labs_t37525ad/background.png"
        )
        test1 = ImageTk.PhotoImage(image3)
        label4 = Label(self.framew, image=test1)
        label4.place(x=10, y=0)
        self.framew.place(anchor="center", relx=0.5, rely=0.5)

        self.lbframe = Frame(self.window, bg="#151d36")
        self.leaderBoard = ttk.Treeview(self.lbframe)
        self.frame2 = Frame(self.window, width=700, height=100)
        self.frame2.pack(padx=25, pady=30)

        image5 = Image.open(
            "/Users/angeldmello/GitRepos/COMP16321-Labs_t37525ad/COMP16321-Labs_t37525ad/tetrislogo.png"
        )
        resized_image = image5.resize((600, 200))
        test2 = ImageTk.PhotoImage(resized_image)
        label5 = Label(self.frame2, image=test2)
        label5.image = test2
        label5.pack()

        global entername
        buttonfont = "15"
        entername = Entry(self.window, width="20", bg="white")
        entername.pack(pady=20)
        entryButton = Button(
            self.window,
            text="Play Game",
            font=("Calibri 22 bold", buttonfont),
            width="20",
            height="5",
            command=self.playGame,
        )
        entryButton.pack(padx=30, pady=20)

        self.lbframe.pack()
        self.leaderBoard.pack()
        self.leaderboard()
        self.window.mainloop()

    def playGame(self):
        # Saves name to file, destroys home page window on button click
        global username
        username = entername.get()
        with open(
            "/Users/angeldmello/GitRepos/COMP16321-Labs_t37525ad/COMP16321-Labs_t37525ad/score.csv",
            "a",
        ) as fobj:
            fobj.write(username + ",")
        fobj.close()
        self.window.destroy()

    def leaderboard(self):
        self.leaderBoard["columns"] = ("Rank", "Name", "Score")
        self.leaderBoard.column("#0", width=0, stretch=NO)
        self.leaderBoard.column("Rank", anchor=CENTER, width=60)
        self.leaderBoard.column("Name", anchor=CENTER, width=90)
        self.leaderBoard.column("Score", anchor=CENTER, width=90)
        self.leaderBoard.heading("#0", text="", anchor=CENTER)
        self.leaderBoard.heading("Rank", text="Rank", anchor=CENTER)
        self.leaderBoard.heading("Name", text="Name", anchor=CENTER)
        self.leaderBoard.heading("Score", text="Score", anchor=CENTER)
        with open(
            "/Users/angeldmello/GitRepos/COMP16321-Labs_t37525ad/COMP16321-Labs_t37525ad/score.csv"
        ) as fobj:
            lines = csv.reader(fobj)
            newlist = sorted(lines, key=lambda col: int(col[1]), reverse=True)
        sortedList = newlist
        serialNo = 0
        for item in sortedList:
            serialNo += 1
            self.leaderBoard.insert(
                parent="", index="end", text="", values=(serialNo, item[0], item[1])
            )


if __name__ == "__main__":
    start = StartUp()
    game = Game()
    quit()
