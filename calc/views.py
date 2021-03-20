# Create your views here.
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from .forms import ValidateFormSerializer
from .models import Truck, Storage

import json
from decimal import Decimal, DecimalException

# shapely import.
from shapely.geometry import Point
import shapely.wkt


import logging
logger = logging.getLogger(__name__)


# Data output for the template
def manage_storages(request):
    context = {}
    storages = Storage.objects.all()
    for str in storages:
        context[str] = list(Truck.objects.filter(is_online=True, storage=str))
    return render(request, 'calc/detail/detail.html',
                  {'context': context,
                   })


def check_entry_of_point(point, polygon):
    return polygon.contains(point)


def update_storages_data(post_data):
    for str, trucks in post_data['storage_data'].items():

        capacity_Fe = 0
        capacity_SiO2 = 0
        capacity_none_type = 0

        storage = Storage.objects.get(id=str)
        polygon = shapely.wkt.loads(storage.coordinates)

        for id, val in trucks['trucks_data'].items():
            point = Point(val['coordinate_x'], val['coordinate_y'])
            if check_entry_of_point(point, polygon):
                truck = Truck.objects.get(id=id)
                capacity_Fe += truck.carrying_capacity * truck.percentage_Fe
                capacity_SiO2 += truck.carrying_capacity * truck.percentage_SiO2
                capacity_none_type += truck.carrying_capacity * \
                    (1 - (truck.percentage_Fe + truck.percentage_SiO2))

        new_capacity_Fe = capacity_Fe + storage.capacity * storage.percentage_Fe
        new_capacity_SiO2 = capacity_SiO2 + storage.capacity * storage.percentage_SiO2
        new_capacity = (new_capacity_Fe +
                        new_capacity_SiO2 +
                        (capacity_none_type +
                         (storage.capacity -
                          ((storage.capacity *
                            storage.percentage_Fe) +
                           (storage.capacity *
                            storage.percentage_SiO2)))))

        try:
            new_persanage_Fe = new_capacity_Fe / new_capacity
            new_persanage_SiO2 = new_capacity_SiO2 / new_capacity
        except (ValueError, DecimalException):
            new_persanage_Fe = 0.0
            new_persanage_SiO2 = 0.0

        storage.capacity = new_capacity
        storage.percentage_SiO2 = new_persanage_SiO2
        storage.percentage_Fe = new_persanage_Fe
        storage.save()


@require_POST
def coordinate_update(request):
    valid_ser = ValidateFormSerializer(data=json.loads(request.POST['data']))
    if valid_ser.is_valid():
        post_data = valid_ser.validated_data
        update_storages_data(post_data)
    else:
        print(valid_ser.errors)
    return JsonResponse({"update": "OK"})
