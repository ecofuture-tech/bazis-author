from bazis.contrib.users.routes_abstract import UserRequiredRouteBase, UserRouteBase
from bazis.core.routes_abstract.jsonapi import JsonapiRouteBase
from bazis.core.schemas import ApiAction, CrudApiAction, SchemaFields

from .models_abstract import AuthorMixin


class AuthorRouteMixin(JsonapiRouteBase):
    abstract: bool = True

    fields: dict[ApiAction, SchemaFields] = {
        CrudApiAction.CREATE: SchemaFields(
            exclude={'author': None, 'author_updated': None},
        ),
        CrudApiAction.UPDATE: SchemaFields(
            exclude={'author': None, 'author_updated': None},
        ),
    }

    def hook_before_create(self, item: AuthorMixin):
        if not self.inject.user.is_anonymous:
            item.author = self.inject.user
        super().hook_before_create(item)

    def hook_before_update(self, item: AuthorMixin):
        if not self.inject.user.is_anonymous:
            item.author_updated = self.inject.user
        super().hook_before_update(item)


class AuthorRouteBase(AuthorRouteMixin, UserRouteBase):
    abstract: bool = True


class AuthorRequiredRouteBase(AuthorRouteMixin, UserRequiredRouteBase):
    abstract: bool = True
