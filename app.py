from flask import Flask
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345@127.0.0.1:3306/project'
app.config['SECRET_KEY'] = 'project'

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from controllers import *
from extensions import *
from models import *
from forms import *


admin=Admin(app)
admin.add_view(ModelView(User,db.session))
admin.add_view(ModelView(Product,db.session))
admin.add_view(ModelView(Category,db.session))
# admin.add_view(ModelView(Subcategory,db.session))
admin.add_view(ModelView(Size,db.session))
admin.add_view(ModelView(Color,db.session))
admin.add_view(ModelView(Contact,db.session))
admin.add_view(ModelView(Comments,db.session))


if '__name__' == '__main__':
    app.init_app(db)
    app.init_app(migrate)



