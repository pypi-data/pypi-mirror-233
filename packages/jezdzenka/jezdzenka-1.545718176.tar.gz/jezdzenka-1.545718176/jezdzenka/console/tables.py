import rich
from rich import box

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from jezdzenka.database import collection
from jezdzenka.translation import _


def show_in_table_normal(rows):
    console = Console()
    rows = sorted(rows, key=lambda row: row['relevant_date'], reverse=True)
    table = Table(show_header=True, header_style="bold blue", show_lines=True)
    table.add_column("#", style="dim", width=3, justify="right")
    table.add_column(_("Description"))
    table.add_column(_("Operator"))
    table.add_column(_("Date"))
    for row in rows:
        table.add_row(str(row.doc_id), row['description'], row['organization'],
                      type_handling('relevant_date', row['relevant_date']))
    console.print(table)


def show_elements_normal(rows):
    rows = sorted(rows, key=lambda row: row['relevant_date'], reverse=False)
    for row in rows:
        show_single(row.doc_id)


def show_elements_verbose(rows):
    rows = sorted(rows, key=lambda row: row['relevant_date'], reverse=False)
    for row in rows:
        show_single_verbose(row.doc_id)


def show_in_table_verbose(rows):
    console = Console()
    rows = sorted(rows, key=lambda row: row['relevant_date'], reverse=True)
    table = Table(show_header=True, header_style="bold blue", show_lines=True)
    table.add_column("#", style="dim", width=3, justify="right")
    table.add_column(_("Description"))
    table.add_column(_("Operator"))
    table.add_column(_("Date"))
    table.add_column(_("Tags"))
    table.add_column(_("Operator's id"))
    table.field_names = ["#", "Description", "Operator", "Date", "Tags", "Operator's id"]
    for row in rows:
        table.add_row(str(row.doc_id), row['description'], row['organization'],
                      type_handling('relevant_date', row['relevant_date']), str(row['tags']), row['id'])
    console.print(table)


def verbose_in_table(element_id):
    console = Console()
    element = collection.get_object_by_id(element_id)
    table = Table()
    table.add_column("Parameter")
    table.add_column("Value")
    for key, data in element.items():
        table.add_row(_(key), str(type_handling(key, data)))
    console.print(table)


def show_single_verbose(element_id):
    element = collection.get_object_by_id(element_id)
    colour = element['colour']
    text = Text()
    count = 0
    for key, data in element.items():
        count += 1
        text.append(_(key) + ": ", style="bold " + colour)
        text.append(str(type_handling(key, data)))
        if count < len(element):
            text.append("\n")
    rich.print(Panel(text, style=colour, title=str(element_id) + ", " + str(element['id'])))


def show_single(element_id):
    params = ["description", "organization", "relevant_date"]
    element = collection.get_object_by_id(element_id)
    colour = element['colour']
    text = Text()
    needed_params = {key: value for key, value in element.items() if key in params}
    count = 0
    for key, data in needed_params.items():
        count += 1
        text.append(_(key) + ": ", style="bold " + colour)
        text.append(str(type_handling(key, data)))
        if count < len(needed_params):
            text.append("\n")
    rich.print(Panel(text, style=colour, title=str(element_id) + ", " + str(element['id'])))


def type_handling(key, data):
    if key == 'type':
        return _(data.value)
    elif key == 'relevant_date':
        return data.strftime("%Y-%m-%d %H:%M:%S")
    elif key == 'archived':
        return "Yes" if data else "No"
    else:
        return data
