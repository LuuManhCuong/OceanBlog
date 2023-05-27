from django.db import models

# Create your models here.


class User(models.Model):
    idUser = models.CharField(max_length=100)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=10)
    avatar = models.CharField(
        max_length=500, default="https://img.freepik.com/premium-vector/female-user-profile-avatar-is-woman-character-screen-saver-with-emotions_505620-617.jpg")
    email = models.EmailField()
    gender = models.CharField(max_length=10, default="")
    createAt = models.DateField(auto_now_add=True)


class Blog(models.Model):
    idPost = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    content = models.TextField()
    destination = models.CharField(max_length=200, default="world")
    view = models.IntegerField(default=0)
    author = models.CharField(max_length=50, default="admin")
    idAuthor = models.CharField(max_length=100, default="1")
    thumbnail = models.CharField(
        max_length=500, default="https://tranhoangkhang1212.github.io/travelix/assets/images/xintro_1.jpg.pagespeed.ic.vc2WNRX2pm.webp")
    date = models.DateField(auto_now_add=True)
    tag = models.CharField(max_length=200, default="#blog")


class Comment(models.Model):
    idComment = models.CharField(max_length=100, default=1)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, default=None)
    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)


class Asset(models.Model):
    idAsset = models.CharField(max_length=100)
    # Sử dụng đường dẫn tương đối
    audio = models.CharField(max_length=100, default='img_video/giobien.mp3')
    # Sử dụng đường dẫn tuyệt đối
    video = models.CharField(
        max_length=100, default='img_video/video.mp4')
