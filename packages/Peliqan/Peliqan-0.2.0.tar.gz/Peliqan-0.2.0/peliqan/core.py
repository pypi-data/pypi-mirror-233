# import necessary modules
import logging

import pandas as pd
from peliqan.client import WritebackClient, BackendServiceClient, DBClient, SFTPClient
from peliqan.exceptions import PeliqanClientException

# get logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.propagate = False

# get log handler
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)

# set log format
formatter = logging.Formatter("[%(asctime)s] %(levelname)s %(name)s %(message)s")

# set format to log handler
sh.setFormatter(formatter)

# add handler to logger
logger.addHandler(sh)


class BasePeliqanClient:
    """
    This base class wraps all operations we want to expose to our internal and external clients.
    """

    def __init__(self, jwt, backend_url):
        self.JWT = jwt
        self.BACKEND_URL = backend_url
        self.__service_client__ = BackendServiceClient(jwt, backend_url)

    def find_resource(self, resource_type, resource_id=None, resource_name=None, **kwargs):
        """

           :param resource_type: can be connection/database/table.
           :param resource_id: id of the resource.
           :param resource_name: name of the resource.
           :param kwargs: additional kwargs can also be passed.
           :return: resource details as a dict.
        """
        return self.__service_client__.find_resource(resource_type, resource_id, resource_name, **kwargs)

    def _to_dtype(self, column_type, tz, enable_datetime_as_string):
        if (
            column_type[0:3].lower() == "int" or
            column_type[0:3].lower() == "num" or
            column_type[0:6].lower() == "bigint"
        ):  # todo add more field types
            type_name = pd.Int64Dtype()

        elif (
            column_type[0:6].lower() == "double" or
            column_type[0:5].lower() == "float" or
            column_type[0:7].lower() == "decimal"
        ):
            type_name = pd.Float64Dtype()

        elif column_type[0:4].lower() == "bool":
            type_name = pd.BooleanDtype()

        elif not enable_datetime_as_string and (
            column_type == "date" or
            column_type[0:9].lower() == "timestamp" or
            column_type[0:8].lower() == "datetime"
        ):
            type_name = pd.DatetimeTZDtype(tz=tz)

        else:
            type_name = pd.StringDtype()

        return type_name

    # todo allow user to set a PK column for the query (or update the guessed PK)
    def load_table(self, table_name='', query='', table_id=None, df=False, fillna_with=None, fillnat_with=None,
                   enable_python_types=True, enable_datetime_as_string=True, tz='UTC'):
        """
        Return the records in a table.

        :param table_name: The name of a table.
        :param query: A valid Trino sql query.
        :param table_id: An integer value that uniquely identifies a table.
        :param df: This flag decides what should be returned by this function. df=True returns a dataframe. df=False returns an array of dicts, where each item represents a row with column name as the key.
        :param fillna_with: Replace empty/invalid values (NA) with a default value. This will also replace NaN values.
        :param fillnat_with: Replace invalid time/datetime values (NaT) with a default value.
        :param enable_python_types: This flag will cause the record's values to be returned as python types
        :param enable_datetime_as_string: This flag will cause date/time/datetime objects to be converted to string.
        :param tz: This is the timezone that will be used to convert date and datetime strings
        to timezone aware datetime objects. This value defaults to 'UTC'.

        :return:
        """

        # table_id will return the raw table data.
        # This causes multiple select and single select to be returned as json objects

        # query and table_name will return the data as if the queried table is a prepended statement.
        # This causes multiple select and single select to be returned as strings instead of a json object

        if query:
            url_suffix = f"?query={query}"
        elif table_id:
            url_suffix = f"?table_id={table_id}"
        elif table_name:
            url_suffix = f"?table_name={table_name}"
        else:
            raise PeliqanClientException("Input 'table_name' (table or view name), 'query' or 'table_id' must be set.")

        json_response = self.__service_client__.get_records(url_suffix)

        error = json_response['error']
        if error:
            raise PeliqanClientException(f"Client encountered a error while fetching records,\n{error}")

        records = json_response['records']
        column_data = json_response['columns']

        columns = []
        dtypes = []
        for column in column_data:
            dtypes.append((column[0], self._to_dtype(column[1], tz, enable_datetime_as_string)))
            columns.append(column[0])

        # Create dataframe
        dataframe = pd.DataFrame(records, columns=columns)
        if enable_python_types:
            for dtype in dtypes:
                dataframe[dtype[0]] = dataframe[dtype[0]].astype(dtype[1])

        dataframe.replace({pd.NaT: fillnat_with, pd.NA: fillna_with}, inplace=True)

        if df:
            return dataframe

        else:
            return dataframe.to_dict('records')

    # todo: make it easier to find table & field ids in UI
    def update_cell(self, row_pk, value, table_id=None, table_name=None, field_id=None, field_name=None):
        if not row_pk:
            raise PeliqanClientException("row_pk must be provided.")

        # BACKEND_URL and JWT are prepended to the generated script,
        # see create_script() --> transform_script() in peliqan/convert_raw_script.py
        base_url = f"{self.BACKEND_URL}/api/database/rows/table/%s/row/"

        if not table_id and not table_name:
            raise PeliqanClientException("table_id or table_name must be provided as kwargs")
        elif not table_id and table_name:
            # only do this if table_id is not provided
            table_id = self.__service_client__.get_cached_results('table', table_name, 'table_id')

        # prioritise field id
        if field_id:
            field_physical_name = f"field_{field_id}"
        elif field_name:
            for key in [table_name, table_id]:
                field_physical_name = self.__service_client__.get_cached_results('table', key, field_name)
                if field_physical_name:
                    break
        else:
            raise PeliqanClientException("field_id or field_name must be provided as kwargs")

        # Discover table_id and field_physical_name
        if not field_physical_name or not table_id:
            lookup_data = self.find_resource('table', resource_id=table_id, resource_name=table_name,
                                             field_id=field_id, field_name=field_name)
            field_physical_name = f"field_{lookup_data['field_id']}"
            table_id = lookup_data['table_id']

        # set the final url
        if type(table_id) != int:
            raise PeliqanClientException("table_id could not be resolved, please check provided arguments.")

        # set table_id to base url
        url = base_url % table_id

        data = {
            'row_id': row_pk,
            'value': value,
            'table_id': table_id,
            field_physical_name: value
        }
        return self.__service_client__.push_cdclog(url, data)

    def refresh_connection_status(self, connection_name=None, connection_id=None, task_id=''):
        base_url = f"{self.BACKEND_URL}/api/servers/%s/syncdb/status/"
        return self.__service_client__.refresh_resource_task_status(
            resource_type='connection',
            refresh_baseurl=base_url,
            resource_name=connection_name,
            resource_id=connection_id,
            task_id=task_id
        )

    def refresh_database_status(self, connection_name=None, database_name=None, database_id=None, task_id=''):
        base_url = f"{self.BACKEND_URL}/api/applications/%s/syncdb/status/"
        return self.__service_client__.refresh_resource_task_status(
            resource_type='database',
            refresh_baseurl=base_url,
            resource_name=database_name,
            resource_id=database_id,
            task_id=task_id,
            connection_name=connection_name
        )

    def refresh_table_status(self, connection_name=None, database_name=None, table_name=None, table_id=None,
                             task_id=''):
        base_url = f"{self.BACKEND_URL}/api/database/tables/%s/syncdb/status/"
        return self.__service_client__.refresh_resource_task_status(
            resource_type='table',
            refresh_baseurl=base_url,
            resource_name=table_name,
            resource_id=table_id,
            task_id=task_id,
            connection_name=connection_name,
            database_name=database_name
        )

    def refresh_connection(self, connection_name=None, connection_id=None):
        base_url = f"{self.BACKEND_URL}/api/servers/%s/syncdb/"
        return self.__service_client__.refresh_resource(resource_type='connection', refresh_baseurl=base_url,
                                                        resource_name=connection_name, resource_id=connection_id)

    def refresh_database(self, connection_name=None, database_name=None, database_id=None):
        base_url = f"{self.BACKEND_URL}/api/applications/%s/syncdb/"
        return self.__service_client__.refresh_resource(resource_type='database', refresh_baseurl=base_url,
                                                        resource_name=database_name, resource_id=database_id,
                                                        connection_name=connection_name)

    def refresh_table(self, connection_name=None, database_name=None, table_name=None, table_id=None):

        base_url = f"{self.BACKEND_URL}/api/database/tables/%s/syncdb/"
        return self.__service_client__.refresh_resource(resource_type='table', refresh_baseurl=base_url,
                                                        resource_name=table_name, resource_id=table_id,
                                                        database_name=database_name, connection_name=connection_name)

    def connect(self, connection=None):
        """
        :param connection: name of the Connection added in Peliqan under Admin > Connections.
        Or a dict with connection properties (credentials etc.).
        """
        if not connection:
            raise PeliqanClientException("connection must be set.")
        connector = WritebackClient(connection, self.JWT, self.BACKEND_URL)
        return connector

    def dbconnect(self, connection=None):
        """
        :param connection: name of the Connection added in Peliqan under Admin > Connections.
        Or a dict with connection properties (credentials etc.).
        """
        if not connection:
            raise PeliqanClientException("connection must be set.")
        connector = DBClient(connection, self.JWT, self.BACKEND_URL)
        return connector

    def sftpconnect(self, connection=None):
        """
        :param connection: name of the Connection added in Peliqan under Admin > Connections.
        Or a dict with connection properties (credentials etc.).
        """
        if not connection:
            raise PeliqanClientException("connection must be set.")
        connector = SFTPClient(connection, self.JWT, self.BACKEND_URL)
        return connector

    def _validate_and_lookup_table(self, table_id, table_name):
        if not table_id and not table_name:
            raise PeliqanClientException("table_id or table_name must be provided as kwargs")
        elif not table_id and table_name:
            # only do this if table_id is not provided
            table_id = self.__service_client__.get_cached_results('table', table_name, 'table_id')

        if not table_id:
            lookup_data = self.find_resource('table', resource_id=table_id, resource_name=table_name)
            table_id = lookup_data['table_id']

        if type(table_id) != int:
            raise PeliqanClientException("table_id could not be resolved, please check provided arguments.")

        return table_id

    def _validate_writeback_status(self, writeback_status):
        error = False
        if type(writeback_status) == list:
            writeback_status_str = ''
            for w in writeback_status:
                w_status = w.upper()
                if w_status not in ["NOT_PROCESSED", "PROCESSED", "CONFIRMED", "FAILED"]:
                    error = True
                    break
                else:
                    writeback_status_str += w_status + ','
            writeback_status = writeback_status_str.rstrip(',')
        elif (
            writeback_status is not None and
            (
                type(writeback_status) != str or writeback_status.upper() not in
                ["NOT_PROCESSED", "PROCESSED", "CONFIRMED", "FAILED"]
            )
        ):
            error = True

        if error:
            raise PeliqanClientException(
                f"writeback_status is not valid. "
                f"Allowed status values are "
                f"'NOT_PROCESSED', 'PROCESSED', 'CONFIRMED', 'FAILED'."
            )

        return writeback_status

    def list_changes(self, table_id=None, table_name=None, writeback_status=None, change_type=None,
                     latest_changes_first=False):
        """
        List the cdc changes in order.
        Optionally, pass writeback_status and/or change_type as a string or list of strings.

        :param table_id: unique integer identifier for a table
        :param table_name: the name or fqn of the table.
        :param writeback_status: valid string or list of string values
        :param change_type: valid string or list of string values
        :param latest_changes_first: use this to get toggle the order of changes (Asc/Desc of id). default is False.
        :return:
        """

        error = False
        # i = insert, u = update, d = delete, t = transformation, f = formula, l = link (to another table)
        # m = multiselect
        if type(change_type) == list:
            change_type_str = ''
            for c in change_type:
                c_type = c.lower()
                if c_type not in ["i", "u", "d", "f", "t", "m", "l"]:
                    error = True
                    break
                else:
                    change_type_str += c_type + ','

            change_type = change_type_str.rstrip(',')
        elif (
            change_type is not None and
            (type(change_type) != str or change_type.lower() not in ["i", "u", "d", "f", "t", "m", "l"])
        ):
            error = True

        if error:
            raise PeliqanClientException(
                f"change_type is not valid. Allowed status values are 'i', 'u', 'd', 'f', 't', 'm', 'l'.\n"
                f"i = insert, u = update, d = delete, t = transformation, f = formula, l = link (to another table)"
                f"m = multiselect."
            )

        writeback_status = self._validate_writeback_status(writeback_status)

        table_id = self._validate_and_lookup_table(table_id, table_name)

        return self.__service_client__.get_cdclogs(table_id=table_id, writeback_status=writeback_status,
                                                   change_type=change_type, latest_changes_first=latest_changes_first)

    def update_writeback_status(self, change_id, writeback_status, table_id=None, table_name=None):
        """
        Update the writeback_status for a cdc log.

        :param change_id: unique integer identifier for a cdc log.
        :param writeback_status: valid status value.
        :param table_id: unique integer identifier for a table
        :param table_name: the name or fqn of the table.
        :return:
        """
        table_id = self._validate_and_lookup_table(table_id, table_name)
        if (
            type(writeback_status) != str or
            writeback_status.upper() not in ["NOT_PROCESSED", "PROCESSED", "CONFIRMED", "FAILED"]
        ):
            raise PeliqanClientException(
                f"writeback_status is not valid. "
                f"Allowed status values are "
                f"'NOT_PROCESSED', 'PROCESSED', 'CONFIRMED', 'FAILED'."
            )

        try:
            change_id = int(change_id)
        except ValueError:
            raise PeliqanClientException("change_id must be a valid integer")

        return self.__service_client__.update_writeback_status(table_id, change_id, writeback_status)

    def list_databases(self):
        """
        Returns a list of all databases in the account including tables and fields in tables.

        :return: list of databases
        """
        return self.__service_client__.get_databases()

    def update_field(self, id, description=None, tags=None):
        """
        Updates a field (column).

        :param id: required, integer, id of the field to update
        :param description: optional, string, description of the field (data catalog metadata)
        :param tags: optional, array of strings, tags assigned to the field (data catalog metadata)
        :return: result of update
        """

        return self.__service_client__.update_field_metadata(id, description, tags)

    def update_table(self, id, name=None, table_type=None, query=None, external=None, primary_field_id=None,
                     settings=None,
                     description=None, tags=None):
        """
        Updates a table.

        :param id: required, integer, id of the table to update
        :param name: optional, string, new name of the table
        :param table_type: optional, string, new type of the table, e.g. 'query'
        :param query: optional, string, new SQL query for tables of type 'query'
        :param external: optional, boolean, true for external tables, false for internal tables
        :param primary_field_id: optional, integer, primary key field id for this table, i.e. the field id in Peliqan.
        See, table details page in Peliqan to get the primary_field_id for a table.
        :param settings: optional, string (json), settings of the table
        :param description: optional, string, description of the table (data catalog metadata)
        :param tags: optional, array of strings, tags assigned to the table (data catalog metadata)
        :return: result of update
        """

        update_result_dict = {}
        update_metadata_result_dict = {}
        if name or table_type or query or external or primary_field_id or settings:
            update_result_dict = self.__service_client__.update_table(id, name, table_type, query, external,
                                                                      primary_field_id, settings)
        if description or tags:
            update_metadata_result_dict = self.__service_client__.update_table_metadata(id, description, tags)
        return {**update_result_dict, **update_metadata_result_dict}

    def update_database(self, id, description=None, tags=None):
        """
        Updates a database.

        :param id: required, integer, id of the database to update
        :param description: optional, string, description of the database (data catalog metadata)
        :param tags: optional, array of strings, tags assigned to the database (data catalog metadata)
        :return: result of update
        """

        return self.__service_client__.update_database_metadata(id, description, tags)

    def generate_sql_union(self, table_ids, sources=None):
        """
        Generates an SQL UNION query for the given tables.
        All columns of all tables will be added to the UNION query.
        If a column does not exist in one of the tables, it will be added with a null value.
        Optionally, a "source" column can be added to indicate from which table each row originated.

        :param table_ids: required, list of integers, list of table ids to include in UNION query
        :param sources: optional, dict, if set an extra 'source' column will be added to indicate to which table the record belongs. Keys are table ids. Values are source value to include in UNION result. Example: { 1: "Paris", 2: "London" }. This will add a column "source" to the UNION where all records from table id 1 will have value "Paris" for the source.
        :return: result of update
        """
        databases = self.__service_client__.get_databases()
        tables = []
        fields = []
        field_types = {}
        fields_to_cast = []
        for database in databases:
            for table in database["tables"]:
                if table["id"] in table_ids:
                    tables.append(table)
                    for field in table["all_fields"]:
                        if field["name"] not in fields:
                            fields.append(field["name"])
                            if field["sql_data_type"]:
                                field_types[field["name"]] = field[
                                    "sql_data_type"]  # Actual field type in source, e.g. timestamp, timestamptz... (might not be available for all sources)
                            else:
                                field_types[field["name"]] = field["type"]  # Peliqan field type, e.g. "date"
                        elif (field["sql_data_type"] and field["sql_data_type"] != field_types[field["name"]]) or field[
                            "type"] != field_types[field["name"]]:
                            fields_to_cast.append(field["name"])

        table_selects = []
        for table in tables:
            table_select_fields = []
            if sources:
                source_name = ""
                for source_table_id, source_table_name in sources.items():
                    if int(source_table_id) == table['id']:
                        source_name = source_table_name
                table_select_fields.append("'%s'" % source_name + " source")
            for field in fields:
                table_has_field = False
                for table_field in table["all_fields"]:
                    if (
                        field[0] == '"' and table_field["name"] == field) or (
                        field[0] != '"' and table_field["name"].lower() == field.lower()
                    ):
                        table_has_field = True
                        break
                if table_has_field:
                    if field in fields_to_cast:
                        if table_field["sql_data_type"] and table_field["sql_data_type"] == "timestamptz":
                            # Postgres fields of type timestamptz (timestamp with timezone) cannot be cast to varchar directly by Trino
                            table_select_fields.append("CAST(CAST(%s AS TIMESTAMP) AS VARCHAR) AS %s" % (field, field))
                        else:
                            table_select_fields.append("CAST(%s AS VARCHAR) AS %s" % (field, field))
                    else:
                        table_select_fields.append(field)
                else:
                    table_select_fields.append("null " + field)
            table_select_fields_str = ", ".join(table_select_fields)

            table_select = "SELECT %s FROM %s" % (table_select_fields_str, table["name"])
            table_selects.append(table_select)

        union = " UNION ALL ".join(table_selects)
        return union

    def get_interface_state(self, interface_id):
        """
        An interface is a saved program. Get the stored state for a specific interface.

        :param interface_id: The id of the interface.
        :return: Any
        """
        return self.__service_client__.get_interface_state(interface_id)

    def set_interface_state(self, interface_id, state):
        """
        An interface is a saved program. Set the state for a specific interface in the peliqan environment.

        :param interface_id: The id of the interface.
        :param state: The data that will be stored as the state value for an interface.
        :return:
        """
        return self.__service_client__.set_interface_state(interface_id, state)
