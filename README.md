# AI-powered-proctoring-system     

# import smtplib
#
# from django.core.files.storage import FileSystemStorage
# from django.http import HttpResponse, JsonResponse
import smtplib

import datetime
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# from numpy import np

# from.models import *
# Create your views here.
from Myapp.models import *


def admin_home(request):
    return render(request,"admin/homeindex.html")

def login_get(request):
    return render(request,'login_index.html')


def login_post(request):
    Username = request.POST["textfield"]
    Password = request.POST["textfield2"]

    lobj=Login.objects.filter(username=Username,password=Password)
    if lobj.exists():
        log1=Login.objects.get(username=Username, password=Password)
        request.session['lid']=log1.id
        if log1.type=='admin':
            return HttpResponse('''<script>alert('login success');window.location='/Myapp/admin_home/'</script>''')
        elif log1.type=='teacher':
            return HttpResponse('''<script>alert('login success');window.location='/Myapp/teacher_home/'</script>''')
        else:
            return HttpResponse(
                '''<script>alert('There is no such user');window.location='/Myapp/login_get/'</script>''')

            # return HttpResponse('''<script>alert('login success');window.location='/Myapp/student_home/'</script>''')
    return HttpResponse('''<script>alert('There is no such user');window.location='/Myapp/login_get/'</script>''')

def logout(request):
    request.session['lid']=""
    return redirect('/Myapp/login_get/')

def add_teacher_get(request):
    from datetime import datetime, timedelta
    date = datetime.now().today()
    # Calculate the minimum date for 18 years ago
    min_date = date - timedelta(days=365 * 18)
    dd = min_date - timedelta(days=5)

    # Format the date to display
    min_date_str = dd.strftime('%Y-%m-%d')
    print(min_date_str)
    return render(request,'admin/Add teacher.html',{'date':min_date_str})

def email_exist(request):
    email = request.POST['email']
    status = Login.objects.filter(username = email).exists()
    return JsonResponse({'status':status})

def add_teacher_post(request):
    Name= request.POST["textfield"]
    Gender= request.POST["RadioGroup1"]
    DOB= request.POST["textfield2"]
    Phone= request.POST["textfield3"]
    Email= request.POST["textfield4"]
    Place= request.POST["textfield5"]
    Post= request.POST["textfield6"]
    Pin= request.POST["textfield7"]
    Qualification= request.POST["textfield8"]
    Experience= request.POST["textfield9"]
    Photo= request.FILES["fileField"]
    from datetime import datetime
    date=datetime.now().strftime("%Y%m%d-%H%M%S")+".jpg"
    fs=FileSystemStorage()
    fs.save(date,Photo)
    path=fs.url(date)
    District=request.POST["textfield10"]
    logj=Login()
    logj.username=Email
    import random
    passw=random.randint(0000,9999)
    logj.password=str(passw)
    logj.type='teacher'
    logj.save()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("safedore3@gmail.com", "yqqlwlyqbfjtewam")
    # App Password
    to = Email
    subject = "Human Activity Recognition Portal - Login Information"
    body = f"""
            Welcome to the Human Activity Recognition Portal.

            Your login details are as follows:
            Username: {Email}
            Password: {passw}

            Please log in and update your password after the first login.
            """
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail("s@gmail.com", to, msg)
    # Disconnect from the server
    server.quit()

    tobj=Teacher()
    tobj.name=Name
    tobj.email=Email
    tobj.phone=Phone
    tobj.dob=DOB
    tobj.gender=Gender
    tobj.experience=Experience
    tobj.qualification=Qualification
    tobj.place=Place
    tobj.post=Post
    tobj.pincode=Pin
    tobj.district=District
    tobj.photo=path
    tobj.LOGIN=logj
    tobj.save()
    return HttpResponse('''<script>alert('Added..Sucessfully...');window.location='/Myapp/add_teacher_get/'</script>''')




def Change_password_get(request):
    return render(request,'admin/Change password.html')

def Change_password_post(request):
    Current_password=request.POST["textfield"]
    New_password=request.POST["textfield2"]
    Confirm_password=request.POST["textfield3"]
    id=request.session['lid']
    chp=Login.objects.get(id=id)
    if chp.password ==Current_password:
        if New_password==Confirm_password:
            Login.objects.filter(id=id).update(password=New_password)
            return HttpResponse('''<script>alert('Changed password successfully');window.location='/Myapp/login_get/'</script>''')
        else:
            return HttpResponse('''<script>alert('Password does not match');window.location='/Myapp/Change_password_get/'</script>''')
    else:
        return HttpResponse( '''<script>alert('You must login first');window.location='/Myapp/login_get/'</script>''')



def Edit_teacher_get(request,id):
    re=Teacher.objects.get(LOGIN_id=id)
    from datetime import datetime,timedelta
    date = datetime.now().today()

    min_date = date - timedelta(days=365 * 18)
    dd = min_date - timedelta(days=5)

    # Format the date to display
    min_date_str = dd.strftime('%Y-%m-%d')
    return render(request,'admin/Edit teacher.html',{'data':re,'date':min_date_str})

