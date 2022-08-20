import datetime
from flask import Flask,render_template,request,session,redirect
import random
from DBConnection import Db

app = Flask(__name__)
app.secret_key="kkkk"
path=r"C:\Users\anuro\PycharmProjects\ANGANVADI_PORTAL\static\images\\"

@app.route('/logout')
def logout():
    session['oo']=""
    # session.clear()
    return redirect('/')


@app.route('/',methods=['GET','POST'])
def login():
    if request.method=="POST":
        username=request.form['textfield']
        password=request.form['textfield2']
        db=Db()
        qry=db.selectOne("select * from login WHERE username='"+username+"' and password='"+password+"'")

        if qry is not None:
            session['lid'] = qry['login_id']
            session['oo'] = "lin"
            if qry['type']=='ADMIN':
                return redirect('/admin_home')
            if qry['type']=='ANGANVADI':
                # session['lii'] = "lin"
                return redirect('/anganvadi_home')
            if qry['type'] == 'ICDS':
                # session['lii'] = "lin"
                return redirect('/ICDS_home')
            if qry['type'] == 'USER':
                # session['lii'] = "lin"
                session['lid']=qry['login_id']
                return redirect('/user_home')
        else:
            return '''<script>alert('user not found');window.location="/"</script>'''

    else:

        return render_template('login.html')


@app.route('/admin_home')
def admin_home():
    if session['oo'] == "lin":
        return render_template('ADMIN/index.html')
    else:
        return redirect('/')



@app.route('/add_ward',methods=['GET','POST'])
def add_ward():
    if session['oo'] == "lin":
        if request.method == "POST":
            wardno = request.form['textfield']
            wardname = request.form['textfield2']
            db = Db()
            db.insert("insert into ward VALUES ('','" + wardno + "','" + wardname + "')")
            return '''<script>alert('success');window.location="/admin_home"</script>'''



        else:
            db = Db()
            qry = db.select("select * from ward")
            return render_template('ADMIN/add_ward.html')
    else:
        return redirect('/')



@app.route('/view_ward')
def view_ward():
    if session['oo'] == "lin":
        db=Db()
        qry=db.select("select * from ward")
        return render_template('ADMIN/view_ward.html',data=qry)
    else:
        return redirect('/')

@app.route('/delward/<id>')
def delward(id):
    if session['oo'] == "lin":
        db=Db()
        qry=db.delete("delete from ward  where ward_id='"+id+"'")
        return redirect('/view_ward')
    else:
        return redirect('/')


@app.route('/add_anganvadi',methods=['GET','POST'])
def add_anganvadi():
    if session['oo'] == "lin":
        if request.method=="POST":
            wardno=request.form['select']
            anganvadino=request.form['textfield2']
            anganvadiplace=request.form['textfield3']
            email=request.form['textfield4']
            password=request.form['textfield5']

            db=Db()
            QRY2=db.insert("insert into login VALUES ('','"+email+"','"+password+"','ANGANVADI')")
            db.insert("insert into anganvadi VALUES ('"+str(QRY2)+"','"+wardno+"','"+anganvadino+"','"+anganvadiplace+"','"+email+"')")
            return '''<script>alert('success');window.location="/admin_home"</script>'''



        else:
            db=Db()
            qry=db.select("select * from ward")
            return render_template('ADMIN/add_anganvadi.html',data=qry)
    else:
        return redirect('/')

@app.route('/view_anganvadi')
def view_anganvadi():
    if session['oo'] == "lin":
        db = Db()
        qry = db.select("select * from anganvadi,ward where anganvadi.ward_id=ward.ward_id")
        return render_template('ADMIN/view_anganvadi.html', data=qry)
    else:
        return redirect('/')


