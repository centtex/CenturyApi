import MySQLdb


def updatedb():
    db = MySQLdb.connect(host="localhost", user="century", passwd="Century#123456", db="CenturyTexDev")
    c = db.cursor()
    sql_stmt = "select col.table_name, col.column_name, col.CHARACTER_MAXIMUM_LENGTH" \
               " from information_schema.columns col" \
               " left join information_schema.tables tab on tab.table_schema = col.table_schema " \
               "and tab.table_type = 'BASE TABLE' where col.data_type in ('varchar', 'text') " \
               "and col.table_schema = 'centurytex' and col.table_name not in " \
               "('Configuration', 'usermaster', 'usertypemaster', 'SyncData', 'alembic_version');"
    print(sql_stmt)

    c.execute(sql_stmt)
    result = c.fetchall()
    for row in result:
        print(row)
        if row[2] > 50:
            sql_stmt = "UPDATE `%s` SET `%s` = REGEXP_REPLACE(%s, '[aeiou]', 'w', 1, 0, 'i')" % (
                row[0], row[1], row[1])
        else:
            sql_stmt = "UPDATE `%s` SET `%s` = REGEXP_REPLACE(%s, '[aeiou]', '', 1, 0, 'i')" % (
                row[0], row[1], row[1])
        try:
            c.execute(sql_stmt)
            db.commit()
        except Exception as e:
            print(e)

    db.close()


updatedb()
