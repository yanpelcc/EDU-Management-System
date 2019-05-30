import tkinter.messagebox
from tkinter import *
import tkinter.font as tkFont
from tkinter.ttk import Treeview
import tkinter.messagebox
import pymysql


def sql_conn(sql):
    conn = pymysql.connect(host="127.0.0.1", user="root", password="yanpelc137", database="学生选课", charset="utf8")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql)
    ret = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return ret


def show_course():
    top = Toplevel()
    top.title('课程表')
    top.maxsize(320, 300)
    Label(top, text='欢迎使用CJLU学生管理系统', width=35, height=2,
          bg='#56764C').grid(row=0, sticky=W + E)
    columns = ('课程号', '课程名')
    tree = Treeview(top, show='headings', columns=columns)
    tree.column('课程号', width=150, anchor='center')
    tree.column('课程名', width=150, anchor='center')
    tree.heading('课程号', text='课程号')
    tree.heading('课程名', text='课程名')
    sql = "select * from course"
    ret = sql_conn(sql)
    for i in range(len(ret)):
        tree.insert('', i, values=(ret[i]['Cnum'], ret[i]['Cname']))
    tree.grid(row=1, sticky=W + E)


class LoginPage(object):
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('CJLU教务系统')
        self.root.maxsize(350, 180)
        Label(self.root, text='欢迎使用CJLU教务系统', width=40, height=2,
              bg='#56764C').grid(row=0, sticky=W + E)

        self.frame = Frame()
        self.frame.grid(row=2, pady=10)
        self.username = StringVar()
        self.password = StringVar()
        Label(self.frame, text='账号: ').grid(row=1, pady=10)
        Entry(self.frame, textvariable=self.username).grid(row=1, column=1)
        Label(self.frame, text='密码: ').grid(row=2, pady=10)
        Entry(self.frame, textvariable=self.password, show='*').grid(row=2, column=1)
        Button(self.frame, text='注册', width=5, command=sign_up).grid(row=3, column=0, pady=10)
        Button(self.frame, text='修改密码', width=10, command=change_password).grid(row=3, column=1, pady=10)
        Button(self.frame, text='登陆', width=5, command=self.loginCheck).grid(row=3, column=2, pady=10)

        self.root.mainloop()

    def loginCheck(self):
        sql = """select * from account where Snum='%s' and pw = '%s'""" % (self.username.get(), self.password.get())
        ret = sql_conn(sql)
        if len(ret) > 0 and self.username.get() == 'admin':
            tkinter.messagebox.showinfo('', '登陆成功!')
            self.root.destroy()
            MainPage()
        elif len(ret) > 0 and self.username.get() != 'admin':
            tkinter.messagebox.showinfo('', '登陆成功!')
            self.root.destroy()
            StudentPage(self.username.get())
        else:
            tkinter.messagebox.showerror(title='错误', message='账号或密码错误！')


def sign_up():
    def sign():
        sql = """select * from student where Snum='%s'""" % (username.get())
        ret = sql_conn(sql)
        try:
            if len(ret) > 0 and password1.get() == password2.get():
                sql = """insert into account values ('%s','%s')""" % (username.get(), password1.get())
                sql_conn(sql)
                tkinter.messagebox.showinfo('', '注册成功!')
                top.destroy()
            else:
                tkinter.messagebox.showerror(title='注册失败', message='学号不存在或两次输入的密码不同！')
        except:
            tkinter.messagebox.showerror(title='警告', message='账号已存在！')

    top = Toplevel()
    top.title('注册')
    top.maxsize(350, 250)
    top.geometry('350x250')
    Label(top, text='欢迎注册CJLU教务系统', width=40, height=2,
          bg='#56764C').grid(row=0, sticky=W + E)

    username = StringVar()
    password1 = StringVar()
    password2 = StringVar()
    Label(top, text='学号: ').place(x=66, y=60)
    Entry(top, textvariable=username).place(x=102, y=60)
    Label(top, text='请输入密码: ').place(x=26, y=110)
    Entry(top, textvariable=password1, show='*').place(x=102, y=110)
    Label(top, text='再次输入密码: ').place(x=13, y=160)
    Entry(top, textvariable=password2, show='*').place(x=102, y=160)
    Button(top, text='确认注册', width=10, command=sign).place(x=130, y=210)


