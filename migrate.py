import re
import sys
from os import path, listdir

from pymysql import OperationalError, ProgrammingError

from database import get_db_connection


def exec_sql_file(cursor, sql_file):
    # print("\n[INFO] Executing SQL script file: '%s'" % sql_file)
    statement = ""

    for line in open(sql_file):
        if re.match(r'--', line):  # ignore sql comment lines
            continue
        if not re.search(r';$', line):  # keep appending lines that don't end in ';'
            statement = statement + line
        else:  # when you get a line ending in ';' then exec statement and reset for next statement
            statement = statement + line
            # print("\n[DEBUG] Executing SQL statement:%s" % statement)
            try:
                cursor.execute(statement)
            except (OperationalError, ProgrammingError) as e:
                print("\n[WARN] MySQLError during execute statement \n\tArgs: '%s'" % (str(e.args)))

            statement = ""


def execute(cursor, files):
    for file in files:
        up_sql = path.abspath('migrate/' + file)
        exec_sql_file(cursor, up_sql)
        print('[ MIGRATION ] Done: ', file)


def get_migrate_files():
    migration_folder = listdir('migrate')

    ups = []
    downs = []
    seeds = []

    for file in migration_folder:
        if 'seed.sql' in file:
            seeds.append(file)
        elif 'up.sql' in file:
            ups.append(file)
        elif 'down.sql' in file:
            downs.append(file)

    return {
        'ups': ups,
        'downs': downs,
        'seeds': seeds
    }


def migrate(argument):
    migration_files = get_migrate_files()
    ups = migration_files['ups']
    downs = migration_files['downs']
    seeds = migration_files['seeds']

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        print(f'[ MIGRATION ] ###### {argument} Start! ######')
        if argument == 'up':
            execute(cursor, ups)
        if argument == 'down':
            execute(cursor, downs)
        if argument == 'seed':
            execute(cursor, seeds)
        if argument == 'all':
            execute(cursor, downs)
            execute(cursor, ups)
            execute(cursor, seeds)
        connection.commit()
        print(f'[ MIGRATION ] ###### {argument} Done!  ######')
    except Exception as error:
        print('[ MIGRATION ] Failed: ', error)
        connection.rollback()
    finally:
        connection.close()


if __name__ == "__main__":
    args = sys.argv
    arg = args[1]

    migrate(arg)
