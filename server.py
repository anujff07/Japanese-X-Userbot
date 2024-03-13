import os
from flask import Flask

app = Flask(__name)

@app.route("/")
def checkstart():
    return "userbot is running"

if name == "main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 8080))
```
