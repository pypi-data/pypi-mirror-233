from abc import ABC
import re
from typing import Union, Dict
from pathlib import Path
from json import loads


class DocBase(ABC):
    """
    Abstract base document generator class.
    """

    def __init__(self, metadata_path: Union[Path, str] = None):
        """
        :param metadata_path: The path to the metadata file. Can be None. See the README for how to format this file.
        """

        # Load the metadata.
        if metadata_path is None:
            """:field
            The metadata dictionary loaded from the metadata file. If there is no metadata file, this is empty.
            """
            self.metadata: dict = dict()
        if metadata_path is not None:
            if isinstance(metadata_path, Path):
                pass
            elif isinstance(metadata_path, str):
                metadata_path = Path(metadata_path)
            else:
                raise Exception("Invalid type: categories_path must be of type str or Path.")
            self.metadata = loads(metadata_path.read_text(encoding="utf-8"))

    def sort_by_metadata(self, class_name: str, doc: str) -> str:
        """
        Sort a document's contents using `self.metadata`.

        :param class_name: The name of the class.
        :param doc: The text of the unsorted document.

        :return: The text of the sorted document.
        """

        # Get each function.
        function_texts = re.findall(r'(#### ((.|\n)*?))(?=####.*?|\Z)', doc)
        function_texts = [f[0] for f in function_texts]
        # Remove the functions from the doc.
        for f in function_texts:
            doc = doc.replace(f, "")
        functions: Dict[str, str] = {re.search(r'#### (.*?)$', f, flags=re.MULTILINE).group(1): f for f in function_texts}
        doc = doc.strip() + "\n\n"
        # Reorganize by category.
        for category in self.metadata[class_name]:
            # Ignore anything in the Ignore category.
            if category == "Ignore":
                continue
            if category != "Constructor":
                doc += f"### {category}\n\n"
                if self.metadata[class_name][category]["description"] != "":
                    category_desc = self.metadata[class_name][category]["description"]
                    category_desc = re.sub(r"^(.(.*))", r"\1", category_desc, flags=re.MULTILINE)
                    doc += f'{category_desc}\n\n'
            for function_name in self.metadata[class_name][category]["functions"]:
                if function_name == "__init__":
                    key = "\\_\\_init\\_\\_"
                else:
                    key = function_name
                doc += functions[key]
            if not doc.endswith("\n\n"):
                doc += "\n\n"
            doc += "***\n\n"
        return doc
