from flask import Flask, render_template

app = Flask(__name__) 

# @app.route("/") 
# def hello(): 
#     return render_template('index.html')

# @app.route('/<myname>')
# def hello(myname=None):
#   return render_template('index.html', name=myname)

@app.route('/<myname>/<int:post_id>')
def hello(myname=None, post_id=None):
  return render_template('index.html', name=myname, post_id=post_id)