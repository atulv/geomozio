from django.http import HttpResponse

def home(request):
    return HttpResponse('use /apis/provider/ to add or get provider \nuse /apis/provider/provider_id/update/ to update provider \nuse /apis/provider/provider_id/delete/ to remove provider \nuse /apis/provider/provider_id/service-area/ to add or get service area \nuse /apis/service-area/service-area_id/update/ to update service area \nuse /apis/service-area/service-area_id/delete/ to remove service area \nuse /apis/get-service-areas/ to get list of service areas containing the given point', content_type='text/plain')
