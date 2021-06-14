import os.path
from rich.console import Console
from rich.markdown import Markdown

console = Console()

class Trees:
    def __init__(self, path, string):
        self.full_path = f"core/trees/{path}.md"
        self.string = string

    def createTrees(self):
        if os.path.isfile(self.full_path) == True:
            pass
        
        else:
            tree = open(self.full_path, "a")
            tree.write(f"{self.string}")
            tree.close()

    def showTrees(self):
        with open(self.full_path) as readme:
            markdown = Markdown(readme.read())
            console.print(markdown)

