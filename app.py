from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

#データベースに保存する内容のカラム
class Post(db.Model):
    # __tablename__='todolist'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100))
    due = db.Column(db.DateTime, nullable=False)

#データベースに追加する
@app.route('/', methods=['GET','POST'])
def index():
    #既存データ：表示させる
    if request.method == 'GET':
        posts = Post.query.order_by(Post.due).all()
        return render_template('index.html', posts=posts, today=date.today())

    #新規データ：追加する
    else:
        title = request.form.get('title')
        detail = request.form.get('detail')
        due = request.form.get('due')

        due = datetime.strptime(due, '%Y-%m-%d')
        new_post = Post(title=title, detail=detail, due=due)

        db.session.add(new_post)
        db.session.commit()
        return redirect('/')

#データを登録するページ
@app.route('/create')
def create():
    return render_template('create.html')

#詳細を表示するページ
#idを指定して該当する項目の詳細を表示(todolistテーブルの主キーはid)
@app.route('/detail/<int:id>')
def detail(id):
    post=Post.query.get(id)
    return render_template('detail.html', post=post)

#idを指定して該当する項目を削除する
@app.route('/delete/<int:id>')
def delete(id):
    post=Post.query.get(id)

    db.session.delete(post)
    db.session.commit()
    return redirect('/')

#idを指定して該当する項目の編集をする
@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    post=Post.query.get(id)
    if request.method=='GET':
        return render_template('update.html', post=post)
    else:
        post.title=request.form.get('title')
        post.detail=request.form.get('detail')
        post.due=datetime.strptime(request.form.get('due'),'%Y-%m-%d')

        db.session.commit()
        return redirect('/')




#idを指定して該当する
if __name__=="__main__":
    # app.run(debug=True)
    app.run()
