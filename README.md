# jsonbass
> A lightweight document database without a query language

## So how does one query documents?
> Well, you query documents using functional functions:

    users = DB.iterate_documents('users', lambda x: x['firstname'] == 'john')

## How does one insert documents?

    user = DB.insert_document('users', {
        'firstname': 'john',
        'lastname': 'doe'
    })

> The document will automatically get an `id` assigned to it.

## How does one update documents?

    def update(doc):
        doc['lastname'] = 'smith'

        return doc

    updated_users = DB.iterate_documents('users', document_update=update)

## The full iterate\_documents method

    DB.iterate_documents(
        column,  # the column to iterate
        document_filter,  # the query
        document_update,  # modify documents
        delete,  # if set to true, found documents will be deleted
        first  # if set to true, you will only get the first document found
    )

## How is the data stored?
> All data is stored in plain json.  
> Let us say that you have 2 database models: `users`, `messages`  
> then the data would be stored like this:

    {
        "users": [...],
        "messages": [...],
    }

> Every model will get their own `list` column in the JSON document.
