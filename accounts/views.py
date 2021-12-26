from django.core.checks import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from youtuber.models import MyYoutuber, YoutuberList
from django.urls import reverse
from allauth.account.views import PasswordChangeView
from .models import User
from django.contrib import messages
# from django.contrib.auth.models import User
# from django.contrib import auth

@login_required
def my_page(request, user_id):

    my_youtubers = MyYoutuber.objects.filter(user=user_id, activated=True).order_by('-listed_date')
    my_youtubers_count = my_youtubers.count()
    my_youtuber_lists = YoutuberList.objects.filter(myyoutuberlist__user=user_id, myyoutuberlist__activated=True)
    my_youtuber_lists_count = my_youtuber_lists.count()

    context = {
        'my_youtuber': my_youtubers,
        'my_youtuber_count': my_youtubers_count,
        'my_youtuber_lists': my_youtuber_lists,
        'my_youtuber_lists_count': my_youtuber_lists_count
        }
    
    return render(request, 'accounts/mypage.html', context)


class CustomPasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        return reverse("youtuber:index")

@login_required
def change_nickname(request):
    if request.method == 'POST':
        change_nickname = request.POST.get('change_nickname')
        try:
            user = User.objects.get(nickname=change_nickname)
            messages.info(request, '중복된 닉네임이 있습니다')
            return redirect('account_change_nickname')
        except ObjectDoesNotExist:
            request.user.nickname = change_nickname
            request.user.save()
            messages.info(request, '닉네임 변경 완료')
            return redirect('account_change_nickname')
    return render(request, 'accounts/change_nickname.html')
    
