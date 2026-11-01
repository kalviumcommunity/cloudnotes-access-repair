import json,os
from http.server import BaseHTTPRequestHandler,HTTPServer
import psycopg
URL=os.environ["DATABASE_URL"]
with psycopg.connect(URL) as c:
    c.execute("CREATE TABLE IF NOT EXISTS notes (id SERIAL PRIMARY KEY, body TEXT NOT NULL)")
class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args): pass
    def reply(self,code,data):
        self.send_response(code);self.send_header("Content-Type","application/json");self.end_headers();self.wfile.write(json.dumps(data).encode())
    def do_GET(self):
        if self.path!="/notes":return self.reply(404,{"error":"not found"})
        with psycopg.connect(URL) as c:
            rows=c.execute("SELECT id,body FROM notes ORDER BY id").fetchall()
        self.reply(200,[{"id":r[0],"text":r[1]} for r in rows])
    def do_POST(self):
        if self.path!="/notes":return self.reply(404,{"error":"not found"})
        data=json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        with psycopg.connect(URL) as c:
            row=c.execute("INSERT INTO notes(body) VALUES (%s) RETURNING id,body",(data["text"],)).fetchone()
        self.reply(201,{"id":row[0],"text":row[1]})
print("CloudNotes listening on "+os.environ["BIND"]+":8080",flush=True)
HTTPServer((os.environ["BIND"],8080),Handler).serve_forever()
