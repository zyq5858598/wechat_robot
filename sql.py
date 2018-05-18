import mysql.connector
host='localhost'
user='root'
passwd='root'
db='saber'
class myMysal():
    def select(self,sql):
        conn = mysql.connector.connect(host=host, user=user, passwd=passwd, db=db)
        cursor = conn.cursor()
        cursor.execute(sql)
        values = cursor.fetchall()
        cursor.close()
        conn.close()
        return values

    def update(self,sql):
        conn = mysql.connector.connect(host=host, user=user, passwd=passwd, db=db)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()

    def select_project_by_gid(self,gid):
        projects = self.select("select * from t_project where group_id ='%s'"%(gid))
        if len(projects) == 1:
            return projects[0]
        else:
            return None
    def select_project_by_name(self,name):
        projects = self.select("select * from t_project where name ='%s'"%(name))
        if len(projects) == 1:
            return projects[0]
        else:
            return None