def Edit_teacher_post(request):
    id=request.POST['id']
    Name=request.POST["textfield"]
    Gender=request.POST["RadioGroup1"]
    DOB=request.POST["textfield2"]
    Phone=request.POST["textfield3"]
    Email=request.POST["textfield4"]
    Place=request.POST["textfield5"]
    post=request.POST["textfield6"]
    pin=request.POST["textfield7"]
    Qualification=request.POST["textfield8"]
    District=request.POST["textfield10"]
    Experience=request.POST["textfield9"]
    logj = Login.objects.get(id=id)
    logj.username = Email
    logj.save()

    tobj = Teacher.objects.get(LOGIN_id=id)
    if 'fileField' in request.FILES:
        Photo = request.FILES["fileField"]
        if Photo !="":
            from datetime import datetime
            date = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
            fs = FileSystemStorage()
            fs.save(date, Photo)
            path = fs.url(date)
            tobj.photo = path

    tobj.name = Name
    tobj.email = Email
    tobj.phone = Phone
    tobj.dob = DOB
    tobj.gender = Gender
    tobj.experience = Experience
    tobj.qualification = Qualification
    tobj.place = Place
    tobj.post = post
    tobj.pincode = pin
    tobj.district = District
    tobj.LOGIN = logj
    tobj.save()
    return HttpResponse('''<script>alert('Updated..Sucessfully...');window.location='/Myapp/View_teacher_get/'</script>''')

def delete_teacher(request,id):
    Teacher.objects.filter(LOGIN_id=id).delete()
    Login.objects.filter(id=id).delete()
    return redirect('/Myapp/View_teacher_get/')

def Send_reply_get(request,id):
    return render(request,'admin/Send reply.html',{'id':id})

def Send_reply_post(request):
    Reply=request.POST["textarea"]
    id=request.POST['id']
    Complaint.objects.filter(id=id).update(reply=Reply,status='Replied')
    return HttpResponse('''<script>alert('Replied..Sucessfully...');window.location='/Myapp/View_complaints_get/'</script>''')


def View_complaints_get(request):
    re=Complaint.objects.all()
    return render(request,'admin/View complaints.html',{'data':re})

def View_complaints_post(request):
    From=request.POST["textfield"]
    To = request.POST["textfield2"]
    re = Complaint.objects.filter(date__range=[From,To])
    return render(request, 'admin/View complaints.html', {'data': re})


def View_feedback_get(request):
    re=Feedback.objects.all()
    return render(request,'admin/View feedback.html',{'data':re})

def View_feedback_post(request):
    From=request.POST["Textfield"]
    To=request.POST["Textfield2"]
    re = Feedback.objects.filter(date__range=[From,To])
    return render(request, 'admin/View feedback.html', {'data': re})


def View_mark_get(request):
    re=Mark.objects.all()
    return render(request,'admin/View mark.html',{'data':re})

def View_mark_post(request):
    From=request.POST["Textfield"]
    To=request.POST["Textfield2"]
    return HttpResponse('ok')





def view_student_get(request):
    re=Student.objects.all()
    return render(request,'admin/view student.html',{'data':re})
def view_student_post(request):
    search=request.POST["textfield"]
    re = Student.objects.filter(name__icontains=search)
    return render(request, 'admin/view student.html', {'data': re})


def View_teacher_get(request):
    re=Teacher.objects.all()
    return render(request,'admin/View teacher.html',{'data':re})

def view_teacher_post(request):
    search=request.POST["textfield"]
    re = Teacher.objects.filter(name__icontains=search)
    return render(request, 'admin/View teacher.html', {'data': re})


#========================


def student_home(request):
    return render(request,"student/Student Home.html")

def st_view_profile(request):
    re=Student.objects.get(LOGIN_id=request.session['lid'])
    return render(request,'student/view profile.html',{'data':re})

def send_complaint_get(request):
    return render(request,'student/send complaint.html')

def send_complaint_post(request):
    Send_complaint=request.POST["textarea"]
    from datetime import datetime
    date = datetime.now().today()
    cc = Student.objects.get(LOGIN_id=request.session['lid'])
    cobj = Complaint()
    cobj.STUDENT = cc
    cobj.complaint = Send_complaint
    cobj.date = date
    cobj.status = 'pending'
    cobj.reply = 'pending'
    cobj.save()
    return HttpResponse(
        '''<script> alert('Complaint Added..');window.location="/Myapp/send_complaint_get/"</script>''')


def send_feedback_get(request):
    return render(request,'student/send feedback.html')

def send_feedback_post(request):
    Send_Feedback=request.POST["textarea"]
    from datetime import datetime
    date = datetime.now().today()
    cc = Student.objects.get(LOGIN_id=request.session['lid'])
    cobj = Feedback()
    cobj.STUDENT = cc
    cobj.feedback = Send_Feedback
    cobj.date = date
    cobj.save()
    return HttpResponse(
        '''<script> alert('Feedback Added..');window.location="/Myapp/send_feedback_get/"</script>''')


def view_exam_historyt_get(request):
    return render(request,'student/view exam history.html')

def view_exam_historyt_post(request):
    Send_Feedback=request.POST["textarea"]

def student_view_profile_get(request):
    return render(request,'student/view profile.html')

def student_view_profile_post(request):
    return render(request,'student/view profile.html')




