import pandas as pd
import json

class Generic:

    def __init__(self, record: dict):
        for k, v in record.items():
            setattr(self, k, v)

    @staticmethod
    def dict_to_object(data: dict, ctx):
        print(data, ctx)
        return Generic(record=data)


    def to_dict(self):
        return self.__dict__

    @classmethod
    def get_object(cls, file_path):
        chunk_df = pd.read_csv(file_path, chunksize=10)
        n_row = 0
        for df in chunk_df:
            for data in df.values:
                generic = Generic(dict(zip(df.columns, list(map(str,data)))))
                # sensor.append(sensor)
                # print(n_row)
                n_row += 1
                yield generic

    @classmethod
    def export_schema_to_create_confluent_schema(cls, file_path):
        columns = next(pd.read_csv(file_path, chunksize=10)).columns

        schema = dict()
        schema.update({
                    "type": "record",
                    "namespace": "com.mycorp.mynamespace",
                    "name": "sampleRecord",
                    "doc": "Sample schema to help you get started.",
                    })

        fields = []    
        for column in columns:
            fields.append(
                        {
                        "name": f"{column}",
                        "type": "string",
                        "doc": "The string type."  
                        }
            )
