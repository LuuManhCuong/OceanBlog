
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from .models import Asset, Blog, User, Comment
from django.db.models import Q
import json
import uuid
import cloudinary.uploader
from datetime import date
from django.contrib.auth.decorators import login_required
# Create your views here.


def res(request):
    response = HttpResponse()
    response.writelines("<h1>Hello World!!!</h1>")
    response.write("This is home app")
    return response


def home(request):
    assets = Asset.objects.all()
    username = request.COOKIES.get('username')
    return render(request, 'index.html', {'assets': assets,"username": username})


def login(request):
    return render(request, 'login.html')


# authent
@csrf_exempt
def check_user(request):
    if request.method == 'POST':
        # Nhận dữ liệu từ yêu cầu POST và chuyển đổi từ byte thành chuỗi
        data = json.loads(request.body.decode('utf-8'))
        # print("data: ", data)
        username = data.get('user-name')
        password = data.get('user-password')

        # print(username)
        # print(password)

        # Kiểm tra người dùng đã tồn tại hay chưa
        if User.objects.filter(username=username, password=password).exists():
            # Lấy thông tin người dùng từ database
            user = User.objects.get(username=username)

            # Lưu thông tin người dùng vào cookies
            response = JsonResponse(
                {'username': user.username, 'email': user.email})
            response.set_cookie("username", user.username)
            response.set_cookie("thumbnail", user.avatar)
            response.set_cookie("idUser", user.idUser)

            return response

        # Trả về phản hồi JSON
        response_data = {'status': 'error',
                         'message': 'Sai thông tin tài khoản'}
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        # Trả về phản hồi lỗi cho các phương thức yêu cầu khác
        response_data = {'status': 'error',
                         'message': 'Phương thức yêu cầu không được hỗ trợ'}
        return HttpResponse(json.dumps(response_data), content_type='application/json', status=405)


@csrf_exempt
def register(request):
    if request.method == 'POST':
        # Nhận dữ liệu từ yêu cầu POST và chuyển đổi từ byte thành chuỗi
        data = json.loads(request.body.decode('utf-8'))
        # print("data: ", data)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        gender = data.get('gender')

        # Kiểm tra xem người dùng đã tồn tại dựa trên trường username hoặc email
        if User.objects.filter(username=username).exists():
            response_data = {'status': 'error',
                             'message': 'Tên người dùng đã tồn tại'}
            return JsonResponse(response_data, status=400)

        if User.objects.filter(email=email).exists():
            response_data = {'status': 'error',
                             'message': 'Email đã được đăng ký'}
            return JsonResponse(response_data, status=400)

        # Tạo đối tượng User mới
        id = uuid.uuid4()
        user = User(idUser=id,
                    username=username,
                    email=email,
                    password=password,
                    gender=gender,
                    )
        user.save()

        # Trả về phản hồi JSON thành công
        response_data = {'status': 'success', 'message': 'Đăng ký thành công'}
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        # Trả về phản hồi lỗi cho các phương thức yêu cầu khác
        response_data = {'status': 'error',
                         'message': 'Phương thức yêu cầu không được hỗ trợ'}
        return HttpResponse(json.dumps(response_data), content_type='application/json', status=405)


def logout(request):
    response = HttpResponse()
    response.delete_cookie("username")
    response.delete_cookie("thumbnail")
    response.delete_cookie("idUser")

    # Chuyển hướng về trang home
    response['Location'] = '/login'
    response.status_code = 302
    return response


def blog(request):
    blogData = Blog.objects.all().order_by('-date')
    return render(request, 'blog.html', {'blogs': blogData})


def my_blog(request):
    idAuthor = request.COOKIES.get('idUser')
    # print("idAuthor: "+idAuthor)
    blogData = Blog.objects.filter(idAuthor=idAuthor).order_by('-date')
    return render(request, 'myBlog.html', {'blogs': blogData})


