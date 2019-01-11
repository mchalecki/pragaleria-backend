import json


def get_endpoint_result(client, endpoint):
	res = client.get(endpoint)
	return json.loads(res.data.decode('utf-8'))


def test_all_author_details_satisfy_same_structure(client):
	for author in get_endpoint_result(client, '/api/authors'):
		author_details = get_endpoint_result(
			client, '/api/authors/{}'.format(author['id'])
		)

		author_fields = {
			'id': int,
			'name': str,
			'slug': str,
			'description': str,
			'image_thumbnail': str,
			'artworks': list
		}

		artwork_fields = {
			'id': int,
			'title': str,
			'description': str,
			'sold': bool,
			'initial_price': str,
			'sold_price': str,
			'year': str,
			'image_original': str,
			'image_thumbnail': str
		}

		for author_key in author_fields.keys():
			assert type(author_details[author_key]) is author_fields[author_key]

			for artwork in author_details['artworks']:
				for artwork_key in artwork_fields.keys():
					assert type(artwork[artwork_key]) is artwork_fields[artwork_key]


def test_if_no_duplicate_artworks(client):
	""" For example Jacek Malinowski id: 15 has identical
		artworks in the database, we would like to filter those out. """
	for author in get_endpoint_result(client, '/api/authors'):
		author_details = get_endpoint_result(
			client, '/api/authors/{}'.format(author['id'])
		)

		artwork_titles = [artwork['title'] for artwork in author_details['artworks']]
		assert len(artwork_titles) == len(set(artwork_titles))


def test_404_if_author_does_not_exist(client):
	res = client.get('/api/authors/9997')
	data = json.loads(res.data.decode('utf-8'))
	assert 'Author does not exist. id: 9997' in data['message']


def test_if_author_has_no_artworks_than_it_does_not_fail(client):
	res = client.get('/api/authors/250')
	data = json.loads(res.data.decode('utf-8'))
	assert data == {
		"id": 250,
		"name": "Małgorzata Warias /Małgorzata Fenrych/",
		"slug": "malgorzata-warias-malgorzata-fenrych",
		"description": (
			"Studiowała malarstwo pod kierunkiem prof. "
			"Z. Grzywacza, następnie prof. S. Wiśniewskiego "
			"oraz prof. A. Rzepki. Dyplom realizowała w pracowni malarstwa sztalugowego na Wydziale "
			"Architektury i Sztuk Pięknych Akademii im. A. Frycza "
			"Modrzewskiego w Krakowie pod kierunkiem prof. Ł. Konieczko. "
			"Autorka wystaw indywidualnych: Salon Artystyczny Dettlofów "
			"(2005), Klub Kultury Paleta (2005), Spokój i Cisza (2007) "
			"oraz uczestniczka kilku wystaw zbiorowych."
		),
		"artworks": [],
		"catalogs": [],
		"image_thumbnail": ""
	}
