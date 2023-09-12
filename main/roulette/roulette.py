import random
import json

from django.conf import settings
from django.http import JsonResponse
from django.views import View

from .models import Cell, Game


# создает игру и ячейки для нее далее связывает их в бд отношением многие ко многим.
class StartView(View):

    def __init__(self, *args, **kwargs):
        super(StartView, self).__init__(*args, **kwargs)
        self.cells = self.__create_cells()
        self.length = len(self.cells)

    @staticmethod
    def __create_cells():
        result = {}
        for cell, weight in zip(settings.CELLS, settings.WEIGHT):
            result[cell] = weight
        return result

    def post(self, request):
        try:
            game = Game.objects.get(is_actual=True)
            return JsonResponse(data={"game_id": game.id})
        except Game.DoesNotExist:
            game = Game.objects.create()
            for cell in self.cells.keys():
                query = Cell.objects.create(title=cell, weight=self.cells[cell], game=game)
                query.save()
            return JsonResponse(data={"game_id": game.id})


# выбирает из возможных ячеек одну, если выпал джекпот делае игру неактуальной(все логируется в бд)
# стиль кода в этом классе для меня эксперементальный, прошу дать оценку в обратной связи
class TwistView(View):

    def __init__(self, *args, **kwargs):
        super(TwistView, self).__init__(*args, **kwargs)
        self.game = None
        self.find_cell = None
        self.index_find_cell = None
        self.cells = None

    def twist(self):
        weight_sum = 0
        for cell in self.cells:
            weight_sum += cell.weight
        index_sum = random.randint(0, weight_sum)
        for index, cell in enumerate(self.cells):
            index_sum -= cell.weight
            if index_sum < 0:
                self.find_cell = cell
                self.index_find_cell = index
                break
            if cell.title == "jackpot" and len(self.cells) == 1:
                self.find_cell = cell

    def update_find_cell(self, request):
        self.find_cell.user = request.user
        self.find_cell.is_actual = False
        self.find_cell.save()

    def add_user(self, request):
        users = [user.username for user in self.game.users.all()]
        if request.user not in users:
            self.game.users.add(request.user)

    def post(self, request):
        self.game = Game.objects.get(id=json.loads(request.body)["game_id"])
        self.add_user(request)
        self.cells = Cell.objects.filter(is_actual=True, game=self.game)
        self.twist()
        self.update_find_cell(request)

        if self.find_cell.title == "jackpot":
            self.game.is_actual = False
            self.game.save()
        return JsonResponse({"cell_title": self.find_cell.title, "is_actual":  self.game.is_actual})
