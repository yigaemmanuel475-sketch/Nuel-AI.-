import os
import json
import ast
import operator
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

Window.clearcolor = (0.02, 0.02, 0.08, 1)


# SAFE MATHEMATICAL ENGINE

class Calculator:

    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod
    }

    def calculate(self, expression):

        try:
            tree = ast.parse(expression, mode="eval")
            return self.evaluate(tree.body)
        except Exception:
            return None

    def evaluate(self, node):

        if isinstance(node, ast.Constant):
            if type(node.value) in (int, float):
                return node.value
            raise ValueError("Invalid number")

        if isinstance(node, ast.BinOp):

            operation = self.operators.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported operation")

            left = self.evaluate(node.left)
            right = self.evaluate(node.right)

            if isinstance(node.op, ast.Pow):
                if abs(right) > 10:
                    raise ValueError("Exponent too large")

            return operation(left, right)

        if isinstance(node, ast.UnaryOp):
            value = self.evaluate(node.operand)

            if isinstance(node.op, ast.USub):
                return -value

            if isinstance(node.op, ast.UAdd):
                return value

        raise ValueError("Invalid expression")


# NUEL OFFLINE BRAIN

class NuelBrain:

    def __init__(self, memory_file):

        self.memory_file = memory_file
        self.memory = self.load_memory()
        self.calculator = Calculator()

    def load_memory(self):

        try:
            with open(self.memory_file, "r") as file:
                data = json.load(file)

                if isinstance(data, dict):
                    return data

        except Exception:
            pass

        return {}

    def save_memory(self):

        try:
            with open(self.memory_file, "w") as file:
                json.dump(self.memory, file, indent=4)

            return True

        except Exception:
            return False

    def remember(self, information):

        key = datetime.now().strftime(
            "%Y%m%d%H%M%S%f"
        )

        self.memory[key] = information

        if self.save_memory():
            return "I've successfully saved that information."

        del self.memory[key]

        return "I couldn't save that information."

    def recall(self, question):

        if not self.memory:
            return "My memory is currently empty."

        question_words = [
            word.lower()
            for word in question.split()
            if len(word) > 3
        ]

        matches = []

        for information in self.memory.values():

            if any(
                word in information.lower()
                for word in question_words
            ):
                matches.append(information)

        if matches:
            return "Here's what I remember:\n\n" + "\n".join(
                "- " + item for item in matches
            )

        return "I couldn't find that information in my memory."

    def knowledge(self, text):

        database = {

            "python": (
                "Python is a popular programming language "
                "used in artificial intelligence, automation, "
                "data analysis and software development."
            ),

            "artificial intelligence": (
                "Artificial Intelligence (AI) is technology "
                "that enables computers to perform tasks "
                "that normally require human intelligence."
            ),

            "machine learning": (
                "Machine learning is a branch of AI where "
                "computers learn patterns from data."
            ),

            "computer": (
                "A computer is an electronic device that "
                "processes information and performs instructions."
            ),

            "internet": (
                "The internet is a worldwide network "
                "connecting computers and other devices."
            ),

            "uganda": (
                "Uganda is a landlocked country in East Africa. "
                "Its capital city is Kampala."
            ),

            "programming": (
                "Programming is the process of writing "
                "instructions that computers execute."
            ),

            "memory": (
                "Computer memory stores information "
                "for temporary or long-term use."
            ),

            "robotics": (
                "Robotics is the field of designing, "
                "building and programming robots."
            )
        }

        for topic, answer in database.items():

            if topic in text:
                return answer

        return None

    def calculate(self, text):

        cleaned = text.lower()

        for phrase in [
            "calculate",
            "what is",
            "solve",
            "compute"
        ]:

            cleaned = cleaned.replace(phrase, "")

        cleaned = cleaned.replace("multiplied by", "*")
        cleaned = cleaned.replace("times", "*")
        cleaned = cleaned.replace("divided by", "/")
        cleaned = cleaned.replace("plus", "+")
        cleaned = cleaned.replace("minus", "-")
        cleaned = cleaned.replace("power of", "**")

        cleaned = cleaned.replace(" ", "")

        allowed = "0123456789+-*/().%"

        if not cleaned or any(
            char not in allowed for char in cleaned
        ):
            return None

        result = self.calculator.calculate(cleaned)

        if result is None:
            return None

        return f"The answer is {result}"

    def think(self, message):

        text = message.lower().strip()

        if not text:
            return "Please enter a message."

        # MEMORY COMMANDS

        if text.startswith("remember "):

            information = message[9:].strip()

            if not information:
                return "What would you like me to remember?"

            return self.remember(information)

        if "what do you remember" in text:

            if not self.memory:
                return "My memory is currently empty."

            return "I remember:\n\n" + "\n".join(
                "- " + item
                for item in self.memory.values()
            )

        # MATHEMATICS

        if any(word in text for word in [
            "calculate",
            "compute",
            "solve",
            "what is"
        ]):

            answer = self.calculate(text)

            if answer:
                return answer

        # TIME AND DATE

        if "time" in text:
            return "Current time: " + datetime.now().strftime(
                "%H:%M"
            )

        if "date" in text:
            return "Today's date: " + datetime.now().strftime(
                "%d/%m/%Y"
            )

        # CONVERSATION

        if text in ["hello", "hi", "hey"]:
            return "Hello! I'm NUEL AI. How can I help you?"

        if "your name" in text:
            return "I am NUEL AI, your personal AI assistant."

        if "who created you" in text:
            return "I am NUEL AI, developed as your personal AI project."

        if "how are you" in text:
            return "I'm operational and ready to assist you."

        if "thank you" in text or text == "thanks":
            return "You're welcome!"

        # BUILT-IN KNOWLEDGE

        answer = self.knowledge(text)

        if answer:
            return answer

        # MEMORY SEARCH

        if any(word in text for word in [
            "what am i",
            "what is my",
            "do you remember",
            "tell me about my"
        ]):

            answer = self.recall(text)

            if "couldn't find" not in answer:
                return answer

        return (
            "I don't have enough information to answer "
            "that question yet. My offline knowledge "
            "database will continue growing."
        )


