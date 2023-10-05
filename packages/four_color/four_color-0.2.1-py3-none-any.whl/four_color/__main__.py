from os import environ, path

from flask import Flask, make_response, redirect, request
from werkzeug.utils import secure_filename

from . import load_image, make_graph, solve_four_color

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def root():
    if request.method != "POST":
        return (
            "<form action='/' enctype='multipart/form-data' "
            "method='POST'><input type='file' name='im' size='30'>"
            "<input type='submit' value='send'></from>"
        )
    f = request.files["im"]
    fn = secure_filename(f.filename) if f else ""
    ext = path.splitext(fn)[1]
    if not fn or not ext.endswith(("png", "gif", "jgp", "jpeg")):
        return redirect("/")
    fn = "fig" + ext
    f.save(fn)
    im = load_image(fn)
    g = make_graph(im)
    solve_four_color(im, g)
    im.save(fn)
    res = make_response()
    with open(fn, "rb") as fp:
        res.data = fp.read()
    res.headers["Content-Type"] = "application/octet-stream"
    res.headers["Content-Disposition"] = "attachment; filename=fig" + ext
    return res


HOST = environ.get("SERVER_HOST", "localhost")
PORT = environ.get("SERVER_PORT", "")
PORT = int(PORT) if PORT.isdigit() else 8000
app.config["MAX_CONTENT_LENGTH"] = 210000
app.debug = True
app.run(HOST, PORT)