def change_password():
    def change():
        sql1 = """select * from account where Snum='%s'""" % username.get()
        ret1 = sql_conn(sql1)
        sql2 = """select * from account where Snum='%s' and pw='%s'""" % (username.get(), oldpassword.get())
        ret2 = sql_conn(sql2)
        if not (len(ret1) > 0):
            tkinter.messagebox.showerror(title='修改失败', message='账号不存在！')
        elif not (len(ret2) > 0):
            tkinter.messagebox.showerror(title='修改失败', message='原密码不正确！')
        elif password1.get() != password2.get():
            tkinter.messagebox.showerror(title='修改失败', message='两次输入的密码不同！')
        else:
            sql = "update account set pw='" + password1.get() + "' where Snum='" + username.get() + "';"
            sql_conn(sql)
            tkinter.messagebox.showinfo('', '修改成功!')
            top.destroy()

    top = Toplevel()
    top.title('修改密码')
    top.maxsize(350, 250)
    top.geometry('350x250')
    Label(top, text='欢迎使用CJLU学生管理系统', width=40, height=2,
          bg='#56764C').grid(row=0, sticky=W + E)

    username = StringVar()
    oldpassword = StringVar()
    password1 = StringVar()
    password2 = StringVar()
    Label(top, text='账号: ').place(x=66, y=60)
    Entry(top, textvariable=username).place(x=110, y=60)
    Label(top, text='请输入原密码: ').place(x=13, y=90)
    Entry(top, textvariable=oldpassword, show='*').place(x=110, y=90)
    Label(top, text='请输入新密码: ').place(x=13, y=120)
    Entry(top, textvariable=password1, show='*').place(x=110, y=120)
    Label(top, text='再次输入密码: ').place(x=13, y=150)
    Entry(top, textvariable=password2, show='*').place(x=110, y=150)
    Button(top, text='确认修改', width=10, command=change).place(x=130, y=200)


