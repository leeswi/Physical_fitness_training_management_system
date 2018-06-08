#!/usr/bin/env python
#coding=utf-8
import os,sys,json
from bottle import request,route,error,run,default_app
from bottle import template,static_file,redirect,abort
import bottle
import logging
from beaker.middleware import SessionMiddleware
from bottle import TEMPLATE_PATH
import time,datetime
import hashlib
from gevent import monkey;
import MySQLdb
import hashlib
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
upload_path = '/'.join((pro_path,'upload'))

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

@route('/assets/<filename:re:.*\.ttf|.*\.otf|.*\.eot|.*\.woff|.*\.svg|.*\.map>')
def server_static(filename):
    """定义/assets/字体资源路径"""
    return static_file(filename, root=assets_path)


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
    # else:
    #     qq = int(qq)
    #     phone = int(phone)
    #     access = int(access)

    sql = """
            INSERT INTO
                user(name,username,passwd,birthday,sex,height,email,Company,weight,access,teamname)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
    data = (name,username,passwd,birthday,sex,height,email,Company,weight,access,teamname)
    result = writeDb(sql,data)
    print result
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
    print id
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

@route('/api/getitem',method=['GET', 'POST'])
@checkLogin
def getitem():
    sql = """
        SELECT
            I.id,
            I.name,
            U.name as userid,
            I.itype,
            date_format(I.adddate,'%%Y-%%m-%%d %%h:%%i:%%s') as adddate,
            date_format(I.startdate,'%%Y-%%m-%%d') as startdate,
            date_format(I.enddate,'%%Y-%%m-%%d') as enddate,
            I.status
        FROM
            item as I
            LEFT OUTER JOIN user as U on U.id=I.userid
        WHERE I.del_status=1
    """
    item_list = readDb(sql,)
    return json.dumps(item_list)



@route('/additem')
@checkLogin
def additem():
    return template('additem',info={})

@route('/additem',method="POST")
@checkLogin
def do_additem():
    s = request.environ.get('beaker.session')
    name = request.forms.get("name")
    itype = request.forms.get("itype")
    startdate = request.forms.get("startdate")
    enddate = request.forms.get("enddate")
    userid = s.get('userid',0)
    content = request.forms.get("content")
    sql = "INSERT INTO item(name,userid,itype,startdate,enddate,content) VALUES(%s,%s,%s,%s,%s,%s)"
    data = (name,userid,itype,startdate,enddate,content)
    result = writeDb(sql,data)
    redirect('/item')

@route('/edititem/<id>')
@checkLogin
def edititem(id):
    s = request.environ.get('beaker.session')
    sql = """
        SELECT
            name,
            userid,
            itype,
            date_format(startdate,'%%Y-%%m-%%d') as startdate,
            date_format(enddate,'%%Y-%%m-%%d') as enddate,
            content,
            status
        FROM
            item
        WHERE id = %s
        """
    result = readDb(sql,(id))
    if not result:
        abort(404)
    if result[0].get('userid') != s.get('userid',None) and s.get('access',None) == 0:
        abort(404)
    return template('additem',info=result[0])

@route('/edititem/<id>',method="POST")
@checkLogin
def do_edititem(id):
    name = request.forms.get("name")
    itype = request.forms.get("itype")
    startdate = request.forms.get("startdate")
    enddate = request.forms.get("enddate")
    content = request.forms.get("content")
    sql = "UPDATE item SET name=%s,itype=%s,startdate=%s,enddate=%s,content=%s WHERE id=%s"
    data = (name,itype,startdate,enddate,content,id)
    result = writeDb(sql,data)
    redirect('/item')

@route('/delitem/<id>')
@checkLogin
def delitem(id):
    s = request.environ.get('beaker.session')
    del_userid = s['userid']
    sql = """
        UPDATE
            item
        SET
            del_userid=%s,
            del_status=%s
        WHERE
            id=%s
    """
    data = (del_userid,0,id)
    result = writeDb(sql,data)
    if result:
        redirect('/item')
    else:
        return '-1'

@route('/dropitem')
@checkLogin
def dropitem():
    return template('dropitem')

@route('/api/dropitem',method=['GET', 'POST'])
@checkLogin
def dropitem():
    sql = """
        SELECT
            I.id,
            I.name,
            U1.name as userid,
            U2.name as del_userid,
            I.itype,
            date_format(I.adddate,'%%Y-%%m-%%d %%h:%%i:%%s') as adddate,
            date_format(I.startdate,'%%Y-%%m-%%d') as startdate,
            date_format(I.enddate,'%%Y-%%m-%%d') as enddate,
            I.status
        FROM
            item as I
            LEFT OUTER JOIN user as U1 on U1.id=I.userid
            LEFT OUTER JOIN user as U2 on U2.id=I.del_userid
        WHERE
            I.del_status=0
        """
    item_list = readDb(sql,)
    return json.dumps(item_list)


@route('/recoveryitem/<id>')
@checkLogin
def recoveryitem(id):
    sql = """
        UPDATE
            item
        SET
            del_status=%s
        WHERE
            id=%s
    """
    data = (1,id)
    result = writeDb(sql,data)
    if result:
        redirect('/dropitem')
    else:
        return '-1'



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
    print startdate

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
    	   ts.userid,
    	   ts.content,
    	   date_format(ts.date,'%%Y-%%m-%%d') as dates,
    	   date_format(ts.begintime,'%%Y-%%m-%%d %%h:%%i:%%s') as begintime,
    	   date_format(ts.finishtime,'%%Y-%%m-%%d %%h:%%i:%%s') as finishtime,
    	   ts.place,
    	   ts.level,
    	   ts.teamid,
    	   case when t.status = 0 then '未开始' when t.status = 1 then '进行中' ELSE '已完成' end as status
    	FROM
    	   plan as T
    	   LEFT OUTER JOIN user as u on u.id=T.inputid
    	   LEFT OUTER JOIN task as ts on ts.id=T.id
    	WHERE
    	   T.id=%s
    """
    taskinfo = readDb(task_sql,(id,))

    return template('infotask',taskinfo=taskinfo,myusername=myusername)

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
    print id
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
    user = s.get('user',None)
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