def view_reply_get(request):
    re=Complaint.objects.filter(STUDENT__LOGIN_id=request.session['lid'])
    return render(request,'student/view reply.html',{'data':re})
def view_reply_post(request):
    fd=request.POST['textfield']
    td=request.POST['textfield2']
    re = Complaint.objects.filter(STUDENT__LOGIN_id=request.session['lid'],date__range=[fd,td])
    return render(request, 'student/view reply.html', {'data': re})

def st_change_password_get(request):
    return render(request,'student/change password.html')

def st_Change_password_post(request):
    Current_password = request.POST["textfield"]
    New_password = request.POST["textfield2"]
    Confirm_password = request.POST["textfield3"]
    id = request.session['lid']
    chp = Login.objects.get(id=id)
    if chp.password == Current_password:
        if New_password == Confirm_password:
            Login.objects.filter(id=id).update(password=New_password)
            return HttpResponse(
                '''<script>alert('Changed password successfully');window.location='/Myapp/login_get/'</script>''')
        else:
            return HttpResponse(
                '''<script>alert('Password does not match');window.location='/Myapp/st_change_password_get/'</script>''')
    else:
        return HttpResponse('''<script>alert('You must login first');window.location='/Myapp/login_get/'</script>''')


#=========================
def teacher_home(request):
    from datetime import datetime
    date=datetime.now().today()
    re=Exam.objects.filter(exam_date__gte=date)

    # mm=Mark.objects.all().order_by('mark')
    return render(request,"teacher/new_homeindex.html",{'data':re})

# def add_question_get(request):
#
#     return render(request,'teacher/add question.html')
#
# def add_question_post(request):
#     Question=request.POST["textarea"]

def Add_student_get(request):
    return render(request,'teacher/Add student.html')

def Add_student_post(request):
    name=request.POST["textfield"]
    Gender=request.POST["RadioGroup1"]
    DOB=request.POST["textfield4"]
    Email=request.POST["textfield2"]
    Phone=request.POST["textfield3"]
    Places=request.POST["textfield5"]
    Post=request.POST["textfield6"]
    pincode=request.POST["textfield7"]
    District=request.POST["textfield8"]
    Photo=request.FILES["fileField"]
    from datetime import datetime
    date = 'student/'+datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
    fs = FileSystemStorage()
    fs.save(date, Photo)
    path = fs.url(date)
    logj = Login()
    logj.username = Email
    import random
    passw = random.randint(0000, 9999)
    logj.password = str(passw)
    logj.type = 'student'
    logj.save()

    # server = smtplib.SMTP('smtp.gmail.com', 587)
    # server.starttls()
    # server.login("safedore3@gmail.com", "yqqlwlyqbfjtewam")
    # # App Password
    # to = Email
    # subject = "Human Activity Recognition Portal - Login Information"
    # body = f"""
    #             Welcome to the Human Activity Recognition Portal.
    #
    #             Your login details are as follows:
    #             Username: {Email}
    #             Password: {passw}
    #
    #             Please log in and update your password after the first login.
    #             """
    # msg = f"Subject: {subject}\n\n{body}"
    # server.sendmail("s@gmail.com", to, msg)
    # # Disconnect from the server
    # server.quit()

    tobj = Student()
    tobj.name = name
    tobj.email = Email
    tobj.phone = Phone
    tobj.dob = DOB
    tobj.gender = Gender
    tobj.place = Places
    tobj.post = Post
    tobj.pincode = pincode
    tobj.district = District
    tobj.photo = path
    tobj.LOGIN = logj
    tobj.save()
    return HttpResponse('''<script>alert('Added..Sucessfully...');window.location='/Myapp/Add_student_get/'</script>''')

def teacher_view_student(request):
    re=Student.objects.all()
    return render(request,'teacher/view student.html',{'data':re})

def teacher_view_student_post(request):
    s=request.POST['textfield']
    re=Student.objects.filter(name__icontains=s)
    return render(request,'teacher/view student.html',{'data':re})

def t_edit_student(request,id):
    re=Student.objects.get(LOGIN_id=id)
    return render(request,'teacher/edit student.html',{'data':re})

def t_edit_student_post(request):
    id=request.POST['id']
    name = request.POST["textfield"]
    Gender = request.POST["RadioGroup1"]
    DOB = request.POST["textfield4"]
    Email = request.POST["textfield2"]
    Phone = request.POST["textfield3"]
    Places = request.POST["textfield5"]
    Post = request.POST["textfield6"]
    pincode = request.POST["textfield7"]
    District = request.POST["textfield8"]

    logj = Login.objects.get(id=id)
    logj.username = Email
    logj.save()

    tobj = Student.objects.get(LOGIN_id=id)
    if 'fileField' in request.FILES:
        Photo = request.FILES["fileField"]
        if Photo !="":
            from datetime import datetime
            date = "student/"+datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
            fs = FileSystemStorage()
            fs.save(date, Photo)
            path = fs.url(date)
            tobj.photo = path

    tobj.name = name
    tobj.email = Email
    tobj.phone = Phone
    tobj.dob = DOB
    tobj.gender = Gender
    tobj.place = Places
    tobj.post = Post
    tobj.pincode = pincode
    tobj.district = District
    tobj.save()
    return HttpResponse('''<script>alert('Updated..Sucessfully...');window.location='/Myapp/teacher_view_student/'</script>''')

