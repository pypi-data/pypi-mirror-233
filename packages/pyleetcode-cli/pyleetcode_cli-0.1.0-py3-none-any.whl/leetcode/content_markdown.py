import os

from markdownify import markdownify
from rich import print
from rich.markdown import Markdown
from rich.panel import Panel

# TODO: handle images
""" Turns the HTML code of the LeetCode question to sections. Then each section is 
    altered to Markdown and later into the Rich Panel. 
    
    - self.sections (list) - list of HTML content splitted to sections 
    - self.panels (list) - contains Markdown content turned into Rich module's Panel """

class LeetQuestionToSections():
    def __init__(self, html: str):
        self.html = html
        
        self.sections = []
        self.panels = []
        self.__divide_into_sections()
        self.__sections_into_panels()
        
        self.__format_the_panels()
        
    def __add_breaks(self):
        # Add the breaks into the Examples section
        self.sections[1] = self.sections[1].replace('<strong>Output:</strong>', '<br><strong>Output:</strong>')
        self.sections[1] = self.sections[1].replace('<strong>Explanation:</strong>', '<br><strong>Explanation:</strong>')
        
    def __format_the_panels(self):
        self.panels[0].title = '[bold]Introduction[/bold]'
        
        self.panels[1].title = '[bold]Examples[/bold]'
        
    def __divide_into_sections(self):
        self.html = self.html.split('<p>&nbsp;</p>')
        for section in self.html:
            self.sections.append(section)
        self.__add_breaks()
    
    def __sections_into_panels(self):
        for section in self.sections:
            section = markdownify(section, strip=['pre'])
            panel = Panel(Markdown(section), width=100)
            self.panels.append(panel)
               
    def __remove_empty_lines(self, section) -> str:
        section = os.linesep.join([
        line for line in section.splitlines()
        if line.strip() != ''])
        return section

    def __getitem__(self, index) -> Panel:
        return self.panels[index]