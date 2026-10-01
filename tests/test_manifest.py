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

from django.apps import apps

import pytest

from bazis.contrib.author.checks import check_routes_author
from bazis.contrib.users.routes_abstract import UserRouteBase
from bazis.core.introspect import validate_manifest


def test_manifest_is_valid():
    assert validate_manifest('bazis.contrib.author') == []


@pytest.mark.django_db
def test_routes_author(sample_app, monkeypatch):
    # the routes of the sample inherit AuthorRouteBase
    assert check_routes_author(None) == []

    class PlainRouteSet(UserRouteBase):
        model = apps.get_model('entity.ParentEntity')

    def actions(*names):
        return {PlainRouteSet: [{'path': '/', 'methods': [], 'action': it} for it in names]}

    monkeypatch.setattr(
        'bazis.core.introspect.route_sets', lambda app: actions('action_list', 'action_create')
    )
    assert [it.id for it in check_routes_author(None)] == ['author.W001']

    # a read-only route does not let the client set the author
    monkeypatch.setattr(
        'bazis.core.introspect.route_sets', lambda app: actions('action_list', 'action_retrieve')
    )
    assert check_routes_author(None) == []
