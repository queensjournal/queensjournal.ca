from django.conf import settings # import the settings file

def media_url(context):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'MEDIA_URL': settings.MEDIA_URL}
    
def static_url(context):
    return {'STATIC_URL': settings.STATIC_URL}