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
        library_id = request.json.get("id")
        member_id = request.json.get("member_id")
        book_or_tape = request.json.get("book_or_tape")
        author_first_name = request.json.get("author_first_name")
        author_last_name = request.json.get("author_last_name")
        book_title = request.json.get("book_title")
        genre = request.json.get("genre")
              
        conn = None
        cursor = None
        results = None
        try:
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO library (member_id, book_or_tape, author_first_name, author_last_name, book_title, genre) VALUES (?, ?, ?, ?, ?, ?)",
                           [member_id, book_or_tape, author_first_name, author_last_name, book_title, genre]
            )
            conn.commit()
            library_id = cursor.lastrowid
        except Exception as e:
            print(e)
        finally:
            print(results)
            if(conn != None):
                conn.rollback() 
                conn.close() 
            if(cursor != None):
                cursor.close()
            if(library_id != None ):


                book ={
                    "id":library_id,
                    "member_id": member_id,
                    "book_or_tape": book_or_tape,
                    "author_first_name": author_first_name,
                    "author_last_name": author_last_name,
                    "boot_title": book_title,
                    "genre": genre          
                }              

                return Response(
                    json.dumps(book, default=str),
                    mimetype="application/json", status=200 
                )
            else: 
                return Response(
                    "Failed", 
                    mimetype="html/text", status=200 
                )   
                         
    if request.method == "PATCH":
        library_id = request.json.get("id")
        member_id = request.json.get("member_id")
        book_or_tape = request.json.get("book_or_tape")
        author_first_name = request.json.get("author_first_name")
        author_last_name = request.json.get("author_last_name")
        book_title = request.json.get("book_title")
        genre = request.json.get("genre")
        
        conn = None
        cursor = None
        try:
            conn = connect()
            cursor = conn.cursor()
            cursor.execute("UPDATE library SET book_or_tape =?, author_first_name =?, author_last_name =?, book_title =?, genre =? WHERE id=?",
                           [book_or_tape, author_first_name, author_last_name, book_title, genre, library_id])
            rows = cursor.rowcount
            conn.commit()
            rowcount = cursor.rowcount            
        except Exception as e:
            print(e)
        finally: 
            if(conn != None):
                conn.rollback() 
                conn.close() 
            if(cursor != None):
                cursor.close()
            if(rowcount == 1):
                book ={
                    "id":library_id,
                    "member_id": member_id,
                    "book_or_tape": book_or_tape,
                    "author_first_name": author_first_name,
                    "author_last_name": author_last_name,
                    "boot_title": book_title,
                    "genre": genre          
                }                   
                return Response(json.dumps(book, default=str),
                                mimetype="application/json",status=200)  
            else: 
                return Response("Failed", mimetype="html/text", status=200)   
    
    
    
    
    
    # if request.method == "DELETE":
    
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
