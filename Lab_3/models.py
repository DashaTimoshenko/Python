from app import db, app

# db.Model = declarative_base()

metadata = db.Model.metadata


class Product(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, db.Sequence('products_product_id_seq'), primary_key=True)
    product_name = db.Column(db.Text, nullable=False)
    product_code = db.Column(db.Text, nullable=False, unique=True)
    unit = db.Column(db.Text, nullable=False)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete_self(self):
        db.session.delete(self)
        db.session.commit()

class Warehouse(db.Model):
    __tablename__ = 'warehouses'

    warehouse_id = db.Column(db.Text, primary_key=True)
    warehouse_name = db.Column(db.Text, nullable=False, unique=True)


    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete_self(self):
        db.session.delete(self)
        db.session.commit()


class Container(db.Model):
    __tablename__ = 'containers'
    __table_args__ = (
        db.UniqueConstraint('warehouse_id', 'container_number'),
    )

    container_id = db.Column(db.Integer, db.Sequence('containers_container_id_seq'), primary_key=True)
    warehouse_id = db.Column(db.ForeignKey('warehouses.warehouse_id', ondelete='CASCADE', onupdate='RESTRICT'))
    container_number = db.Column(db.Text, nullable=False)

    warehouse = db.relationship('Warehouse', backref=db.backref('children', cascade='all,delete'))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete_self(self):
        db.session.delete(self)
        db.session.commit()

class Storage(db.Model):
    __tablename__ = 'storage'

    container_id = db.Column(db.ForeignKey('containers.container_id', ondelete='CASCADE', onupdate='RESTRICT'), primary_key=True, nullable=False)
    product_id = db.Column(db.ForeignKey('products.product_id', ondelete='CASCADE', onupdate='RESTRICT'), primary_key=True, nullable=False)
    quantity = db.Column(db.Numeric, nullable=False)

    container = db.relationship('Container', backref=db.backref('children', cascade='all,delete'))
    product = db.relationship('Product', backref=db.backref('children', cascade='all,delete'))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete_self(self):
        db.session.delete(self)
        db.session.commit()

    def update_self(self, quantity):
        self.quantity = quantity
        db.session.commit()


with app.app_context():
    db.create_all()
db.session.commit()