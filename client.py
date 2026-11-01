import json,sys,urllib.request,urllib.error
url="http://localhost:18095/notes"
try:
    if sys.argv[1]=="list":request=urllib.request.Request(url)
    elif sys.argv[1]=="add":request=urllib.request.Request(url,data=json.dumps({"text":sys.argv[2]}).encode(),headers={"Content-Type":"application/json"})
    else:raise SystemExit("Use list or add TEXT")
    with urllib.request.urlopen(request,timeout=4) as r:print("HTTP",r.status,r.read().decode())
except (urllib.error.URLError,ConnectionError,TimeoutError) as ex:
    print("REQUEST FAILED:",str(ex));sys.exit(1)
