from database import get_db_connection


def truncate(table: str):
    connection = get_db_connection()
    cursor = connection.cursor()

    with cursor:
        cursor.execute('''
            TRUNCATE %s
        ''', table)

        connection.commit()

    connection.close()