@app.route('/delanganvadi/<id>')
def delanganvadi(id):
    if session['oo'] == "lin":
        db = Db()
        qry = db.delete("delete from anganvadi  where anganvadi_id='"+id+"'")
        qry1 = db.delete("delete from login  where login_id='"+id+"'")
        return redirect('/view_anganvadi')
    else:
        return redirect('/')


@app.route('/edtanganvadi/<aid>',methods=['get','post'])
def edtanganvadi(aid):
    if session['oo'] == "lin":
        if request.method=="POST":
            db = Db()
            wardno = request.form['select']
            anganvadino = request.form['textfield2']
            anganvadiplace = request.form['textfield3']
            email = request.form['textfield4']
            qry = db.update("update anganvadi set ward_id='"+wardno+"',anganvadi_number='"+anganvadino+"',place='"+anganvadiplace+"',Email='"+email+"' where anganvadi_id='"+str(aid)+"'")
            return  '''<script>alert('success');window.location="/admin_home"</script>'''
        else:
            db=Db()
            res=db.selectOne("select * from anganvadi,ward where anganvadi.ward_id=ward.ward_id and anganvadi_id='"+str(aid)+"'")
            res1=db.select("select * from ward ")
            return render_template("ADMIN/update_anganvadi.html",data=res,data1=res1)
    else:
        return redirect('/')



@app.route('/view_record/<id>')
def view_record(id):
    if session['oo'] == "lin":
        db=Db()
        qry = db.select("select * from record,user,anganvadi where record.user_id=user.user_id and record.anganvadi_id=anganvadi.anganvadi_id and record.anganvadi_id='"+str(id)+"'")
        return render_template('ADMIN/view_record.html',data=qry)
    else:
        return redirect('/')



@app.route('/view_feedback')
def view_feedback():
    if session['oo'] == "lin":
        db = Db()
        qry = db.select("select * from feedback,user where feedback.user_id=user.user_id")
        return render_template('ADMIN/view_feedback.html',data=qry)
    else:
        return redirect('/')



@app.route('/view_user/<id1>')
def view_user(id1):
    if session['oo'] == "lin":
        db = Db()
        qry = db.select("select * from user,ward,anganvadi where user.ward_id=ward.ward_id and user.anganvadi_id=anganvadi.anganvadi_id and user.anganvadi_id='"+str(id1)+"'")
        return render_template('ADMIN/view_user.html',data=qry)
    else:
        return redirect('/')



@app.route('/view_doubt')
def view_doubt():
    if session['oo'] == "lin":
        db = Db()
        qry = db.select("select * from doubt,user where doubt.user_id=user.user_id")
        return render_template('ADMIN/view_doubt.html',data=qry)
    else:
        return redirect('/')


@app.route('/send_reply/<did>',methods=['GET','POST'])
def send_reply(did):
    if session['oo'] == "lin":
        if request.method=="POST":
            reply=request.form['textarea']
            db=Db()
            db.update("update doubt set reply='"+reply+"',reply_date=curdate() where doubt_id='"+did+"'")
            return '''<script>alert('success');window.location="/admin_home"</script>'''
        else:
            return render_template('ADMIN/send_reply.html')
    else:
        return redirect('/')

@app.route('/view_reply')
def view_reply():
    if session['oo'] == "lin":
        db = Db()
        qry = db.select("select * from doubt,user where doubt.user_id=user.user_id ")
        return render_template('USER/view_reply.html',data=qry)
    else:
        return redirect('/')

@app.route('/view_birth')
def view_birth1():
        if session['oo'] == "lin":
            db = Db()
            qry = db.select("select * from birth")
            return render_template('ADMIN/view_birth.html', data=qry)
        else:
            return redirect('/')

@app.route('/view_death')
def view_death1():
        if session['oo'] == "lin":
            db = Db()
            qry = db.select("select * from death")
            return render_template('ADMIN/view_death.html', data=qry)
        else:
            return redirect('/')


