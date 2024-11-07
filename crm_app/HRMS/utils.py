import json
from django.conf import settings

def load_country_data():
    json_path = f"{settings.BASE_DIR}/crm_app/static/data/country_states_phonecode.json"
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)