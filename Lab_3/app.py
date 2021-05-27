from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for, request, redirect, json
from flask import Flask
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:040801@localhost:5432/lab_3_bd"
# SQLALCHEMY_TRACK_MODIFICATIONS = 'False'

db = SQLAlchemy(app)
db.init_app(app)

from models import Product, Warehouse, Container, Storage
from query import *


@app.route('/')
def index():
    return redirect('/warehouse_crud')
#        render_template('warehouses.html')

@app.route('/warehouse_crud', methods=['POST', 'GET'])
def warehouse_crud():
    if request.method == 'POST':
        new_warehouse_id = request.form['warehouse_id']
        new_warehouse_name = request.form['warehouse_name']
        # new_warehouse = Warehouse(warehouse_id=new_warehouse_id, warehouse_name=new_warehouse_name)

        try:
            new_warehouse = Warehouse(warehouse_id=new_warehouse_id, warehouse_name=new_warehouse_name).create()
            return redirect('/warehouse_crud')
        except:
            return redirect('/warehouse_crud')
            # return 'There was an issue adding your warehouse'

    else:
        warehouses = get_all_warehouses()
        return render_template('warehouses.html', warehouses=warehouses)

@app.route('/warehouse_crud/delete/<string:warehouse_id>', methods=['POST', 'GET'])
def warehouse_crud_delete(warehouse_id):

    if request.method == 'POST':
        try:
            warehouse_to_delete = Warehouse.query.get_or_404(warehouse_id)
            warehouse_to_delete.delete_self()
            return redirect('/warehouse_crud')
        except:
            return 'There was a problem deleting that warehouse'



@app.route('/container_crud', methods=['POST', 'GET'])
def container_crud():
    if request.method == 'POST':
        new_warehouse_id = request.form['warehouse_id']
        new_container_number = request.form['container_number']
        try:
            new_container = Container(warehouse_id=new_warehouse_id, container_number=new_container_number).create()
            return redirect('/container_crud')
        except:
            return redirect('/container_crud')
            # return 'There was an issue adding your container'

    else:
        containers = get_all_containers()
        warehouses = get_all_warehouses()
        return render_template('containers.html', containers=containers, warehouses=warehouses)

@app.route('/container_crud/delete/<string:container_id>', methods=['POST', 'GET'])
def container_crud_delete(container_id):

    if request.method == 'POST':
        try:
            container_to_delete = Container.query.get_or_404(container_id)
            container_to_delete.delete_self()
            return redirect('/container_crud')
        except:
            return 'There was a problem deleting that container'


@app.route('/product_crud', methods=['POST', 'GET'])
def product_crud():
    if request.method == 'POST':
        new_product_name = request.form['product_name']
        new_product_code = request.form['product_code']
        new_unit = request.form['unit']
        try:
            new_product = Product(product_name=new_product_name, product_code=new_product_code, unit=new_unit).create()
            return redirect('/product_crud')
        except:
            return redirect('/product_crud')
            # return 'There was an issue adding your product'

    else:
        products = get_all_products()
        return render_template('products.html', products=products)

@app.route('/product_crud/delete/<string:product_id>', methods=['POST', 'GET'])
def product_crud_delete(product_id):

    if request.method == 'POST':
        try:
            product_to_delete = Product.query.get_or_404(product_id)
            product_to_delete.delete_self()
            return redirect('/product_crud')
        except:
            return 'There was a problem deleting that product'




@app.route('/storage_crud', methods=['POST', 'GET'])
def storage_crud():
    if request.method == 'POST':
        new_warehouse_id = request.form['warehouse_id']
        new_container_id = request.form['container_number']
        new_product_code = request.form['product_code']
        new_quantity = float(request.form['quantity'])

        try:
            product_id = get_id_by_product_code(new_product_code)
            new_storage = Storage(container_id=new_container_id, product_id=product_id, quantity=new_quantity).create()
            return redirect('/storage_crud')
        except:
            return redirect('/storage_crud')
            # return 'There was an issue adding information about storage of product. \n\nPerhaps such a product is already stored in this container or there is no product with this code.'
    else:
        warehouses = get_all_warehouses()
        res = get_product_storage_inf()
        return render_template('storage.html', storages=res, warehouses=warehouses)

@app.route('/get_sub_category', methods=('GET', 'POST'))
def get_sub_category():
    warehouse_id = request.form['warehouse_id']
    item_list = get_containers_by_warehouse(warehouse_id)
    result_list = dict()
    for item in item_list:
        result_list[item.container_id] = item.container_number
    return json.dumps(result_list)


@app.route('/storage_crud/delete/<int:container_id>/<int:product_id>', methods=['POST', 'GET'])
def storage_crud_delete(container_id, product_id):

    if request.method == 'POST':
        try:
            storage_to_delete = Storage.query.get_or_404([container_id, product_id])
            storage_to_delete.delete_self()
            return redirect('/storage_crud')
        except:
            return 'There was a problem deleting that record'

@app.route('/storage_crud/update/<int:container_id>/<int:product_id>', methods=['GET', 'POST'])
def update(container_id, product_id):

    if request.method == 'POST':
        try:
            storage_to_update = Storage.query.get_or_404([container_id, product_id])
            storage_to_update.update_self(request.form['quantity'])
            return redirect('/storage_crud')
        except:
            return 'There was an issue updating this record'
    else:
        try:
            storage_to_update = Storage.query.get_or_404([container_id, product_id])
            text = get_update_text(container_id, product_id)
            return render_template('update.html', storage=storage_to_update, text=text)
        except:
            return 'There was an issue updating this record'



if __name__ == '__main__':
    app.run()