def delete_student(request,id):
    Student.objects.filter(LOGIN_id=id).delete()
    Login.objects.filter(id=id).delete()
    return redirect('/Myapp/teacher_view_student/')



def teach_change_password_get(request):
    return render(request,'teacher/change password.html')

def teach_Change_password_post(request):
    Current_password = request.POST["textfield"]
    New_password = request.POST["textfield2"]
    Confirm_password = request.POST["textfield3"]
    id = request.session['lid']
    chp = Login.objects.get(id=id)
    if chp.password == Current_password:
        if New_password == Confirm_password:
            Login.objects.filter(id=id).update(password=New_password)
            return HttpResponse(
                '''<script>alert('Changed password successfully');window.location='/Myapp/login_get/'</script>''')
        else:
            return HttpResponse(
                '''<script>alert('Password does not match');window.location='/Myapp/teach_change_password_get/'</script>''')
    else:
        return HttpResponse('''<script>alert('You must login first');window.location='/Myapp/login_get/'</script>''')






def edit_profile_get(request):
    return render(request,'teacher/edit profile.html')

def edit_profile_post(request):
    Name=request.POST["textfield"]
    Gender=request.POST["RadioGroup1"]
    DOB=request.POST["textfield2"]
    Phone=request.POST["textfield3"]
    Email=request.POST["textfield4"]
    Place=request.POST["textfield5"]
    Post=request.POST["textfield6"]
    Pin=request.POST["textfield7"]
    Qualification=request.POST["textfield8"]
    Experience=request.POST["textfield9"]
    Photo=request.POST["FileField"]
    return HttpResponse()




def conduct_exam_get(request):
    from datetime import datetime
    date = datetime.now().today()
    return render(request,'teacher/conduct exam.html',{'date':date})

def conduct_exam_post(request):
    Exam_Name=request.POST["textfield"]
    Exam_Date=request.POST["textfield2"]
    From_Time=request.POST["textfield3"]
    To_Time=request.POST["textfield4"]
    e=Exam()
    e.date=datetime.datetime.now().today()
    e.exam_date=Exam_Date
    e.exam_name=Exam_Name
    e.from_time=From_Time
    e.to_time=To_Time
    e.status='pending'
    e.save()

    return HttpResponse('''<script>alert('Exam Added..');window.location='/Myapp/conduct_exam_get/'</script>''')


def t_view_exam(request):
    from datetime import datetime
    today = datetime.now().today()
    re=Exam.objects.all()
    return render(request,'teacher/view_exam.html',{'data':re})


def t_view_emotion(request,id):
    angry=student_emotion.objects.filter(Exam_id=id,emotion="Angry").count()
    disgus=student_emotion.objects.filter(Exam_id=id,emotion="Disgusted").count()
    fear=student_emotion.objects.filter(Exam_id=id,emotion="Fearful").count()
    happy=student_emotion.objects.filter(Exam_id=id,emotion="Happy").count()
    nue=student_emotion.objects.filter(Exam_id=id,emotion="Neutral").count()
    sad=student_emotion.objects.filter(Exam_id=id,emotion="Sad").count()
    sur=student_emotion.objects.filter(Exam_id=id,emotion="Surprised").count()
    not_stress=happy+nue+sur
    stress=angry+disgus+fear+sad
    print(fear,"fffffffff")
    return render(request,'teacher/pie_chart.html',{'stress':stress,'not_stress':not_stress})
    # return render(request,'teacher/pie_chart.html',{'angry':angry,'disgus':disgus,'fear':fear,'happy':happy,'nue':nue,'sad':sad,'sur':sur})



def t_view_attendance(request,id):
    data=student_attendance.objects.filter(EXAM_id=id)
    return render(request,'teacher/View Attendance.html',{'data':data})


def t_edit_exam(request,id):
    from datetime import datetime
    today = datetime.now().today()  # Get today's date
    re = Exam.objects.get(id=id)
    return render(request,'teacher/edit exam.html',{'data':re,'date':today})

def t_edit_exam_post(request):
    id=request.POST['id']
    Exam_Name = request.POST["textfield"]
    Exam_Date = request.POST["textfield2"]
    From_Time = request.POST["textfield3"]
    To_Time = request.POST["textfield4"]
    e = Exam.objects.get(id=id)
    e.date = datetime.datetime.now().today()
    e.exam_date = Exam_Date
    e.exam_name = Exam_Name
    e.from_time = From_Time
    e.to_time = To_Time
    e.save()

    return HttpResponse('''<script>alert('Exam Updated..');window.location='/Myapp/t_view_exam/'</script>''')

def t_delete_exam(request,id):
    Exam.objects.filter(id=id).delete()
    return redirect('/Myapp/t_view_exam/')

def add_question(request,id):
    request.session['exid']=id
    return render(request,'teacher/add question.html',{'id':id})

