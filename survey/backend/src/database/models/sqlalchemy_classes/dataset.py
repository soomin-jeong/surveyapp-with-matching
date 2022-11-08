import pandas as pd
from ....app import db
import json
class Dataset(db.Model):
    __tablename__= 'dataset'
    name = db.Column(db.String(128), unique=True)
    id = db.Column(db.Integer(), primary_key=True)
    file_path = db.Column(db.String(1024))
    num_users = db.Column(db.Integer())
    num_items = db.Column(db.Integer())

    def load_dataset(self):
        try:
            dataset = pd.read_csv(filepath_or_buffer= self.file_path, sep=',', dtype='str')
            return dataset
        except FileNotFoundError as e:
            raise FileNotFoundError("ERROR:\nDataset:file not found")

    def __str__(self):
        return json.dumps({
            'id': self.id,
            'file_path': self.file_path,
            'num_items': self.num_items,
            'num_users': self.num_users,
            'name': self.name
        })
