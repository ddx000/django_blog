# Django-Blog
A easy blog when I learned Django Framework from Youtube Tutorial Series teached by Corey Schafer  
and the notes below are some code-snippnet for me.

# Command line

- djando-admin
- djando-admin startproject your_project_name
- python manage.py runserver
- python manage.py startapp app_name

**CREATE SUPERUSER**
- 記得先跑migrate
- python manage.py createsuperuser


=======
# Migration
# 每次創造MODEL 都必須要MIGRATION
**建造Migration - From Model**
- python manage.py makemigrations  
> 在RUN MIGRATIONS前先建造一些migration
> migration-->務必在admin.py register

**看看Migration下了什麼SQL語法**
- python manage.py sqlmigrate blog 0001

**跑各個migrations**
- python manage.py migrate  


> 註：其實django.contrib.auth.models裡面就提供了很多管理使用者的模組，基本上是建立好了，我們這邊感覺就像是利用內建的user, 不用再重造輪子，所以sqlite一打開時，基本上就是內建那些基礎的使用者模組，blog.models是我們在create Migrations後，在migrate 進去(下SQL指令) database的，用ORM的缺點其實是要常常調SQL出來看他到底做了什麼語法



# URL
url 要指定路徑的機制

# TEMPLATES
- register in app.py
- use base.py reduce repeatitive code
- extends / block / endblock
    ```python
    {% extends "blog/base.html" %}  
    {% block content %}    
    {% endblock content %}
    ```
- 使用靜態static {% load static %}載入.css
- {% url 'url_name' %} 減少hard code
- 前端善用code snippnet 減少一些框架(就是偷懶)

# DATABASE ORM
- Sqlite for testing, and mysql for deploying
- Easy switch from this


# run shell
- python manage.py shell

    user = User.objects.filter(username = 'ddx000').first()  
    post_1 = Post(title='First Blog',content='this is test from python shell',author_id = user)
    post_1.save()
    

# Admin後臺機制
- 可以把一些東西加進去admin裡面，用lib提供的介面manipulate sql
- admin.py file
- admin.site.register(Post)

# User Registration
- 運用cmd建立一個user control app(模組化設計)
- python manage.py startapp user
- 在user/apps.py 下copy UserConfig
- 記得要在Setting下面掛載 - 'user.apps.UserConfig'

> 步驟-->建立APP-->Settings掛載APP-->設定URL route-->設定views  
這樣主伺服器就有辦法利用URL重新指向那個模組(前提是 要掛載上去)

# Render

- render(request, templated_name, para as dictionary)


# 關於註冊機制

- 在View裡面新增  
    from django.contrib.auth.forms import UserCreationForm
- 若要更多功能可以自己改寫這個class(add email)
- 可以用lib, crispy基於bootstrap4上把註冊表單最佳化(前端)
    
- 流程
1. 使用者送出request url route到註冊介面
2. url route to views.py
3. 如果第一次打開註冊介面, render register.html with 一個空的UserCreationForm
4. 使用者在register.html填寫資料後，可以用submit_btn用POST的方式
5. 如果POST沒有指定route, 其實就是right back回來原本的路徑view.py
6. 加邏輯判斷 if 接收到POST後形成一個新的(UserCreationForm)這個model,     
    form = UserRegisterForm(request.POST)
7. 這樣就能redirect, 這邊可以用django的message機制, 而這message機制已經是基於cookies or sessions 儲存的變數
=======
- 在View裡面新增  
    from django.contrib.auth.forms import UserCreationForm

# Login-logout

 ```python
    from user import views as user_views
    path('login/',auth_views.LoginView.as_view(template_name = 'user/login.html'), name ="login"),
    path('logout/',auth_views.LogoutView.as_view(template_name = 'user/logout.html'), name ="logout"),
    LOGIN_REDIRECT_URL = 'blog-home1'
```

- 點入登入/登出時，用login/logout去渲染
- 直接封裝了系統登入/登出 在Django模組裡面
- 登入登出由於是預設模組，需要至Settings做些變更
- Navigation bar前端可以直接加上邏輯 (IF ELSE)
 ```html
  {% if user.is_authenticated %}
    <a class="nav-item nav-link" href="{% url 'profile' %}">Profile</a>
    <a class="nav-item nav-link" href="{% url 'logout' %}">Logout</a>
  {% else %}
    <a class="nav-item nav-link" href="{% url 'login' %}">Login</a>
    <a class="nav-item nav-link" href="{% url 'register' %}">Register</a>
  {% endif %}
```
- 可以加上@decorater - @login_required 判斷是否登入
- 當然這個會自動導向到登入畫面 也需要去setting裡面改 LOGIN_URL = 'login'
- django裡面的user似乎是保留字 不必特別傳入 前端可以直接show user.username


> https://www.youtube.com/watch?v=FdVuKt_iuSI&t=1575s
> 3/29進度14:15