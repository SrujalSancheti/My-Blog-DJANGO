from django.shortcuts import render,redirect
from django.http import HttpResponse
from blog1.models import Post,BlogComment
from django.contrib import messages
from blog1.templatetags import extras

# Create your views here.
def blogHome(request):
    allPosts = Post.objects.all()
    context = {'allPosts':allPosts}
    return render(request,'blog1/blogHome.html',context)

def blogPost(request,slug):
    post = Post.objects.filter(slug=slug).first()
    post.views = post.views + 1
    post.save()
    comments = BlogComment.objects.filter(post=post ,parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    # print(replies,comments)
    # print(replyDict)
    context = {'post': post,'comments':comments,'user':request.user,'replyDict':replyDict}
    return render(request,'blog1/blogPost.html',context)

def postComment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        postsno = request.POST.get("postsno")
        post = Post.objects.get(sno=postsno)
        parentSno = request.POST.get("parentSno")
        if parentSno == "":
            comment = BlogComment(comment=comment,user=user,post=post)
            comment.save()
            messages.success(request,"Commented Successfully")
        else:
            parent= BlogComment.objects.get(sno=parentSno  )
            comment = BlogComment(comment=comment,user=user,post=post,parent=parent)
            comment.save()
            messages.success(request,"Replied Successfully")
    return redirect(f"/blog1/{post.slug}")