class MainPage(object):
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('CJLU学生管理系统')
        self.root.maxsize(700, 600)
        Label(self.root, text='欢迎使用CJLU学生管理系统', font=tkFont.Font(size=18), width=60, height=2,
              bg='#56764C').grid(row=0, sticky=W + E)

        self.columns = ('学号', '姓名', '性别', '年龄')
        self.table = Treeview(self.root, height=14, show="headings", columns=self.columns)
        self.table.column('学号', width=150, anchor='center')
        self.table.column('姓名', width=150, anchor='center')
        self.table.column('性别', width=150, anchor='center')
        self.table.column('年龄', width=150, anchor='center')
        self.table.heading('学号', text="学号")
        self.table.heading('姓名', text="姓名")
        self.table.heading('性别', text="性别")
        self.table.heading('年龄', text="年龄")
        self.all_data()
        self.table.bind('<Double-1>', self.treeview_click)
        self.table.grid(row=1, sticky=W + E)

        self.frame = Frame()
        self.frame.grid(row=3, pady=20)
        self.snum = StringVar()
        self.sname = StringVar()
        self.sex = StringVar()
        self.age = StringVar()
        Label(self.frame, text="学号：").grid(row=1, column=0)
        Entry(self.frame, textvariable=self.snum).grid(row=1, column=1)
        Label(self.frame, text="姓名：").grid(row=2, column=0)
        Entry(self.frame, textvariable=self.sname).grid(row=2, column=1)
        Label(self.frame, text="性别：").grid(row=3, column=0)
        Entry(self.frame, textvariable=self.sex).grid(row=3, column=1)
        Label(self.frame, text="年龄：").grid(row=4, column=0)
        Entry(self.frame, textvariable=self.age).grid(row=4, column=1)

        Button(self.frame, text="查看课程表", width=12, command=self.open_course).grid(row=0, column=2, pady=2)
        Button(self.frame, text="查看选课信息", width=18, command=self.open_courese_s).grid(row=0, column=1)
        Button(self.frame, text="搜索", width=12, command=self.select).grid(row=1, column=2, padx=10, pady=2)
        Button(self.frame, text="修改", width=12, command=self.update).grid(row=1, column=3, pady=2)
        Button(self.frame, text="插入", width=12, command=self.insert).grid(row=2, column=2)
        Button(self.frame, text="删除", width=12, command=self.delete).grid(row=2, column=3)
        Button(self.frame, text="清空", width=12, command=self.clear).grid(row=4, column=2)
        Button(self.frame, text="退出", width=12, command=self.root.destroy).grid(row=4, column=3)

        self.root.mainloop()

    def open_course(self):
        Course()

    def open_courese_s(self):
        CourseSelect(self.snum.get())

    def all_data(self):
        sql = "select * from student"
        ret = sql_conn(sql)
        self.tab(ret)

    def tab(self, ret):
        for i in range(len(ret)):
            self.table.insert('', i, values=(ret[i]['Snum'], ret[i]['Sname'], ret[i]['sex'], ret[i]['age']))

    def delete_tab(self):
        items = self.table.get_children()
        [self.table.delete(item) for item in items]

    def select(self):
        if self.snum.get() == '' and self.sname.get() == '' and self.sex.get() == '' and self.age.get() == '':
            self.delete_tab()
            self.all_data()
            tkinter.messagebox.showerror('警告', '请输入要查询的信息！')
        elif self.snum.get() != '':
            sql = "select * from student where Snum='" + self.snum.get() + "';"
            ret = sql_conn(sql)
            self.delete_tab()
            self.tab(ret)
        elif self.sname.get() != '':
            sql = "select * from student where Sname like '" + self.sname.get() + "%';"
            ret = sql_conn(sql)
            self.delete_tab()
            self.tab(ret)
        elif self.sex.get() != '' and self.age.get() != '':
            sql = "select * from student where sex='" + self.sex.get() + "' and age='" + self.age.get() + "';"
            ret = sql_conn(sql)
            self.delete_tab()
            self.tab(ret)
        else:
            sql = "select * from student where sex='" + self.sex.get() + "' or age='" + self.age.get() + "';"
            ret = sql_conn(sql)
            self.delete_tab()
            self.tab(ret)

    def update(self):
        if self.snum.get() == '' or self.sname.get() == '' or self.sex.get() == '' or self.age.get() == '':
            tkinter.messagebox.showerror('警告', '请填写完整！')
        else:
            sql1 = "update student set sex='" + self.sex.get() + "' where Snum='" + self.snum.get() + "';"
            sql2 = "update student set Sname='" + self.sname.get() + "' where Snum='" + self.snum.get() + "';"
            sql3 = "update student set age='" + self.age.get() + "' where Snum='" + self.snum.get() + "';"
            sql_conn(sql1)
            sql_conn(sql2)
            sql_conn(sql3)
            tkinter.messagebox.showinfo('', '修改成功!')

        self.delete_tab()
        self.all_data()

    def insert(self):
        if self.sname.get() == '' or self.snum.get() == '':
            tkinter.messagebox.showerror('警告', '请填写完整！')
        else:
            try:
                sql = """insert into student values ('%s','%s','%s','%s');""" % (
                    self.snum.get(), self.sname.get(), self.sex.get(), self.age.get())
                sql_conn(sql)
                tkinter.messagebox.showinfo('', '添加成功!')
            except:
                tkinter.messagebox.showerror('警告', '学生已存在！')

        self.delete_tab()
        self.all_data()

    def delete(self):
        if self.snum.get() == '':
            tkinter.messagebox.showerror('警告', '请填写完整！')

        ret = sql_conn("""select * from student where Snum='%s'""" % self.snum.get())
        if len(ret) > 0:
            sql = "delete from student where Snum='" + self.snum.get() + "';"
            sql_conn(sql)
            tkinter.messagebox.showinfo('', '删除成功!')
            self.delete_tab()
            self.all_data()
        else:
            tkinter.messagebox.showerror('错误', '没有此学生！')

    def clear(self):
        self.snum.set('')
        self.sname.set('')
        self.sex.set('')
        self.age.set('')
        self.delete_tab()
        self.all_data()

    def treeview_click(self, event):
        item = self.table.focus()
        self.snum.set(self.table.item(item)['values'][0])
        self.sname.set(self.table.item(item)['values'][1])
        self.sex.set(self.table.item(item)['values'][2])
        self.age.set(self.table.item(item)['values'][3])


