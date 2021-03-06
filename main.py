#!/usr/bin/env python
#coding=utf-8
import os,sys,json
from bottle import request,route,error,run,default_app
from bottle import template,static_file,redirect,abort
import logging
from beaker.middleware import SessionMiddleware
from bottle import TEMPLATE_PATH
import datetime
from gevent import monkey;
import MySQLdb
import hashlib
import xlrd
import time
monkey.patch_all()

db_name = 'task'
db_user = 'root'
db_pass = '123456'
db_ip = 'localhost'
db_port = 3306


#获取本脚本所在的路径
pro_path = os.path.split(os.path.realpath(__file__))[0]
#split分离路径和文件名
sys.path.append(pro_path)

#定义assets路径，即静态资源路径，如css,js,及样式中用到的图片等
assets_path = '/'.join((pro_path,'assets'))

#定义图片路径
images_path = '/'.join((pro_path,'images'))

#定义提供文件下载的路径
download_path = '/'.join((pro_path,'download'))

#定义文件上传存放的路径
upload_path = '/'.join((pro_path,'log/upload'))

#定义模板路径
TEMPLATE_PATH.append('/'.join((pro_path,'views')))

#定义日志目录
log_path = ('/'.join((pro_path,'log')))

#定义日志输出格式
logging.basicConfig(level=logging.ERROR,
        format = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S',
        filename = "%s/error_log" % log_path,
        filemode = 'a')

def writeDb(sql,db_data=()):
    """
    连接mysql数据库（写），并进行写的操作
    """
    try:
        conn = MySQLdb.connect(db=db_name,user=db_user,passwd=db_pass,host=db_ip,port=int(db_port),charset="utf8")
        cursor = conn.cursor()
    except Exception,e:
        print e
        logging.error('数据库连接失败:%s' % e)
        return False

    try:
        cursor.execute(sql,db_data)
        conn.commit()
    except Exception,e:
        conn.rollback()
        logging.error('数据写入失败:%s' % e)
        return False
    finally:
        cursor.close()
        conn.close()
    return True


def readDb(sql,db_data=()):
    """
    连接mysql数据库（从），并进行数据查询
    """
    try:
        conn = MySQLdb.connect(db=db_name,user=db_user,passwd=db_pass,host=db_ip,port=int(db_port),charset="utf8")
        cursor = conn.cursor()
    except Exception,e:
        print e
        logging.error('数据库连接失败:%s' % e)
        return False

    try:
        cursor.execute(sql,db_data)
        data = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
    except Exception,e:
        print e
        logging.error('数据执行失败:%s' % e)
        return False
    finally:
        cursor.close()
        conn.close()
    return data


#设置session参数
session_opts = {
    'session.type':'file',
    'session.cookei_expires':3600,
    'session.data_dir':'/tmp/sessions',
    'sessioni.auto':True
    }

def checkLogin(fn):
    """验证登陆，如果没有登陆，则跳转到login页面"""
    def BtnPrv(*args,**kw):
        s = request.environ.get('beaker.session')
        if not s.get('userid',None):
            return redirect('/login')
        return fn(*args,**kw)
    return BtnPrv

def checkAccess(fn):
    """验证权限，如果非管理员权限，则返回404页面"""
    def BtnPrv(*args,**kw):
        s = request.environ.get('beaker.session')
        if not s.get('userid',None):
            return redirect('/login')
        elif s.get('access',None) == 0:
            abort(404)
        return fn(*args,**kw)
    return BtnPrv




@error(404)
def error404(error):
    """定制错误页面"""
    return template('404')


@route('/assets/<filename:re:.*\.css|.*\.js|.*\.png|.*\.jpg|.*\.gif>')
def server_static(filename):
    """定义/assets/下的静态(css,js,图片)资源路径"""
    return static_file(filename, root=assets_path)

@route('/assets/js/<filename:re:.*\.css|.*\.js|.*\.png|.*\.jpg|.*\.gif>')
def server_static(filename):
    """定义/assets/下的静态(css,js,图片)资源路径"""
    return static_file(filename, root=assets_path)

@route('/assets/<filename:re:.*\.ttf|.*\.otf|.*\.eot|.*\.woff|.*\.svg|.*\.map>')
def server_static(filename):
    """定义/assets/字体资源路径"""
    return static_file(filename, root=assets_path)

@route('/images/<filename:re:.*\.jpg|.*\.png>')
def server_static(filename):
    """定义图片资源路径"""
    return static_file(filename, root=images_path)

@route('/log/upload/<filename:re:.*\.xls|.*\.xlsx>')
def server_static(filename):
    """定义图片资源路径"""
    return static_file(filename, root=upload_path)

@route('/')
@checkLogin   #函数调用
def index():
    return template('index',message='')

@route('/user')
@checkAccess
def user():
    teamname_sql = "select id,name from team;"
    team_result = readDb(teamname_sql, )

    return template('user',team_result=team_result)

