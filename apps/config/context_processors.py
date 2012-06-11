from config.models import SiteConfig


def global_config(request):
    config, created = SiteConfig.objects.get_or_create(pk=1)
    return {'config': config}
