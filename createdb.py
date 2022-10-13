#データベースを作成する
from app import db, app

# db.create_all()でのデータベース作成の注意
#Flask-SQLAlchemyのバージョン3.0以降はコンテキストが必要
#https://stackoverflow.com/questions/73961938/flask-sqlalchemy-db-create-all-raises-runtimeerror-working-outside-of-applicat
#pathは./instance/todo.db

with app.app_context():
    db.create_all()