def add_question_post(request):
    id=request.POST['id']
    qstn=request.POST['textarea']
    opn1=request.POST['1']
    opn2=request.POST['2']
    opn3=request.POST['3']
    opn4=request.POST['4']
    ansr=request.POST['ans']
    aa=Question()
    aa.EXAM_id=id
    aa.question=qstn
    aa.option1=opn1
    aa.option2=opn2
    aa.option3=opn3
    aa.option4=opn4
    aa.answer=ansr
    aa.save()
    return HttpResponse(f'''<script>alert('Question Added..');window.location='/Myapp/add_question/{id}'</script>''')


def view_questions_get(request,eid):
    re=Question.objects.filter(EXAM_id=eid)
    request.session['exid']=eid
    return render(request,'teacher/view questions.html',{'data':re})
def view_questions_post(request):
    return render(request,'teacher/view questions.html')

def edit_question(request,qid):
    re=Question.objects.get(id=qid)
    return render(request,'teacher/edit question.html',{'data':re})

def edit_question_post(request):
    id=request.POST['id']
    qstn = request.POST['textarea']
    opn1 = request.POST['1']
    opn2 = request.POST['2']
    opn3 = request.POST['3']
    opn4 = request.POST['4']
    ansr = request.POST['ans']
    aa = Question.objects.get(id=id)
    aa.question = qstn
    aa.option1 = opn1
    aa.option2 = opn2
    aa.option3 = opn3
    aa.option4 = opn4
    aa.answer = ansr
    aa.save()
    return HttpResponse(f'''<script>alert('Question Updated..');window.location='/Myapp/view_questions_get/{id}'</script>''')


def delete_question(request,id):
    re=Question.objects.filter(id=id).delete()
    return redirect('/Myapp/view_questions_get/{id}')

def teacher_view_profile_get(request):
    re=Teacher.objects.get(LOGIN_id=request.session['lid'])
    return render(request,'teacher/view profile.html',{'data':re})


def teacher_View_mark_get(request,id):
    re=Mark.objects.filter(EXAM_id=id)
    return render(request,'teacher/View mark.html',{'data':re})

def teacher_View_mark_get_post(request):
    From=request.POST["Textfield"]
    To=request.POST["Textfield2"]
    re = Mark.objects.filter(date__range=[From,To])
    return render(request, 'admin/View mark.html', {'data': re})


#============Android====================================
def and_login(request):
    username = request.POST['username']
    password = request.POST['passwprd']
    re=Login.objects.filter(username=username,password=password)
    if re.exists():
        ree = Login.objects.get(username=username, password=password)
        ss=Student.objects.get(LOGIN_id=ree.id)


        if ree.type=='student':
            return JsonResponse({'status':'ok', 'lid':ree.id, 'type':ree.type,'email':ree.username,'photo':str(ss.photo),"name":ss.name})
        else:
            return JsonResponse({'status':'no'})
    else:
        return JsonResponse({'status':'noo'})


def and_view_profile(request):
    lid=request.POST['lid']
    re=Student.objects.get(LOGIN_id=lid)
    return JsonResponse({'status':'ok','name':re.name,'email':re.email,'phone':re.phone,'photo':re.photo,'place':re.place,'dob':re.dob})

def and_view_exam(request):
    from datetime import datetime
    date=datetime.now().today()
    # current_time = datetime.now().strftime('%H:%M')
    re=Exam.objects.filter(exam_date__gte=date)
    l=[]
    for i in re:
        l.append({
            'id':i.id,
            'edate':i.exam_date,
            'ename':i.exam_name,
            'ftime':i.from_time,
            'ttime':i.to_time,

        })
    return JsonResponse({'status':'ok','data':l})


def and_view_question(request):
    eid=request.POST['eid']
    print(eid,"sdfghjk")
    re=Question.objects.filter(EXAM_id=eid).order_by('?')
    l=[]
    for i in re:
        l.append({
            'id':i.id,
            'question':i.question,
            'option1':i.option1,
            'option2':i.option2,
            'option3':i.option3,
            'option4':i.option4,
            'exm':i.EXAM.id,
            'answer':i.answer

        })
    return JsonResponse({'status':"ok",'data':l})

def attendexam(request):
    lid=request.POST['lid']
    mark=request.POST['mark']
    eid=request.POST['eid']
    re=Mark.objects.filter(EXAM_id=eid,STUDENT__LOGIN_id=lid)
    if re.exists():
        return JsonResponse({'status': "no"})
    else:
        mm=Mark()
        from datetime import datetime
        mm.date=datetime.now().today()
        mm.EXAM_id=eid
        mm.STUDENT=Student.objects.get(LOGIN_id=lid)
        mm.mark=mark
        mm.save()
        return JsonResponse({'status':"ok"})


