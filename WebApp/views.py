from flask import Blueprint,request, render_template,redirect,url_for,flash,abort
from flask_login import login_required,current_user
from . import db ,admin
from . models import User, Expence
from flask_admin.contrib.sqla import ModelView

views = Blueprint('views',__name__)

@views.route("/",methods = ["GET","POST"])
@login_required
def home():
    if request.method =="POST":
        name= request.form.get('name')
        date= request.form.get('date')
        amount= request.form.get('amount')
        goods= request.form.get('goods')

        exp = Expence(name = name , date = date , amount = amount , goods = goods , added_by = current_user.id)

        db.session.add(exp)
        db.session.commit()
        flash('Goods Added Successfully')
    
    detail = Expence.query.all()
    total = total_amount()
    total_user_amount = user_amount(current_user.id)
    user = User.query.all()
    per_head_amount = total//len(user)
    # amount = amount_by_user()
    your_dues = total_user_amount - per_head_amount 
    return render_template('home.html',detail = detail, user = current_user,total_amount = total,total_user_amount = total_user_amount,per_head_amount = per_head_amount,your_dues = your_dues)


@views.route("/delete/<int:id>", methods = ['GET','POST'])
@login_required
def delete(id):
    exp = Expence.query.filter_by(id =id).first()
    if exp:
        db.session.delete(exp)
        db.session.commit()
        flash('Goods Deleted Successfully',category='error')
        return redirect(url_for('views.home'))
    
@views.route("/update/<int:id>", methods = ['POST','GET'])
@login_required
def update(id):
    exp = Expence.query.filter_by(id = id).first()
    
    if request.method == 'POST':
        exp.amount= request.form.get('amount')
        exp.goods= request.form.get('goods')
        db.session.commit()
        flash('Goods Updated Successfully', category='success')
        return redirect(url_for('views.home'))
    
def total_amount():
    detail = Expence.query.all()
    total = 0
    for i in detail:
        total+=int(i.amount)
    return total

    
def user_amount(id):
    total_user_amount = 0
    exp = Expence.query.filter_by(added_by = id)
    for i in exp:
        total_user_amount+=int(i.amount)
    return total_user_amount

@views.route("/amount_detail",methods = ["GET","POST"])
@login_required
def amount_by_user():
    user_list = []
    user_dict = {}
    # total =0 
    users = User.query.all()
    per_head_amount = total_amount()//len(users)
    for user in users:
        user_dict['id']=(user.id)
        user_dict['name']=user.username
        total_user_amount=user_amount(user.id)
        user_dict['amount'] = total_user_amount
        user_dict['your_dues'] = total_user_amount - per_head_amount 


        
        # exp = Expence.query.filter_by(added_by = user.id)
        # for i in exp:
        #     total += int(i.amount)
        # user_dict['total'] = total
        # total=0
        user_list.append(user_dict)
        user_dict = {}
    return render_template('all-user-amount.html', users = user_list)

@views.route("/user_exp_detail/<int:id>",methods = ["GET"])
@login_required
def user_exp_detail(id):
    user_exp = Expence.query.filter_by(added_by = id)
    detail = Expence.query.all()
    total = 0
    for i in detail:
        total+=int(i.amount)
    total_user_amount = user_amount(current_user.id)
    user = User.query.all()
    per_head_amount = total//len(user)
    # amount = amount_by_user()
    your_dues = total_user_amount-per_head_amount
    print(user_exp)
    return render_template('user-exp-details.html', detail = user_exp,total_amount = total,total_user_amount = total_user_amount,per_head_amount = per_head_amount,your_dues = your_dues, user = user)

# print(amount_by_user())

class MyModelView(ModelView):
    def is_accessible(self):
        if current_user.is_admin:
            return True
        return abort(401)


admin.add_view(MyModelView(User,db.session))
admin.add_view(MyModelView(Expence,db.session))
    




