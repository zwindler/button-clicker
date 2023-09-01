#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import psycopg2
from flask import Flask, render_template, request
app = Flask(__name__)

def create_conn():
    try:
        conn = psycopg2.connect("dbname='buttonclicker' user='buttonclicker' host='postgresql-service' password='buttonclicker'")
        return conn
    except Exception as e:
        print(f"Error: {e}")
        raise

def get_cursor(conn):
    cursor = conn.cursor()
    return cursor

def init_db(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS click (click_id SERIAL PRIMARY KEY,
                                                        sender VARCHAR(255) NOT NULL)""")

def count_click(cursor):
    cursor.execute("""SELECT COUNT(*) FROM click""")
    rows = cursor.fetchall()
    count=0
    for row in rows:
        count+=row[0]
    return count

def add_click(cursor, sender):
    cursor.execute("INSERT INTO click (sender) VALUES (%s);", (sender,))

@app.route("/")
def publish():
    conn = create_conn()
    cursor = get_cursor(conn)
    cur_cookies=str(count_click(cursor))
    conn.close()
    return render_template("home.html", message_bienvenue=str(cur_cookies))

@app.route("/click")
def linkclick():
    try:
        with create_conn() as conn:
            with get_cursor(conn) as cursor:
                add_click(cursor, request.remote_addr)
                new_cookies = count_click(cursor)
                conn.commit()
        return render_template("home.html", message_bienvenue=str(new_cookies))
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred."

def main():
    conn = create_conn()
    init_db(get_cursor(conn))
    conn.commit()
    conn.close()
    app.run(host='0.0.0.0', port=8080)
    sys.exit()

if __name__ == '__main__':
    main()