@route('/adduser',method="POST")
@checkAccess
def adduser():
    name = request.forms.get("name")
    username = request.forms.get("username")
    passwd = request.forms.get("passwd")
    birthday = request.forms.get("birthday")
    sex = request.forms.get("sex")
    height = request.forms.get("height")
    email = request.forms.get("email")
    Company = request.forms.get("Company")
    weight = request.forms.get("weight")
    access = request.forms.get("access")
    teamname = request.forms.get("teamname")
    #把密码进行md5加密码处理后再保存到数据库中
    m = hashlib.md5()
    m.update(passwd)
    passwd = m.hexdigest()

    #检测表单各项值，如果出现为空的表单，则返回提示

    if not (name and username and access):
        message = "表单不允许为空！"
        print message
        return '-2'
    sql = """
            INSERT INTO
                user(name,username,passwd,birthday,sex,height,email,Company,weight,access,teamname)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
    data = (name,username,passwd,birthday,sex,height,email,Company,weight,access,teamname)
    result = writeDb(sql,data)

    if result:
        return '0'
    else:
        return '-1'

@route('/changeuser/<id>',method="POST")
@checkAccess
def changeuser(id):
    name = request.forms.get("name")
    username = request.forms.get("username")
    passwd = request.forms.get("passwd")
    birthday = request.forms.get("birthday")
    sex = request.forms.get("sex")
    height = request.forms.get("height")
    email = request.forms.get("email")
    Company = request.forms.get("Company")
    weight = request.forms.get("weight")
    access = request.forms.get("access")
    teamname = request.forms.get("teamname")
    #把密码进行md5加密码处理后再保存到数据库中
    if not passwd:
        sql = "select passwd from user where id = %s"
        passwd = readDb(sql,id)[0]['passwd']
    else:
        m = hashlib.md5()
        m.update(passwd)
        passwd = m.hexdigest()

    def checkRequest(list_data):
        for i in list_data:
            if not i.strip():
                return '-2'

    if not (name and username and access):
        message = "表单不允许为空！"
        return '-2'


    sql = """
            UPDATE user SET
            name=%s,username=%s,passwd=%s,birthday=%s,sex=%s,height=%s,email=%s,Company=%s,weight=%s,access=%s,teamname=%s
            WHERE id=%s
        """
    data = (name,username,passwd,birthday,sex,height,email,Company,weight,access,teamname,id)
    result = writeDb(sql,data)
    if result:
        return '0'
    else:
        return '-1'

@route('/deluser',method="POST")
@checkAccess
def deluser():
    id = request.forms.get('str').rstrip(',')
    if not id:
        return '-1'

    sql = "delete from user where id in (%s)" % id
    result = writeDb(sql,)
    if result:
        return '0'
    else:
        return '-1'

@route('/api/getuser',method=['GET', 'POST'])
@checkAccess
def getuser():
    sql = """
    SELECT
        U.id,
        U.name,
        U.username,
        date_format(U.birthday,'%%Y-%%m-%%d') as birthday,
        U.sex,
        U.height,
        U.weight,
        U.email,
        U.access,
        U.teamname,
        date_format(U.adddate,'%%Y-%%m-%%d') as adddate,
        CASE U.access WHEN 0 THEN '学员' WHEN 1 THEN '管理员' WHEN 2 THEN '负责人' end as access 
    FROM
        user as U
    """
    userlist = readDb(sql,)
    return json.dumps(userlist)

@route('/taskinfo')
@checkLogin
def taskinfo():
    s = request.environ.get('beaker.session')
    return template('taskinfo',session=s)

@route('/api/gettask',method=['GET','POST'])
@checkLogin
def tasklist():
    status = request.query.witchbtn or -1
    wherestr = "WHERE 1=1"
    if int(status) in [0,1,2]:
        wherestr = ' '.join((wherestr,'AND T.status=%d' % int(status)))
    sql = """
           SELECT
                T.id,
                T.planname,
                date_format(T.begin,'%%Y-%%m-%%d') as begin,
                date_format(T.end,'%%Y-%%m-%%d') as end,
                T.status,
                u.name
           FROM
                plan as T
                LEFT OUTER JOIN user as u on u.id=T.inputid
            {where} AND T.del_status=1
        """.format(where=wherestr)

    tasklist = readDb(sql,)
    return json.dumps(tasklist)

@route('/item')
@checkLogin
def item():
    s = request.environ.get('beaker.session')
    return template('item',session=s)

@route('/api/getcontent',method=['GET', 'POST'])
@checkLogin
def getcontent():
    sql = """
        SELECT
            p.cid,
            p.content
        FROM
            pcontent as p
    """
    content_list = readDb(sql,)
    return json.dumps(content_list)

@route('/api/getplace',method=['GET', 'POST'])
@checkLogin
def getplace():
    sql = """
        SELECT
            p.plid,
            p.place
        FROM
            pplace as p
    """
    place_list = readDb(sql,)
    return json.dumps(place_list)



@route('/addtask')
@checkLogin
def addtask():
    user_sql = "select id,name from user;"
    item_sql = "select id,name from item;"
    department_sql = "select id,name from department;"
    user_data = readDb(user_sql,)
    item_data = readDb(item_sql,)
    department_data = readDb(department_sql,)
    return template('addtask',user_data=user_data,item_data=item_data,department_data=department_data,task_data=[{}])

@route('/addtask',method="POST")
@checkLogin
def do_addtask():
    s = request.environ.get('beaker.session')
    inputid = s['userid']
    subject = request.forms.get("subject")
    userid = int(request.forms.get("userid"))
    startdate = request.forms.get("startdate")
    enddate = request.forms.get("enddate")


    sql = """
        INSERT INTO
        plan(planname,inputid,begin,end)
        VALUES(%s,%s,%s,%s)
    """
    data = (subject,userid,startdate,enddate)
    result = writeDb(sql,data)
    if result:
        redirect('/taskinfo')
    else:
        return '添加失败'

@route('/edittask/<id>')
@checkLogin
def edittask(id):
    s = request.environ.get('beaker.session')
    user_sql = "select id,name from user;"
    item_sql = "select id,name from item;"
    department_sql = "select id,name from department;"
    task_sql = """
        SELECT
            id,
            inputid,
            subject,
            status,
            itemid,
            departmentid,
            startdate,
            enddate,
            priority,
            content,
            CASE WHEN userid<0 THEN depid ELSE userid END as userid,
            CASE WHEN assistid<0 THEN assdepid ELSE assistid END as assistid
        FROM
            task
        WHERE
            id=%s
        """
    user_data = readDb(user_sql,)
    item_data = readDb(item_sql,)
    department_data = readDb(department_sql,)
    task_data = readDb(task_sql,(id))
    #如果任务不是自己发的，或者不是管理员权限，则不允许访问
    if task_data[0].get('inputid') != s.get('userid',None) and s.get('access',None) == 0:
        abort(404)
    return template('addtask',info={},user_data=user_data,item_data=item_data,department_data=department_data,task_data=task_data)


@route('/edittask/<id>',method="POST")
@checkLogin
def do_edittask(id):
    subject = request.forms.get("subject")
    userid = int(request.forms.get("userid"))
    assistid = int(request.forms.get("assistid"))
    itemid = int(request.forms.get("itemid"))
    priority = int(request.forms.get("priority"))
    departmentid = int(request.forms.get("departmentid"))
    startdate = request.forms.get("startdate")
    enddate = request.forms.get("enddate")
    content = request.forms.get("content")

    #判断表单选的userid是否大于99999，如果大于，就把这个值存到depid字段中，并把userid设成-2，表示末指定
    if userid > 99999:
        depid = userid
        userid = -2
    else:
        depid = -2

    #判断表单选的assistid是否大于99999，如果大于，就把这个值存到dassdepid字段中，并把assistid设成-2，表示末指定
    if assistid > 99999:
        assdepid = assistid
        assistid = -2
    else:
        assdepid = -2

    sql = """
        UPDATE
            task
        SET
            subject=%s,
            userid=%s,
            depid=%s,
            assistid=%s,
            assdepid=%s,
            itemid=%s,
            priority=%s,
            departmentid=%s,
            startdate=%s,
            enddate=%s,
            content=%s
        WHERE
            id=%s
    """
    data = (subject,userid,depid,assistid,assdepid,itemid,priority,departmentid,startdate,enddate,content,id)
    result = writeDb(sql,data)
    if result:
        redirect('/taskinfo')
    else:
        return '修改失败'

@route('/taskSignIn/<id>/<tid>')
@checkLogin
def SignIn(id,tid):
    #获取任务详细内容页
    s = request.environ.get('beaker.session')
    myusername = s['name']
    sql = "UPDATE task SET SignIn=1 WHERE tid = %s"
    result = writeDb(sql,(tid,))
    if result:
        redirect ("/infotask/"+id)
    else:
        return '-1'

@route('/infotask/<id>')
@checkLogin
def infotask(id):
    #获取任务详细内容页
    s = request.environ.get('beaker.session')
    myusername = s['name']
    task_sql = """
    	SELECT
    	   T.id,
    	   u.name,
    	   T.planname,
    	   T.inputid,
    	   T.status,
    	   date_format(T.begin,'%%Y-%%m-%%d') as startdate,
    	   date_format(T.end,'%%Y-%%m-%%d') as enddate,
    	   case when t.status = 0 then '未开始' when t.status = 1 then '进行中' ELSE '已完成' end as status
    	FROM
    	   plan as T
    	   LEFT OUTER JOIN user as u on u.id=T.inputid
    	WHERE
    	   T.id=%s
    """
    taskinfo = readDb(task_sql,(id,))
    sql2 = "select name from user where access=2"
    chargeman = readDb(sql2, )
    sql3 = "select content from pcontent"
    content = readDb(sql3, )
    sql4 = "select place from pplace"
    place = readDb(sql4, )
    sql5 = "select name from team"
    teamid = readDb(sql5, )
    return template('infotask',taskinfo=taskinfo,myusername=myusername,teamid=teamid,place=place,chargeman=chargeman,content=content)

@route('/api/gettaskinfo/<id>',method=['GET', 'POST'])
@checkAccess
def gettaskinfo(id):
    sql1 = """
    SELECT
        t.id,
        te.chargeman as name,
        t.tid,
        date_format(t.date,'%%Y-%%m-%%d ') as date,
        date_format(t.begintime, '%%k:%%i:%%s') as begintime,
        t.place,
        pc.level,
        t.lasttime,
        t.teamid,
        t.content,
        t.SignIn
    FROM
        task as t 
        LEFT OUTER JOIN pcontent as pc on pc.content=t.content
        LEFT OUTER JOIN team as te on te.name=t.teamid
    WHERE
        t.id=%s AND del_status = 1
    """
    tasklist = readDb(sql1,(id,))
    return json.dumps(tasklist)

@route('/infotask/<id>',method="POST")
@checkLogin
def do_infotask(id):
    s = request.environ.get('beaker.session')
    reply_userid = s['userid']

    try:
        argv = request.forms.get('oper')
    except Exception:
        argv = 'None'
    if argv == 'start':
        sql = "UPDATE task SET status=%s WHERE id = %s"
        result = writeDb(sql,(1,id))
        if result :
            return '1'
    elif argv == 'end':
        now_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "UPDATE task SET status=%s,finishdate=%s WHERE id = %s"
        res = writeDb(sql,(2,now_date,id))
        if res :
            return '1'

    else:
        content = request.forms.get('content')
        sql = "INSERT INTO task_reply(userid,content,taskid) VALUES(%s,%s,%s)"
        data = (reply_userid,content,id)
        writeDb(sql,data)
        redirect('/infotask/%s' % id)

@route('/addtaskinfo/<id>',method="POST")
@checkAccess
def addtaskinfo(id):
    date = request.forms.get("date")
    begintime = request.forms.get("begintime")
    lasttime = request.forms.get("lasttime")
    content = request.forms.get("content")
    place = request.forms.get("place")
    teamid = request.forms.get("teamid")
    #检测表单各项值，如果出现为空的表单，则返回提示
    if not (date):
        message = "表单不允许为空！"
        print message
        return '-2'

    sql = """
            INSERT INTO
                task(id,date,begintime,lasttime,content,place,teamid)
            VALUES(%s,%s,%s,%s,%s,%s,%s)
        """
    data = (id,date,begintime,lasttime,content,place,teamid)
    result = writeDb(sql,data)

    if result:
        return '0'
    else:
        return '-1'

@route('/changetaskinfo/<id>/<tid>',method="POST")
@checkAccess
def changeuser(id,tid):
    date = request.forms.get("date")
    begintime = request.forms.get("begintime")
    lasttime = request.forms.get("lasttime")
    content = request.forms.get("content")
    place = request.forms.get("place")
    teamid = request.forms.get("teamid")
    if not (date):
        message = "表单不允许为空！"
        return message
    sql = """
            UPDATE task SET
            date=%s,begintime=%s,lasttime=%s,content=%s,place=%s,teamid=%s
            WHERE id=%s AND tid=%s
        """
    data = (date,begintime,lasttime,content,place,teamid,id,tid)
    result = writeDb(sql,data)
    if result:
        return '0'
    else:
        return '-1'

@route('/deltaskinfo',method=['POST','GET'])
@checkLogin
def deltaskinfo():
    """删除任务，其实就是把任务的删除状态改成0（0为被删除，1为正常）"""
    s = request.environ.get('beaker.session')
    del_userid = s['userid']
    str = request.forms.get("str")
    id = request.forms.get("id")
    print id
    tid = str.split(',')
    success=0
    length = 0
    for i in tid:
        if i:
            length=length+1
            sql = """
                        UPDATE
                            task
                        SET
                            del_userid=%s,
                            del_status=%s
                        WHERE
                            tid=%s
                    """
            data = (del_userid, 0, i)
            result = writeDb(sql, data)
            if result:
                success=success+1
    if success==length:
        return '0'
    else:
        return '-1'

@route('/api/getdepartment',method=['POST','GET'])
@checkLogin
def getdepartment():
    """获取部门列表的接口"""
    sql = "select * from team;"
    sql2 = """
    select
        t.id,
        t.name,
        t.chargeman,
        group_concat(t.person) as person
    from
        (
        select 
            T.id,
            T.name as name,
            T.chargeman,
            u.name as person 
        from 
            team as T
            LEFT OUTER JOIN user as u on u.teamname=T.name
        ) as t
    group by t.id
    """
    result = readDb(sql2,)
    return json.dumps(result)

@route('/department')
@checkAccess
def department():
    """部门列表页"""
    chargeman_sql = "select name from user where access=2"
    chargeman_result = readDb(chargeman_sql,)
    return template('department',chargeman_result=chargeman_result)

@route('/adddepartment',method="POST")
@checkAccess
def do_addpartment():
    """增加部门"""
    name = request.forms.get("name")
    chargeman = request.forms.get("chargeman")
    sql = "INSERT INTO team(name,chargeman) VALUES(%s,%s)"
    data = (name,chargeman)
    result = writeDb(sql,data)
    if result:
        return '0'
    else:
        return '-1'

@route('/editdepartment/<id>',method="POST")
@checkAccess
def editpartment(id):
    """修改部门"""
    name = request.forms.get("name")
    chargeman = request.forms.get("chargeman")
    sql = "UPDATE team SET name=%s,chargeman=%s WHERE id=%s"
    data = (name,chargeman,id)
    result = writeDb(sql,data)
    if result:
        return '0'
    else:
        return '-1'

@route('/deldepartment',method="POST")
@checkAccess
def deluser():
    """删除部门"""
    id = request.forms.get('str').rstrip(',')

    if not id:
        return '-1'

    sql = "delete from team where id in (%s)"
    result = writeDb(sql,id)
    if result:
        return '0'
    else:
        return '-1'

@route('/login')
def login():
    """用户登陆"""
    return template('login',message='')

@route('/login',method='POST')
def do_login():
    """用户登陆过程，判断用户帐号密码，保存SESSION"""
    username = request.forms.get('username').strip()
    passwd = request.forms.get('passwd').strip()
    if not username or not passwd:
        message = u'帐号或密码不能为空！'
        return template('login',message=message)

    m = hashlib.md5()
    m.update(passwd)
    passwd_md5 = m.hexdigest()
    auth_sql = '''
        SELECT
            id,username,name,access
        FROM
            user
        WHERE
            username=%s and passwd=%s
        '''
    auth_user = readDb(auth_sql,(username,passwd_md5))
    if auth_user:
        s = request.environ.get('beaker.session')
        s['username'] = username
        s['name'] = auth_user[0]['name']
        s['userid'] = auth_user[0]['id']
        s['access'] = auth_user[0]['access']
        s.save()
    else:
        message = u'帐号或密码错误！'
        return template('login',message=message)
    return redirect('/')

@route('/logout')
@checkLogin
def logout():
    """退出系统"""
    s = request.environ.get('beaker.session')
    try:
        s.delete()
    except Exception:
        pass
    return redirect('/login')

@route('/mytask')
@checkLogin
def mytask():
    """关于我的任务页面"""
    return template('mytask')


@route('/api/mytask',method=['GET','POST'])
@checkLogin
def getmytask():
    """获取关于我的任务API接口"""
    s = request.environ.get('beaker.session')
    myid = s['userid']
    status = request.query.witchbtn or -1
    wherestr = "WHERE 1=1"
    if int(status) in [0,1,2]:
        wherestr = ' '.join((wherestr,'AND T.status=%d' % int(status)))

    sql = """
        SELECT
            t.id,
            t.inputid,
            t.subject,
            t.status,
            t.itemid,
            t.departmentid,
            t.startdate,
            t.enddate,
            t.priority,
            case when t.userid is null then t.zrbm when t.userid is not null then t.userid end as userid,
            case when t.assistid is null then t.xzbm when t.assistid is not null then t.assistid end as assistid
        FROM
          (
            SELECT
                T.id,
                Ui.name as inputid,
                T.subject,
                T.status,
                u.name as userid,
                depid.name as zrbm,
                xzr.name as assistid,
                    xzbm.name as xzbm,
                    item.name as itemid,
                    department.name as departmentid,
                date_format(T.startdate,'%%Y-%%m-%%d') as startdate,
                date_format(T.enddate,'%%Y-%%m-%%d') as enddate,
                T.priority
            FROM
               task as T
               LEFT OUTER JOIN user as u on u.id=T.userid
               LEFT OUTER JOIN user as Ui on Ui.id=T.inputid
               LEFT OUTER JOIN department as depid on depid.id=T.depid
               LEFT OUTER JOIN user as xzr on xzr.id=T.assistid
               LEFT OUTER JOIN department as xzbm on xzbm.id=T.assdepid
               INNER JOIN item on item.id=T.itemid
               INNER JOIN department ON department.id=T.departmentid
            {where} AND T.del_status=1 AND (T.userid=%s or T.assistid=%s )
            ORDER BY
                status,priority,enddate
            ) AS t
    """.format(where=wherestr)
    result = readDb(sql,(myid,myid))
    return json.dumps(result)

@route('/score')
@checkLogin
def showscore():
    """成绩管理界面"""
    s = request.environ.get('beaker.session')
    return template('score',session=s)

@route('/api/getscorelist',method="POST")
@checkLogin
def getscore():
    """获取成绩信息"""
    status = request.query.witchbtn or -1
    wherestr = "WHERE 1=1"
    s = request.environ.get('beaker.session')
    if int(status) in [0,1,2]:
        wherestr = ' '.join((wherestr,'AND S.status=%d' % int(status)))
    sql = """
            SELECT
                S.id,
                S.inputid,
                S.subject,
                u.name as inputid,
                date_format(S.date,'%%Y-%%m-%%d') as date,
                S.del_status
            FROM
               scorelist as S
               LEFT OUTER JOIN user as u on u.id=S.inputid
            {where} AND S.del_status=1
    """.format(where=wherestr)
    result = readDb(sql,)
    return json.dumps(result)

@route('/infoscore/<date>')
@checkLogin
def getscore(date):
    s = request.environ.get('beaker.session')
    str = date
    sql = """
        SELECT
            sc.id,
            sc.subject,
            date_format(sc.date,'%%Y%%m%%d') as date,
            u.name as name,
            sc.inputid
        FROM
            scorelist AS sc
            LEFT OUTER JOIN user as u on u.id=sc.inputid
        WHERE
            sc.date = %s
            
    """
    result = readDb(sql, (str,))
    return template('scoreinfo',scoreinfo=result,session=s)

@route('/infoscore/<date>',method='POST')
@checkAccess
def get_file(date):
    s = request.environ.get('beaker.session')
    upload = request.files.get("file")
    print upload.filename
    upload.save('./upload', overwrite=True)
    xlsfile = r'./upload/'+upload.filename
    book = xlrd.open_workbook(xlsfile)
    # 设置连接数据库
    database = MySQLdb.connect(db=db_name,user=db_user,passwd=db_pass,host=db_ip,port=int(db_port),charset="utf8")
    # 设置字符集
    database.set_character_set('utf8')
    cursor = database.cursor()
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')
    sql = """
    REPLACE INTO 
        score (id,wugongli,dangang1,sibaimi,dangang2,date) 
    VALUES 
        (%s,%s,%s,%s,%s,%s)
    """
    sheet = book.sheet_by_index(0)
    for r in range(1, sheet.nrows):
        id = sheet.cell(r, 0).value
        wugongli = xlrd.xldate_as_tuple(sheet.cell(r, 1).value,0)
        w_t = str(wugongli[3]) + ':' + str(wugongli[4]) + ':' + str(wugongli[5])
        dangang1 = sheet.cell(r, 2).value
        sibaimi = xlrd.xldate_as_tuple(sheet.cell(r, 3).value,0)
        s_t = str(sibaimi[3]) + ':' + str(sibaimi[4]) + ':' + str(sibaimi[5])
        dangang2 = sheet.cell(r, 4).value
        date = date
        values = (id, w_t, dangang1, s_t, dangang2, date)
        cursor.execute(sql, values)
    cursor.close()
    database.commit()
    database.close()
    redirect('/infoscore/'+date)



@route('/api/getscoreinfo/<date>',method=['GET', 'POST'])
@checkAccess
def getscoreinfo(date):
    dates = date[0:4]+"-"+date[4:6]+"-"+date[6:8]
    sql = """
    SELECT
        uu.id,
        uu.name,
        T.date,
        case when T.wugongli is null then "暂无" when T.wugongli is not null then T.wugongli end as wugongli,
        case when T.sibaimi is null then "暂无" when T.sibaimi is not null then T.sibaimi end as sibaimi,
        case when T.dangang1 is null then "暂无" when T.dangang1 is not null then T.dangang1 end as dangang1,
        case when T.dangang2 is null then "暂无" when T.dangang2 is not null then T.dangang2 end as dangang2,
        T.teamname
    FROM
        (
        SELECT
            u.id,
            u.name as name,
            S.wugongli,
            S.sibaimi,
            S.dangang1,
            S.dangang2,
            u.teamname as teamname,
            date_format(s.date,'%%Y-%%m-%%d') as date
        FROM
            user as u
            LEFT JOIN score as S on u.id=S.id
        where
            date is null or date = %s
        ) as T
    RIGHT JOIN user as uu on uu.id=T.id
    """
    scorelist = readDb(sql,(dates,))
    return json.dumps(scorelist)

@route('/addscorelist',method="POST")
@checkAccess
def addscore():
    subject = request.forms.get("subject")
    date = request.forms.get("date")
    name = request.forms.get("chargeman")

    if not (subject and date and name):
        message = "表单不允许为空！"
        return message

    sql1 = """
            SELECT 
              id 
            FROM 
              user 
            WHERE 
              name = %s
            """
    inputid = readDb(sql1, (name,))
    inputid = inputid[0]['id']
    sql = """
            INSERT INTO
                scorelist(subject,inputid,date)
            VALUES(%s,%s,%s)
        """
    data = (subject,inputid,date)
    result = writeDb(sql,data)
    if result:
        return '0'
    else:
        return '-1'

@route('/changescore/<id>',method="POST")
@checkAccess
def changeuser(id):
    subject = request.forms.get("subject")
    date = request.forms.get("date")
    name = request.forms.get("chargeman")
    if not (subject and date and name):
        message = "表单不允许为空！"
        return message
    sql1 = """
        SELECT 
          id 
        FROM 
          user 
        WHERE 
          name = %s
        """
    inputid = readDb(sql1,(name,))
    inputid = inputid[0]['id']
    sql2 = """
            UPDATE scorelist SET
            subject=%s,date=%s,inputid=%s
            WHERE id=%s
        """
    data = (subject,date,inputid,id)

    result = writeDb(sql2,data)
    if result:
        return '0'
    else:
        return '-1'

@route('/changeuserscore/<date>',method="POST")
@checkAccess
def changeuserscore(date):
    date = date[0:4] + "-" + date[4:6] + "-" + date[6:8]
    name = request.forms.get("name")
    wugongli = request.forms.get("wugongli")
    sibaimi = request.forms.get("sibaimi")
    dangang1 = request.forms.get("dangang1")
    dangang2 = request.forms.get("dangang2")
    if not (name):
        message = "表单不允许为空！"
        return message
    sql1 = """
            SELECT 
              id 
            FROM 
              user 
            WHERE 
              name = %s
            """
    inputid = readDb(sql1, (name,))
    id = inputid[0]['id']
    sql2 = """
        SELECT * FROM score WHERE date=%s AND id=%s 
    """
    result2 = readDb(sql2,(date,id))
    if(result2==[]):
        print "3"
        sql3 = """
                INSERT INTO score(
                id,wugongli,sibaimi,dangang1,dangang2,date)
                VALUES(%s,%s,%s,%s,%s,%s)
            """
        data = (id,wugongli,sibaimi,dangang1,dangang2,date)
        print data
        result3 = writeDb(sql3,data)
        if result3:
            return '0'
        else:
            return '-1'
    else:
        sql4 = """
            UPDATE score SET
                wugongli=%s,sibaimi=%s,dangang1=%s,dangang2=%s
            WHERE id=%s AND date=%s
        """
        data = (wugongli,sibaimi,dangang1,dangang2,id,date)
        result4 = writeDb(sql4,data)
        if result4:
            return '0'
        else:
            return '-1'

@route('/delscore/<id>')
@checkLogin
def delscore(id):
    """删除任务，其实就是把任务的删除状态改成0（0为被删除，1为正常）"""
    s = request.environ.get('beaker.session')
    del_userid = s['userid']
    sql = """
        UPDATE
            scorelist
        SET
            del_userid=%s,
            del_status=%s
        WHERE
            id=%s
    """
    data = (del_userid,0,id)
    result = writeDb(sql,data)
    if result:
        redirect('/score')
    else:
        return '-1'

@route('/addscore',method="POST")
@checkAccess
def addscore():
    subject = request.forms.get("subject")
    date = request.forms.get("date")
    name = request.forms.get("chargeman")

    if not (subject and date and name):
        message = "表单不允许为空！"
        return message

    sql1 = """
            SELECT 
              id 
            FROM 
              user 
            WHERE 
              name = %s
            """
    inputid = readDb(sql1, (name,))
    inputid = inputid[0]['id']
    sql = """
            INSERT INTO
                scorelist(subject,inputid,date)
            VALUES(%s,%s,%s)
        """
    data = (subject,inputid,date)
    result = writeDb(sql,data)
    if result:
        return '0'
    else:
        return '-1'

@route('/droptask')
@checkAccess
def droptask():
    """删除任务页面，即任务回收站"""
    return template('droptask')

@route('/api/droptask',method=["GET","POST"])
@checkAccess
def get_droptask():
    """获取被删除的任务API接口"""
    sql = """
    SELECT
       t.id,
       t.inputid,
       t.del_userid,
       t.subject,
       t.status,
       t.itemid,
       t.departmentid,
       t.startdate,
       t.enddate,
       t.priority,
       case when t.userid is null then t.zrbm when t.userid is not null then t.userid end as userid,
       case when t.assistid is null then t.xzbm when t.assistid is not null then t.assistid end as assistid
    FROM
       (
        SELECT
            T.id,
            Ui.name as inputid,
            Ud.name as del_userid,
            T.subject,
            T.status,
            u.name as userid,
            depid.name as zrbm,
            xzr.name as assistid,
            xzbm.name as xzbm,
            item.name as itemid,
            department.name as departmentid,
            date_format(T.startdate,'%%Y-%%m-%%d') as startdate,
            date_format(T.enddate,'%%Y-%%m-%%d') as enddate,
            T.priority
       FROM
            task as T
            LEFT OUTER JOIN user as u on u.id=T.userid
            LEFT OUTER JOIN user as Ui on Ui.id=T.inputid
            LEFT OUTER JOIN user as Ud on Ud.id=T.del_userid
            LEFT OUTER JOIN department as depid on depid.id=T.depid
            LEFT OUTER JOIN user as xzr on xzr.id=T.assistid
            LEFT OUTER JOIN department as xzbm on xzbm.id=T.assdepid
            INNER JOIN item on item.id=T.itemid
            INNER JOIN department ON department.id=T.departmentid
        WHERE T.del_status=0
        ) AS t
    """
    result = readDb(sql,)
    return json.dumps(result)

@route('/deltask/<id>')
@checkLogin
def deltask(id):
    """删除任务，其实就是把任务的删除状态改成0（0为被删除，1为正常）"""
    s = request.environ.get('beaker.session')
    del_userid = s['userid']
    sql = """
        UPDATE
            plan
        SET
            del_userid=%s,
            del_status=%s
        WHERE
            id=%s
    """
    data = (del_userid,0,id)
    result = writeDb(sql,data)
    if result:
        redirect('/taskinfo')
    else:
        return '-1'

@route('/delcontent/<id>/<cid>')
@checkLogin
def delcontent(id,cid):
    """删除任务，其实就是把任务的删除状态改成0（0为被删除，1为正常）"""
    s = request.environ.get('beaker.session')
    del_userid = s['userid']
    sql = "DELETE FROM pcontent WHERE cid=%s"
    result = writeDb(sql,(cid,))
    if result:
        redirect('/infotask/'+id)
    else:
        return '-1'

@route('/delplace/<id>/<plid>')
@checkLogin
def delplace(id,plid):
    """删除任务，其实就是把任务的删除状态改成0（0为被删除，1为正常）"""
    s = request.environ.get('beaker.session')
    del_userid = s['userid']
    sql = "DELETE FROM pplace WHERE plid=%s"
    result = writeDb(sql,(plid,))
    if result:
        redirect('/infotask/'+id)
    else:
        return '-1'

@route('/scoremore')
@checkLogin
def getscoremore():
    s = request.environ.get('beaker.session')
    id = s['userid']
    #耐力计算公式：24分-17分=420秒，1-（成绩-17分）/420秒=耐力值
    #速度计算公式：2分40秒-1分40秒=60秒，1-（成绩-100秒）/60秒=速度值
    #力量计算公积：（单杠1+单杠2*2）/(36+20*2)=力量值（假设单杠1 12个及格，2 9个及格）
    sql = """
        SELECT
            FORMAT(1-(((avg(time_to_sec(s.wugongli)))-1020)/420),2)*100 as naili,
            FORMAT(1-(((avg(time_to_sec(s.sibaimi)))-100)/60),2)*100 as sudu,
            FORMAT((AVG(s.dangang1)+AVG(s.dangang2)*2)/76,2)*100 as liliang,
            u.height,
            u.weight
        FROM
        (
        SELECT 
            id,
            wugongli,
            sibaimi,
            case when dangang1 = '暂无' then null else dangang1 end as dangang1,
            case when dangang2 = '暂无' then null else dangang2 end as dangang2
        FROM
            score
        WHERE
            id=%s
        ) AS s
        LEFT OUTER JOIN user as u on u.id=s.id
    """
    result = readDb(sql,(id,))
    name_sql = "select id,name from user;"
    name_result = readDb(name_sql, )
    AVG_sql = """
    SELECT 
        FORMAT(1-(((avg(time_to_sec(s.wugongli)))-1020)/420),2)*100 as naili,
        FORMAT(1-(((avg(time_to_sec(s.sibaimi)))-100)/60),2)*100 as sudu,
        FORMAT((AVG(s.dangang1)+AVG(s.dangang2)*2)/76,2)*100 as liliang,
        AVG(u.height) as height,
        AVG(u.weight) as weight
    FROM
        score AS s
    LEFT OUTER JOIN user as u on u.id=s.id
    WHERE
        date=(
        SELECT MAX(date) FROM score
        )
    """
    AVG_result = readDb(AVG_sql,)
    Date_sql = "SELECT subject,date FROM scorelist WHERE del_status=1"
    date_result = readDb(Date_sql,)

    dsql = 'select MAX(date) from score'
    res = readDb(dsql,)
    date = res[0].get('MAX(date)')
    Sum_sql = """
    SELECT
        count((wugongli > '00:21:00' AND wugongli <= '00:23:00') OR NULL) AS 'w_jige',
        count((wugongli <= '00:21:00' AND wugongli>'00:19:00') OR NULL) AS 'w_lianghao',
        count(wugongli <= '00:19:00' OR NULL)  AS 'w_youxiu',
        count(wugongli > '00:23:00' OR NULL)  AS 'w_bujige',
        count((sibaimi > '00:02:15' AND sibaimi <= '00:02:30') OR NULL) AS 'z_jige',
        count((sibaimi <= '00:02:15' AND sibaimi>'00:02:00') OR NULL) AS 'z_lianghao',
        count(sibaimi <= '00:02:00' OR NULL)  AS 'z_youxiu',
        count(sibaimi > '00:02:30' OR NULL)  AS 'z_bujige',
        count((dangang1 >= 12 AND dangang1 < 18) OR NULL) AS '1_jige',
        count((dangang1 < 25 AND dangang1>=18) OR NULL) AS '1_lianghao',
        count(dangang1 >= 25 OR NULL)  AS '1_youxiu',
        count(dangang1 < 12 OR NULL)  AS '1_bujige',
        count((dangang2 >= 9 AND dangang2 < 12) OR NULL) AS '2_jige',
        count((dangang2 < 18 AND dangang2>=12) OR NULL) AS '2_lianghao',
        count(dangang2 >= 18 OR NULL)  AS '2_youxiu',
        count(dangang2 < 9 OR NULL)  AS '2_bujige'
    FROM score
    WHERE date = %s
    """
    sum_result=readDb(Sum_sql,(date,))
    return template('scoremore',result=result,name=name_result,date=date_result,sum=sum_result,select="",AVG_result=AVG_result)

@route('/scoremore',method="POST")   #响应用户查询————成绩分析
@checkLogin
def getscoremore():
    s = request.environ.get('beaker.session')
    id = s['userid']
    select_id = request.forms.get("name")
    select_date = request.forms.get("date")
    sql = """
        SELECT
            FORMAT(1-(((avg(time_to_sec(s.wugongli)))-1020)/420),2)*100 as naili,
            FORMAT(1-(((avg(time_to_sec(s.sibaimi)))-100)/60),2)*100 as sudu,
            FORMAT((AVG(s.dangang1)+AVG(s.dangang2)*2)/76,2)*100 as liliang,
            u.height,
            u.weight
        FROM
        (
        SELECT 
            id,
            wugongli,
            sibaimi,
            case when dangang1 = '暂无' then null else dangang1 end as dangang1,
            case when dangang2 = '暂无' then null else dangang2 end as dangang2
        FROM
            score
        WHERE
            id=%s
        ) AS s
        LEFT OUTER JOIN user as u on u.id=s.id
    """
    result = readDb(sql,(id,))
    name_sql = "select id,name from user;"
    name_result = readDb(name_sql, )
    #雷达图 平均成绩
    AVG_sql = """  
        SELECT 
            FORMAT(1-(((avg(time_to_sec(s.wugongli)))-1020)/420),2)*100 as naili,
            FORMAT(1-(((avg(time_to_sec(s.sibaimi)))-100)/60),2)*100 as sudu,
            FORMAT((AVG(s.dangang1)+AVG(s.dangang2)*2)/76,2)*100 as liliang,
            AVG(u.height) as height,
            AVG(u.weight) as weight
        FROM
            score AS s
        LEFT OUTER JOIN user as u on u.id=s.id
        WHERE
            date=(
            SELECT MAX(date) FROM score
            )
        """
    AVG_result = readDb(AVG_sql, )
    #雷达图 选中项成绩
    if(select_id):
        sql2 = """
                SELECT
                    FORMAT(1-(((avg(time_to_sec(s.wugongli)))-1020)/420),2)*100 as naili,
                    FORMAT(1-(((avg(time_to_sec(s.sibaimi)))-100)/60),2)*100 as sudu,
                    FORMAT((AVG(s.dangang1)+AVG(s.dangang2)*2)/76,2)*100 as liliang,
                    u.height,
                    u.weight,
                    u.name
                FROM
                (
                SELECT 
                    id,
                    wugongli,
                    sibaimi,
                    case when dangang1 = '暂无' then null else dangang1 end as dangang1,
                    case when dangang2 = '暂无' then null else dangang2 end as dangang2
                FROM
                    score
                WHERE
                    id=%s
                ) AS s
                LEFT OUTER JOIN user as u on u.id=s.id
            """
        select_res = readDb(sql2,(select_id,))
    else:
        select_res = ""
    Date_sql = "SELECT subject,date FROM scorelist WHERE del_status=1"
    date_result = readDb(Date_sql,)
    #柱形图 统计和
    Sum_sql = """
        SELECT
            count((wugongli > '00:21:00' AND wugongli <= '00:23:00') OR NULL) AS 'w_jige',
            count((wugongli <= '00:21:00' AND wugongli>'00:19:00') OR NULL) AS 'w_lianghao',
            count(wugongli <= '00:19:00' OR NULL)  AS 'w_youxiu',
            count(wugongli > '00:23:00' OR NULL)  AS 'w_bujige',
            count((sibaimi > '00:02:15' AND sibaimi <= '00:02:30') OR NULL) AS 'z_jige',
            count((sibaimi <= '00:02:15' AND sibaimi>'00:02:00') OR NULL) AS 'z_lianghao',
            count(sibaimi <= '00:02:00' OR NULL)  AS 'z_youxiu',
            count(sibaimi > '00:02:30' OR NULL)  AS 'z_bujige',
            count((dangang1 >= 12 AND dangang1 < 18) OR NULL) AS '1_jige',
            count((dangang1 < 25 AND dangang1>=18) OR NULL) AS '1_lianghao',
            count(dangang1 >= 25 OR NULL)  AS '1_youxiu',
            count(dangang1 < 12 OR NULL)  AS '1_bujige',
            count((dangang2 >= 9 AND dangang2 < 12) OR NULL) AS '2_jige',
            count((dangang2 < 18 AND dangang2>=12) OR NULL) AS '2_lianghao',
            count(dangang2 >= 18 OR NULL)  AS '2_youxiu',
            count(dangang2 < 9 OR NULL)  AS '2_bujige'
        FROM score
        WHERE date = %s
        """
    if (select_date):
        sum_result = readDb(Sum_sql, (select_date,))
    else:
        dsql = 'select MAX(date) from score'
        res = readDb(dsql, )
        date = res[0].get('MAX(date)')
        sum_result = readDb(Sum_sql, (date,))
    return template('scoremore',result=result,name=name_result,date=date_result,sum=sum_result,select=select_res,AVG_result=AVG_result)

if __name__ == '__main__':
    app = default_app()
    app = SessionMiddleware(app, session_opts)
    run(app=app,host='127.0.0.1', port=9090,debug=True,server='gevent')