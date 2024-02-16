from wagtail import VERSION as WAGTAIL_VERSION

if WAGTAIL_VERSION >= (5, 1):
    from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
else:
    from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import TestModelAdminOne, TestModelAdminThree, TestModelAdminTwo


class TestModelAdminOneAdmin(ModelAdmin):
    model = TestModelAdminOne
    menu_label = "Model Admin One"
    menu_icon = "pilcrow"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("title",)
    search_fields = ("title",)


modeladmin_register(TestModelAdminOneAdmin)


class TestModelAdminTwoAdmin(ModelAdmin):
    model = TestModelAdminTwo
    menu_label = "Model Admin Two"
    menu_icon = "pilcrow"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("title",)
    search_fields = ("title",)


modeladmin_register(TestModelAdminTwoAdmin)


class TestModelAdminThreeAdmin(ModelAdmin):
    model = TestModelAdminThree
    menu_label = "Model Admin Three"
    menu_icon = "pilcrow"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("title",)
    search_fields = ("title",)


modeladmin_register(TestModelAdminThreeAdmin)
