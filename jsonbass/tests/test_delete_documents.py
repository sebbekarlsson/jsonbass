from jsonbass.db import DB


def test_delete_documents():
    column = 'notes'

    DB.delete_all_documents(column)

    notes = [
        {
            'text': 'I should by milk today',
            'tags': ['milk', 'food', 'todo']
        },
        {
            'text': 'Go to the gym',
            'tags': ['fitness', 'health']
        },
        {
            'text': 'Call mother',
            'tags': ['health', 'social']
        }
    ]

    for _note in notes:
        note = DB.insert_document(column, _note)

        assert isinstance(note, dict)
        assert 'text' in note
        assert 'tags' in note
        assert 'id' in note

    assert len(list(DB.iterate_documents(column))) == 3

    DB.iterate_documents(
        column,
        lambda x: 'gym' in x['text'].lower(),
        delete=True
    )

    assert len(list(DB.iterate_documents(column))) == 2
