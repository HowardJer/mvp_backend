from flask import Flask, request, Response
# from flask_cors import CORS
import mariadb
import dbcreds
import json
import sys

app = Flask(__name__)
# CORS(app)

def connect(): 
    return mariadb.connect(
        host = dbcreds.host,
        port = dbcreds.port,
        user = dbcreds.user,
        password = dbcreds.password,
        database = dbcreds.database 
    )

@app.route("/library",methods=["GET", "POST", "PATCH", "DELETE"])  
def book():
    if request.method == "GET":
        conn = None
        cursor = None
        results = None
        try:
            conn = connect()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM library")
            results = cursor.fetchall()
        except Exception as e:
            print(e)
        finally: 
            print(results)
            if(conn != None):
              
                conn.close() 
            if(cursor != None):
                cursor.close()
            if(results != None or results == []):
                library = []
            return Response(
                    json.dumps(results, default=str),
                    mimetype="application/json",
                    status=200)
            else: 
                return Response("Failed", mimetype="html/text", status=400)         
    if request.method == "POST":
        content = request.json.get("content")
        conn = None
        cursor = None
        results = None
        try:
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO blog_list (content) VALUES (?)",
                           [content]
            )
            conn.commit()
            blog_id = cursor.lastrowid
        except Exception as e:
            print(e)
        finally: 
            if(conn != None):
                conn.rollback() 
                conn.close() 
            if(cursor != None):
                cursor.close()
            if(blog_id != None ):


                blog ={
                    "id":blog_id,
                    "content": content
                }              

                return Response(
                    json.dumps(blog, default=str),
                    mimetype="application/json", status=200 #200
                )
            else: 
                return Response(
                    "Failed", 
                    mimetype="html/text", status=200 #400
                )            
    # if request.method == "PATCH":
    #     content = request.json.get("content")
    #     blog_id = request.json.get("id")
    #     conn = None
    #     cursor = None
    #     try:
    #         conn = connect()
    #         cursor = conn.cursor()
    #         cursor.execute("UPDATE blog_list SET  content =? WHERE id=?",
    #                        [content, blog_id])
    #         conn.commit()
    #         rowcount = cursor.rowcount            
    #     except Exception as e:
    #         print(e)
    #     finally: 
    #         if(conn != None):
    #             conn.rollback() 
    #             conn.close() 
    #         if(cursor != None):
    #             cursor.close()
    #         if(rowcount == 1):
    #             blog ={
    #                 "id":blog_id,
    #                 "content": content
    #             }              
    #             return Response(json.dumps(blog, default=str),
    #                             mimetype="application/json",status=200)  
    #         else: 
    #             return Response("Failed", mimetype="html/text", status=200)   
    #     blog_id = request.json.get("id")
    #     conn = None
    #     cursor = None
    #     try:
    #         conn = connect()
    #         cursor = conn.cursor()
    #         cursor.execute("DELETE FROM blog_list WHERE id=?",[blog_id])
    #         rows = cursor.rowcount
    #         conn.commit()
    #         rowcount = cursor.rowcount
    #     except Exception as e:
    #         print(e)
    #     finally: 
    #         if(conn != None):
    #             conn.rollback() 
    #             conn.close() 
    #         if(cursor != None):
    #             cursor.close()
    #         if(rowcount == 1): 

    #             return Response("Success",mimetype="html/text",status=200)  
    #             return Response("Failed", mimetype="html/text", status=200)                        
