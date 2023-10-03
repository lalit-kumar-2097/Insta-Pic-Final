
from django.http import JsonResponse
import json
import requests
from django.conf import settings
if not settings.configured:
    settings.configure()

# from django.conf import settings
# if not settings.configured:
#     settings.configure(default_settings='settings.py', DEBUG=True)

json_data = {'Nepal': 'Kathmandu', 'Italy': 'Rome', 'England': 'London'}

print(json_data)
print(JsonResponse({'data': json_data}, safe = False))