@app.route('/view_attendence/<bid>')
def view_attendence1(bid):
        if session['oo'] == "lin":
            db = Db()
            # qry = db.select("select * from attendence")
            # return render_template('ADMIN/view_attendence.html', data=qry)
            qry = db.select("select * from attendence,anganvadi where attendence.anganvadi_id=anganvadi.anganvadi_id and attendence.anganvadi_id='" + str(bid) + "'")
            return render_template('ADMIN/view_attendence.html', data=qry)
        else:
            return redirect('/')





@app.route('/view_event')
def view_event1():
        if session['oo'] == "lin":
            db = Db()
            qry = db.select("select * from event")
            return render_template('ADMIN/view_event.html', data=qry)
        else:
            return redirect('/')








# ----------------------------------------------------------------------------------------------------------------------
#                              ANGANVADI MODULE
# -------------------------------------------------------------------------------------------------------------------------



@app.route('/anganvadi_home')
def anganvadi_home():
    if session['oo'] == "lin":
        return render_template('ANGANVADI/index1.html')
    else:
        return redirect('/')


@app.route('/add_user',methods=['GET','POST'])
def add_user():
    if session['oo'] == "lin":
        if request.method=="POST":
            name=request.form['textfield']
            dob=request.form['textfield2']
            gender=request.form['radio1']
            phonenumber=request.form['textfield3']
            address=request.form['textarea']
            category=request.form['radio']
            email=request.form['textfield5']
            wardno=request.form['select']
            password = request.form['textfield6']
            db = Db()
            QRY1 = db.insert("insert into login VALUES ('','" + email + "','" + str(password) + "','USER')")
            db.insert("insert into user VALUES ('" + str(QRY1) + "','"+name+"','"+dob+"','"+gender+"','"+phonenumber+"','"+address+"','"+category+"','"+email+"','"+wardno+"','"+str(session['lid'])+"')")
            return '''<script>alert('success');window.location="/anganvadi_home"</script>'''


        else:
            db=Db()
            qry=db.select("select * from ward")
            return render_template('ANGANVADI/add_user.html',data=qry)
    else:
        return redirect('/')


@app.route('/view_user1')
def view_user1():
    if session['oo'] == "lin":
        db = Db()
        qry = db.select("select * from user,anganvadi where user.anganvadi_id=anganvadi.anganvadi_id and user.anganvadi_id='"+str(session['lid'])+"'")
        return render_template('ANGANVADI/view_user.html',data=qry)
    else:
        return redirect('/')

@app.route('/del_user/<id>')
def del_user(id):
    if session['oo'] == "lin":
        db = Db()
        qry = db.delete("delete from user where user_id='"+id+"'")
        qry1 = db.delete("delete from login where login_id='"+id+"'")
        return redirect('/view_user1')
    else:
        return redirect('/')

@app.route('/edt_user/<aid>',methods=['get','post'])
def edt_user(aid):
    if session['oo'] == "lin":
        if request.method=="POST":
            db = Db()
            name = request.form['textfield']
            dob = request.form['textfield2']
            gender = request.form['radio1']
            phonenumber = request.form['textfield3']
            address = request.form['textarea']
            category = request.form['radio']
            email = request.form['textfield5']
            wardno = request.form['select']
            db.update("update `user` set name='"+name+"',dob='"+dob+"',gender='"+gender+"',phone_number='"+phonenumber+"',address='"+address+"',category='"+category+"',email='"+email+"',ward_id='"+wardno+"' where user_id='"+str(aid)+"'")
            # db.update("update `user` set name='"+name+"',dob='"+dob+"',gender='"+gender+"',phone_number='"+phonenumber+"',address='"+address+"',category='"+category+"',Email='"+email+"',ward_number='"+wardno+"' where user_id='"+str(aid)+"'")
            return  '''<script>alert('success');window.location="/view_user1"</script>'''
        else:
            db=Db()
            res=db.selectOne("select * from user,ward,anganvadi where user.ward_id=ward.ward_id and user.anganvadi_id=anganvadi.anganvadi_id and user_id='"+str(aid)+"'")
            res1=db.select("select * from ward ")
            return render_template("ANGANVADI/update_user.html",data=res,data1=res1)
    else:
        return redirect('/')


