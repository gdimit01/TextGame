import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk

# ASCII art for demonstration (replace with actual art)
ROOM_ART = {
    "Liminal Space": """
    --------
   |        |
   | LSpace |
   |        |
    --------
    """,
    "Mirror Maze": """
    --------
   | Mirror|
   |  Maze |
   |       |
    --------
    """,
    "Bat Cavern": """
    --------
   |  Bat  |
   |Cavern|
   |       |
    --------
    """,
    "Bazaar": """
    --------
   | Bazaar|
   |       |
   |       |
    --------
    """,
    "Meat Locker": """
    --------
   |  Meat |
   |Locker |
   |       |
    --------
    """,
    "Quicksand Pit": """
    --------
   |Quick- |
   | sand  |
   |  Pit  |
    --------
    """,
    "Volcano": """
    --------
   |Volcano|
   |       |
   |       |
    --------
    """,
    "Dojo": """
    --------
   |  Dojo |
   |       |
   |       |
    --------
    """,
}


class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Text Adventure Game")

        self.frame_sidebar = tk.Frame(self.root, width=200, bg="grey")
        self.frame_sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.frame_main = tk.Frame(self.root)
        self.frame_main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(
            self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.selected_option = tk.StringVar()

        self.inventory = []
        self.current_room = "Liminal Space"
        self.msg = ""

        self.prompt()

    def prompt(self):
        messagebox.showinfo(
            "Welcome",
            "Welcome to my game\n\nYou must collect all six items before fighting the boss.",
        )
        self.display_room()

    def display_room(self):
        for widget in self.frame_sidebar.winfo_children():
            widget.destroy()

        for widget in self.frame_main.winfo_children():
            widget.destroy()

        self.status_var.set(
            f"Room: {self.current_room} | Inventory: {', '.join(self.inventory)}"
        )

        # Display ASCII art (or any other content)
        art_label = tk.Label(
            self.frame_main,
            text=ROOM_ART.get(self.current_room, ""),
            font=("Courier", 14),
        )
        art_label.pack(pady=50)

        # Available actions
        available_actions = []
        if (
            "Item" in rooms[self.current_room]
            and rooms[self.current_room]["Item"] not in self.inventory
        ):
            available_actions.append("Get")

        available_directions = [
            d
            for d in rooms[self.current_room].keys()
            if d in ["North", "South", "East", "West"]
        ]
        if available_directions:
            available_actions.append("Go")

        for action in available_actions:
            action_button = tk.Button(
                self.frame_sidebar,
                text=action,
                command=lambda a=action: self.handle_action(a),
            )
            action_button.pack(fill=tk.X)

    def handle_action(self, action):
        if action == "Go":
            direction = self.get_direction()
            self.current_room = rooms[self.current_room][direction]
        elif action == "Get":
            item = rooms[self.current_room]["Item"]
            if item not in self.inventory:
                self.inventory.append(item)
            self.msg = (
                f"{item} retrieved!"
                if item not in self.inventory
                else f"You already have the {item}"
            )

        if "Boss" in rooms[self.current_room].keys():
            if len(self.inventory) < 6:
                self.msg = f"You lost a fight with {rooms[self.current_room]['Boss']}."
                self.game_over()
            else:
                self.msg = f"You beat {rooms[self.current_room]['Boss']}!"
                self.game_over()
        else:
            self.display_room()

    def get_direction(self):
        available_directions = [
            d
            for d in rooms[self.current_room].keys()
            if d in ["North", "South", "East", "West"]
        ]
        direction = simpledialog.askstring(
            "Direction", "Choose a direction: " + ", ".join(available_directions)
        )
        while direction not in available_directions:
            direction = simpledialog.askstring(
                "Direction",
                "Choose a valid direction: " + ", ".join(available_directions),
            )
        return direction

    def game_over(self):
        messagebox.showinfo("Game Over", self.msg)
        self.root.destroy()

    def run(self):
        self.root.mainloop()


# Map
rooms = {
    "Liminal Space": {"North": "Mirror Maze", "South": "Bat Cavern", "East": "Bazaar"},
    "Mirror Maze": {"South": "Liminal Space", "Item": "Crystal"},
    "Bat Cavern": {"North": "Liminal Space", "East": "Volcano", "Item": "Staff"},
    "Bazaar": {
        "West": "Liminal Space",
        "North": "Meat Locker",
        "East": "Dojo",
        "Item": "Altoids",
    },
    "Meat Locker": {"South": "Bazaar", "East": "Quicksand Pit", "Item": "Fig"},
    "Quicksand Pit": {"West": "Meat Locker", "Item": "Robe"},
    "Volcano": {"West": "Bat Cavern", "Item": "Elderberry"},
    "Dojo": {"West": "Bazaar", "Boss": "Shadow Man"},
}

inventory = []
vowels = ["a", "e", "i", "o", "u"]
current_room = "Liminal Space"
msg = ""

game = Game()
game.run()