@route('/api/getscoreinfo/<date>',method=['GET', 'POST'])
@checkAccess
def getscoreinfo(date):
    dates = date[0:4]+"-"+date[4:6]+"-"+date[6:8]
    print dates
    sql = """
        SELECT
            S.id,
            u.name as name,
            S.wugongli,
            S.sibaimi,
            S.dangang1,
            S.dangang2,
            u.teamname as teamname,
            date_format(s.date,'%%Y-%%m-%%d') as date
        FROM
            score AS S
            LEFT OUTER JOIN user as u on u.id=S.id
        WHERE 
            S.date = %s
    """
    scorelist = readDb(sql,(dates,))
    return json.dumps(scorelist)

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

@route('/recoverytask/<id>')
@checkLogin
def recovery(id):
    """恢复任务，即把任务的删除状态从0改成1（0为被删除，1为正常）"""
    sql = """
        UPDATE
            task
        SET
            del_status=%s
        WHERE
            id=%s
    """
    data = (1,id)
    result = writeDb(sql,data)
    if result:
        redirect('/droptask')
    else:
        return '-1'

@route('/infoitem/<id>')
@checkLogin
def infoitem(id):
    """任务内容详情页"""
    item_sql = """
       SELECT
            I.id,
            I.name,
            U.name as userid,
            I.itype,
            date_format(I.adddate,'%%Y-%%m-%%d') as adddate,
            date_format(I.startdate,'%%Y-%%m-%%d') as startdate,
            date_format(I.enddate,'%%Y-%%m-%%d') as enddate,
            I.content,
            I.status
        FROM
            item AS I
            LEFT OUTER JOIN user AS U on I.userid = U.id
        WHERE
            I.id=%s
    """

    task_count_sql = """
        select
          (select count(1) from task where itemid=%s) as cou,
          (select count(1) from task where status=0 and itemid=%s) as wait,
          (select count(1) from task where status=1 and itemid=%s) as doing,
          (select count(1) from task where status=2 and itemid=%s) as finish
    """
    item_data = readDb(item_sql,(id))
    task_count = readDb(task_count_sql,(id,id,id,id))
    return template('infoitem',item_data=item_data,task_count=task_count)

@route('/api/getiteminfo',method=["GET","POST"])
@checkLogin
def do_infoitem():
    try:
        id = request.environ.get('HTTP_REFERER',0)
        id = id.split('/')[-1]
    except Exception:
        id = 0;
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
         WHERE T.del_status=1 AND T.itemid = %s
         ) AS t
     """
    result = readDb(sql,(id))
    return json.dumps(result)

@route('/api/get_item_task/<id>',method=['GET','POST'])
@checkLogin
def tasklist(id):
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
            {where} AND T.del_status=1 AND T.itemid=%s
            ) AS t
        """.format(where=wherestr)

    tasklist = readDb(sql,(id))
    return json.dumps(tasklist)



if __name__ == '__main__':
    app = default_app()
    app = SessionMiddleware(app, session_opts)
    run(app=app,host='127.0.0.1', port=9090,debug=True,server='gevent')