@app.route('/add_productlist',methods=['GET','POST'])
def add_productlist():
    if session['oo'] == "lin":
        if request.method =="POST":
            a= request.form.getlist('CheckboxGroup1')
            a1=','.join(a)
            b= request.form.getlist('CheckboxGroup2')
            b1 = ','.join(b)
            c= request.form.getlist('CheckboxGroup3')
            c1 = ','.join(c)
            d = request.form.getlist('CheckboxGroup4')
            d1 = ','.join(d)
            e= request.form.getlist('CheckboxGroup5')
            e1 = ','.join(e)
            f = request.form.getlist('CheckboxGroup6')
            f1 = ','.join(f)
            db = Db()
            db.insert("insert into product VALUES ('','"+a1+"','"+b1+"','"+c1+"','"+d1+"','"+e1+"','"+f1+"','"+str(session['lid'])+"')")
            return '''<script>alert('success');window.location="/anganvadi_home"</script>'''
        else:
             return render_template('ANGANVADI/add_productlist.html')
    else:
        return redirect('/')

@app.route('/view_productlist1')
def view_productlist1():
    if session['oo'] == "lin":
        db = Db()
        qry = db.select("select * from product,anganvadi where product.anganvadi_id=anganvadi.anganvadi_id and product.anganvadi_id='"+str(session['lid'])+"'")
        return render_template('ANGANVADI/view_productlist.html',data=qry)
    else:
        return redirect('/')



@app.route('/del_product/<id>')
def del_product(id):
    if session['oo'] == "lin":
        db = Db()
        qry = db.delete("delete from product where product_id='"+id+"'")
        return redirect('/view_productlist1')
    else:
        return redirect('/')



@app.route('/add_service',methods=['GET','POST'])
def add_service():
    if session['oo'] == "lin":
        if request.method == "POST":
            services=request.form.getlist('CheckboxGroup1')
            s=','.join(services)
            meetings=request.form.getlist('CheckboxGroup2')
            m=','.join(meetings)
            date = request.form['textfield']
            time = request.form['textfield2']
            a_place = request.form['textfield3']
            db = Db()
            db.insert("insert into service VALUES('','"+s+"','"+m+"','"+date+"','"+time+"','"+a_place+"','"+str(session['lid'])+"')")
            return '''<script>alert('success');window.location="/anganvadi_home"</script>'''
        else:
            return render_template('ANGANVADI/add_service.html')
    else:
        return redirect('/')

@app.route('/view_services1')
def view_services1():
    if session['oo'] == "lin":
        db = Db()
        qry = db.select("select * from service,anganvadi where service.anganvadi_id=anganvadi.anganvadi_id and service.anganvadi_id='"+str(session['lid'])+"'")
        return render_template('ANGANVADI/view_services.html',data=qry)
    else:
        return redirect('/')


@app.route('/del_service/<id>')
def del_service(id):
    if session['oo'] == "lin":
        db = Db()
        qry = db.delete("delete from service where service_id='"+id+"'")
        return redirect('/view_services1')
    else:
        return redirect('/')



@app.route('/add_record/<id>',methods=['GET','POST'])
def add_record(id):
    if session['oo'] == "lin":
        if request.method=="POST":
            # userid=request.form['select']
            productname=request.form['textfield']
            productamount=request.form['textfield2']
            cltpoduct=request.form['textfield3']
            remproduct=request.form['textfield4']
            db=Db()
            db.insert("insert into record VALUES('','"+id+"','"+productname+"','"+productamount+"','"+cltpoduct+"','"+remproduct+"','"+str(session['lid'])+"')")
            return '''<script>alert('success');window.location="/anganvadi_home"</script>'''
        else:
            db=Db()
            qry = db.select("select * from user")
            return render_template('ANGANVADI/add_record.html',data=qry)
    else:
        return redirect('/')


