import pymysql.cursors
config = {
          'host':'192.168.10.10',
          'port':3306,
          'user':'homestead',
          'password':'secret',
          'db':'mginet',
          'charset':'utf8mb4',
          'cursorclass':pymysql.cursors.DictCursor,
          }
def getRelatedKnowledge(att):
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    sql = "select value from knowledge_database where att = '" + att + "'"
    knowledge_count = cur.execute(sql)
    if knowledge_count >= 1:
        knows = []
        res = cur.fetchall()
        for val in res:
            knows.append(val['value'].encode('utf-8'))
    else:
        knows = []
    cur.close()
    conn.close()
    return knows

def getTask():
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    sql = "select id, title, pdf_path, status from extraction_tasks where status = 0 limit 1"
    task_count = cur.execute(sql)
    if task_count >= 1:
        task = cur.fetchone()
        task_id = task['id']
        sql = 'update extraction_tasks set status = 1 where id = %d' % task_id
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        return 200, task
    else:
        cur.close()
        conn.close()
        return 400, []

def updateTask(task_id, result):
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    status = 2
    sql = u'''update extraction_tasks set status = %d, result = '%s' where id = %d''' % (status, result.decode('utf-8'), task_id)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    return 200