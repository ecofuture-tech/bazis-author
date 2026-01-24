from django.contrib import admin

from bazis.contrib.author.admin_abstract import AuthorAdminMixin
from bazis.core.admin_abstract import AutocompleteMixin, DtAdminMixin

from .models import ChildEntity, DependentEntity, ExtendedEntity, ParentEntity


@admin.register(ChildEntity)
class ChildEntityAdmin(AuthorAdminMixin, AutocompleteMixin, DtAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'child_name', 'child_is_active')
    list_filter = ('child_is_active',)
    search_fields = ('child_name', 'child_description')


@admin.register(DependentEntity)
class DependentEntityAdmin(AuthorAdminMixin, AutocompleteMixin, DtAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'dependent_name', 'dependent_is_active')
    list_filter = ('dependent_is_active',)
    search_fields = ('dependent_name', 'dependent_description')


@admin.register(ExtendedEntity)
class ExtendedEntityAdmin(AuthorAdminMixin, AutocompleteMixin, DtAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'extended_name', 'extended_is_active')
    list_filter = ('extended_is_active',)
    search_fields = ('extended_name', 'extended_description')


class ChildEntityInline(AuthorAdminMixin, AutocompleteMixin, admin.TabularInline):
    model = ParentEntity.child_entities.through
    extra = 0


class DependentEntityInline(AuthorAdminMixin, AutocompleteMixin, admin.TabularInline):
    model = DependentEntity
    extra = 0


class ExtendedEntityInline(AuthorAdminMixin, AutocompleteMixin, admin.TabularInline):
    model = ExtendedEntity
    extra = 0


@admin.register(ParentEntity)
class ParentEntityAdmin(AuthorAdminMixin, AutocompleteMixin, DtAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    inlines = (ChildEntityInline, DependentEntityInline, ExtendedEntityInline)