@app.route('/view_record1')
def view_record1():
    if session['oo'] == "lin":
        db = Db()
        qry = db.select("select * from record,user,anganvadi where record.user_id=user.user_id and record.anganvadi_id=anganvadi.anganvadi_id and record.anganvadi_id='"+str(session['lid'])+"'")
        return render_template('ANGANVADI/view_record.html', data=qry)
    else:
        return redirect('/')



@app.route('/add_notification',methods=['GET','POST'])
def add_notification():
    if session['oo'] == "lin":
        if request.method == "POST":
            notification= request.form['textarea']
            db = Db()
            db.insert("insert into notification VALUES('','" + notification + "',curdate(),'"+str(session['lid'])+"')")
            return '''<script>alert('success');window.location="/anganvadi_home"</script>'''

        # import smtplib
        #
        # s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        #
        # s.starttls()
        #
        # s.login("smartfuddonation@gmail.com", "smart@789")
        #
        # msg = MIMEMultipart()  # create a message.........."
        #
        # msg['From'] = "smartfuddonation@gmail.com"
        #
        # msg['To'] = id
        #
        # msg['Subject'] = "Your Password for Smart Donation Website"
        #
        # body = "Your Password is:- - " + str(pwd)
        #
        # msg.attach(MIMEText(body, 'plain'))
        #
        # s.send_message(msg)
        else:
            return render_template('ANGANVADI/add_notification.html')
    else:
        return redirect('/')

@app.route('/view_notification1')
def view_notification1():
    if session['oo'] == "lin":
        db = Db()
        print(session['lid'])
        qry = db.select("select * from notification,anganvadi where notification.anganvadi_id=anganvadi.anganvadi_id and notification.anganvadi_id='"+str(session['lid'])+"'")
        return render_template('ANGANVADI/view_notification.html', data=qry)
    else:
        return redirect('/')


@app.route('/del_notification/<id>')
def del_notification(id):
    if session['oo'] == "lin":
        db = Db()
        qry = db.delete("delete from notification where notification_id='"+id+"'")
        return redirect('/view_notification1')
    else:
        return redirect('/')



@app.route('/view_feedback1')
def view_feedback1():
    if session['oo'] == "lin":
        db = Db()
        qry = db.select("select * from feedback,user where feedback.user_id=user.user_id")
        return render_template('ANGANVADI/view_feedback.html', data=qry)
    else:
        return redirect('/')

@app.route('/add_birth', methods=['GET', 'POST'])
def add_birth():
    if session['oo'] == "lin":
        if request.method == "POST":
            name = request.form['textfield']
            dob=request.form['textfield2']
            gender=request.form['radio']
            father=request.form['textfield3']
            mother=request.form['textfield4']
            address=request.form['textarea']
            db = Db()
            db.insert("insert into birth VALUES('','"+name+"','"+dob+"','"+gender+"','"+father+"','"+mother+"','"+address+"','"+str(session['lid'])+"')")
            return '''<script>alert('success');window.location="/anganvadi_home"</script>'''
        else:
            return render_template('ANGANVADI/add_birth.html')

    else:
        return redirect('/')

@app.route('/anganvadi_view_birth')
def anganvadi_view_birth():
        if session['oo'] == "lin":
            db = Db()
            qry = db.select("select * from birth,anganvadi where birth.anganvadi_id=anganvadi.anganvadi_id and birth.anganvadi_id='" + str(session['lid']) + "'")
            return render_template('ANGANVADI/view_birth.html', data=qry)
        else:
            return redirect('/')


