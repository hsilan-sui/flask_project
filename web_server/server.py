from flask import Flask, render_template, request, redirect

app = Flask(__name__) 

@app.route("/") 
def home(): 
    return render_template('index.html')

@app.route('/<string:page_name>') 
def html_page(page_name): 
    return render_template(page_name)

# 定義使用者提交表單的API端點 以及 收到表單資料後 要回傳給前端的內容
@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        return redirect('/thankyou.html')

# @app.route('/about.html') 
# def about(): 
#     return render_template('/about.html')

# @app.route("/works.html") 
# def works(): 
#     return render_template('works.html')

# @app.route("/contact.html") 
# def contact(): 
#     return render_template('contact.html')