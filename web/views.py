import os

import requests
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse

from hello.spider import *
from web.models import *
from threading import Thread
from django.db.utils import IntegrityError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

IMG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media')


def admin(request):
    if request.session.get('admin', False):
        return render(request, 'admin.html')
    else:
        return HttpResponseRedirect(reverse('web:login'))


def send_email(request):
    subject = '问候'
    if request.method == 'POST':
        # from_email = settings.DEFAULT_FROM_EMAIL
        content_txt = '欢迎浏览本网页'
        template_html = 'email.html'
        html = loader.get_template(template_html)
        content_html = html.render()
        to_email = request.POST['email']

        msg = EmailMultiAlternatives(
            subject, body=content_txt, to=[to_email]
        )
        msg.attach_alternative(content_html, 'text/html')
        msg.send()
        request.session['msg'] = '邮件发送成功'
        messages.add_message(request, message='邮件发送成功', level=messages.INFO)
        return HttpResponseRedirect(reverse('index'))
    # render(request, 'index.html')


def login(request):
    return render(request, 'web/login.html')


def is_login(request):
    if request.method == 'POST':
        name = request.POST['name'].strip()
        pwd = request.POST['pwd'].strip()
        try:
            user = User.objects.get(name=name)
        except BaseException:
            messages.add_message(request, messages.INFO, '用户未注册')
            return HttpResponseRedirect(reverse('web:login'))
        else:
            if check_password(pwd, user.password):
                if name == 'admin':
                    request.session['admin'] = 'true'
                    request.session.set_expiry(0)
                    return HttpResponseRedirect(reverse('web:admin'))
                return HttpResponseRedirect(reverse('index'))
            else:
                messages.add_message(request, messages.INFO, '用户名或者密码错误')
                return HttpResponseRedirect(reverse('web:login'))


def movie_list(request):
    msg = '暂无电影宣传海报图片资源'
    movie_pics = Movies.objects.all()
    paginator = Paginator(movie_pics, 25)
    page_nums = paginator.num_pages
    current_page = int(request.GET.get('page', 1))
    if page_nums > 10:
        if current_page + 5 > page_nums:
            page_range = range(page_nums-9, page_nums+1)
        elif current_page - 5 < 1:
            page_range = range(1, 11)
        else:
            page_range = range(current_page-5, current_page+5)
    else:
        page_range = range(1, page_nums+1)

    if movie_pics:
        try:
            page = paginator.get_page(current_page)
        except PageNotAnInteger:
            page = paginator.get_page(1)
        except EmptyPage:
            page = paginator.get_page(1)
        return render(request, 'web/movie-list.html',
                      {'page': page, 'page_range': page_range})
    else:
        return render(request, 'web/movie-list.html', {'msg': msg})


def save_img(url, img_name):
    req = requests.get(url)
    img = req.content
    pic_file = IMG_FILE + '/movie-pic'
    if not os.path.exists(pic_file):
        os.mkdir(pic_file)

    with open(pic_file + f'/{img_name}.jpg', 'wb') as f:
        f.write(img)


def spider(request):
    if request.method == 'POST':
        page = request.POST['page'].strip()
        tasks = []
        for item in get_details(BASE_URL, int(page)):
            try:
                Movies(name=item['movie_name']).save()
            except IntegrityError:
                request.session['error'] = '你已经爬取过该页面了！'
                request.session.set_expiry(20)
            else:
                t = Thread(target=save_img, args=(item['img_src'], item['movie_name']))
                tasks.append(t)
            # save_img(item['img_src'], item['movie_name'])
        for task in tasks:
            task.start()
        return HttpResponseRedirect(reverse('web:admin'))


def register_page(request):
    return render(request, 'register.html')


def register(request):
    if request.method == 'POST':
        name = request.POST['name'].strip()
        pwd = request.POST['pwd'].strip()
        if name and pwd:
            try:
                User(name=name, user_password=pwd).save()
            except IntegrityError:
                messages.add_message(request, messages.INFO, '用户名以存在')
                return HttpResponseRedirect(reverse('web:register-page'))
            else:
                return HttpResponseRedirect(reverse('web:register-page'))
    else:
        return HttpResponseRedirect(reverse('web:register-page'))