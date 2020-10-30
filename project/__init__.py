from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Site.db'
app.config['SECRET_KEY']="My5ecretK3y"
app.config["SQLALCHEMY_ECHO"] = True


db=SQLAlchemy(app)
if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
        def _fk_pragma_on_connect(dbapi_con, con_record):  
            dbapi_con.execute('pragma foreign_keys=ON')

        
        event.listen(db.engine, 'connect', _fk_pragma_on_connect)

from project import routes