def face_checking(request):
    lid = request.POST['lid']
    eid = request.POST['examid']
    count = request.POST['count']
    pic=request.FILES['pic']
    from datetime import datetime

    import face_recognition

    p = "D:\\HumanActivityRecognition\\media\\"
    from datetime import datetime
    datee=datetime.now().strftime("%Y%m%d-%H%M%S")+".jpg"

    # import base64
    # a=base64.b64decode(pic)
    # fh=open("D:\\HumanActivityRecognition\\media\\"+datee+".jpg","wb")
    # path="/media/"+datee+".jpg"
    # fh.write(a)
    # fh.close()
    #

    # s = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"

    # pic.save("D:\\HumanActivityRecognition\\media\\a.jpg")
    # pic.save(p + s)

    # path = "/media/" + s
    data = Student.objects.get(LOGIN_id=lid)
    fs = FileSystemStorage()
    fs.save(datee,pic)
    path=fs.url(datee)

    # qry = "SELECT * FROM `student` WHERE `student_lid`='" + l_id + "'"
    # data = db.selectOne(qry)
    print(data.photo)
    picture_of_me = face_recognition.load_image_file("D:\\HumanActivityRecognition" + data.photo)
    # picture_of_me = face_recognition.load_image_file("C:\\Users\\ayisha\\PycharmProjects\\PROCTOR" + data.photo)

    try:
        import cv2

        print("face inside")
        my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]
        lndmrk = my_face_encoding
        # else:


        unknown_picture = face_recognition.load_image_file(p + datee)
        # print(unknown_picture)
        unknown_face_encoding = face_recognition.face_encodings(unknown_picture)
        oo = ""
        print(len(unknown_face_encoding))
        totalpersons = len(unknown_face_encoding)


        if totalpersons > 1:
            qry = Procturingactivity()
            qry.STUDENT = Student.objects.get(LOGIN_id=lid)
            qry.EXAM = Exam.objects.get(id=eid)
            qry.activityname = str(totalpersons)+" Detected"
            qry.date = datetime.now().today()
            qry.type = 'Muliple Face'
            qry.photo = path
            qry.save()

            # qry = "INSERT INTO `procturingactivity` (`stlid`,`examid`,`activityname`,`date`,`type`,`photo`) VALUES ('" + l_id + "','" + examid + "','" + str(
            #     totalpersons) + " Present in screen',CURDATE(),'Person Count','" + path + "')"
            # db = Db()
            # db.insert(qry)

        c = 0
        for s in range(0, len(unknown_face_encoding)):
            results = face_recognition.compare_faces([lndmrk], unknown_face_encoding[s], tolerance=.5)
            print("r2")
            for i in results:
                if i == True:
                    oo = "yes"
                    c = c + 1
                    break
            print(results)

        if c == 1:
            print("r3")
            print("oooo")
            # c=len()
            return JsonResponse({"status": "ok", "count": len(unknown_face_encoding)})
        else:
            print("r4")
            print("hooo")
            qry = Procturingactivity()
            qry.STUDENT = Student.objects.get(LOGIN_id=lid)
            qry.EXAM = Exam.objects.get(id=eid)
            qry.activityname = "Invalid person"
            qry.date = datetime.now().today()
            qry.type = 'FaceRecognition'
            qry.photo = path
            qry.save()
            # qry = "INSERT INTO `procturingactivity` (`stlid`,`examid`,`activityname`,`date`,`type`,`photo`) VALUES ('" + l_id + "','" + examid + "','Invalid person',CURDATE(),'FaceRecognition','" + path + "')"
            # db = Db()
            # db.insert(qry)
            return JsonResponse({"status": 'no'})
    except:
        return JsonResponse({"status": 'no'})


