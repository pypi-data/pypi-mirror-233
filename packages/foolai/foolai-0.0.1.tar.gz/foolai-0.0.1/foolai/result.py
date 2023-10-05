from rich import print
from rich.panel import Panel


class Result:
    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description
        

def show_result_panel(title: str, description: str):
    icon_party = ":party_popper:"
    title = f"{icon_party} {title} {icon_party}"
    panel = Panel.fit(description, title=title, border_style="yellow", padding=(1, 2))

    print()
    print(panel)
    print()