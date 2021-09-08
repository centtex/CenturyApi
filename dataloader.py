from datetime import datetime, date
import pandas as pd
import MySQLdb
import os
from time import time
import zipfile
import shutil

env = 'dev'
if env == 'prod':
    BASE_DIR = os.getcwd()
    _HOST = 'localhost'
    _USER = 'century'
    _PASSWORD = 'Century#123456'
    _DATABASE_NAME = 'CenturyTexDev'
else:
    BASE_DIR = os.path.dirname(os.getcwd())
    _HOST = 'localhost'
    _USER = 'ubuntu'
    _PASSWORD = '9930343106ASD'
    _DATABASE_NAME = 'centurytexlive'


def dfToSql(filename, tablename, db):
    try:
        c = db.cursor()

        truncate_sql = "SET FOREIGN_KEY_CHECKS = 0; TRUNCATE TABLE %s; SET FOREIGN_KEY_CHECKS = 1;" % tablename
        c.execute(truncate_sql)

        data = pd.read_csv(filepath_or_buffer=filename, sep='|', encoding='utf-8', low_memory=False)
        data = data.astype(str)
        data = data.where(data.notnull(), None)
        # data.fillna(0, inplace=True)

        if tablename == 'companymaster':
            indices = [i for i, x in enumerate(data.columns) if ("year" in x.lower())]
        else:
            indices = [i for i, x in enumerate(data.columns) if ("date" in x.lower())]

        cols = "`,`".join([str(i) for i in data.columns.tolist()])

        _sql = "INSERT INTO `" + tablename + "` (`" + cols + "`) VALUES (" + "%s," * \
               (len(data.iloc[0]) - 1) + "%s)"

        for column in data:
            if data[column].str.contains('True').any():
                data[column].replace('True', 1, inplace=True)
            if data[column].str.contains('False').any():
                data[column].replace('False', 0, inplace=True)
            if data[column].str.contains('nan').any():
                data[column].replace('nan', '', inplace=True)

        for i, row in data.iterrows():
            # for r in row:
            #     if r and not isinstance(r, str) and math.isnan(r):
            #         r = 0
            for j in indices:
                if row[j]:
                    try:
                        row[j] = datetime.strptime(row[j], '%d/%m/%Y %I:%M:%S %p')
                    except(ValueError, TypeError):
                        row[j] = None
                else:
                    row[j] = None

            t_row = tuple(row)
            t_row = tuple(None if x == '' else x for x in t_row)
            c.execute(_sql, tuple(t_row))

        db.commit()
    except (TypeError, MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
        return e


def getlastUploadedFile():
    db = MySQLdb.connect(host=_HOST, user=_USER, passwd=_PASSWORD, db=_DATABASE_NAME)
    c = db.cursor()
    sql_stmt = 'SELECT id, SyncFileName FROM SyncData WHERE SyncDate >= CURDATE() order by SyncDate DESC limit 1;'
    c.execute(sql_stmt)
    data = c.fetchall()
    db.commit()
    db.close()
    if data:
        return data[0]
    else:
        return None


def unzip_file(zip_src, dst_dir):
    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, "r")
        for file in fz.namelist():
            fz.extract(file, dst_dir)
    else:
        return "Please upload zip file"


def extractfilesandsync():
    start = time()
    target_path_ = os.path.join(BASE_DIR, "extracted")
    # Check if folder already exist, if exist remove folder
    if os.path.exists(target_path_) and os.path.isdir(target_path_):
        shutil.rmtree(target_path_)
    # get last uploaded filename
    response = getlastUploadedFile()
    if response:
        filename = response[1]
        _id = response[0]
    else:
        return "No record Found in DB", 0

    # if file exist unzip it
    if os.path.exists(BASE_DIR + '/' + filename):
        # unzip all files to target path
        ret = unzip_file(BASE_DIR + '/' + filename, target_path_)
        if ret:
            return ret, _id
    else:
        return "File Missing", _id

    # initialize backup path
    backup_path = os.path.join(BASE_DIR, "backupsqldata")
    # create backup folder
    os.makedirs(backup_path, exist_ok=True)
    # Move zip file to backup folder
    shutil.move(os.path.join(BASE_DIR, filename), os.path.join(backup_path, filename))

    files = os.listdir(target_path_)

    if files:
        db = MySQLdb.connect(host=_HOST, user=_USER, passwd=_PASSWORD, db=_DATABASE_NAME)
        for f in files:
            filepath = target_path_ + '/' + f
            table_name = f.split('.')[0].replace("_", "").lower()
            res = dfToSql(filepath, table_name, db)
            if res:
                return res, _id
        db.close()
    else:
        print("no update found")
        return "no update found"

    print('Full Activity took {0:.2f} seconds'.format(time() - start))
    return None, _id


def updatedb(msg, _id):
    db = MySQLdb.connect(host=_HOST, user=_USER, passwd=_PASSWORD, db=_DATABASE_NAME)
    c = db.cursor()
    sql_stmt = "UPDATE `SyncData` SET `SyncCompletedOn` = %s , `SyncCompleted` = %s, `Reason` =%s WHERE `id` = %s"
    if msg == 'Success':
        c.execute(sql_stmt, tuple([datetime.now(), 'S', "", _id]))
    else:
        if type(msg) == str:
            c.execute(sql_stmt, tuple([datetime.now(), 'F', msg.strip()[:250], _id]))
        else:
            c.execute(sql_stmt, tuple([datetime.now(), 'F', msg.args[1].strip()[:250], _id]))

    db.commit()
    db.close()


errormsg, _id = extractfilesandsync()

if _id != 0:
    if errormsg:
        updatedb(errormsg, _id)
    else:
        updatedb("Success", _id)
else:
    print(errormsg)
