from flask import render_template_string
from ..utils import get_jinja_subtemplate

class ColumnLayout:
    """
    Represents a layout with multiple columns, where components can be added to 
    specific columns. Each column acts as a container for a group of components.
    """
    def __init__(self, num_columns):
        """
        Initializes a layout with the specified number of columns.

        Args:
            num_columns (int): Number of columns to be created.
        """
        self.columns = [[] for _ in range(num_columns)]

    def add_to_column(self, col_index, *components):
        """
        Add components to a specific column.

        Args:
            col_index (int): The index of the column to add components to.
            components: One or more components to add to the specified column.
        """
        for component in components:
            self.columns[col_index].append(component)

    def render(self):
        """
        Render the entire column layout as an HTML string. 
        Each component in the column will be rendered and added to its 
        respective column.

        Returns:
            str: HTML representation of the column layout with all the added components.
        """
        rendered_columns = []
        for column in self.columns:
            rendered_components = [comp.render() for comp in column]
            rendered_columns.append(
                f"<div class='flex-grow w-full md:flex-grow-0 md:w-1/2 px-2 max-h-[75vh] max-w-[90%] overflow-y-auto'>{'' .join(rendered_components)}</div>")  # noqa: E501
        return f"<div class='flex flex-col md:flex-row space-y-2 md:space-y-0 md:space-x-2'>{'' .join(rendered_columns)}</div>"  # noqa: E501


class ExpanderLayout:
    """
    Represents an expander layout, which typically displays content in a collapsible 
    view. Components can be added to the expander, which will be rendered inside 
    the collapsed view.
    """
    def __init__(self, label: str, id: str, components: list):
        """
        Initializes an expander layout.

        Args:
            label (str): Display label for the expander.
            id (str): A unique identifier for the expander. This helps in 
                distinguishing it from other expanders on the same page or view.
            components (list): A list of components that will be rendered inside 
                the expander when it's expanded.
        """
        self.label = label
        self.id = id
        self.components = components

    def render(self):
        """
        Render the entire expander layout as an HTML string.
        Each component inside the expander will be rendered and added to the 
        collapsed view.

        Returns:
            str: HTML representation of the expander layout with all the 
                added components.
        """
        return render_template_string(
            get_jinja_subtemplate("layouts/expanderlayout.j2"),
            label=self.label,
            id=self.id,
            components=[comp.render() for comp in self.components])
