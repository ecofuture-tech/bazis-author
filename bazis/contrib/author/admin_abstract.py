from django.utils.translation import gettext_lazy as _

from admin_auto_filters.filters import AutocompleteFilterFactory

from bazis.core.utils.sets_order import OrderedSet


class AuthorAdminMixin:
    def get_search_fields(self, request):
        return tuple(OrderedSet(super().get_search_fields(request) + ('author__username',)))

    def get_readonly_fields(self, request, obj=None):
        return tuple(
            OrderedSet(super().get_readonly_fields(request, obj) + ('author', 'author_updated'))
        )

    def get_list_filter(self, request):
        return (AutocompleteFilterFactory(_('Author'), 'author'),) + super().get_list_filter(
            request
        )

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        else:
            obj.author_updated = request.user
        return super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for obj in instances:
            if not obj.author:
                obj.author = request.user
            else:
                obj.author_updated = request.user
            obj.save()
        formset.save_m2m()
