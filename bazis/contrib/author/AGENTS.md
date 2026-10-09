# bazis-author — guide for AI agents

Author fields for Bazis models: `author` (who created the record) and `author_updated`
(who changed it last), filled from the user of the request. Clients cannot set them.
Needs bazis-users. bazis-permit uses `author` as the selector `author`
(`entity.document.item.change.author`).

## Setup

```python
from bazis.contrib.author.admin_abstract import AuthorAdminMixin
from bazis.contrib.author.models_abstract import AuthorMixin
from bazis.contrib.author.routes_abstract import AuthorRequiredRouteBase, AuthorRouteBase

class Document(AuthorMixin, DtMixin, UuidMixin, JsonApiMixin):
    title = models.CharField('Title', max_length=255)

class DocumentRouteSet(AuthorRouteBase):         # or AuthorRequiredRouteBase (401 for anonymous)
    model = apps.get_model('docs.Document')

@admin.register(Document)
class DocumentAdmin(AuthorAdminMixin, DtAdminMixin, admin.ModelAdmin):
    ...
```

- Add `bazis.contrib.author` to `BS_INSTALLED_APPS` (it registers the system check). The
  package has no models and no settings; `makemigrations` adds the two foreign keys
  (`on_delete=SET_NULL`, nullable) to each model with `AuthorMixin`.
- With bazis-permit: `class DocumentRouteSet(PermitRouteBase, AuthorRouteBase)`.

## How the fields are filled

- `AuthorRouteMixin` (in `AuthorRouteBase`, `AuthorRequiredRouteBase`) excludes `author`
  and `author_updated` from the CREATE and UPDATE schemas, so neither the attributes nor
  the relationships endpoints accept them, and sets `author` in `hook_before_create`,
  `author_updated` in `hook_before_update`. An anonymous request does not set them.
- `AuthorMixin.save()` sets `author` (if empty) and `author_updated` from
  `UserMixin.CTX_USER_REQUEST` of bazis-users: the user routes set it (`UserRouteBase`),
  Django views only with `bazis.contrib.users.middleware.UserRequestMiddleware` in
  `MIDDLEWARE`. Without a user in the context (Celery tasks, shell, management commands)
  the fields stay as they are: set them explicitly there.
- `AuthorAdminMixin` sets `author` from `request.user` if it is empty, `author_updated`
  otherwise (also in inline formsets), makes both fields read-only, adds the search by
  `author__username` and an autocomplete filter by author (the admin of the user model
  needs `search_fields`).

## Titles

The fields have no `verbose_name`: the schemas title them `author` and `author updated`,
in every language. Give them a title in the route, without a migration
(`SchemaField` of `bazis.core.schemas`, `gettext_lazy as _`):

```python
class DocumentRouteSet(AuthorRouteBase):
    fields = {
        None: SchemaFields(include={
            'author': SchemaField(source='author', title=_('Author')),
            'author_updated': SchemaField(source='author_updated', title=_('Updated by')),
        }),
    }
```

The CREATE and UPDATE schemas still leave them out (`AuthorRouteMixin` excludes them, and
an exclusion wins). Redeclaring the fields on the model also titles them, at the cost of a
migration of each model.

## Rules

- Every JSON:API route of an `AuthorMixin` model inherits `AuthorRouteMixin` (usually
  through `AuthorRouteBase`): with a plain route a client sets the author to any user
  (`author.W001`, `manage.py bazis_doctor`).
- Never add `author` or `author_updated` to the `include` of a CREATE or UPDATE schema.
