from typing import List
from glob import glob
from tqdm.auto import tqdm
import os

from .api import Api


class Deposition(object):
    """eposition class.
    This class is used to interact with a specific zenodo deposition.
    """

    def __init__(self, files:List, title:str, id:int, submitted:bool, **kwargs):
        self.files = files
        self.title = title
        self.id = id
        self.submitted = submitted
        self.other = kwargs
        self.api = Api()

    def __repr__(self):
        return f"Deposition({self.id}, {self.title})"

    @classmethod
    def from_json(cls, json):
        return cls(**json)

    @classmethod
    def from_id(cls, id):
        r = Api().deposition_retrieve(id).json()
        return cls.from_json(r)

    @classmethod
    def from_title(cls, title):
        api = Api()
        id = api.get_deposition_ids_from_title(title)[0]
        return cls.from_id(id)

    def delete_file(self, fname):
        file_id = [f['id'] for f in self.files if f['filename'] == fname][0]
        self.api.deposition_files_delete(self.id, file_id)

    def create_new_version(self):
        data = self.api.deposition_actions_newversion(self.id).json()
        self = Deposition.from_json(data)
        self.api.deposition_actions_edit(self.id)

    def upload_files(self, regex):
        if self.submitted:
            self.create_new_version()

        for fpath in tqdm(glob(regex), desc="Uploading"):
            fname = os.path.basename(fpath)
            if fname in self.filenames:
                self.delete_file(fname)
            r = self.api.deposition_files_create(self.id, fname, fpath)
            if r.status_code != 200:
                raise RuntimeError(f"Failed to upload {fname} to Zenodo: {r.json()}")


    @property
    def filenames(self):
        return [f['filename'] for f in self.files]