# NUEL APPLICATION

class NuelApp(App):

    def build(self):

        self.title = "NUEL AI"

        memory_file = os.path.join(
            self.user_data_dir,
            "nuel_memory.json"
        )

        self.brain = NuelBrain(memory_file)

        self.root_layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        self.dashboard()

        return self.root_layout

    def dashboard(self):

        self.root_layout.clear_widgets()

        self.root_layout.add_widget(Label(
            text="[b]NUEL AI[/b]",
            markup=True,
            font_size=40,
            color=(0.2, 0.7, 1, 1)
        ))

        self.root_layout.add_widget(Label(
            text="YOUR PERSONAL INTELLIGENCE"
        ))

        self.root_layout.add_widget(Button(
            text="OPEN AI CHAT",
            on_press=self.open_chat
        ))

        self.root_layout.add_widget(Button(
            text="MEMORY CENTRE",
            on_press=self.open_memory
        ))

        self.root_layout.add_widget(Button(
            text="SETTINGS",
            on_press=self.open_settings
        ))

    def open_chat(self, instance):

        self.root_layout.clear_widgets()

        header = BoxLayout(
            size_hint_y=None,
            height=55
        )

        header.add_widget(Label(
            text="[b]NUEL AI CHAT[/b]",
            markup=True
        ))

        header.add_widget(Button(
            text="HOME",
            size_hint_x=0.3,
            on_press=lambda x: self.dashboard()
        ))

        self.root_layout.add_widget(header)

        self.messages = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=10,
            padding=10
        )

        self.messages.bind(
            minimum_height=self.messages.setter("height")
        )

        scroll = ScrollView()
        scroll.add_widget(self.messages)

        self.root_layout.add_widget(scroll)

        bottom = BoxLayout(
            size_hint_y=None,
            height=55,
            spacing=5
        )

        self.message_input = TextInput(
            hint_text="Talk to NUEL...",
            multiline=False
        )

        send = Button(
            text="SEND",
            size_hint_x=0.3,
            on_press=self.send_message
        )

        self.message_input.bind(
            on_text_validate=self.send_message
        )

        bottom.add_widget(self.message_input)
        bottom.add_widget(send)

        self.root_layout.add_widget(bottom)

        self.add_message(
            "NUEL AI",
            "My offline intelligence engine is ready!"
        )

    def send_message(self, instance):

        message = self.message_input.text.strip()

        if not message:
            return

        self.message_input.text = ""

        self.add_message("YOU", message)

        try:
            response = self.brain.think(message)

        except Exception as error:
            response = "Processing error: " + str(error)

        self.add_message("NUEL AI", response)

    def add_message(self, sender, message):

        label = Label(
            text=f"[b]{sender}[/b]\n{message}",
            markup=True,
            size_hint_y=None,
            halign="left",
            valign="middle"
        )

        label.bind(
            width=lambda obj, width: setattr(
                obj, "text_size", (width, None)
            )
        )

        label.bind(
            texture_size=lambda obj, size: setattr(
                obj, "height", size[1] + 20
            )
        )

        self.messages.add_widget(label)

    def open_memory(self, instance):

        self.root_layout.clear_widgets()

        self.root_layout.add_widget(Label(
            text="[b]NUEL MEMORY CENTRE[/b]",
            markup=True,
            font_size=25,
            size_hint_y=None,
            height=60
        ))

        self.memory_display = Label(
            text=self.get_memories(),
            size_hint_y=None,
            halign="left",
            valign="top"
        )

        self.memory_display.bind(
            width=lambda obj, width: setattr(
                obj, "text_size", (width, None)
            )
        )

        self.memory_display.bind(
            texture_size=lambda obj, size: setattr(
                obj, "height", size[1] + 30
            )
        )

        scroll = ScrollView()
        scroll.add_widget(self.memory_display)

        self.root_layout.add_widget(scroll)

        self.root_layout.add_widget(Button(
            text="REFRESH MEMORY",
            on_press=self.refresh_memory
        ))

        self.root_layout.add_widget(Button(
            text="BACK HOME",
            on_press=lambda x: self.dashboard()
        ))

    def get_memories(self):

        if not self.brain.memory:
            return "No memories stored yet."

        return "\n\n".join(
            self.brain.memory.values()
        )

    def refresh_memory(self, instance):

        self.brain.memory = self.brain.load_memory()

        self.memory_display.text = self.get_memories()

    def open_settings(self, instance):

        self.root_layout.clear_widgets()

        self.root_layout.add_widget(Label(
            text="[b]NUEL AI SETTINGS[/b]",
            markup=True,
            font_size=25
        ))

        self.root_layout.add_widget(Label(
            text=(
                "SYSTEM: OPERATIONAL\n\n"
                "BRAIN: OFFLINE ENGINE\n\n"
                "MEMORY: ENABLED\n\n"
                "VOICE: COMING SOON\n\n"
                "ONLINE INTELLIGENCE: COMING SOON"
            )
        ))

        self.root_layout.add_widget(Button(
            text="BACK HOME",
            on_press=lambda x: self.dashboard()
        ))


if __name__ == "__main__":
    NuelApp().run()
