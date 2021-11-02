import pymysql
import pytz
import myutils
from email.utils import COMMASPACE

_host = ''
_user = ''
_password = ''
_db = ''

_charset = 'utf32'

debug = False
local_tz = pytz.timezone('Europe/Moscow')


def format_openedreportlocation(chat_id):
    id, report_timestamp, phone = NumReportInProcess(chat_id)
    c = getconnect()
    rows = select(c, 'reports', True, 'id', id=id)
    for row in rows._rows:
        distrid = str(row['distributor_id'])
        city = str(row['city'])
        street = str(row['street'])
        bldng = str(row['bldng'])
        phone = str(row['phone'])
    distrname = getdistrnamebyid(distrid)
    return 'Локация : {}, г. {} ул. {} д. {} \n '.format(distrname, city, street, bldng), distrid, distrname, city, street, bldng


def format_openedreportinfo(chat_id):
    id, report_timestamp, phone = NumReportInProcess(chat_id)
    return 'Открыт отчет: {} от {} \n'.format(id, report_timestamp)


def NumReportInProcess(chat_id):
    c = getconnect()
    rows = select(c, 'reports', True, 'reports_in_process', chat_id=chat_id)
    if rows.rowcount < 1:   # нет строки
        return 0, '', ''
    else:
        id = 0
        report_timestamp = ''
        for row in rows._rows:
            id = myutils.safe_cast(row['id'], int, 0)
            report_timestamp = str(row['report_timestamp'])
            phone = myutils.safe_cast(row['phone'], str, '')
        return id, report_timestamp, phone


def GetDistribByRepId(reports_id):
    c = getconnect()
    rows = select(c, 'reports', True, 'id', id=reports_id)
    if rows.rowcount < 1:   # нет строки
        return 0
    else:
        id = ''
        for row in rows._rows:
            id = myutils.safe_cast(row['distributor_id'], int, 0)
        return id


def getdistridbyname(distr_name):
    c = getconnect()
    id = 0
    with c.cursor() as cur:
        sql = 'select id from distributor where name = "{}"'.format(str(distr_name))
        cur.execute(sql)
        for row in cur:
            id = myutils.safe_cast(row['id'], int, 0)
    return id


def getdistrnamebyid(distr_id):
    c = getconnect()
    name = ''
    with c.cursor() as cur:
        sql = 'select name from distributor where id = {}'.format(str(distr_id))
        cur.execute(sql)
        for row in cur:
            name = row['name']
    return name


def GetAllDistrs():
    c = getconnect()
    rows = select(c, 'distributor', False)
    return rows


def OpenReportInProcess(chat_id):
    try:
        c = getconnect()
        id = ins(c, 'reports', telegram_id=chat_id, reports_in_process=chat_id)
        return id
    except Exception as exc:
        print("OpenReportInProcess: {} \n {} \n {} \n".format(type(exc), exc.args, exc))
        return 0


def CloseReportInProcess(id):
    try:
        c = getconnect()
        upd(c, 'reports', id, reports_in_process=0)
        return id
    except Exception as exc:
        print("CloseReportInProcess: {} \n {} \n {} \n".format(type(exc), exc.args, exc))
        return 0


def get_distr_mails(distr_name):
    try:
        id_contact_distr = 0
        id_contact_fro = 0
        connection_ = getconnect()
        distr_mails = []
        with connection_.cursor() as cur:
            sql = 'select contact_distr_id, contact_froneri_id from distributor where name = "{}"'.format(str(distr_name))
            cur.execute(sql)
            for row in cur:
                id_contact_distr = myutils.safe_cast(row['contact_distr_id'], int, 0)
                id_contact_fro   = myutils.safe_cast(row['contact_froneri_id'], int, 0)
        with connection_.cursor() as cur:
            sql = 'select email from contacts where id in ('+str(id_contact_distr)+' , '+str(id_contact_fro)+')'
            cur.execute(sql)
            for row in cur:
                if str(row['email']) != '':
                    distr_mails.append(row['email'])
        disconnect(connection_)
        return distr_mails
    except Exception as exc:
        print("get_distr_mails: {} \n {} \n {} \n".format(type(exc), exc.args, exc))


def getmails(distr_id, city, street, bldng):
    try:
        mails = []
        contact_mails = get_contact_mails(city, street, bldng)
        distr_mails   = get_distr_mails(distr_id)
        if len(contact_mails) > 0:
            mails.append(COMMASPACE.join(contact_mails))
        if len(distr_mails) > 0:
            mails.append(COMMASPACE.join(distr_mails))
        return mails
    except Exception as exc:
        print("getmails: {} \n {} \n {} \n".format(type(exc), exc.args, exc))


