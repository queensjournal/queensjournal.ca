from django.contrib.admin import ModelAdmin


class HiddenAdminModel(ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
