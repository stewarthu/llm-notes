from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, inspect, MetaData, Table, select, delete
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql.sqltypes import NullType
import json
import os
import datetime

DB = 'sqlite:///sample.db'

# Function to determine SQLAlchemy type from Python type
def get_sqlalchemy_type(py_type):
    if py_type == str:
        return String(200)
    elif py_type == int:
        return Integer
    elif py_type == float:
        return Float
    else:
        return NullType

# Declare the base class
Base = declarative_base()

def table_factory(table_name, columns):
    class Table(Base):
        __tablename__ = table_name
        #__table_args__ = {'extend_existing': True} 
        id = Column(Integer, primary_key=True)
        for name, column_type in columns.items():
            locals()[name] = Column(column_type)
            #setattr(Table, name, Column(column_type))
    return Table

# Define the Metadata class
class Metadata(Base):
    __tablename__ = 'metadata'
    #__table_args__ = {'extend_existing': True} 
    id = Column(Integer, primary_key=True)
    table_name = Column(String(200))
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)
    description = Column(String(200))

def create_meta_table(db_str = DB):
    # Create the engine and session
    engine = create_engine(db_str)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create MetaData instance
    meta = MetaData()

    # Delete the associated metadata
    if not inspect(engine).has_table('metadata'):
        metadata_table = MetaData()
    ### already exists, return True
    else:
        print("table metadata already exists...doing nothing.")
        return True

    # Create the tables
    Base.metadata.create_all(engine)
    session.commit()

    print("table metadata successfully created.")
    return True

def create_table_from_json(file_path, db_str = DB):
    # Get the file name without extension as table name
    table_name = os.path.splitext(os.path.basename(file_path))[0]

    # Create the engine and session
    engine = create_engine(db_str)
    Session = sessionmaker(bind=engine)
    session = Session()

    meta = MetaData()

    # Drop the table if it already exists
    if inspect(engine).has_table(table_name):
        table = Table(table_name, meta, autoload_with=engine)
        table.drop(engine)

    # Delete the associated metadata
    if inspect(engine).has_table('metadata'):
        metadata_table = Table('metadata', meta, autoload_with=engine)
        delete_statement = delete(metadata_table).where(metadata_table.columns.table_name == table_name)
        session.execute(delete_statement)
        session.commit()

    # Load the JSON data
    with open(file_path) as file:
        data = json.load(file)

    # Extract the records and metadata from the data
    records = data.pop('data', [])
    metadata = data

    # Create a dictionary to store the column definitions
    columns = {}

    # Iterate over the items in the first record to create columns
    for key, value in records[0].items():
        # Convert key from camel case to snake case
        column_name = ''.join(['_' + i.lower() if i.isupper() else i for i in key]).lstrip('_')
        columns[column_name] = get_sqlalchemy_type(type(value))

    # Define the Data class dynamically
    Data = table_factory(table_name, columns)

    # Create the tables
    Base.metadata.create_all(engine)

    # Insert JSON data into the table
    for item in records:
        # Convert record to snake case keys
        record = {k: v for k, v in zip(columns.keys(), item.values())}
        session.add(Data(**record))

    # Insert metadata into the metadata table
    for key, value in metadata.items():
        record = Metadata(table_name=table_name, description=f"{key}: {value}")
        session.add(record)

    session.commit()

    # Return the table name and columns
    return table_name, list(columns.keys())

def query_table(table_name, db_str = DB, limit = 5):
    # Create the engine and session
    engine = create_engine(db_str)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Reflect the table
    metadata = MetaData()
    table = Table(table_name, metadata, autoload_with=engine)

    # Query the first 5 records of the table
    records_query = select(table).limit(limit)
    records = session.execute(records_query).fetchall()
    return records

def query_metadata(table_name, db_str = DB):
    # Create the engine and session
    engine = create_engine(db_str)
    Session = sessionmaker(bind=engine)
    session = Session()

    metadata = MetaData()
    metadata_table = Table('metadata', metadata, autoload_with=engine)
    metadata_query = select(metadata_table).where(metadata_table.columns.table_name == table_name)
    metadata_records = session.execute(metadata_query).fetchall()
    return metadata_records


if __name__ == '__main__':
    # Test the function
    for file_name in ['movement.json', 'price.json', 'cost.json', 'promo.json']:
        create_meta_table()
        table_name, columns = create_table_from_json(file_name)
        print(f"\nTable Name: {table_name}")
        print("\ncolums: =====================================")
        print(f"Columns: {columns}")

        print("\nrecords: =====================================")
        records = query_table(table_name)
        print(records)

        print("\nmeta data: =====================================\n")
        meta_data = query_metadata(table_name)
        print(meta_data)
