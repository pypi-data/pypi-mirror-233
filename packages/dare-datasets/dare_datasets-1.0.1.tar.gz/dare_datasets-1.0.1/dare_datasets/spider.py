from typing import Dict, Optional

import pandas as pd

from dare_datasets.dataset_abc import Dataset
from dare_datasets.processing.spider.dealiasing import dealias_tables
from dare_datasets.processing.spider.execute_sqlite_query import \
    execute_sqlite_query
from dare_datasets.processing.spider.lower import lowercase_query
from dare_datasets.processing.spider.serialize_schema import serialize_schema
from dare_datasets.repositories.huggingface import \
    get_file_from_huggingface_hub
from dare_datasets.utils.require_files import requires_files
from dare_datasets.utils.unzip import unzip_files

HUGGINGFACE_REPO = "spider"


class Spider(Dataset):
    """
    **Usage**
    ```python
    from dare_datasets import Spider

    spider = Spider()
    df = spider.get()
    ```
    """

    def __init__(self, cache_dir: Optional[str] = None) -> None:
        super().__init__(HUGGINGFACE_REPO, cache_dir)

    def get_info(self) -> Dict[str, str]:
        """
        Returns a dictionary containing information about the dataset.
        """
        return {
            "name": "Spider",
            "description": "Yale Semantic Parsing and Text-to-SQL Challenge.",
            "huggingface_repo": HUGGINGFACE_REPO,
            "original_url": "https://yale-lily.github.io/spider",
            "formats": ["json"],  # List of available formats
            "dataset_folder": self.dataset_folder if self.data is not None else "NOT_YET_LOADED"
        }

    def _init_data(self):
        """
        Downloads the Spider dataset from Huggingface, unzips it, and loads the
        train set, dev set, and tables files.
        """
        # Download the dataset from huggingface
        get_file_from_huggingface_hub(
            repo_id=HUGGINGFACE_REPO, cache_dir=self.cache_dir,
            post_processing=[
                (unzip_files, [self.dataset_folder, ["data/spider.zip"]])
            ])

        # Load the train json file
        train_df = pd.read_json(self.dataset_folder +
                                "spider/train_spider.json")
        # Load the dev json file
        dev_df = pd.read_json(self.dataset_folder + "spider/dev.json")
        # Load the tables (schema) json file
        tables_df = pd.read_json(
            self.dataset_folder + "spider/tables.json")

        self.data = {'train': train_df, 'dev': dev_df, 'tables': tables_df}

    @requires_files
    def get(self) -> Dict[str, pd.DataFrame]:
        """
        Returns a dictionary with the train and dev splits of the dataset,
        containing only the NL Question, SQL query and db_id.

        Returns:
            Dict[str, pd.DataFrame]: A dictionary with keys "train" and "dev",
                and the corresponding DataFrames with columns "question",
                "query", and "db_id".
        """
        return {
            'train': self.data['train'][['question', 'query', 'db_id']],
            'dev': self.data['dev'][['question', 'query', 'db_id']]
        }

    @requires_files
    def get_raw(self) -> Dict[str, pd.DataFrame]:
        """
        Returns a dictionary containing the train, dev, and tables json files
        that have been directly loaded as Pandas DataFrames.

        Returns:
            Dict[str, pd.DataFrame]: A dictionary with keys "train" and "dev",
                and the entire corresponding json file loaded as a DataFrame.
        """
        return self.data

    @requires_files
    def _check_db_id(self, db_id: str) -> None:
        """
        Checks if the given db_id is valid.

        Args:
            db_id (str): A database id

        Returns:
            None if the db_id is a valid one else raise a FileNotFound exception
        """
        if not (self.data["tables"]["db_id"] == db_id).any():
            raise FileNotFoundError(f"The requested db_id ({db_id}) does not exist!")

    @requires_files
    def get_schema(self, db_id: str) -> pd.DataFrame:
        """Returns the schema json object that corresponds to the given db_id.

        Args:
            db_id (str): A database id that should appear in the tables.json file.

        Returns:
            pd.DataFrame: The json object in the tables.json file that corresponds
                to the given db_id.
        """
        return self.data['tables'][self.data['tables']['db_id'] == db_id]

    @requires_files
    def execute_query(self, sql_query: str, db_id: str) -> pd.DataFrame:
        """
        Returns the result after executing the query in the database

        Args:
            sql_query (str): The query to be executed.
            db_id (str): The id of the database to execute the query.

        Returns:
            pd.DataFrame: The execution result of the given sql_query in the database that
            corresponds to the given db_id.
        """

        self._check_db_id(db_id=db_id)

        # Get the path of the sqlite file
        sqlite_path = self.dataset_folder + f"spider/database/{db_id}/{db_id}.sqlite"

        return execute_sqlite_query(sql_query=sql_query, sqlite_path=sqlite_path)

    @requires_files
    def serialize_schema(self, db_id: str,
                         with_db_id: bool = True,
                         with_fp_relations: bool = False,
                         db_id_sep: str = " | ",
                         table_sep: str = " | ",
                         table_column_sep: str = " : ",
                         column_sep: str = " , ",
                         fp_relations_sep: str = " | ",
                         fp_relation_sep: str = " , "
                         ) -> str:
        """
        Returns the schema of the db as a string.

        Args:
            db_id (str): The database id, which schema will be serialized
            with_db_id (bool): If True the serialization will contain the id of the database
            with_fp_relations (bool): If True the serialization will contain the foreign-primary key relations of
                                      the schema
            db_id_sep (str): The separator string between the db id and the rest of the schema
            table_sep (str): The separation string between two tables of the schema
            table_column_sep (str): The separation string between a table and its columns
            column_sep (str): The separation string between two columns of the schema
            fp_relations_sep (str): The separation string between the foreign-primary key relations and the rest of
                                    the schema
            fp_relation_sep (str): The separation string between two foreign-primary key relations of the schema

        Returns:
            str: The database schema in a string format
        """

        self._check_db_id(db_id=db_id)

        # Get the schema of the database
        schema = self.get_schema(db_id=db_id)

        return serialize_schema(schema=schema, with_db_id=with_db_id, with_fp_relations=with_fp_relations,
                                db_id=db_id, db_id_sep=db_id_sep, table_sep=table_sep,
                                table_column_sep=table_column_sep, column_sep=column_sep,
                                fp_relations_sep=fp_relations_sep, fp_relation_sep=fp_relation_sep)

    @staticmethod
    def dealias_query_tables(query: str) -> str:
        """
        Remove aliases from the given query and replace them with the original table names.

        Args:
            query (str): A string of the SQL Query to be de-aliased.

        Returns:
            str: The SQL query with all table aliases removed.
        """
        return dealias_tables(query)

    @staticmethod
    def lower_case_query(query: str) -> str:
        """
        Lower case the query without changing values that appear in the query.

        Args:
            query (str): A string of the SQL Query to be lower cased.

        Returns:
            str: The SQL query with characters lower cased.
        """
        return lowercase_query(query)
