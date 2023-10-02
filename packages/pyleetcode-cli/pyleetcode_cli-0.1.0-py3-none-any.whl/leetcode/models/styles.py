from typing import Optional, Union

import rich
from rich import print
from rich.align import VerticalAlignMethod
from rich.bar import Bar
from rich.color import Color
from rich.columns import Columns
from rich.console import (Console, ConsoleOptions, JustifyMethod,
                          OverflowMethod, RenderableType, RenderResult)
from rich.containers import Renderables
from rich.jupyter import JupyterMixin
from rich.panel import Panel
from rich.segment import Segment
from rich.style import Style, StyleType
from rich.table import Table
from rich.text import Text

difficulty_retranslate = {'Easy': '🟢 Easy', 
                        'Medium': '🟡 Medium',
                        'Hard': '🔴 Hard'}

status_retranslate = {'ac': '✅ Solved',
                      'notac': '🟡 Attempted',
                      None: '❌ Not attempted',
                      'Wrong Answer': '❌ Wrong Answer',
                      'Accepted': '✅ Accepted',
                      'Runtime Error': '❌ Runtime Error',
                      'Time Limit Exceeded': '❌ Time Limit Exceeded',}

ALERT = Style(color='red', bold=True)

class LeetTable(Table):
    def __init__(self, *args, width=100,**kwargs):
        super().__init__(*args, **kwargs)
        self.box = rich.box.ROUNDED
        self.header_style = Style(color='blue', bold=True)
        self.width = width
        
        self.difficulty_column_index = None
        self.status_column_index = None
    
    def add_column(self, header: RenderableType = "", footer: RenderableType = "", *, header_style: StyleType | None = None, footer_style: StyleType | None = None, style: StyleType | None = None, justify: JustifyMethod = "left", vertical: VerticalAlignMethod = "top", overflow: OverflowMethod = "ellipsis", width: int | None = None, min_width: int | None = None, max_width: int | None = None, ratio: int | None = None, no_wrap: bool = False) -> None:
        if header == 'Difficulty':
            self.difficulty_column_index = len(self.columns)
        elif header == 'Status':
            self.status_column_index = len(self.columns)
        return super().add_column(header, footer, header_style=header_style, footer_style=footer_style, style=style, justify=justify, vertical=vertical, overflow=overflow, width=width, min_width=min_width, max_width=max_width, ratio=ratio, no_wrap=no_wrap)

    def add_row(self, *renderables: RenderableType | None, style: StyleType | None = None, end_section: bool = False) -> None:
        if self.difficulty_column_index or self.status_column_index:
            renderables = list(renderables)
            if self.difficulty_column_index is not None:
                renderables[self.difficulty_column_index] = difficulty_retranslate[renderables[self.difficulty_column_index]]
            if self.status_column_index is not None:
                renderables[self.status_column_index] = status_retranslate[renderables[self.status_column_index]]
            renderables = tuple(renderables)
        return super().add_row(*renderables, style=style, end_section=end_section)

    
class CustomBar(Bar):
    BEGIN_BLOCK_ELEMENTS = ["█", "█", "█", "▐", "▐", "▐", "▕", "▕"]
    END_BLOCK_ELEMENTS = [" ", "▏", "▎", "▍", "▌", "▋", "▊", "▉"]
    FULL_BLOCK = "█"
    BACKGROUND_BLOCK = "░"
    
    def __init__(
        self,
        end: float,
        *,
        info: str = None,
        size: float = 50,
        begin: float = 0,
        width: Optional[int] = 50,
        color: Union[Color, str] = "default",
        bgcolor: Union[Color, str] = "default"):
        super().__init__(size, begin, end, width=width, color=color, bgcolor=bgcolor)
        self.info = info
    
    def __rich_console__(self, console, options):
        width = min(
            self.width if self.width is not None else options.max_width,
            options.max_width,
        )

        if self.begin >= self.end:
            yield Segment(" " * width, self.style)
            yield Segment.line()
            return

        prefix_complete_eights = int(width * 8 * self.begin / self.size)
        prefix_bar_count = prefix_complete_eights // 8
        prefix_eights_count = prefix_complete_eights % 8

        body_complete_eights = int(width * 8 * self.end / self.size)
        body_bar_count = body_complete_eights // 8
        body_eights_count = body_complete_eights % 8

        # When start and end fall into the same cell, we ideally should render
        # a symbol that's "center-aligned", but there is no good symbol in Unicode.
        # In this case, we fall back to right-aligned block symbol for simplicity.

        prefix = " " * prefix_bar_count
        if prefix_eights_count:
            prefix += self.BEGIN_BLOCK_ELEMENTS[prefix_eights_count]

        body = self.FULL_BLOCK * body_bar_count
        if body_eights_count:
            body += self.END_BLOCK_ELEMENTS[body_eights_count]

        suffix = self.BACKGROUND_BLOCK * (width - len(body))

        if self.info is not None:
            yield self.info + ' '
        yield Segment(prefix + body[len(prefix):] + suffix, self.style)
        yield Segment.line()

class SubmitEvaluation():
    def __init__(self, runtime_perc, memory_perc) -> None:
        self.runtime_perc: float = runtime_perc
        self.memory_perc: float = memory_perc
        
    def __rich_console__(self, console, options):
        beat_text = Text(f"Beats {self.runtime_perc} of Leetcode users", justify='center')
        runtime_bar = CustomBar(size=100, 
                                end=float(self.runtime_perc) // 1, 
                                width=50)
        runtime_container = Renderables([beat_text, runtime_bar])
        
        beat_text = Text(f"Beats {self.memory_perc} of Leetcode users", justify='center')
        memory_bar = CustomBar(size=100, 
                               end=float(self.memory_perc) // 1, 
                               width=50)
        memory_container = Renderables([beat_text, memory_bar])
        
        runtime_panel = Panel(runtime_container, title=Text('Runtime', style='bold'))
        memory_panel = Panel(memory_container, title=Text('Memory', style='bold'))
        
        columns = Columns([runtime_panel, memory_panel])  
        yield columns

# class statsContainer():
#     def __init__()