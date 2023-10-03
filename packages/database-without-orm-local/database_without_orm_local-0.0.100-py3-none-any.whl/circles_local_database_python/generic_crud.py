from typing import Any

from dotenv import load_dotenv
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum

from .connector import Connector
from .utils import validate_select_table_name, validate_none_select_table_name

load_dotenv()

# Constants
DATABASE_WITHOUT_ORM_PYTHON_GENERIC_CRUD_COMPONENT_ID = 206
DATABASE_WITHOUT_ORM_PYTHON_GENERIC_CRUD_COMPONENT_NAME = 'circles_local_database_python\\generic_crud'
DEVELOPER_EMAIL = 'akiva.s@circ.zone'

# Logger setup
logger = Logger.create_logger(object={
    'component_id': DATABASE_WITHOUT_ORM_PYTHON_GENERIC_CRUD_COMPONENT_ID,
    'component_name': DATABASE_WITHOUT_ORM_PYTHON_GENERIC_CRUD_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
})

class GenericCRUD:
    """A class that provides generic CRUD functionality"""
    def __init__(self, schema_name: str, connection: Connector = None, id_column_name: str = None) -> None:
        """Initializes the GenericCRUD class. If connection is not provided, a new connection will be created."""
        self.schema_name = schema_name
        self.connection = connection or Connector.connect(
            schema_name=schema_name)
        self.cursor = self.connection.cursor()
        self.id_column_name = id_column_name

    def set_id_column_name(self, id_column_name: str) -> None:
        logger.start(object={"id_column_name": id_column_name})
        self.id_column_name = id_column_name
        logger.end()

    def insert(self, table_name: str, json_data: dict) -> int:
        """Inserts a new row into the table and returns the id of the new row or -1 if an error occurred."""
        logger.start(object={"table_name": table_name, "json_data": json_data})
        try:
            validate_none_select_table_name(table_name)
            columns = ','.join(json_data.keys())
            values = ','.join(['%s' for _ in json_data])
            insert_query = f"INSERT INTO {self.schema_name}.{table_name} ({columns}) VALUES ({values})"
            self.cursor.execute(insert_query, tuple(json_data.values()))
            self.connection.commit()
            logger.end("Data inserted successfully.")
            return self.cursor.lastrowid()
        except Exception as e:
            logger.exception("Error inserting json_data", object=e)
            logger.end()
            raise

    def select_by_id(self, view_table_name: str, select_clause_value: str = "*", id_column_name: str = None,
                     id_column_value: Any = None, limit: int = 100, order_by: str = "") -> list:
        """Selects data from the table and returns it as a list of tuples."""
        logger.start(object={"view_table_name": view_table_name, "select_clause_value": select_clause_value,
                             "id_column_value": id_column_value})
        if id_column_name is None:
            id_column_name = self.id_column_name
        try:
            validate_select_table_name(view_table_name)
            if self.id_column_name and id_column_value:
                where = f"{self.id_column_name}={id_column_value}"
                result = self.select_by_where(
                view_table_name,select_clause_value,where,limit, order_by)
            logger.end("Data selected successfully.", object={"result": str(result)})
            return result           
        except Exception as e:
            logger.exception("Error selecting json_data", object=e)
            logger.end()
            raise

    def select_by_where(self, view_table_name: str, select_clause_value: str = "*",
                         where: str = None, limit: int = 100, order_by: str = "") -> list:
        """Selects data from the table and returns it as a list of tuples."""
        logger.start(object={"table_name": view_table_name, "select_clause_value": select_clause_value,
                     "where": where, "limit": limit, "order_by": order_by})
        select_query = f"SELECT {select_clause_value} FROM {self.schema_name}.{view_table_name} " + (
            f"WHERE {where} " if where else "") + (f"ORDER BY {order_by}" if order_by else "") + f" LIMIT {limit}"
        self.cursor.execute(select_query)
        result = self.cursor.fetchall()
        logger.end("Data selected successfully.",
                   object={"result": str(result)})
        return result

    def select_one(self, view_table_name: str, select_clause_value: str = "*", id_column_value: Any = None,
                   where: str = None) -> tuple:
        """Selects data from the table and returns it as a tuple."""
        # select handles all the validation / logs
        logger.start(object={"table_name": view_table_name, "select_clause_value": select_clause_value, "id_column_name": self.id_column_name,
                             "id_column_value": id_column_value, "where": where})
        try:
            if self.id_column_name and id_column_value != None:
                result = self.select_by_column_id(view_table_name, select_clause_value,
                                 id_column_value, limit=1)
            else:
                result = self.select_by_where(view_table_name, select_clause_value, where, limit=1) [0]
        except Exception as e:
            logger.exception("Error selecting json_data", object=e)
            logger.end()
            raise
        return result

    def update(self, table_name: str, json_data: dict, id_column_value: Any = None,
               where: str = None) -> None:
        """Updates data in the table.
        If id_column_name and id_column_value are provided, the row with the given id_column_value will be updated.
        If where is provided, the rows that match the where clause will be updated."""
        logger.start(object={"table_name": table_name, "json_data": json_data, "id_column_name": self.id_column_name,
                             "id_column_value": id_column_value, "where": where})
        try:
            validate_none_select_table_name(table_name)
            set_values = ', '.join(
                [f"{k}=%s" for k in json_data.keys()]) + ("," if json_data else "")
            if self.id_column_name and id_column_value:
                where = f"{self.id_column_name}={id_column_value}"
            if where:
                update_query = f"UPDATE {self.schema_name}.{table_name} SET {set_values} updated_timestamp=CURRENT_TIMESTAMP() WHERE {where}"
                self.cursor.execute(update_query, tuple(json_data.values()))
            else:
                message = "Update requires a 'where', or id_column_name and id_column_value."
                logger.error(message)
                logger.end()
                raise Exception(message)

            self.connection.commit()
            logger.end("Data updated successfully.")
        except Exception as e:
            logger.exception("Error updating json_data", object=e)
            logger.end()
            raise

    def delete_by_id(self, table_name: str, id_column_name: str = None, id_column_value: Any = None) -> None:
        """Deletes data from the table by id"""
        logger.start(object={"table_name": table_name, "id_column_name": self.id_column_name,
                             "id_column_value": id_column_value})
        if id_column_name is None:
            id_column_name = self.id_column_name
        try:
            self.update(table_name=table_name, json_data={}, id_column_value=id_column_value)
            if self.id_column_name and id_column_value != None:
                update_query = f"UPDATE {self.schema_name}.{table_name} SET end_timestamp=CURRENT_TIMESTAMP() WHERE {self.id_column_name}={id_column_value}"
                self.cursor.execute(update_query)
                self.connection.commit()
            logger.end("Deleted successfully.")
        except Exception as e:
            logger.exception("Error while deleting", object=e)
            logger.end()
            raise

    def delete_by_where(self, table_name: str, where: str = None) -> None:
        """Deletes data from the table by WHERE."""
        logger.start(object={"table_name": table_name, "where": where})
        try:
            self.update(table_name=table_name, json_data={}, where=where)
            if where != None:
                update_query = f"UPDATE {self.schema_name}.{table_name} SET end_timestamp=CURRENT_TIMESTAMP() WHERE {where}"
                self.cursor.execute(update_query)
                self.connection.commit()
            logger.end("Deleted successfully.")
        except Exception as e:
            logger.exception("Error while deleting", object=e)
            logger.end()
            raise

    def select_one_by_id(self, view_table_name: str, select_clause_value: str = "*", id_column_name: str = None, id_column_value: Any = None) -> tuple:
        """Selects one row from the table by ID and returns it as a tuple."""
        logger.start(object={"view_table_name": view_table_name, "select_clause_value": select_clause_value, "id_column_name": id_column_name,
                             "id_column_value": id_column_value})
        where = f"{id_column_name}={id_column_value}"
        try:
            result = self.select_by_where(
                view_table_name, select_clause_value, where, limit=1)[0]
        except Exception as e:
            logger.exception("Error selecting json_data", object=e)
            logger.end()
            raise
        logger.end("Data selected successfully.",
                   object={"result": str(result)})
        return result

    def select_one_by_where(self, view_table_name: str, select_clause_value: str = "*", where: str = None) -> list:
        """Selects one row from the table based on a WHERE clause and returns it as a tuple."""
        logger.start(object={"view_table_name": view_table_name,
                     "select_clause_value": select_clause_value, "where": where})
        try:
            result = self.select_by_where(
                view_table_name, select_clause_value, where=where, limit=1)[0]
        except Exception as e:
            logger.exception("Error selecting json_data", object=e)
            logger.end()
            raise
        logger.end("Data selected successfully.",
                   object={"result": str(result)})
        return result

    def select_multi_by_id(self, view_table_name: str, select_clause_value: str = "*", id_column_name: str = None, id_column_value: Any = None, limit: int = 100, order_by: str = "") -> list:
        """Selects multiple rows from the table by ID and returns them as a list of tuples."""
        logger.start(object={"view_table_name": view_table_name, "select_clause_value": select_clause_value, "id_column_name": id_column_name,
                             "id_column_value": id_column_value, "limit": limit, "order_by": order_by})
        where = f"{id_column_name}={id_column_value}"
        try:
            result = self.select_by_where(
                view_table_name, select_clause_value, where, limit, order_by)
        except Exception as e:
            logger.exception("Error selecting json_data", object=e)
            logger.end()
            raise
        logger.end("Data selected successfully.",
                   object={"result": str(result)})
        return result

    def select_multi_by_where(self, view_table_name: str, select_clause_value: str = "*", where: str = None, limit: int = 100, order_by: str = "") -> list:
        """Selects multiple rows from the table based on a WHERE clause and returns them as a list of tuples."""
        logger.start(object={"view_table_name": view_table_name,
                     "select_clause_value": select_clause_value, "where": where})
        try:
            result = self.select_by_where(
                view_table_name, select_clause_value, where, limit, order_by)
        except Exception as e:
            logger.exception("Error selecting json_data", object=e)
            logger.end()
            raise
        logger.end("Data selected successfully.",
                   object={"result": str(result)})
        return result

    def switch_db(self, new_database: str) -> None:
        """Switches the database to the given database name."""
        logger.start(object={"schema_name": new_database})
        self.connection.set_schema(new_database)
        self.schema_name = new_database
        logger.end("Schema set successfully.")

    def close(self) -> None:
        """Closes the connection to the database."""
        logger.start()
        self.connection.close()
        logger.end()
