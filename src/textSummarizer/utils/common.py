import os
from box.exceptions import BoxValueError
import yaml
from textSummarizer.logging import logger
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any


from box import Box
import yaml
from pathlib import Path
import logging

def read_yaml(path_to_yaml: Path) -> Box:
    """
    The function `read_yaml` reads a YAML file from the given path and returns its content as a `Box`
    object.
    
    :param path_to_yaml: The parameter `path_to_yaml` is the path to the YAML file that you want to
    read. It should be a `Path` object, which represents the file path
    :type path_to_yaml: Path
    :return: a Box object that contains the content of the YAML file.
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logging.info(f"Yaml file '{path_to_yaml}' loaded successfully")
            return Box(content)
    except (BoxValueError, ValueError):
        raise ValueError("Yaml file is empty")
    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """
    The function `create_directories` creates a list of directories at the specified paths.
    
    :param path_to_directories: A list of paths where the directories should be created
    :type path_to_directories: list
    :param verbose: The `verbose` parameter is a boolean flag that determines whether or not to display
    additional information or logs during the execution of the function. If `verbose` is set to `True`,
    the function will log a message indicating that a directory has been created at each path. If
    `verbose` is set, defaults to True (optional)
    """
    """create list of directories

    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")


@ensure_annotations
def get_size(path: Path) -> str:
    """
    The function `get_size` takes a file path as input and returns the size of the file in kilobytes.
    
    :param path: The `path` parameter is the path of the file for which you want to get the size in
    kilobytes
    :type path: Path
    :return: a string that represents the size of the file in kilobytes. The string is in the format "~
    {size_in_kb} KB", where {size_in_kb} is the calculated size in kilobytes.
    """
    """get size in KB

    Args:
        path (Path): path of the file

    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"