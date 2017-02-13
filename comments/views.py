from django.shortcuts import render,render_to_response,get_object_or_404,redirect
from django.views.generic import ListView,CreateView
from .models import Comment,Rating
from django.db.models import Avg
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def CommentView(request):
    comment_list=Comment.objects.all().order_by('-date')
    context={
        'comment_list':comment_list,
        }
    return render(request,'comments/comment-list.html',context)

class CreateCommentView(CreateView):
    template_name='comments/comment-edit.html'
    model=Comment
    fields=['title','comment']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateCommentView, self).form_valid(form)

def detail(request,comment_id):
    comment=get_object_or_404(Comment,pk=comment_id)
    rating=Rating.objects.filter(comment=comment_id).count()
    return render(request, 'comments/detail.html', {'comment': comment,'rating':rating,})

def like(request,comment_id):
    if not Rating.objects.filter(user=request.user,comment_id=comment_id).count():
        like=Rating(user=request.user,comment_id=comment_id,value=1)
        like.save()
        return HttpResponseRedirect(reverse('comments:detail', args=(comment_id,)))
    return HttpResponseRedirect(reverse('comments:detail', args=(comment_id,)))
