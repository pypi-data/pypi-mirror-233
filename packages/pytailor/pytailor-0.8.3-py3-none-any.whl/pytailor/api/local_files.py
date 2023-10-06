from typing import List, Dict, Optional
from os.path import abspath

from pytailor.api.base import APIBase
from pytailor.utils import check_local_files_exist, walk_and_apply, get_or_create_node_id


class LocalFiles(APIBase):
    """
    Create a new LOCAL fileset.
    """

    def __init__(self, node_id: Optional[str] = None, **files: List[str]):
        self.__files = {}
        if node_id is None:
            files = walk_and_apply(files, val_cond=lambda x: isinstance(x, str), val_apply=abspath)
            check_local_files_exist(files)
        self.node_id = node_id or get_or_create_node_id()
        self.__files.update(files)

    @property
    def files(self) -> Dict[str, List[str]]:
        return self.__files

    @files.setter
    def files(self, files: Dict[str, List[str]]):
        self.__files = files

    @property
    def file_tags(self) -> List[str]:
        return list(self.__files.keys())
