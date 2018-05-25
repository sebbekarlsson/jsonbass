import json
import os
from jsonbass.config import config
from jsonbass.random_utils import get_random_string
from jsonbass.exceptions import NoSuchColumnException


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

        if delete and not document_filter:
            data[column] = []

        try:
            entities = [
                document_update(x) if document_update else x
                for x in filter(document_filter, data[column])
            ]
        except KeyError:
            raise NoSuchColumnException('{} is not an existing column'.format(
                str(column)
            ))

        if delete and document_filter:
            for i, entity in enumerate(data[column]):
                if entity in entities:
                    del data[column][i]

        elif document_update:
            data[column] = entities

        if delete or document_update:
            DB.write(data)

        return entities[0] if (entities and first) else entities

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
