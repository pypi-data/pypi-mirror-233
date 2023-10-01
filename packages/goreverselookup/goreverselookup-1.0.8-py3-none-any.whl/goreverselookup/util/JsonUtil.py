import json
import os
from types import SimpleNamespace

from .FileUtil import FileUtil

import logging

# from logging import config
# config.fileConfig("../logging_config.py")
logger = logging.getLogger(__name__)


class JsonUtil:
    @classmethod
    def load_json(cls, filepath: str):
        """
        Loads a json file and returns the json object (a dictionary).

        Parameters:
          - (str) filepath
        """
        logger.info(f"Load JSON received input filepath: {filepath}")
        initial_filepath = filepath

        if not os.path.exists(filepath):
            if not os.path.isabs(filepath):
                fileutil = FileUtil()
                filepath = fileutil.find_file(filepath)  # attempt backtrace file search
                logger.info(f"Filepath after file search: {filepath}")

                if filepath is None:
                    raise Exception(
                        "Filepath when attempting load JSON is None! Initial filepath"
                        f" was {initial_filepath}"
                    )

                # current_dir = os.path.dirname(os.path.abspath(traceback.extract_stack()[0].filename))
                # filepath = os.path.join(current_dir, filepath)

        # bugfix: if filepath is empty, I want load_json to return {} instead of JSONDecodeError
        if FileUtil.is_file_empty(filepath):
            return {}

        with open(filepath, "r") as f:
            data = json.load(f)
            return data

    @classmethod
    def save_json(cls, data_dictionary: dict, filepath: str):
        """
        Saves the data_dictionary as json to the filepath.

        Parameters:
          - (dict) data_dictionary: the data to be saved as the json
          - (str) filepath: the filepath where the json is to be stored
        """
        if ".json" not in filepath:
            filepath = f"{filepath}.json"

        logger.info(f"Saving json to: {filepath}")
        with open(filepath, "w") as f:
            json.dump(data_dictionary, f, indent=4)

        """
        try: # this works on mac, not on windows
            current_dir = os.path.dirname(os.path.abspath(traceback.extract_stack()[0].filename))
            os.makedirs(os.path.dirname(os.path.join(current_dir, filepath)), exist_ok=True) # Create directory for the report file, if it does not exist
            with open(os.path.join(current_dir, filepath), 'w') as f:
                json.dump(data_dictionary, f, indent=4)
        except OSError:
            # pass the error on the first attempt
            pass

        try: # if first attempt fails, try using current_dir = os.getcwd(), this works on windows
            windows_filepath = FileUtil.find_win_abs_filepath(filepath)
            os.makedirs(os.path.dirname(windows_filepath), exist_ok=True) # Create directory for the report file, if it does not exist
            with open(windows_filepath, 'w') as f:
                json.dump(data_dictionary, f, indent=4)
            #current_dir = os.getcwd()
            #os.makedirs(os.path.dirname(os.path.join(current_dir, filepath)), exist_ok=True)
        except OSError:
            logger.info(f"ERROR creating filepath {filepath} at {os.getcwd()}")
        """


class JsonToClass:
    object_representation = ""
    source_json = ""

    def __init__(self, data):
        """
        Converts a JSON eg. '{"name": "John Smith", "hometown": {"name": "New York", "id": 123}}'
        to a class, which can be queried with eg. x.name, x.hometown.name, x.hometown.id

        Warning: keys and values must be double-quote delimited (single-quotes are bugged)
        Warning: avoid usage of single quotes inside json string values (doing so breaks this code)

        Tip: http://json.parser.online.fr/ is very useful for debugging JSON errors, just remove starting ' and '

        Params:
            - data: a json representation of the data

        Returns: a class with the following member fields
            - object_representation: a SimpleNamespace instance, representing the objectified json
            - source_json: the json from which the SimpleNamespace was built

        Example usage: you want to convert a JSON to a Python object (class instance):
        json_string = '{"name": "John Smith", "hometown": {"name": "New York", "id": 123}}'
        json_namespace = SimpleNamespaceCustom(json_string)
        object_representation = json_namespace.object_representation
        src_json = json_namespace.source_json
        """

        # Parse JSON into an object with attributes corresponding to dict keys.
        if (
            "isn't" in data
        ):  # TODO: this is a hardcoded solution. Avoid any ' characters in the json values or change json to class loading.
            data = data.replace("isn't", "is not")

        if "None" in data:  # hardcoded bugfix
            data = data.replace("None", '"None"')

        if "inf" in data:  # hardcoded bugfix
            data = data.replace("inf", '"inf"')

        if "'" in data:
            data = data.replace("'", '"')  # SimpleNamespace bugs out with single-quotes

        if "nan" in data:
            data = data.replace("nan", "0")

        x = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        self.object_representation = x
        self.source_json = data


class SimpleNamespaceUtil:
    """
    Utility functions for SimpleNamespace
    """

    def __init__():
        return 0

    @staticmethod
    def simpleNamespace_to_json(simple_namespace: SimpleNamespace):
        """
        TODO: incomplete function
        Converts a simpleNamespace object to a json string
        """
        # def iterate_members(base_member, result={}):
        #    submembers = []
        #    if isinstance(base_member, object):
        #        for attr in dir(base_member):
        #            if not callable(getattr(base_member, attr)) and not attr.startswith("__"):
        #                value = getattr(base_member, attr)
        #                if isinstance(value, object):
        #                    iterate_members(value, result)
        #                else:
        #                    result[attr] = value
        #                submembers.append(attr)
        #
        # member_fields = []
        # for attr in dir(simple_namespace):
        #    if not callable(getattr(simple_namespace, attr)) and not attr.startswith("__"):
        #        member_fields.append(attr)
        #
        return 0


def json_to_class(data: str):
    """
    Converts a JSON eg. '{"name": "John Smith", "hometown": {"name": "New York", "id": 123}}'
    to a class, which can be queried with eg. x.name, x.hometown.name, x.hometown.id

    Warning: keys and values must be double-quote delimited (single-quotes are bugged)
    Warning: avoid usage of single quotes inside json string values (doing so breaks this code)

    Tip: http://json.parser.online.fr/ is very useful for debugging JSON errors, just remove starting ' and '

    Params:
      - data: a json representation of the data

    Returns:
      - a class from the input json data
    """
    if (
        "isn't" in data
    ):  # TODO: this is a hardcoded solution. Avoid any ' characters in the json values or change json to class loading.
        data = data.replace("isn't", "is not")

    if "None" in data:  # hardcoded bugfix
        data = data.replace("None", '"None"')

    if "inf" in data:  # hardcoded bugfix
        data = data.replace("inf", '"inf"')

    if "'" in data:
        data = data.replace("'", '"')  # SimpleNamespace bugs out with single-quotes

    if "nan" in data:
        data = data.replace("nan", "0")

    x = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    return x