def blogDetail(request, idPost):
    # print("DeteaiL : ", idPost)
    username = request.COOKIES.get('username')
    blog = get_object_or_404(Blog, idPost=idPost)
    comments = Comment.objects.filter(post__idPost=idPost).order_by('-createdAt').select_related(
        'author')
    comment_count = Comment.objects.filter(post__idPost=idPost).count()

    return render(request, 'blogDetail.html', {'blog': blog, "comments": comments, "comment_count": comment_count, "username": username})


@csrf_exempt
def get_latest_blogs(request):
    latest_blogs = Blog.objects.order_by('-date')[:6].values(
        'idPost',
        'thumbnail',
        'title',
        'content',
        'date',
        'tag'
    )
    return JsonResponse(list(latest_blogs), safe=False)


@csrf_exempt
def createBlog(request):
    if request.method == "POST":
        # Lấy dữ liệu từ form
        title = request.POST.get('title')
        destination = request.POST.get('destination')
        tag = request.POST.get('tag')
        content = request.POST.get('content')
        thumbnail = request.FILES.get('thumbnail')

        # print(title)
        # print(destination)
        # print(tag)
        # print(content)

        # Tải lên ảnh lên Cloudinary
        upload_result = cloudinary.uploader.upload(thumbnail)

        # Lấy URL của ảnh từ kết quả upload
        thumbnail_url = upload_result['secure_url']
        # print("url: " + thumbnail_url)

        id = uuid.uuid4()
        author = request.COOKIES.get('username')
        idAuthor = request.COOKIES.get('idUser')
        # print("author: " + author)
        newBlog = Blog(idPost=id, title=title, content=content,
                       destination=destination, author=author, idAuthor=idAuthor, thumbnail=thumbnail_url, tag=tag)
        newBlog.save()
        # Trả về kết quả hoặc render template tương ứng
        return my_blog(request)

    return render(request, 'createBlog.html')


@csrf_exempt
def deleteBlog(request, idPost):
    print("Delte: " + idPost)
    Blog.objects.filter(idPost=idPost).delete()
    return redirect('me/blog')


def contact(request):
    return render(request, 'contact.html')


@csrf_exempt
def createComment(request):
    if request.method == "POST":
        idPost = request.POST.get("idPost")
        content = request.POST.get("content")
        idUser = request.COOKIES.get('idUser')

        idComment = uuid.uuid4()
        author = User.objects.get(idUser=idUser)
        post = Blog.objects.get(idPost=idPost)

        newComment = Comment(idComment=idComment,
                             author=author, post=post, content=content)
        newComment.save()

        return blogDetail(request, idPost)
    return redirect('blog')


@csrf_exempt
def searchBlog(request):
    keyword = request.GET.get("keyword")
    print("key: ", keyword)
 # Tìm kiếm các bài viết có tiêu đề hoặc nội dung chứa từ khóa
    results = Blog.objects.filter(
        Q(title__icontains=keyword) | Q(content__icontains=keyword)).order_by('-date')

    return render(request, 'blog.html', {'blogs': results})


@csrf_exempt
def profile(request):
    if request.method == "POST":
        # Lấy dữ liệu từ form
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        avatar = request.FILES.get('avatar')
        idUser = request.COOKIES.get('idUser')

        # print(username)
        # print(password)
        # print(email)
        # print(gender)

        # Tải lên ảnh lên Cloudinary
        upload_result = cloudinary.uploader.upload(avatar)

        # Lấy URL của ảnh từ kết quả upload
        avatar_url = upload_result['secure_url']
        print("url: " + avatar_url)

        # Lấy thông tin người dùng từ database
        currentUser = User.objects.get(idUser=idUser)

        currentUser.username = username
        currentUser.password = password
        currentUser.email = email
        currentUser.gender = gender
        currentUser.avatar = avatar_url

        currentUser.save()

        # Lưu thông tin người dùng vào cookies
        response = HttpResponseRedirect('/home')
        response.set_cookie("username", username)
        response.set_cookie("thumbnail", avatar_url)
        response.set_cookie("idUser", idUser)

        return response

    return render(request, 'home.html')
