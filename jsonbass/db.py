import json
import os
from jsonbass.config import config
from jsonbass.random_utils import get_random_string


class DB(object):

    @staticmethod
    def get_database():
        if not os.path.isfile(config['db_file']):
            data = {}
        else:
            with open(config['db_file']) as _file:
                data = _file.read()
            _file.close()

        return json.loads(data) if data else {}

    @staticmethod
    def write(data):
        with open(config['db_file'], 'w+') as _file:
            _file.write(json.dumps(data))
        _file.close()

    @staticmethod
    def iterate_documents(
            column,
            document_filter=None,
            document_update=None,
            delete=False,
            first=False
    ):
        data = DB.get_database()
        modified = False

        entities = [
            document_update(x) if document_update else x
            for x in filter(document_filter, data[column])
        ]

        if delete:
            for i, entity in enumerate(data[column]):
                if entity in entities:
                    del data[column][i]
                    modified = True

        if document_update:
            data[column] = entities
            modified = True

        if modified:
            DB.write(data)

        return entities

    @staticmethod
    def insert_document(column, doc):
        data = DB.get_database()

        if column not in data:
            data[column] = []

        if 'id' not in doc:
            doc['id'] = get_random_string(24)

        if not DB.iterate_documents(
                column, lambda x: x['id'] == doc['id'], first=True):
            data[column].append(doc)
        else:
            raise Exception('Document with id: {} already exists'.format(
                doc['id']
            ))

        DB.write(data)

        return doc

    @staticmethod
    def delete_all_documents(column=None):
        data = DB.get_database()

        if column:
            data[column] = []
        else:
            data = {}

        with open(config['db_file'], 'w+') as _file:
            _file.write(json.dumps(data))
        _file.close()

        return data
