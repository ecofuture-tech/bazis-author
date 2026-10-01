# Copyright 2026 EcoFuture Technology Services LLC and contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Django system checks of bazis-author (see `manage.py bazis_doctor`).
"""

from django.core.checks import Warning, register


#: the route actions that write the fields of the CREATE / UPDATE schema
WRITE_ACTIONS = {
    'CREATE': {'action_create'},
    'UPDATE': {
        'action_update',
        'action_post_relationships',
        'action_update_relationships',
        'action_delete_relationships',
    },
}
AUTHOR_FIELDS = ('author', 'author_updated')


def writable_author_fields(route_cls, actions: set[str]) -> list[str]:
    """
    The author fields that the route lets a client set: the fields of the CREATE and
    UPDATE schemas of the actions the route serves.
    """
    from bazis.core.schemas import CrudApiAction

    result = []
    for action_name, route_actions in WRITE_ACTIONS.items():
        if not actions & route_actions:
            continue
        fields = route_cls.build_schema_factory(getattr(CrudApiAction, action_name)).fields
        for name in AUTHOR_FIELDS:
            field = fields.get(name)
            if field is not None and not field.read_only and name not in result:
                result.append(name)
    return result


@register()
def check_routes_author(app_configs, **kwargs):
    """
    A JSON:API route of an `AuthorMixin` model must keep `author` and `author_updated` out
    of its create and update schemas (`AuthorRouteMixin` does): otherwise a client sets the
    author of a record to any user. Runs when the application is loaded
    (`manage.py bazis_doctor`).
    """
    from bazis.core.introspect import loaded_app, route_sets

    if (app := loaded_app()) is None:
        return []

    from bazis.core.routes_abstract.jsonapi import JsonapiRouteBase

    from .models_abstract import AuthorMixin

    messages = []
    for route_cls, routes in route_sets(app).items():
        model = getattr(route_cls, 'model', None)
        if not (
            issubclass(route_cls, JsonapiRouteBase)
            and isinstance(model, type)
            and issubclass(model, AuthorMixin)
        ):
            continue
        if fields := writable_author_fields(route_cls, {it['action'] for it in routes}):
            messages.append(
                Warning(
                    f'The route {route_cls.__module__}.{route_cls.__qualname__} lets a client '
                    f'set {", ".join(fields)} of {model._meta.label}.',
                    hint=(
                        'Inherit it from bazis.contrib.author.routes_abstract.AuthorRouteBase '
                        '(AuthorRequiredRouteBase, AuthorRouteMixin), or exclude the fields '
                        'from its CREATE and UPDATE schemas.'
                    ),
                    obj=route_cls,
                    id='author.W001',
                )
            )
    return messages
