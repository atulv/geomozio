import json
from django.shortcuts import render
from mozio.models import Provider, ServiceArea
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.contrib.gis.geos import Polygon, Point
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
from django.db import IntegrityError

@csrf_exempt
def provider(request):
    """Creates a provider if request is POST and retrives if reqeust if GET."""
    if request.method == 'POST':
        return add_provider(request)
    else:
        return get_provider(request)

def add_provider(request):
    """
    Creates provider, accepts name,email,phone,language,currenct as
    POST params.
    """
    errors = []
    resp = {}
    name = request.POST.get('name').strip()
    if not name:
        errors.append('invalid value for name')
    email = request.POST.get('email').strip()
    try:
        validate_email(email)
    except ValidationError:
        errors.append('invalid value for email')
    phone = request.POST.get('phone').strip()
    if not phone:
        errors.append('invalid value for phone')
    language = request.POST.get('language').strip()
    if not language:
        errors.append('invalid value for language')
    currency = request.POST.get('currency').strip()
    if not currency:
        errors.append('invalid value for currency')
    
    if errors:
        resp['errors'] = errors
        return HttpResponse(json.dumps(resp), content_type='application/json')

    try:
        Provider.objects.create(name=name, email=email, phone=phone, language=language, currency=currency)
    except IntegrityError:
        return HttpResponse('email %s already in use'%email, content_type='text/plain')
    return HttpResponse(json.dumps(resp), content_type='application/json')

def get_provider(request):
    """Retrieves provider by email."""
    provider_email = request.GET.get('email')
    try:
        provider = Provider.objects.get(email=provider_email)
    except Provider.DoesNotExist:
        pass
    else:
        return HttpResponse(json.dumps({'provider':provider.to_json()}), content_type='application/json')
    return HttpResponse(json.dumps({'provider':{}}), content_type='application/json')

@csrf_exempt
def update_provider(request, provider_id):
    """Updates provider's infromation."""
    try:
        provider = Provider.objects.get(id=provider_id)
    except Provider.DoesNotExist:
        return HttpResponseBadRequest('Invalid provider', content_type='text/plain')
    
    provider.name = request.POST.get('name',' ').strip() or provider.name
    provider.phone = request.POST.get('phone',' ').strip() or provider.phone
    email = request.POST.get('email',' ').strip()
    if email:
        try:
            validate_email(email)
            provider.email = email
        except ValidationError:
            return HttpResponseBadRequest('invalid value for email', content_type='text/plain')
    
    provider.language = request.POST.get('language',' ').strip() or provider.language
    provider.currency = request.POST.get('currency',' ').strip() or provider.currency
    try:
        provider.save()
    except IntegrityError:
       return HttpResponseBadRequest('email %s already in use'%email, content_type='text/plain')
    return HttpResponse('provider sucessfully updated', content_type='text/plain')

@csrf_exempt
def remove_provider(request, provider_id):
    """Removes provider with id provider_id."""
    try:
        provider = Provider.objects.get(id=provider_id)
    except Provider.DostNotExist:
        return HttpResponseBadRequest('provider does not exist', content_type='text/plain')
    provider.delete()
    return HttpResponse('provider deleted successfully', content_type='text/plain')

@csrf_exempt
def service_area(request, provider_id):
    """Creates service area if request is POST and retrieves if request is GET."""
    if request.method == 'POST':
        return add_service_area(request, provider_id)
    else:
        return get_service_area()

def add_service_area(request, provider_id):
    """Creates service area, accepts name, price, geojson."""
    errors = []
    name = request.POST.get('name')
    price = request.POST.get('price')
    geojson = request.POST.get('geojson')
    if not name:
        errors.append('invalid value for name')
    if not price:
        errors.append('invalid value for price')
    try:
        geojson = json.loads(geojson)
    except ValueError:
        errors.append('invalid value for geojson')

    if errors:
        return HttpResponseBadRequest(json.dumps({'errors':errors}), content_type='application/json')
    
    try:
        polygon = Polygon(*geojson['coordinates'])
    except Exception, e:
        return HttpResponseBadRequest(e, content_type='text/plain')
    ServiceArea.objects.create(name=name, price=price, provider_id=provider_id, region=polygon)

    return HttpResponse('service area added successfully', content_type='text/plain')

def get_service_area(request):
    """Retrieves service area by provider_id and name."""
    service_area_name = request.GET.get('name')
    provider_id = request.GET.get('provider_id')
    try:
        service_area = ServiceArea.objects.get(provider_id=provider_id, name=service_area_name)
    except ServiceArea.DoesNotExist:
        pass
    else:
        return HttpResponse(json.dumps({'service_area': service_area.to_json()}), content_type='application/json')
    return HttpResonse(json.dumps({'service_area':{}}), content_type='application/json')

@csrf_exempt
def update_service_area(request, service_area_id):
    """Updates name, price and region of service area."""
    try:
        service_area = ServiceArea.objects.get(id=service_area_id)
    except ServiceArea.DoesNotExist:
        return HttpResponseBadRequest('invalid service area', content_type='text/plain')
    name = request.POST.get('name').strip()
    if name:
        service_area.name = name
    price = request.POST.get('price')
    try:
        price = float(price)
    except ValueError:
        return HttpResponseBadRequest('invalid value for price', content_type='text/plain')
    service_area.price = price
    geojson = request.POST.get('geojson')
    if geojson:
        try:
            polygon = json.loads(geojson)
            service_area.region = Polygon(geojson["coordinates"])
        except ValueError:
            return HttpResponseBadRequest('invalid value for geojson', content_type='text/plain')
    service_area.save()
    return HttpResponse('updated service area successfully', 'text/plain')

@csrf_exempt
def remove_service_area(request, service_area_id):
    """Deletes service area with id service_area_id."""
    try:
        service_area = ServiceArea.objects.get(id=service_area_id)
    except ServiceArea.DoesNotExist:
        return HttpResponseBadRequest('invalid service_area_id', content_type='text/plain')
    service_area.delete()

    return HttpResponse('service area deleted successfully', content_type='text/plain')

def query_service_area(request):
    """
    Returns all the service ares containing the point
    
    """
    lngt = request.GET.get('lat')
    latt = request.GET.get('lng')
    
    try:
        lngt = float(lngt)
    except ValueError:
        return HttpResponseBasRequest('invalid value for longitude', content_type='text/plain')
    
    try:
        latt = float(latt)
    except ValueError:
        return HttpResponseBasRequest('invalid value for lattitude', content_type='text/plain')
    
    if lngt and latt:
        point = Point(latt, lngt)
        region_containing_point = ServiceArea.objects.filter(region__contains=point)
        service_area_list = [service_area.to_json() for service_area in region_containing_point]
        return HttpResponse(json.dumps({'service_area_list':service_area_list}), content_type='application/json')
    else:
        return HttpResponseBadRequest('invalid lngt or latt', content_type='text/plain')