class StudentPage(object):
    def __init__(self, username):
        self.username = username
        text = """欢迎%s同学使用CJLU学生选课系统""" % (
            sql_conn("""select Sname from student where Snum='%s'""" % self.username)[0]['Sname'])
        self.root = tkinter.Tk()
        self.root.title('CJLU学生选课系统')
        self.root.maxsize(700, 600)
        Label(self.root, text=text, font=tkFont.Font(size=18), width=60, height=2,
              bg='#56764C').grid(row=0, sticky=W + E)

        self.columns = ('学号', '课程号', '成绩')
        self.table = Treeview(self.root, height=14, show="headings", columns=self.columns)
        self.table.column('学号', width=150, anchor='center')
        self.table.column('课程号', width=150, anchor='center')
        self.table.column('成绩', width=150, anchor='center')
        self.table.heading('学号', text="学号")
        self.table.heading('课程号', text="课程号")
        self.table.heading('成绩', text="成绩")
        self.all_data()
        self.table.bind('<Double-1>', self.treeview_click)
        self.table.grid(row=1, sticky=W + E)

        self.frame = Frame()
        self.frame.grid(row=3, pady=20)
        self.cnum = StringVar()
        Label(self.frame, text="课程号：").grid(row=1, column=0)
        Entry(self.frame, textvariable=self.cnum).grid(row=1, column=1)

        Button(self.frame, text="查看课程表", width=12, command=show_course).grid(row=0, column=1, pady=2)
        Button(self.frame, text="增加选课", width=12, command=self.insert).grid(row=1, column=2, padx=10, pady=2)
        Button(self.frame, text="删除选课", width=12, command=self.delete).grid(row=1, column=3, pady=2)
        Button(self.frame, text="清空", width=12, command=self.clear).grid(row=2, column=2, pady=10)
        Button(self.frame, text="退出", width=12, command=self.root.destroy).grid(row=2, column=3, pady=10)

    def all_data(self):
        sql = """select * from course_s where Snum='%s'""" % self.username
        ret = sql_conn(sql)
        self.tab(ret)

    def tab(self, ret):
        for i in range(len(ret)):
            self.table.insert('', i, values=(ret[i]['Snum'], ret[i]['Cnum'], ret[i]['score']))

    def delete_tab(self):
        items = self.table.get_children()
        [self.table.delete(item) for item in items]

    def insert(self):
        if self.cnum.get() == '':
            tkinter.messagebox.showerror('警告', '请输入课程号！')
        else:
            ret = sql_conn("""select * from course where Cnum='%s'""" % self.cnum.get())
            try:
                if len(ret) > 0:
                    sql = """insert into course_s values('%s','%s','')""" % (self.username, self.cnum.get())
                    sql_conn(sql)
                    self.delete_tab()
                    self.all_data()
                    tkinter.messagebox.showinfo('', '添加成功!')
                else:
                    tkinter.messagebox.showerror('错误', '没有此课程！')
            except:
                tkinter.messagebox.showerror('警告', '已选修此课程！')

    def delete(self):
        if self.cnum.get() == '':
            tkinter.messagebox.showerror('警告', '请输入课程号！')
        else:
            ret = sql_conn("""select * from course_s where Cnum='%s'""" % self.cnum.get())
            if len(ret) > 0:
                sql = """delete from course_s where Cnum='%s'""" % self.cnum.get()
                sql_conn(sql)
                self.delete_tab()
                self.all_data()
                tkinter.messagebox.showinfo('', '删除成功!')
            else:
                tkinter.messagebox.showerror('错误', '没有此课程！')

    def clear(self):
        self.cnum.set('')

    def treeview_click(self, event):
        item = self.table.focus()
        self.cnum.set(self.table.item(item)['values'][1])


