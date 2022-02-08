from django.shortcuts import render, redirect
from .models import MyBoard, MyMember
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password, check_password

def index(request):
    myboard = MyBoard.objects.all().order_by('-id')
    paginator = Paginator(myboard, 7)
    page_num = request.GET.get('page','1')

    # 페이지에 있는 모델 가져오기
    page_obj = paginator.get_page(page_num)

    # 관련 메서드
    print(type(page_obj))
    print(page_obj.count)
    print(page_obj.paginator.num_pages) #총페이지수
    print(page_obj.paginator.page_range)    #1부터 범위 반복
    print(page_obj.has_next())  #다음페이지가 있다면 True 반환
    print(page_obj.has_previous())  #이전페이지가 있다면 True 반환
    try:
        print(page_obj.next_page_number())  #다음페이지 number 반환
        print(page_obj.previous_page_number()) #이전페이지 number 반환
    except:
        pass
    print(page_obj.start_index())
    print(page_obj.end_index())
    # order_by => default는 오름차순, -붙이면 내림차순
    # return render(request, 'index.html', {'list' : MyBoard.objects.all().order_by('-id')})

    return render(request, 'index.html', {'list' : page_obj})

def insert_form(request):
    return render(request, 'insert.html')

def insert_res(request):
    myname = request.POST['myname']
    mytitle = request.POST['mytitle']
    mycontent = request.POST['mycontent']

    result = MyBoard.objects.create(myname=myname, mytitle=mytitle, mycontent=mycontent, mydate=timezone.now())

    if result:      # 제대로 결과가 출력되었다면
        return redirect('index')
    else:
        return redirect('insertform')

def detail(request, id):
    return render(request, 'detail.html', {'dto':MyBoard.objects.get(id=id)})

def update_form(request, id):
    return render(request, 'update.html', {'dto' : MyBoard.objects.get(id=id)})

def update_res(request):
    id = request.POST['id']
    mytitle = request.POST['mytitle']
    mycontent = request.POST['mycontent']

    myboard = MyBoard.objects.filter(id=id)
    result_title = myboard.update(mytitle=mytitle)
    result_content = myboard.update(mycontent=mycontent)

    if result_title + result_content == 2:
        return redirect('/detail/' + id)
    else:
        return redirect('updateform/'+id)

def delete(request, id):
    result_delete = MyBoard.objects.filter(id=id).delete()

    if result_delete[0]:
        return redirect('index')
    else:
        return redirect('detail/' + id)

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        myname = request.POST['myname']
        mypassword = request.POST['mypassword']
        myemail = request.POST['myemail']

        mymember = MyMember(myname=myname, mypassword=make_password(mypassword), myemail=myemail)
        mymember.save()

        return redirect('/')

    return redirect('/')

def login(request):
    if request.method =='GET':
        return render(request, 'login.html')
    else:
        myname = request.POST['myname']
        mypassword = request.POST['mypassword']

        mymember = MyMember.objects.get(myname=myname)

        if check_password(mypassword, mymember.mypassword):
            request.session['myname'] = mymember.myname
            return redirect('/')
        else:
            return render('/login')

def logout(request):
    del request.session['myname']
    return redirect('/')

