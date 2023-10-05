import unittest

from starter_service.avro_parser import avsc_to_pydantic


class Test(unittest.TestCase):
    avro_schema = {
        "name": "KeyValuePairUpdate",
        "namespace": "osint",
        "type": "record",
        "doc": "Array of key-value pairs to update a single article or media item.",
        "fields": [
            {
                "name": "origin",
                "type": "string",
                "doc": "The microservice's name that created the metadata"
            },
            {
                "name": "refId",
                "doc": "The GUID of the item that must be updated, i.e. an article or media item.",
                "type": "string"
            },
            {
                "name": "schema",
                "doc": "The type of item that the refId refers to",
                "type": {
                    "type": "enum",
                    "name": "Schema",
                    "symbols": [
                        "ARTICLE",
                        "MEDIA_ITEM"
                    ]
                }
            },
            {
                "name": "timestamp",
                "type": "long",
                "logicalType": "timestamp-seconds",
                "doc": "Timestamp in UNIX Epoch in seconds."
            },
            {
                "name": "keyValuePairs",
                "doc": "A list of key value pairs",
                "type": [
                    {
                        "name": "KeyValuePairs",
                        "type": "array",
                        "items": {
                            "name": "KeyValuePair",
                            "type": "record",
                            "doc": "A single key-value pair",
                            "fields": [
                                {
                                    "name": "key",
                                    "doc": "The property key",
                                    "type": "string"
                                },
                                {
                                    "name": "value",
                                    "doc": "The property value: when it is null, the item will be set to null.",
                                    "type": [
                                        "null",
                                        "string",
                                        "boolean",
                                        "double"
                                    ],
                                    "default": None
                                }
                            ]
                        }
                    }
                ]
            }
        ]
    }

    def test_avsc_to_pydantic_reserved(self):
        class_python, class_name = avsc_to_pydantic(self.avro_schema)
        print(class_python)


if __name__ == '__main__':
    unittest.main()
