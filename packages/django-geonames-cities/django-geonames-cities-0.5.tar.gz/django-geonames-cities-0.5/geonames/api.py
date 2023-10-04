import json

from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse

from geonames.models import Country, GeonamesAdm1, GeonamesAdm2, GeonamesAdm3, \
    GeonamesAdm4, GeonamesAdm5, PopulatedPlace


@login_required
def countries(request):
    try:
        q = request.GET.get('term', '')
        countries = Country.objects.filter(name__icontains=q)
        results = []
        for c in countries:
            country_json = {
                'id': c.id,
                'label': c.name,
                'code': c.code,
                'value': c.name,
                'data_loaded': c.data_loaded,
                'nic_type': '',
                'nic_input_mask': '',
                'it_codice_catastale': c.it_codice_catastale
            }
            # if used with geonames_address ...
            if hasattr(c, 'nationalidentificationcodetype_set') and c.nationalidentificationcodetype_set.count() > 0:
                # TODO: we start with just one, make it a list and manage the choice of the type
                country_json['nic_type'] = c.nationalidentificationcodetype_set.all()[0].name
                country_json['nic_input_mask'] = c.nationalidentificationcodetype_set.all()[0].input_mask
            results.append(country_json)
        data = json.dumps(results)
    except:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


#@login_required
def municipalities(request):
    try:
        q = request.GET.get('term', '')
        country_id = request.GET.get('country_id', '')
        country = Country.objects.get(id=country_id)
        results = []
        content_types = []
        for ml in country.municipality_levels.split(" "):
            content_types.append(ContentType.objects.get(app_label='geonames', model__iexact=ml))
        municipalities = []
        n_of_results = 20
        for ct in content_types:
            if ct.model == "geonamesadm1":
                municipalities += GeonamesAdm1.objects.filter(name__icontains=q, country__id=country_id)[:n_of_results]
            elif ct.model == "geonamesadm2":
                municipalities += GeonamesAdm2.objects.filter(name__icontains=q, adm1__country__id=country_id)[
                                  :n_of_results]
            elif ct.model == "geonamesadm3":
                municipalities += GeonamesAdm3.objects.filter(name__icontains=q, adm2__adm1__country__id=country_id)[
                                  :n_of_results]
            elif ct.model == "geonamesadm4":
                municipalities += GeonamesAdm4.objects.filter(name__icontains=q,
                                                              adm3__adm2__adm1__country__id=country_id)[:n_of_results]
            elif ct.model == "geonamesadm5":
                municipalities += GeonamesAdm5.objects.filter(name__icontains=q,
                                                              adm4__adm3__adm2__adm1__country__id=country_id)[
                                  :n_of_results]
            elif ct.model == "populatedplace":
                municipalities += PopulatedPlace.objects.filter(name__icontains=q, country__id=country_id)[
                                  :n_of_results]
        # TODO: if I have an exact match I send it as the first result;
        #  also if it starts with is to be prioritizes ws contains
        municipalities.sort(key=lambda x: x.name)
        for m in municipalities:
            municipality_json = {}
            municipality_json['id'] = m.id
            municipality_json['label'] = m.name
            municipality_json['value'] = m.name
            municipality_json['content_type'] = ct.model
            municipality_json['content_type_id'] = ct.id
            if ct.model == "geonamesadm3" and country.code == 'IT':
                municipality_json['label'] = ("%s ( %s )" % (m.name, m.adm2.code))
                municipality_json['value'] = municipality_json['label']
                municipality_json['codice_catastale'] = m.it_codice_catastale
            results.append(municipality_json)
        data = json.dumps(results)
    except:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
