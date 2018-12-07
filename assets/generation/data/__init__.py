simple_schema = {
    "doc": "TestSchema",
    "name": "TS",
    "type": "record",
    "fields": [
        {
            "doc": "ID",
            "name": "id",
            "type": "string",
            "jsonldPredicate": "@id"
        },
        {
            "doc": "REV",
            "name": "rev",
            "type": "string"
        },
        {
            "type": "string",
            "name": "name"
        }
    ]
}