def get_contact_mails(city, street, bldng):
    try:
        id_contact = 0
        connection_ = getconnect()
        contact_mails = []
        with connection_.cursor() as cur:
            sql = 'select id_contact from locations where city ="{}" and street="{}" and bldng = "{}"'.format(city, street, bldng)
            cur.execute(sql)
            for row in cur:
                id_contact = row['contact_id']
        with connection_.cursor() as cur:
            sql = 'select email from contacts where id = {}'.format(str(id_contact))
            cur.execute(sql)
            for row in cur:
                if str(row['email']) != '':
                    contact_mails.append(row['email'])
        disconnect(connection_)
        return contact_mails
    except Exception as exc:
        print("get_contact_mails: {} \n {} \n {} \n".format(type(exc), exc.args, exc))


def get_distr_mails(distr_id):
    try:
        id_contact_distr = 0
        id_contact_fro = 0
        connection_ = getconnect()
        distr_mails = []
        with connection_.cursor() as cur:
            sql = 'select contact_distr_id, contact_froneri_id from distributor where id = {}'.format(str(distr_id))
            cur.execute(sql)
            for row in cur:
                id_contact_distr = myutils.safe_cast(row['contact_distr_id'], int, 0)
                id_contact_fro   = myutils.safe_cast(row['contact_froneri_id'], int, 0)
        with connection_.cursor() as cur:
            sql = 'select email from contacts where id in ({}, {})'.format(id_contact_distr, id_contact_fro)
            cur.execute(sql)
            for row in cur:
                if str(row['email']) != '':
                    distr_mails.append(row['email'])
        disconnect(connection_)
        return distr_mails
    except Exception as exc:
        print("get_distr_mails: {} \n {} \n {} \n".format(type(exc), exc.args, exc))


def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt) # .normalize might be unnecessary


#   return utc_to_local(utc_dt).strftime('%Y-%m-%d %H:%M:%S.%f %Z%z')
def aslocaltimestr(utc_dt):
    return utc_to_local(utc_dt).strftime('%Y-%m-%d %H:%M:%S.%f')


def getconnect():
    connect = pymysql.connect(host = _host,
                              user = _user,
                              password = _password,
                              db = _db,
                              port = 3306,
                              cursorclass = pymysql.cursors.DictCursor)
    #connect = connect.cursor()
    return connect


def disconnect(connection):
    connection.close()


# return selected rows as dictionary
def select(connection, table, isrestrbyfld, fldname='', **kwargs):
    try:
        vals = ''
        if isrestrbyfld:
            if kwargs is not None:
                for key, value in kwargs.items():
                    vals = vals + '"' + myutils.safe_cast(value, str, '0') + '", '
                vals = vals[0:-2]

            with connection.cursor() as cur:
                sql = 'select * from {} where {} in ({})'.format(table, fldname, vals)
                cur.execute(sql)
                cur.fetchall()
        else:
            with connection.cursor(pymysql.cursors.DictCursor) as cur:
                sql = 'select * from {}'.format(table)
                cur.execute(sql)
                cur.fetchall()
        #return dict(cur)
        return cur
    except Exception as ex:
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)


# return id (int) of inserted row
def ins(connection, table, ischeckdupl=False, flddupl='', valdupl='', **kwargs):
    id = 0
    global debug
    try:
        fields = ""
        vals = ""
        if ischeckdupl == True:
            with connection.cursor() as cur:
                sql = 'select max(id) from {} where {} = "{}"'.format(table, flddupl, valdupl)
                cur.execute(sql)
                for row in cur:
                    id = row['max(id)']
                if id is None:
                    id = 0
            connection.commit()
        if int(id) == 0:  # dublia ne nashli ili i ne iskali tk poh
            if kwargs is not None:
                for key, value in kwargs.items():
                    fields = fields + key + ", "
                    vals = vals + "\"" + str(value) + "\", "
            fields = fields[0:-2]
            vals = vals[0:-2]
            with connection.cursor() as cursor:
                sql = "INSERT INTO " + table + " (" + fields + ") VALUES (" + vals + ")"
                if debug == True:
                    print("ins : " + sql)
                cursor.execute(sql)
            connection.commit()
            with connection.cursor() as cur:
                sql = "select max(id) from " + table
                cur.execute(sql)
                for row in cur:
                    id = row['max(id)']
            connection.commit()
            if debug == True : print("ins id: " + str(id))
    except Exception as ex:
        id = -1
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    finally:
        return id


def upd(connection, table, id=0, **kwargs):
    try:
        vals = ""
        if kwargs is not None:
            for key, value in kwargs.items():
                vals = vals + key + " = \"" + str(value) + "\", "
        vals = vals[0:-2]
        with connection.cursor() as cursor:
            sql = "update " + table + " set " + vals + " where id = " + str(id)
            if debug == True:
                print("upd : " + sql)
            cursor.execute(sql)
        connection.commit()
    finally:
        sql = ""


def delete(connection, table, all=False, id=0):
    with connection.cursor() as cursor:
        sql = "delete FROM " + table
        if all != True:
            sql = sql + " WHERE id = " + str(id)
        if debug == True:
            print("del : " + sql)
        cursor.execute(sql)
        connection.commit()