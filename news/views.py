from django.conf import settings
from django.db.models.deletion import Collector
from django.db.utils import ConnectionRouter
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, QueryDict, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
import json
import ast

from django.urls import reverse

from .models import Article, WebsiteUser, Comment, Like, Dislike
from django.core.mail import send_mail
from .enums import Category

def authenticated(redirect):
    def decorator(f):
        def auth(request):
            if request.user.is_authenticated:
                return f(request)
            else:
                if redirect:
                    return HttpResponseRedirect(reverse('news:logging'))
                else:
                    returnObject = {
                        'status': 'not logged in'
                    }
                    return returnObject
        return auth
    return decorator

def user_not_exists(pageUrl):
    def decorator(f):
        def exists(request):
            if not ('username' in request.POST and 'password' in request.POST):
                return render(request, pageUrl, {})
            else:
                return f(request)
        return exists
    return decorator

def exists_example_test(f):
    def checkExists(request):
        return HttpResponseRedirect(reverse('news:logging'))
    return checkExists

def healthcheck(request):
    return HttpResponse(200)

def reactions(request):
    article = request.GET
    article = str(article.get('article'))
    
    response = likerDislikerHelper(request, article, 0)

    return HttpResponse(json.dumps(response))

def like(request):
    article = request.GET
    article = str(article.get('article'))
    
    response = likerDislikerHelper(request, article, 1)

    return HttpResponse(json.dumps(response))

def dislike(request):
    article = request.GET
    article = str(article.get('article'))
    
    response = likerDislikerHelper(request, article, -1)

    return HttpResponse(json.dumps(response))

@authenticated(redirect=False)
def likerDislikerHelper(request, ident, adjust):
    articleObject = Article.objects.get(ident=ident)
    user = WebsiteUser.objects.get(user=request.user)
    cl = Like.objects.filter(article=articleObject, user=user)
    cd = Dislike.objects.filter(article=articleObject, user=user)
    status = "success"
    if (cl.first() or cd.first()):
        if (adjust == 0):
            if (cl.first()):
                status = "disable-dislike"
            else:
                status = "disable-like"
        else:
            if (cl.first()):
                status = cl.first().delete()
            else:
                status = cd.first().delete()
    elif (adjust == 1):
        status = "disable-dislike"
        l = Like(user=user, article=articleObject)
        l.save()
    elif (adjust == -1):
        status = "disable-like"
        d = Dislike(user=user, article=articleObject)
        d.save()

    likes = Like.objects.filter(article=articleObject)
    dislikes = Dislike.objects.filter(article=articleObject)

    returnObject = {
        'status': status,
        'likes': likes.count(),
        'dislikes': dislikes.count()
    }
    return returnObject

@authenticated(redirect=False)
def editcomment(request):
    payload = QueryDict(request.body)
    ident = str(payload.get('ident'))
    commentText = str(payload.get('commentText'))
    commentObject = Comment.objects.get(ident=ident)
    relatedComments = Comment.objects.filter(in_reply_to=commentObject)
    commentObject.text = commentText
    commentObject.save()

    replyIdents = []
    for comment in relatedComments:
        replyIdents.append(str(comment.ident))

    response = {
        'status': 'success',
        'commentId': str(ident),
        'newText': commentText,
        'replies': replyIdents
    }

    return HttpResponse(json.dumps(response))

def cascadeobjects(obj):
    router = ConnectionRouter(settings.DATABASE_ROUTERS)
    using = router.db_for_write(obj.__class__)
    collection = Collector(using)
    collection.collect([obj])
    return collection.instances_with_model()

@authenticated(redirect=False)
def deletecomment(request):
    payload = request.GET
    ident = str(payload.get('comment'))
    commentObject = Comment.objects.get(ident=ident)
    commentObjectsInReply = cascadeobjects(commentObject)

    replyIdents = []
    for comment in commentObjectsInReply:
        replyIdents.append(str(comment[1].ident))

    commentObject.delete()

    response = {
        'status': 'success',
        'commentId': str(ident),
        'replies': replyIdents
    }

    return HttpResponse(json.dumps(response))

@authenticated(redirect=False)
def comment(request):
    payload = request.POST
    ident = str(payload.get('ident'))
    commentText = str(payload.get('commentText'))
    inReplyTo = str(payload.get('inReplyTo'))

    inReplyToComment = None
    inReplyToCommentText = ''

    if (len(inReplyTo)):
        inReplyToComment = Comment.objects.get(ident=inReplyTo)
        inReplyToCommentText = inReplyToComment.text

    articleObject = Article.objects.get(ident=ident)
    user = WebsiteUser.objects.get(user=request.user)
    c = Comment(user=user, text=commentText, article=articleObject, in_reply_to=inReplyToComment)
    c.save()

    response = {
        'status': 'success',
        'commentAdded': commentText,
        'commentId': str(c.ident),
        'inReplyTo': inReplyToCommentText
    }

    return HttpResponse(json.dumps(response))

