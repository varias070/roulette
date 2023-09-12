from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Count
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView
from django.views import View
from django.contrib.auth.models import User

from .forms import LoginUserForm, RegisterUserForm
from .models import Game


class Home(TemplateView):
    template_name = 'roulette/home.html'


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'roulette/login.html'

    def get_success_url(self):
        return reverse_lazy('roulette:home')


class LogoutUser(LogoutView):
    next_page = 'roulette:home'


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'roulette/register.html'

    def get_success_url(self):
        return reverse('roulette:home')


class SearchView(View):

    def get_roulette_participant(self):
        games = Game.objects.all()
        result = []
        for game in games:
            result.append({"number_game": game.id, "users": game.users.all().count()})
        return result

    def get_most_active_users(self):
        # почему-то запрос User.objects.annotate(count_cells=Count("cell"), member_game=Count("game"))
        # .values("count_cells", "member_game") - работает не соответсвуя нагенирированомму sql запросу
        # агрегатная функция Avg считает среднееарефмитическое между айди связзанных обьектов и их количеством
        # поэтому иду обходным путем
        count_cells = User.objects.annotate(
            count_cells=Count("cell"),
        ).values("count_cells")
        member_game = User.objects.annotate(member_game=Count("game")).values("member_game", "id")
        result = []
        for cells, member in zip(count_cells, member_game):
            member_game = member["member_game"]
            cells = cells["count_cells"]
            if cells != 0 or member_game != 0:
                average = cells / member_game
                result.append({"id": member["id"], "avg_count_scrolling": average, "member_game": member["member_game"]})
        return result

    def get(self, request):
        roulette_participant = self.get_roulette_participant()
        most_active_users = self.get_most_active_users()
        return JsonResponse({"roulette_participant": roulette_participant, "most_active_users": most_active_users})