def attend_exam(request):
    import face_recognition

    import cv2
    l_id = request.form["lid"]
    pic = request.files["pic"]
    examid = request.form["examid"]
    count = request.form["count"]

    from datetime import datetime
    date=datetime.now().today()

    print(pic, "jghhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh", "count", count)

    students=Student.objects.all()

    for student in students:
        image_path = f"C:\\Users\\amaya\\PycharmProjects\\HumanActivityRecognition{student['photo']}"
        try:
            picture_of_me = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(picture_of_me)
            if face_encodings:
                my_face_encoding = face_encodings[0]
                self.known_images.append(my_face_encoding)
                self.known_ids.append(student['id'])
                self.student_details.append(student)
        except Exception as e:
            print(f"Error loading image for {student['name']}: {e}")

    p = "D:\\HumanActivityRecognition\\Myapp\\static\\check\\"
    from datetime import datetime

    import base64

    s = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"

    pic.save("D:\\HumanActivityRecognition\\Myapp\\static\\a.jpg")
    # pic.save(p + s)

    path = "/static/check/" + s

    if int(count) > 1:
        qry=Procturingactivity()
        qry.STUDENT=Student.objects.get(LOGIN_id=l_id)
        qry.EXAM=Exam.objects.get(id=examid)
        qry.activityname="Present in screen"
        qry.date=date
        qry.type='Person Count'
        qry.photo=path
        qry.save()

        # qry = "INSERT INTO `procturingactivity` (`stlid`,`activityname`,`date`,`type`,`photo`) VALUES ('" + l_id + "','" + examid + "','" + str(
        #     count) + " Present in screen',CURDATE(),'Person Count','" + path + "')"
        # db = Db()
        # db.insert(qry)

    #####################HEAD POSE ESTIMATION

    # image = cv2.imread(p+s)
    image = cv2.imread("D:\\HumanActivityRecognition\\Myapp\\static\\a.jpg")
    cv2.imwrite(p + s, image)

    print(p + s, "========================================")

    # Flip the image horizontally for a later selfie-view display
    # Also convert the color space from BGR to RGB
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    # To improve performance
    image.flags.writeable = False

    # Get the results
    results = face_mesh.process(image)

    print(results)

    # To improve performance
    image.flags.writeable = True

    # Convert the color space from RGB to BGR
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    img_h, img_w, img_c = image.shape
    face_3d = []
    face_2d = []
    import yolo
    print(p + s)

    dob = yolo.check("D:\\HumanActivityRecognition\\Myapp\\static\\a.jpg")
    if dob != "no":
        qry = Procturingactivity()
        qry.STUDENT = Student.objects.get(LOGIN_id=l_id)
        qry.EXAM = Exam.objects.get(id=examid)
        qry.activityname = "dob"
        qry.date = date
        qry.type = 'Object Recognition'
        qry.photo = p
        qry.save()
        # qry = "INSERT INTO `procturingactivity` (`stlid`,`examid`,`activityname`,`date`,`type`,`photo`) VALUES ('" + l_id + "','" + examid + "','" + str(
        #     dob) + "',CURDATE(),'Object Recognition','" + p + "')"
        # db = Db()
        # db.insert(qry)
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for idx, lm in enumerate(face_landmarks.landmark):
                if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                    if idx == 1:
                        nose_2d = (lm.x * img_w, lm.y * img_h)
                        nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 8000)
                    x, y = int(lm.x * img_w), int(lm.y * img_h)
                    # Get the 2D Coordinates
                    face_2d.append([x, y])
                    # Get the 3D Coordinates
                    face_3d.append([x, y, lm.z])
                    # Convert it to the NumPy array
            face_2d = np.array(face_2d, dtype=np.float64)
            # Convert it to the NumPy array
            face_3d = np.array(face_3d, dtype=np.float64)

            focal_length = 1 * img_w

            cam_matrix = np.array([[focal_length, 0, img_h / 2],
                                   [0, focal_length, img_w / 2],
                                   [0, 0, 1]])

            dist_matrix = np.zeros((4, 1), dtype=np.float64)

            success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

            rmat, jac = cv2.Rodrigues(rot_vec)

            angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

            x = angles[0] * 360
            y = angles[1] * 360

            # print(y)

            # See where the user's head tilting
            if y < -10:
                text = "Looking Left"
                print(text)
                qry = Procturingactivity()
                qry.STUDENT = Student.objects.get(LOGIN_id=l_id)
                qry.EXAM = Exam.objects.get(id=examid)
                qry.activityname = "Looking Left"
                qry.date = date
                qry.type = 'head pose'
                qry.photo = path
                qry.save()
                # qry = "INSERT INTO `procturingactivity` (`stlid`,`examid`,`activityname`,`date`,`type`,`photo`) VALUES ('" + l_id + "','" + examid + "','Looking Left',CURDATE(),'head pose','" + path + "')"
                # db = Db()
                # db.insert(qry)
            elif y > 10:
                text = "Looking Right"
                print(text)
                qry = Procturingactivity()
                qry.STUDENT = Student.objects.get(LOGIN_id=l_id)
                qry.EXAM = Exam.objects.get(id=examid)
                qry.activityname = "Looking Right"
                qry.date = date
                qry.type = 'head pose'
                qry.photo = path
                qry.save()
                # qry = "INSERT INTO `procturingactivity` (`stlid`,`examid`,`activityname`,`date`,`type`,`photo`) VALUES ('" + l_id + "','" + examid + "','Looking Right',CURDATE(),'head pose','" + path + "')"
                # db = Db()
                # db.insert(qry)
            elif x < -10:
                text = "Looking Down"
                print(text)

                qry = Procturingactivity()
                qry.STUDENT = Student.objects.get(LOGIN_id=l_id)
                qry.EXAM = Exam.objects.get(id=examid)
                qry.activityname = "Looking Down"
                qry.date = date
                qry.type = 'head pose'
                qry.photo = path
                qry.save()
                # qry = "INSERT INTO `procturingactivity` (`stlid`,`examid`,`activityname`,`date`,`type`,`photo`) VALUES ('" + l_id + "','" + examid + "','Looking Down',CURDATE(),'head pose','" + path + "')"
                # db = Db()
                # db.insert(qry)
            else:
                text = "Forward"
                print(text)

                qry = Procturingactivity()
                qry.STUDENT = Student.objects.get(LOGIN_id=l_id)
                qry.EXAM = Exam.objects.get(id=examid)
                qry.activityname = "Looking Straight"
                qry.date = date
                qry.type = 'head pose'
                qry.photo = path
                qry.save()
                # qry = "INSERT INTO `procturingactivity` (`stlid`,`examid`,`activityname`,`date`,`type`,`photo`) VALUES ('" + l_id + "','" + examid + "','Looking Straight',CURDATE(),'head pose','" + path + "')"
                # db = Db()
                # db.insert(qry)

                # Add the text on the image
                # cv2.putText(image, text, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                #
                # # Display the nose direction
                # nose_3d_projection, jacobian = cv2.projectPoints(nose_3d, rot_vec, trans_vec, cam_matrix, dist_matrix)
                #
                # p1 = (int(nose_2d[0]), int(nose_2d[1]))
                # p2 = (int(nose_3d_projection[0][0][0]), int(nose_3d_projection[0][0][1]))
                #
                # cv2.line(image, p1, p2, (255, 0, 0), 2)
                #
                # cv2.imshow('Head Pose Estimation', image)
                #
                # cv2.waitKey(100000)

    ####################END HEAD POSE







    import face_recognition

    data=Student.objects.get(LOGIN_id=l_id)

    # qry = "SELECT * FROM `student` WHERE `student_lid`='" + l_id + "'"
    # data = db.selectOne(qry)
    print(data.photo)
    picture_of_me = face_recognition.load_image_file("D:\\HumanActivityRecognition" + data.photo)

    try:

        print("face inside")
        my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]
        lndmrk = my_face_encoding
        # else:


        unknown_picture = face_recognition.load_image_file(p + s)
        # print(unknown_picture)
        unknown_face_encoding = face_recognition.face_encodings(unknown_picture)
        oo = ""
        print(len(unknown_face_encoding))
        totalpersons = len(unknown_face_encoding)



        if totalpersons > 1:
            qry = Procturingactivity()
            qry.STUDENT = Student.objects.get(LOGIN_id=l_id)
            qry.EXAM = Exam.objects.get(id=examid)
            qry.activityname = "Looking Straight"
            qry.date = date
            qry.type = 'head pose'
            qry.photo = path
            qry.save()

            # qry = "INSERT INTO `procturingactivity` (`stlid`,`examid`,`activityname`,`date`,`type`,`photo`) VALUES ('" + l_id + "','" + examid + "','" + str(
            #     totalpersons) + " Present in screen',CURDATE(),'Person Count','" + path + "')"
            # db = Db()
            # db.insert(qry)

        c = 0
        for s in range(0, len(unknown_face_encoding)):
            results = face_recognition.compare_faces([lndmrk], unknown_face_encoding[s], tolerance=.5)
            print("r2")
            for i in results:
                if i == True:
                    oo = "yes"
                    c = c + 1
                    break
            print(results)

        if c == 1:
            print("r3")
            print("oooo")
            # c=len()
            return JsonResponse({"status":"ok", "count":len(unknown_face_encoding)})






        else:
            print("r4")
            print("hooo")
            qry = Procturingactivity()
            qry.STUDENT = Student.objects.get(LOGIN_id=l_id)
            qry.EXAM = Exam.objects.get(id=examid)
            qry.activityname = "Invalid person"
            qry.date = date
            qry.type = 'FaceRecognition'
            qry.photo = path
            qry.save()
            # qry = "INSERT INTO `procturingactivity` (`stlid`,`examid`,`activityname`,`date`,`type`,`photo`) VALUES ('" + l_id + "','" + examid + "','Invalid person',CURDATE(),'FaceRecognition','" + path + "')"
            # db = Db()
            # db.insert(qry)
            return JsonResponse({"status":'no'})
    except:
        return JsonResponse({"status": 'no'})


