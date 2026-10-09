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
The title of the author fields in the schemas: the fields have no verbose_name, a route
gives them a title (`SchemaField(title=...)`, sample `DependentEntityRouteSet`) without a
migration.
"""

import pytest
from bazis_test_utils.utils import get_api_client


def relation_titles(schema: dict) -> dict:
    relationships = next(
        v
        for k, v in schema['$defs'].items()
        if k.endswith('__Relationships') and 'author' in v.get('properties', {})
    )
    return {
        name: relationships['properties'][name]['title'] for name in ('author', 'author_updated')
    }


@pytest.mark.django_db(transaction=True)
def test_route_gives_the_author_fields_a_title(sample_app):
    response = get_api_client(sample_app).get('/api/v1/entity/dependent_entity/schema_list/')

    assert response.status_code == 200
    assert relation_titles(response.json()) == {'author': 'Author', 'author_updated': 'Updated by'}

    # without a title of the route: the names of the fields
    response = get_api_client(sample_app).get('/api/v1/entity/parent_entity/schema_list/')
    assert relation_titles(response.json()) == {
        'author': 'author',
        'author_updated': 'author updated',
    }