@app.route('/add_death', methods=['GET', 'POST'])
def add_death():
    if session['oo'] == "lin":
        if request.method == "POST":
            name = request.form['textfield']
            gender = request.form['radio']
            dob=request.form['textfield2']
            address=request.form['textarea']
            dod=request.form['textfield3']
            db = Db()
            db.insert("insert into death VALUES('','"+name+"','"+gender+"','"+dob+"','"+address+"','"+dod+"','"+str(session['lid'])+"')")
            return '''<script>alert('success');window.location="/anganvadi_home"</script>'''
        else:
            return render_template('ANGANVADI/add_death.html')

    else:
        return redirect('/')

@app.route('/ang_view_death')
def ang_view_death():
        if session['oo'] == "lin":
            db = Db()
            qry = db.select("select * from death,anganvadi where death.anganvadi_id=anganvadi.anganvadi_id and death.anganvadi_id='" + str(session['lid']) + "'")
            return render_template('ANGANVADI/view_death.html', data=qry)
        else:
            return redirect('/')

@app.route('/add_attendence/', methods=['GET', 'POST'])
def add_attendence():
    if session['oo'] == "lin":
        if request.method == "POST":
            name = request.form['textfield']
            month=request.form['textfield2']
            prdate = request.form['textfield3']
            abdate=request.form['textfield5']
            db = Db()
            db.insert("insert into attendence VALUES('','" + name + "','" + month + "','" + prdate + "','" + abdate + "','" + str(session['lid']) + "')")
            return '''<script>alert('success');window.location="/anganvadi_home"</script>'''
        else:
            return render_template('ANGANVADI/add_attendence.html')

    else:
        return redirect('/')

@app.route('/ang_view_attendence')
def ang_view_attendence():
        if session['oo'] == "lin":
            db = Db()
            qry = db.select("select * from attendence,anganvadi where attendence.anganvadi_id=anganvadi.anganvadi_id and attendence.anganvadi_id='" + str(session['lid']) + "'")
            return render_template('ANGANVADI/view_attendence.html', data=qry)
        else:
            return redirect('/')


@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if session['oo'] == "lin":
        if request.method == "POST":
            name = request.form['textfield']
            photo=request.files['fileField']
            date = request.form['textfield2']
            d=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            photo.save(path+d+'.jpg')
            p='/static/images/'+d+'.jpg'
            db = Db()
            db.insert("insert into event VALUES('','" + name + "','" + p + "','" + date + "','" + str(session['lid']) + "')")
            return '''<script>alert('success');window.location="/anganvadi_home"</script>'''
        else:
            return render_template('ANGANVADI/add_event.html')

    else:
        return redirect('/')
@app.route('/ang_view_event')
def ang_view_event():
        if session['oo'] == "lin":
            db = Db()
            qry = db.select("select * from event,anganvadi where event.anganvadi_id=anganvadi.anganvadi_id and event.anganvadi_id='" + str(session['lid']) + "'")
            return render_template('ANGANVADI/view_event.html', data=qry)
        else:
            return redirect('/')




#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                ICDS
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@app.route('/ICDS_home')
def ICDS_home():
    if session['oo'] == "lin":
        return render_template('ICDS/index2.html')
    else:
        return redirect('/')


@app.route('/view_anganvadi2')
def view_anganvadi2():
    if session['oo'] == "lin":
        db = Db()
        qry = db.select("select * from anganvadi")
        return render_template('ICDS/view_anganvadi.html',data=qry)
    else:
        return redirect('/')




@app.route('/view_productlist2/<id>')
def view_producctlist2(id):
    if session['oo'] == "lin":
        db = Db()
        qry = db.select("select * from product,anganvadi where product.anganvadi_id=anganvadi.anganvadi_id and product.anganvadi_id='"+str(id)+"'")
        return render_template('ICDS/view_productlist.html',data=qry)
    else:
        return redirect('/')