class CourseSelect(object):
    def __init__(self, in_snum):
        self.in_snum = in_snum
        self.root = Toplevel()
        self.root.title('选课表')
        self.root.maxsize(450, 450)
        self.root.geometry('450x450')
        Label(self.root, text='欢迎使用CJLU学生管理系统', width=45, height=2,
              bg='#56764C').grid(row=0, sticky=W + E)
        self.columns = ('学号', '课程号', '成绩')
        self.tree = Treeview(self.root, show='headings', columns=self.columns)
        self.tree.column('学号', width=150, anchor='center')
        self.tree.column('课程号', width=150, anchor='center')
        self.tree.column('成绩', width=150, anchor='center')
        self.tree.heading('学号', text='学号')
        self.tree.heading('课程号', text='课程号')
        self.tree.heading('成绩', text='成绩')
        if in_snum == '':
            self.all_data()
            self.flag = 0
        else:
            self.flag = 1
            sql = """select * from course_s where Snum='%s'""" % self.in_snum
            ret = sql_conn(sql)
            self.tab(ret)

        self.tree.bind('<Double-1>', self.treeview_click)
        self.tree.grid(row=1, sticky=W + E)

        self.snum = StringVar()
        self.cnum = StringVar()
        self.score = StringVar()
        Label(self.root, text="学号：").place(x=50, y=270)
        Entry(self.root, textvariable=self.snum).place(x=90, y=270)
        Label(self.root, text="课程号：").place(x=37, y=300)
        Entry(self.root, textvariable=self.cnum).place(x=90, y=300)
        Label(self.root, text="成绩：").place(x=50, y=330)
        Entry(self.root, textvariable=self.score).place(x=90, y=330)

        Button(self.root, text="搜索", width=12, command=self.select).place(x=300, y=250)
        Button(self.root, text="修改成绩", width=12, command=self.update).place(x=300, y=280)
        Button(self.root, text="插入", width=12, command=self.insert).place(x=300, y=310)
        Button(self.root, text="删除", width=12, command=self.delete).place(x=300, y=340)
        Button(self.root, text="退出", width=12, command=self.root.destroy).place(x=300, y=380)
        Button(self.root, text="清空", width=12, command=self.clear).place(x=170, y=380)

        self.root.mainloop()

    def all_data(self):
        sql = """select * from course_s"""
        ret = sql_conn(sql)
        self.tab(ret)

    def tab(self, ret):
        for i in range(len(ret)):
            self.tree.insert('', i, values=(ret[i]['Snum'], ret[i]['Cnum'], ret[i]['score']))

    def delete_tab(self):
        items = self.tree.get_children()
        [self.tree.delete(item) for item in items]

    def select(self):
        if self.snum.get() == '' and self.cnum.get() == '' and self.score.get() == '':
            if self.flag == 1:
                self.tab(sql_conn("""select * from course_s where Snum='%s'""" % self.in_snum))
            else:
                self.all_data()
            tkinter.messagebox.showerror('警告', '请输入要查询的信息！')
        elif self.snum.get() != '' and self.cnum.get() != '':
            sql = "select * from course_s where Snum='" + self.snum.get() + "'and Cnum='" + self.cnum.get() + "';"
            ret = sql_conn(sql)
            self.delete_tab()
            self.tab(ret)
        elif self.snum.get() != '':
            sql = "select * from course_s where Snum='" + self.snum.get() + "';"
            ret = sql_conn(sql)
            self.delete_tab()
            self.tab(ret)
        elif self.cnum.get() != '':
            sql = "select * from course_s where Cnum='" + self.cnum.get() + "';"
            ret = sql_conn(sql)
            self.delete_tab()
            self.tab(ret)
        else:
            sql = "select * from course_s where score='" + self.score.get() + "';"
            ret = sql_conn(sql)
            self.delete_tab()
            self.tab(ret)

    def update(self):
        if self.score.get() == '':
            tkinter.messagebox.showerror('警告', '请填写成绩！')
        else:
            sql = "update course_s set score='" + self.score.get() + "' where Snum='" + self.snum.get() + "';"
            sql_conn(sql)
            self.delete_tab()
            if self.flag == 1:
                self.tab(sql_conn("""select * from course_s where Snum='%s'""" % self.in_snum))
            else:
                self.all_data()
            tkinter.messagebox.showinfo('', '修改成功!')

    def insert(self):
        if self.snum.get() == '' or self.cnum.get() == '':
            tkinter.messagebox.showerror('警告', '请输入学号和课程号！')
        else:
            ret = sql_conn("""select * from course_s where Cnum='%s'""" % self.cnum.get())
            try:
                if len(ret) > 0:
                    sql = """insert into course_s values('%s','%s','%s')""" % (
                        self.snum.get(), self.cnum.get(), self.score.get())
                    sql_conn(sql)
                    self.delete_tab()
                    if self.flag == 1:
                        self.tab(sql_conn("""select * from course_s where Snum='%s'""" % self.in_snum))
                    else:
                        self.all_data()
                    tkinter.messagebox.showinfo('', '添加成功!')
                else:
                    tkinter.messagebox.showerror('错误', '没有此课程！')
            except:
                tkinter.messagebox.showerror('错误', '已存在此信息！')

    def delete(self):
        if self.cnum.get() == '' or self.snum.get() == '':
            tkinter.messagebox.showerror('警告', '请输入学号和课程号！')
        else:
            ret = sql_conn(
                """select * from course_s where Snum='%s' and Cnum='%s'""" % (self.snum.get(), self.cnum.get()))
            if len(ret) > 0:
                sql = """delete from course_s where Snum='%s' and Cnum='%s'""" % (self.snum.get(), self.cnum.get())
                sql_conn(sql)
                self.delete_tab()
                if self.flag == 1:
                    self.tab(sql_conn("""select * from course_s where Snum='%s'""" % self.in_snum))
                else:
                    self.all_data()
                tkinter.messagebox.showinfo('', '删除成功!')
            else:
                tkinter.messagebox.showerror('错误', '没有此信息！')

    def clear(self):
        self.snum.set('')
        self.cnum.set('')
        self.score.set('')

        self.delete_tab()
        if self.flag == 1:
            self.tab(sql_conn("""select * from course_s where Snum='%s'""" % self.in_snum))
        else:
            self.all_data()

    def treeview_click(self, event):
        item = self.tree.focus()
        self.snum.set(self.tree.item(item)['values'][0])
        self.cnum.set(self.tree.item(item)['values'][1])
        self.score.set(self.tree.item(item)['values'][2])


