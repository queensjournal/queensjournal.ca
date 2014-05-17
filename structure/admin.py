from structure.models import FlatPlanSection,\
    FlatPlanConfig, FrontPageConfig
from django.contrib import admin



class FlatPlanSectionInline(admin.TabularInline):
    model = FlatPlanSection


class FlatPlanConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'list_sections')
    inlines = [
        FlatPlanSectionInline,
    ]


admin.site.register(FlatPlanConfig, FlatPlanConfigAdmin)


class FrontPageConfigAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request):
        return False


admin.site.register(FrontPageConfig, FrontPageConfigAdmin)
