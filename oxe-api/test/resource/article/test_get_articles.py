import datetime

from test.BaseCase import BaseCase


class TestGetArticles(BaseCase):

    @BaseCase.login
    def test_ok(self, token):
        self.db.insert({
                "id": 1,
                "title": "TITLE",
                "publication_date": datetime.date.today() + datetime.timedelta(days=1)
            }, self.db.tables["Article"])
        self.db.insert({
                "id": 2,
                "title": "TITLE2",
                "publication_date": datetime.date.today()
            }, self.db.tables["Article"])

        response = self.application.get('/article/get_articles',
                                        headers=self.get_standard_header(token))

        self.assertEqual(200, response.status_code)
        self.assertEqual([
            {
                'abstract': None,
                'end_date': None,
                'external_reference': None,
                'handle': None,
                'id': 1,
                'image': None,
                'is_created_by_admin': 0,
                'link': None,
                'publication_date': (datetime.date.today() + datetime.timedelta(days=1))
                    .strftime('%Y-%m-%d') + "T00:00:00",
                'start_date': None,
                'status': 'DRAFT',
                'sync_content': None,
                'sync_global': None,
                'sync_id': None,
                'sync_node': None,
                'sync_status': 'OK',
                'title': 'TITLE',
                'type': 'NEWS'
            },
            {
                'abstract': None,
                'end_date': None,
                'external_reference': None,
                'handle': None,
                'id': 2,
                'image': None,
                'is_created_by_admin': 0,
                'link': None,
                'publication_date': datetime.datetime.today().strftime('%Y-%m-%d') + "T00:00:00",
                'start_date': None,
                'status': 'DRAFT',
                'sync_content': None,
                'sync_global': None,
                'sync_id': None,
                'sync_node': None,
                'sync_status': 'OK',
                'title': 'TITLE2',
                'type': 'NEWS'
            },
        ], response.json)
