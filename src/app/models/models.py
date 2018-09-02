from app.application import db


class Terms(db.Model):
	__tablename__ = '2c191c_terms'
	term_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200))
	slug = db.Column(db.String(200))
	term_group = db.Column(db.Integer)
	term_order = db.Column(db.Integer)

	def __repr__(self):
		return 'id: {}, name: {}'.format(self.term_id, self.name)


class TermTaxonomies(db.Model):
	__tablename__ = '2c191c_term_taxonomy'
	term_taxonomy_id = db.Column(db.Integer, primary_key=True)
	term_id = db.Column(db.Integer)
	taxonomy = db.Column(db.String(32))
	description = db.Column(db.Text())

	def __repr__(self):
		return 'term_id: {}, taxonomy: {}, description: {}'.format(
			self.term_id, self.taxonomy, self.description
		)
