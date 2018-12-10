import sys, os, django

# sys.path.append("/home/ubuntu/linecare/linecare_core/")  # here store is root folder(means parent).
sys.path.append("/home/linecare/project_linecare/")  # here store is root folder(means parent).

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "linecare_core.settings")
django.setup()

import json
from django.db import IntegrityError, DataError

from drug_information.models import GenericName, Drug
from drug_information.models.drug_models import ActiveIngredient, DrugActiveIngredient

# json_src = '/home/ubuntu/linecare/documentation/drugs/openfda/endpoints/drug-ndc-0001-of-0001.json'
json_src = '/home/linecare/documentation/drugs/openfda/endpoints/drug-ndc-0001-of-0001.json'

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

        data = {
            'name': _name,
            'marketing_status': _marketing_status,
            'route': _route,
            'pharm_class': _pharm_class,
        }

        if _dosage_form:
            dosage_form = [x.strip() for x in _dosage_form.split(',')]
            data['dosage_form'] = dosage_form

        if _generic_name:
            try:
                data['generic_name'] = GenericName.objects.create(
                    name=_generic_name.lower()
                )
            except IntegrityError:
                data['generic_name'] = GenericName.objects.get(name__iexact=_generic_name)
        else:
            data['generic_name'] = None

        try:
            drug = Drug.objects.create(**data)
        except IntegrityError:
            drug = Drug.objects.get(name=_name)
        except DataError:
            print(f'{_name}')
            drug = False

        if _active_ingredients and drug:
            for active_ingredient in _active_ingredients:
                try:
                    ai = ActiveIngredient.objects.get(name=active_ingredient['name'])
                except ActiveIngredient.DoesNotExist:
                    ai = ActiveIngredient.objects.create(
                        name=active_ingredient.get('name', '')
                    )
                try:
                    DrugActiveIngredient.objects.create(
                        drug=drug,
                        active_ingredient=ai,
                        strength=active_ingredient.get('strength', '')
                    )
                except IntegrityError:
                    pass
