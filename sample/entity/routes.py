from django.apps import apps

from bazis.contrib.author.routes_abstract import AuthorRequiredRouteBase, AuthorRouteBase
from bazis.core.schemas import SchemaFields


class ChildEntityRouteSet(AuthorRouteBase):
    model = apps.get_model('entity.ChildEntity')

    fields = {
        None: SchemaFields(
            include={
                'parent_entities': None,
            },
        ),
    }


class DependentEntityRouteSet(AuthorRouteBase):
    model = apps.get_model('entity.DependentEntity')


class ExtendedEntityRouteSet(AuthorRequiredRouteBase):
    model = apps.get_model('entity.ExtendedEntity')


class ParentEntityRouteSet(AuthorRouteBase):
    model = apps.get_model('entity.ParentEntity')

    # add fields (extended_entity, dependent_entities) to schema
    fields = {
        None: SchemaFields(
            include={'extended_entity': None, 'dependent_entities': None},
        ),
    }
