import sys, os, django

# sys.path.append("/home/ubuntu/linecare/linecare_core/")  # here store is root folder(means parent).
sys.path.append("/home/linecare/project_linecare/")  # here store is root folder(means parent).

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "linecare_core.settings")
django.setup()

import json
from django.db import IntegrityError, DataError

from drug_information.models import GenericName, Drug
from drug_information.models.drug_models import ActiveIngredient, DrugActiveIngredient, DosageForm, DrugDosageForm, \
    PharmaceuticalClass, DrugPharmaceuticalClass, DrugRoute, DrugRouteDelivery

# json_src = '/home/ubuntu/linecare/documentation/drugs/openfda/endpoints/drug-ndc-0001-of-0001.json'
json_src = '/home/linecare/documentation/drugs/openfda/endpoints/sample.json'

with open(json_src) as j:
    data = json.load(j)

for med in data['results']:
    _generic_name = med.get('generic_name', None)
    _name = med.get('brand_name', None)
    _base_name = med.get('brand_name_base', None)
    _marketing_status = med.get('product_type', None)
    _route = med.get('route', None)
    _active_ingredients = med.get('active_ingredients', None)
    _pharm_class = med.get('pharm_class', None)
    _dosage_form = med.get('dosage_form', None)

    if _name and (_marketing_status == 'HUMAN OTC DRUG' or _marketing_status == 'HUMAN PRESCRIPTION DRUG'):
        print(f'{_name}...')

        print(f'{type(_route)}: {_route}')

        if _generic_name:
            generic_names = [x.strip for x in _generic_name.split(',')]
            data['meta'] = {
                'generic_names': json.dumps(generic_names)
            }
