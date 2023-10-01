import csv
from io import StringIO

import pandas as pd
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection, cursor


class PostgresHandler:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn: connection = None
        self.cursor: cursor = None

    def connect(self):
        self.conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

    def execute_query(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def read_sql_query(self, query, params=None):
        df = pd.read_sql_query(query, self.conn, params=params)
        return df

    def execute_update(self, query, params=None):
        self.cursor.execute(query, params)
        self.conn.commit()

    def insert_records(self, table_name, records):
        columns = records[0].keys()
        values = [tuple(record.values()) for record in records]

        insert_query = sql.SQL("INSERT INTO {} ({}) VALUES {}").format(
            sql.Identifier(table_name),
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(sql.Placeholder() * len(records))
        )

        self.execute_update(insert_query, values)


    def delete_then_create_table_and_populate_from_df(self, table_name, df):
        from sqlalchemy import create_engine
        import io

        engine = create_engine(
            f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}')
        df.head(0).to_sql(table_name, engine, if_exists='replace', index=False)

        conn = engine.raw_connection()
        cur = conn.cursor()
        output = io.StringIO()
        df.to_csv(output, sep='\t', header=False, index=False)
        output.seek(0)
        contents = output.getvalue()
        cur.copy_from(output, table_name, null="")  # null values become ''
        conn.commit()
        cur.close()
        conn.close()

    #TODO: this method can still be improved. for large dataframes, we can buffer loading its rows into memory
    # and then insert them in batches
    def insert_rows_from_df(self, table_name, df, null='\\\\N'):
        sio = StringIO()
        writer = csv.writer(sio, delimiter="|")
        writer.writerows(df.values)
        sio.seek(0)

        with self.conn.cursor() as c:
            c.copy_from(
                file=sio,
                table=table_name,
                columns=list(df.columns),
                sep="|",
                null=null
            )
            self.conn.commit()

    def insert_rows_from_df_schema_supported(self, table_name, schema_name, df):
        buf = StringIO()
        df.to_csv(buf, index=False)
        buf.seek(0)
        copy_sql = """
                   COPY %s FROM stdin WITH CSV HEADER
                   """
        with self.conn.cursor() as c:
            c_name = f'{schema_name}.{table_name}'
            c.copy_expert(sql=copy_sql % c_name, file=buf)
            self.conn.commit()




    def delete_records(self, table_name, condition, params=None, schema_name=None):
        if schema_name is None:
            schema_name='public'

        delete_query = sql.SQL("DELETE FROM {}.{} WHERE {}").format(
            sql.Identifier(schema_name),
            sql.Identifier(table_name),
            sql.SQL(condition)
        )
        self.execute_update(delete_query, params)



    def close(self):
        self.cursor.close()
        self.conn.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

