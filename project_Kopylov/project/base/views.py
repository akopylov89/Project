from django.http import HttpResponse, Http404
from datetime import datetime,date
from django.http import HttpResponseRedirect
from models import Players, StatPlayerGames
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from project.settings import QUANTITY_FOR_PAGE
from . import forms
from . import models
from django.shortcuts import get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required()
def baseview(request):
    return render(request, 'base.html')

def logout_view(request):
    logout(request)
    return render(request, 'logout.html')

def account_view(request):
    return render(request, 'base.html')

def change_player_xp(request, player_id):
    player = Players.objects.get(id=player_id)
    form = forms.ChangePlayerXp(data={"id": player.id, "xp": player.xp})
    if request.method == 'POST':
        form = forms.ChangePlayerXp(request.POST)
        if form.is_valid():
            error = False
            player.xp = form.cleaned_data["xp"]
            if player.xp < 0 or player.xp > 2147483647:
                error = True
                return render(request, 'xp_change_form.html', {'error': error})
            else:
                player.save()
                return HttpResponseRedirect("/playerchanged/%d" % player.id)

    template_data = {
        "form": form,
        "player": player
    }

    return render(request, 'xp_change_form.html', template_data)

def playerchanged(request, player_id):
    template_data = {
        "player_id": player_id
    }
    return render(request, "playerchanged.html", template_data)

def userinfo(request):
    form = forms.Searchbyemail()
    if 'email' in request.GET:
        searched_email = request.GET['email']
        player_list = Players.objects.filter(email=searched_email)

    else:
        player_list = Players.objects.all()
    error = False
    if len(player_list) < 1:
        error = True
    else:
        page = request.GET.get('page')
        paginator = Paginator(player_list, QUANTITY_FOR_PAGE)
        try:
            player_list = paginator.page(page)

        except PageNotAnInteger:
            player_list = paginator.page(1)

        except EmptyPage:
            player_list = paginator.page(paginator.num_pages)

    template_data = {
        "form": form,
        "players": player_list,
        "version": "1.0",
        "error": error
    }
    return render(request, 'user_info.html', template_data)

def stat_player_games(request):
    form = forms.StatPlayerGamesSearch()
    if 'start_with_year' in request.GET:
        start_year = request.GET['start_with_year']
        print(start_year)
        stat_list = StatPlayerGames.objects.filter(target_date__gte = date(int(start_year),1,1))
        if 'end_with_year' in request.GET:
            end_year = request.GET['end_with_year']
            stat_list = StatPlayerGames.objects.filter(target_date__gte = date(int(start_year),1,1),
                                                       target_date__lte = date(int(end_year),1,1))
            if 'start_with_month' in request.GET:
                start_month = request.GET['start_with_month']
                stat_list = StatPlayerGames.objects.filter(target_date__gte = date(int(start_year),int(start_month),1),
                                                           target_date__lte = date(int(end_year),1,1))
                if 'end_with_month' in request.GET:
                    end_month = request.GET['end_with_month']
                    stat_list = StatPlayerGames.objects.filter(target_date__gte = date(int(start_year),int(start_month),1),
                                                               target_date__lte = date(int(end_year),int(end_month),1))
                    if 'start_with_day' in request.GET:
                        start_day = request.GET['start_with_day']
                        stat_list = StatPlayerGames.objects.filter(target_date__gte = date(int(start_year),int(start_month),int(start_day)),
                                                                   target_date__lte = date(int(end_year),int(end_month),1))
                        if 'end_with_day' in request.GET:
                            end_day = request.GET['end_with_day']
                            stat_list = StatPlayerGames.objects.filter(target_date__gte = date(int(start_year),int(start_month),int(start_day)),
                                                                       target_date__lte = date(int(end_year),int(end_month),int(end_day)))
    else:
        stat_list = StatPlayerGames.objects.all()
    error = False
    if len(stat_list) < 1:
        error = True
    page = request.GET.get('page')
    paginator = Paginator(stat_list, QUANTITY_FOR_PAGE)
    try:
        stat_list = paginator.page(page)
    except PageNotAnInteger:
        stat_list = paginator.page(1)

    except EmptyPage:
        stat_list = paginator.page(paginator.num_pages)
    template_data = {
        "form": form,
        "stat_list": stat_list,
        "version": "1.0",
        "error": error
        }
    return render(request, 'stat_player_games.html', template_data)


# Create your views here.