@app.route('/view_service2/<id>')
def view_service2(id):
    if session['oo'] == "lin":
        db = Db()
        qry = db.select("select * from service,anganvadi where service.anganvadi_id=anganvadi.anganvadi_id and service.anganvadi_id='"+str(id)+"'")
        return render_template('ICDS/view_services.html',data=qry)
    else:
        return redirect('/')


@app.route('/view_user2/<id1>')
def view_user2(id1):
    if session['oo'] == "lin":
        db = Db()
        qry = db.select("select * from user,ward,anganvadi where user.ward_id=ward.ward_id and user.anganvadi_id=anganvadi.anganvadi_id and user.anganvadi_id='"+str(id1)+"'")
        return render_template('ICDS/view_user.html',data=qry)
    else:
        return redirect('/')




@app.route('/view_record2/<id>')
def view_record2(id):
    if session['oo'] == "lin":
        db=Db()
        qry = db.select("select * from record,user,anganvadi where record.user_id=user.user_id and record.anganvadi_id=anganvadi.anganvadi_id and record.anganvadi_id='" + str(id) + "'")
        return render_template('ICDS/view_record.html',data=qry)
    else:
        return redirect('/')

@app.route('/view_feedback2')
def view_feedback2():
    if session['oo'] == "lin":
        db = Db()
        qry = db.select("select * from feedback,user where feedback.user_id=user.user_id")
        return render_template('ICDS/view_feedback.html', data=qry)
    else:
        return redirect('/')


@app.route('/view_birth3')
def view_birth3():
        if session['oo'] == "lin":
            db = Db()
            qry = db.select("select * from birth")
            return render_template('ICDS/view_birth.html', data=qry)
        else:
            return redirect('/')
@app.route('/view_death3')
def view_death3():
        if session['oo'] == "lin":
            db = Db()
            qry = db.select("select * from death")
            return render_template('ICDS/view_death.html', data=qry)
        else:
            return redirect('/')


@app.route('/view_attendence3/<cid>')
def view_attendence3(cid):
        if session['oo'] == "lin":
            db = Db()
            # qry = db.select("select * from attendence")
            # return render_template('ICDS/view_attendence.html', data=qry)
            qry = db.select("select * from attendence,anganvadi where attendence.anganvadi_id=anganvadi.anganvadi_id and attendence.anganvadi_id='" + str(cid) + "'")
            return render_template('ICDS/view_attendence.html', data=qry)
        else:
            return redirect('/')



@app.route('/view_event3')
def view_event3():
        if session['oo'] == "lin":
            db = Db()
            qry = db.select("select * from event")
            return render_template('ICDS/view_event.html', data=qry)
        else:
            return redirect('/')



#---------------------------------------------------------------------------------------------------------------------------
#                                      USER
#---------------------------------------------------------------------------------------------------------------------------


@app.route('/user_home')
def user_home():
    if session['oo'] == "lin":
        return render_template('USER/index3.html')
    else:
        return redirect('/')

@app.route('/view_profile')
def view_profile():
    if session['oo'] == "lin":
        db=Db()
        uid = session['lid']
        qry = db.selectOne("select * from user where user_id='"+str(session['lid'])+"'"  )
        return render_template('USER/view_profile.html', data=qry)
    else:
        return redirect('/')

@app.route('/update_profile/<a>',methods=['get','post'])
def update_profile(a):
    if session['oo'] == "lin":
        if request.method=="POST":
            db = Db()
            name = request.form['textfield']
            dob = request.form['textfield2']
            gender = request.form['radio1']
            phonenumber = request.form['textfield3']
            address = request.form['textarea']
            category = request.form['radio']
            email = request.form['textfield5']
            wardno = request.form['select']
            db.update("update user set name='"+name+"',dob='"+dob+"',gender='"+gender+"',phone_number='"+phonenumber+"',address='"+address+"',category='"+category+"',email='"+email+"',ward_id='"+wardno+"' where user_id='"+str(a)+"'")
            # db.update("update `user` set name='"+name+"',dob='"+dob+"',gender='"+gender+"',phone_number='"+phonenumber+"',address='"+address+"',category='"+category+"',Email='"+email+"',ward_number='"+wardno+"' where user_id='"+str(aid)+"'")
            return  '''<script>alert('success');window.location="/view_profile"</script>'''
        else:
            db=Db()
            res=db.selectOne("select * from user,ward,anganvadi where user.ward_id=ward.ward_id and user.anganvadi_id=anganvadi.anganvadi_id and user_id='"+str(a)+"'")
            res1=db.select("select * from ward ")
            return render_template("USER/update_profile.html",data=res,data1=res1)
    else:
        return redirect('/')




