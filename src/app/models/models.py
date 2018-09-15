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


class TermRelationships(db.Model):
    __tablename__ = '2c191c_term_relationships'
    object_id = db.Column(db.Integer, primary_key=True)
    term_taxonomy_id = db.Column(db.Integer, primary_key=True)


class Posts(db.Model):
    __tablename__ = '2c191c_posts'
    id = db.Column(db.Integer, primary_key=True)
    post_author = db.Column(db.Integer)
    post_date = db.Column(db.DateTime)
    post_date_gmt = db.Column(db.DateTime)
    post_content = db.Column(db.Text())
    post_title = db.Column(db.Text())
    post_excerpt = db.Column(db.Text())
    post_status = db.Column(db.String(20))
    comment_status = db.Column(db.String(20))
    ping_status = db.Column(db.String(20))
    post_password = db.Column(db.String(255))
    post_name = db.Column(db.String(200))
    to_ping = db.Column(db.Text())
    pinged = db.Column(db.Text())
    post_modified = db.Column(db.DateTime)
    post_modified_gmt = db.Column(db.DateTime)
    post_content_filtered = db.Column(db.Text())
    post_parent = db.Column(db.Integer)
    guid = db.Column(db.String(255))
    menu_order = db.Column(db.Integer)
    post_type = db.Column(db.String(20))
    post_mime_type = db.Column(db.String(100))
    comment_count = db.Column(db.Integer)


class Postmeta(db.Model):
    __tablename__ = '2c191c_postmeta'
    meta_id =  db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    meta_key = db.Column(db.String(255))
    meta_value = db.Column(db.Text())