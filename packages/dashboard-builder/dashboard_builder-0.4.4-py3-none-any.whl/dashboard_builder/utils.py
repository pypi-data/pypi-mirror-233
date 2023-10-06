import os
import sys

def get_jinja_subtemplate(template_name):
    """
    Retrieves the content of a specified Jinja subtemplate.

    This function assumes that the subtemplate is located under 
    the 'components/templates' directory, which is relative to the current 
    file's location. It also adds the parent folder to the system path 
    (e.g., the root folder of the dashboard_builder package).

    Args:
        template_name (str): Name of the Jinja subtemplate file to be read.

    Returns:
        str: Content of the specified Jinja subtemplate.

    Example:
        >>> get_jinja_subtemplate("inputs/inputdropdown.j2")

    Note:
        This function modifies the system path by inserting a new path at the beginning.
    """
    current_dir = os.path.dirname(__file__)
    sys.path.insert(0, os.path.abspath(os.path.join(current_dir, "../../")))
    template_path = os.path.join(current_dir, 'components/templates', template_name)
    
    with open(template_path, 'r') as file:
        return file.read()