@app.route('/view_productlist3')
def view_productlist3():
    if session['oo'] == "lin":
        db = Db()
        qry = db.select("select * from product,user where product.anganvadi_id=user.anganvadi_id and user.user_id='"+str(session['lid'])+"'")
        return render_template('USER/view_productlist.html',data=qry)
    else:
        return redirect('/')


@app.route('/view_service3')
def view_service3():
    if session['oo'] == "lin":
        db = Db()
        qry = db.select("select * from service,user where service.anganvadi_id=user.anganvadi_id and user.user_id='"+str(session['lid'])+"'")
        return render_template('USER/view_services.html',data=qry)
    else:
        return redirect('/')


@app.route('/view_notification3')
def view_notification3():
    if session['oo'] == "lin":
        db = Db()
        qry = db.select("select * from notification,user where notification.anganvadi_id=user.anganvadi_id and user.user_id='"+str(session['lid'])+"'")
        return render_template('USER/view_notification.html', data=qry)
    else:
        return redirect('/')


@app.route('/send_feedback',methods=['GET','POST'])
def send_feedback():
    if session['oo'] == "lin":
        if request.method == "POST":
            feedback= request.form['textarea']
            db = Db()
            db.insert("insert into feedback VALUES('','"+str(session['lid'])+"','"+ feedback + "',curdate())")
            return '''<script>alert('success');window.location="/user_home"</script>'''
        else:
            return render_template('USER/feedback.html')
    else:
        return redirect('/')



@app.route('/view_feedback3')
def view_feedback3():
    if session['oo'] == "lin":
        db = Db()
        qry = db.select("select * from feedback,user where feedback.user_id=user.user_id")
        return render_template('USER/view_feedback.html', data=qry)
    else:
        return redirect('/')



@app.route('/send_doubt',methods=['GET','POST'])
def send_doubt():
    if session['oo'] == "lin":
        if request.method == "POST":
            doubt= request.form['textarea']
            db = Db()
            db.insert("insert into doubt VALUES('','"+str(session['lid'])+"','"+ doubt + "',curdate(),'pending','')")
            return '''<script>alert('success');window.location="/user_home"</script>'''
        else:
            return render_template('USER/doubt.html')
    else:
         return redirect('/')

#
# @app.route('/view_doubt3')
# def view_doubt3():
#     db = Db()
#     qry = db.select("select * from doubt,user where doubt.user_id=user.user_id")
#     return render_template('USER/view_doubt.html',data=qry)

@app.route('/view_reply3')
def view_reply3():
    if session['oo'] == "lin":
        db = Db()
        qry = db.select("select * from doubt,user where doubt.user_id=user.user_id ")
        return render_template('USER/view_reply.html',data=qry)
    else:
        return redirect('/')


@app.route('/view_event4')
def view_event4():
        if session['oo'] == "lin":
            db = Db()
            qry = db.select("select * from event,anganvadi,user where event.anganvadi_id=anganvadi.anganvadi_id and user.anganvadi_id=anganvadi.anganvadi_id and user.user_id='"+str(session['lid'])+"'")
            return render_template('USER/view_event.html', data=qry)
        else:
            return redirect('/')

if __name__ == '__main__':
    app.run(port=4000)
















