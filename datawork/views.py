from django.shortcuts import render, redirect
from time import sleep
from .forms import *
from django.db.models import Q
# Create your views here.


def login_signup(r):
    if r.session.has_key('user'):
        return redirect(index)

    else:
        form = UserSignup(r.POST or None)
        if r.method == 'POST' and form.is_valid():
            form.save()
            sleep(1)
            user = User.objects.get(email=r.POST.get('email')).id
            r.session['user'] = user
            print(r.session['user'])
            return redirect(login_signup)

        return render(r, 'login_signup.html', {'user_form': form})


def login(r):
    if r.session.has_key('user'):
        return redirect(index)

    if r.method == 'POST':
        email_mobile = r.POST.get('email')
        password = r.POST.get('password')
        check = User.objects.filter(Q(Q(email=email_mobile) | Q(mobile=email_mobile)) & Q(password=password))
        if check:
            check = User.objects.get(Q(Q(email=email_mobile) | Q(mobile=email_mobile)) & Q(password=password)).id
            r.session['user'] = check
            return redirect(index)

        else:
            return redirect(login_signup)


def index(r):
    if r.session.has_key('user'):
        return render(r, 'home.html', {
            'login_user': User.objects.get(id=r.session['user']),       # Common dictionary
            'user': User.objects.all().exclude(id=r.session['user']),   # Common dictionary
            'post': Post.objects.all(),
        })

    else:
        return redirect(login_signup)


def private_profile(r):
    if r.session.has_key('user'):
        dp_update = Dpupdate()
        user_update = Userupdate(None, instance=User.objects.get(id=r.session['user']))
        if r.method == 'POST':
            dp_update = Dpupdate(r.POST, r.FILES, instance=User.objects.get(id=r.session['user']))
            dp_update.save()
            return redirect(private_profile)
        return render(r, 'private_profile.html', {
            'login_user': User.objects.get(id=r.session['user']),       # Common dictionary
            'user': User.objects.all().exclude(id=r.session['user']),   # Common dictionary
            'dp_update': dp_update,
            'post': Post.objects.filter(user_id=r.session['user']),
            'user_update': user_update,
        })
    else:
        return redirect(login_signup)


def public_profile(r, u_id):
    if r.session.has_key('user'):
        return render(r, 'public_profile.html', {
            'login_user': User.objects.get(id=r.session['user']),       # Common dictionary
            'user': User.objects.all().exclude(id=r.session['user']),   # Common dictionary
            'post': Post.objects.filter(user_id=u_id),
            'filter_user': User.objects.get(id=u_id),
        })
    else:
        return redirect(login_signup)


def user_update(r):
    if r.session.has_key('user'):
        if r.method == 'POST':
            user_update = Userupdate(r.POST, instance=User.objects.get(id=r.session['user']))
            user_update.save()
            return redirect(private_profile)
        else:
            return redirect(private_profile)
    else:
        return redirect(login_signup)


def post(r):
    if r.session.has_key('user'):
        if r.method == "POST":
            post = Post()
            post.post_desc = r.POST.get('post_text')
            post.user_id = User(r.session['user'])
            post.save()
            return redirect(index)
        else:
            return redirect(index)
    else:
        return redirect(login_signup)


def delete_post(r, p_id):
    if r.session.has_key('user'):
        post = Post.objects.filter(p_id=p_id)
        post.delete()
        return redirect(private_profile)
    else:
        return redirect(login_signup)


def like_dislike(r, p_id):
    if r.session.has_key('user'):
        like = Likes.objects.filter(post_id=p_id, user_id=r.session['user']).count()
        if like > 0:
            like = Likes.objects.filter(post_id=p_id, user_id=r.session['user'])
            like.delete()
            return redirect(index)
        else:
            like = Likes()
            like.post_id = Post(p_id)
            like.user_id = User(r.session['user'])
            like.save()
            return redirect(index)
    else:
        return redirect(login_signup)


def message(r, u_id=None):
    if r.session.has_key('user'):
        if u_id == None:
            return render(r, 'msg.html', {
                'login_user': User.objects.get(id=r.session['user']),  # Common dictionary
                'user': User.objects.all().exclude(id=r.session['user']),  # Common dictionary
            })
        else:
            return render(r, 'message.html', {
                'login_user': User.objects.get(id=r.session['user']),       # Common dictionary
                'user': User.objects.all().exclude(id=r.session['user']),   # Common dictionary
                'filter_user': User.objects.get(id=u_id),
                'message': Message.objects.all(),
            })
    else:
        return redirect(login_signup)


def send_message(r, u_id):
    if r.session.has_key('user'):
        if r.method == "POST":
            msg = Message()
            msg.sender_id = User(r.session['user'])
            msg.receiver_id = User(u_id)
            msg.message = r.POST.get('message')
            msg.save()
            return redirect("../../message/"+str(u_id)+"/")
    else:
        return redirect(login_signup)


def logout(r):
    if r.session.has_key('user'):
        del r.session['user']
        return redirect(login_signup)
    else:
        return redirect(login_signup)