@authenticated(redirect=False)
def comments(request):
    payload = request.GET
    ident = str(payload.get('article'))
    articleObject = Article.objects.get(ident=ident)

    filtered = Comment.objects.filter(article=articleObject)

    returnItems = []

    for comment in filtered:
        replyText = ''
        if (comment.in_reply_to != None):
            replyText = comment.in_reply_to.text
        mapped = mapCommentToSchema(comment, replyText)
        returnItems.append(mapped)

    response = {
        'status': 'success',
        'comments': returnItems,
        'user': str(request.user)
    }

    return HttpResponse(json.dumps(response))

def mapCommentToSchema(comment, replyText):
    return {
        'user': comment.user.user.username,
        'text': comment.text,
        'article': str(comment.article.ident),
        'ident': str(comment.ident),
        'inReplyTo': replyText
    }

@authenticated(redirect=True)
def landing(request):
    template = loader.get_template('news/articleHome.html')
    user = WebsiteUser.objects.get(user=request.user)
    categories = user.fave_categories
    if categories is None:
        context = {
            'articles': Article.objects.all()
        }
    else:
        categories = ast.literal_eval(categories)
        context = {
            'articles': Article.objects.filter(category__in=categories),
            'categories': categories
        }

    return HttpResponse(template.render(context, request))

def getArticles(request):
    category = request.GET
    category = str(category.get('filter'))
    if (category == ''):
        filtered = Article.objects.all()
    else:
        category = category.split(", ")
        filtered = Article.objects.filter(category__in=category)

    returnItems = []

    for article in filtered:
        mapped = mapArticleToSchema(article)
        returnItems.append(mapped)

    response = {
        'status': 'success',
        'articles': returnItems,
    }

    return HttpResponse(json.dumps(response))

def mapArticleToSchema(article):
    return {
        'content': article.content,
        'title': article.title,
        'pubDate': str(article.pub_date),
        'ident': article.ident,
        'category': article.category
    }

@user_not_exists(pageUrl='news/login.html')
def logging(request):
    username = request.POST['username']
    password = request.POST['password']
    user = WebsiteUser.objects.filter(user__username=username)
    auth_user = authenticate(request, username=username, password=password)
    if auth_user is not None:
        login(request, auth_user)
        return redirect(reverse('news:landing'))
    else:
        if len(user) == 0:
            error_user_context = {
                'erroruser': True
            }
            return render(request, 'news/login.html', error_user_context)
        else:
            error_context = {
                'incorrectlogin': True
            }
            return render(request, 'news/login.html', error_context)

def logging_out(request):
    logout(request)
    return redirect(reverse('news:logging'))

@user_not_exists(pageUrl='news/signup.html')
def signup(request):
    firstname1 = request.POST['firstname']
    surname1 = request.POST['surname']
    username1 = request.POST['username']
    email1 = request.POST['email']
    dob1 = request.POST['dob']
    password1 = request.POST['password']
    abstract_user = User.objects.create_user(username=username1, first_name=firstname1, last_name=surname1,
                                             email=email1, password=password1)
    abstract_user.save()
    user = WebsiteUser(user=abstract_user, DOB=dob1)
    user.save()
    send_email(email1, firstname1)

    response = {
        'status': 'ok'
    }

    return HttpResponse(json.dumps(response))

def send_email(email, first_name):
    recipient = email
    sender = 'fakenewswebsite0@gmail.com'
    subject = 'Welcome to Fake News Website'
    message = 'Thank you for registering with us ' + first_name + '. Enjoy your time with Fake News'
    send_mail(subject, message, sender, [recipient], fail_silently=False)

@authenticated(redirect=True)
def profile(request):
    profile = WebsiteUser.objects.get(user=request.user)
    categories = Category.optionsDict()
    context = {
        'profile': profile,
        'categories': categories
    }
    return render(request, 'news/profile.html', context)

def updateProfile(request):
    if request.is_ajax and request.method == "PUT":
        data = QueryDict(request.body)
        user = WebsiteUser.objects.get(user=request.user)
        categories = data.get("categories")
        setUser(user, categories, None, False)
        response = {
            'status': 'Profile ' + user.user.username + 'updated successfully'
        }
        return HttpResponse(json.dumps(response))
    return JsonResponse('fail', status=400, safe=False)

def updatePicture(request):
    if request.is_ajax and 'img' in request.FILES:
        user = WebsiteUser.objects.get(user=request.user)
        picture = request.FILES['img']
        setUser(user, None, picture, False)
        return HttpResponse(user.image.url)
    return JsonResponse('fail', status=400, safe=False)

def deletePicture(request):
    if request.is_ajax and request.method == "DELETE":
        user = WebsiteUser.objects.get(user=request.user)
        setUser(user, None, None, True)
        return JsonResponse('Profile ' + user.user.username + ' picture removed', status=200, safe=False)
    return JsonResponse('fail', status=400, safe=False)

def setUser(user, categories, image, delete):
    if categories is not None:
        user.fave_categories = categories
    if image is None:
        if delete:
            user.image = None
    else:
        user.image = image
    user.save()