class Course(object):
    def __init__(self):
        self.root = Toplevel()
        self.root.title('选课表')
        self.root.maxsize(410, 450)
        self.root.geometry('410x450')
        Label(self.root, text='欢迎使用CJLU学生管理系统', width=45, height=2,
              bg='#56764C').grid(row=0, sticky=W + E)
        self.columns = ('课程号', '课程名')
        self.tree = Treeview(self.root, show='headings', columns=self.columns)
        self.tree.column('课程号', width=150, anchor='center')
        self.tree.column('课程名', width=150, anchor='center')
        self.tree.heading('课程号', text='课程号')
        self.tree.heading('课程名', text='课程名')
        self.all_data()
        self.tree.bind('<Double-1>', self.treeview_click)
        self.tree.grid(row=1, sticky=W + E)

        self.cnum = StringVar()
        self.cname = StringVar()
        Label(self.root, text="课程号：").place(x=30, y=270)
        Entry(self.root, textvariable=self.cnum).place(x=80, y=270)
        Label(self.root, text="课程名：").place(x=30, y=300)
        Entry(self.root, textvariable=self.cname).place(x=80, y=300)

        Button(self.root, text="搜索", width=12, command=self.select).place(x=290, y=250)
        Button(self.root, text="修改课程名", width=12, command=self.update).place(x=290, y=280)
        Button(self.root, text="插入", width=12, command=self.insert).place(x=290, y=310)
        Button(self.root, text="删除", width=12, command=self.delete).place(x=290, y=340)
        Button(self.root, text="退出", width=12, command=self.root.destroy).place(x=290, y=380)
        Button(self.root, text="清空", width=12, command=self.clear).place(x=170, y=380)

    def all_data(self):
        sql = """select * from course"""
        ret = sql_conn(sql)
        self.tab(ret)

    def tab(self, ret):
        for i in range(len(ret)):
            self.tree.insert('', i, values=(ret[i]['Cnum'], ret[i]['Cname']))

    def delete_tab(self):
        items = self.tree.get_children()
        [self.tree.delete(item) for item in items]

    def select(self):
        if self.cnum.get() == '' and self.cname.get() == '':
            tkinter.messagebox.showerror('警告', '请填写完整！')
        elif self.cnum.get() != '':
            sql = "select * from course where Cnum='" + self.cnum.get() + "';"
            ret = sql_conn(sql)
            self.delete_tab()
            self.tab(ret)
        else:
            sql = "select * from course where Cname like '%" + self.cname.get() + "%';"
            ret = sql_conn(sql)
            self.delete_tab()
            self.tab(ret)

    def update(self):
        if self.cnum.get() == '' or self.cname.get() == '':
            tkinter.messagebox.showerror('警告', '请填写完整！')
        else:
            sql = "update course set Cname='" + self.cname.get() + "' where Cnum='" + self.cnum.get() + "';"
            sql_conn(sql)
            self.delete_tab()
            self.all_data()
            tkinter.messagebox.showinfo('', '修改成功!')

    def insert(self):
        if self.cnum.get() == '' or self.cname.get() == '':
            tkinter.messagebox.showerror('警告', '请填写完整！')
        else:
            try:
                sql = """insert into course values ('%s','%s');""" % (self.cnum.get(), self.cname.get())
                sql_conn(sql)
                self.delete_tab()
                self.all_data()
                tkinter.messagebox.showinfo('', '添加成功!')
            except:
                tkinter.messagebox.showerror('警告', '课程已存在！')

    def delete(self):
        if self.cnum.get() == '':
            tkinter.messagebox.showerror('警告', '请输入课程号！')
        else:
            ret = sql_conn("""select * from course where Cnum='%s'""" % self.cnum.get())
            if len(ret) > 0:
                sql = """delete from course where Cnum='%s'""" % self.cnum.get()
                sql_conn(sql)
                self.delete_tab()
                self.all_data()
                tkinter.messagebox.showinfo('', '删除成功!')
            else:
                tkinter.messagebox.showerror('错误', '没有此课程！')

    def clear(self):
        self.cnum.set('')
        self.cname.set('')
        self.delete_tab()
        self.all_data()

    def treeview_click(self, event):
        item = self.tree.focus()
        self.cnum.set(self.tree.item(item)['values'][0])
        self.cname.set(self.tree.item(item)['values'][1])


LoginPage()