def send_complaints_user_post(request):
    lid = request.POST["lid"]
    from datetime import datetime
    date = datetime.now().date().today()
    complaint = request.POST["complaint"]
    status = "pending"
    reply = 'pending'
    cobj = Complaint()
    cobj.date = date
    cobj.complaint= complaint
    cobj.status = status
    cobj.reply = reply
    cobj.STUDENT=Student.objects.get(LOGIN_id=lid)
    cobj.save()
    return JsonResponse({'status':'ok'})
def view_reply_user_post(request):
    lid = request.POST['lid']
    sf = Complaint.objects.filter(STUDENT__LOGIN_id=lid)
    l = []
    for i in sf:
        l.append({'id': i.id, 'date': i.date, 'complaint': i.complaint, 'status': i.status, 'reply': i.reply,})
    return JsonResponse({'status': 'ok', 'data': l})


def and_send_feedback(request):
    lid=request.POST['lid']
    feedback=request.POST['feedback']
    f=Feedback()
    from datetime import datetime
    date = datetime.now().date().today()
    f.date=date
    f.feedback=feedback
    f.STUDENT_id=Student.objects.get(LOGIN_id=lid).id
    f.save()
    return JsonResponse({'status':'ok'})


def and_view_feedback(request):
    # lid = request.POST['lid']
    sf = Feedback.objects.all()
    l = []
    for i in sf:
        l.append({'id': i.id, 'date': i.date, 'feedback': i.feedback, 'stname': i.STUDENT.name})
    return JsonResponse({'status': 'ok', 'data': l})


def and_change_password(request):
    lid=request.POST['lid']
    cpass=request.POST['cpass']
    npass=request.POST['npass']
    cmpass=request.POST['cmpass']
    l=Login.objects.filter(id=lid,passsword=cpass)
    if l.exists():
        if npass == cmpass:
            ll=Login.objects.filter(id=lid,passsword=cpass)
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'no'})
    else:
        return JsonResponse({'status': 'no'})




def and_view_mark(request):
    lid=request.POST['lid']
    sf = Mark.objects.filter(STUDENT__LOGIN_id=lid)
    l = []
    for i in sf:
        l.append({'id': i.id, 'date': i.EXAM.date, 'exm': i.EXAM.exam_name, 'mark': i.mark})
    return JsonResponse({'status': 'ok', 'data': l})


def view_procter_activity(request,id):
    re=Procturingactivity.objects.filter(EXAM_id=id).exclude(STUDENT_id=1)
    return render(request,'teacher/View procteractivity.html',{'data':re})








