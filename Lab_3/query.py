from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for, request, redirect, json
from models import Product, Warehouse, Container, Storage
from app import db

def get_all_warehouses():
    return Warehouse.query.order_by(Warehouse.warehouse_id).all()

def get_all_containers():
    return Container.query.order_by(Container.container_id).all()

def get_containers_by_warehouse(warehouse_id):
    return Container.query.filter_by(warehouse_id=warehouse_id).all()

def get_all_products():
    return Product.query.order_by(Product.product_id).all()

def get_id_by_product_code(new_product_code):
    q = db.session.query(Product.product_id).filter(
        Product.product_code == new_product_code,
    ).all()
    return q[0][0]



def get_product_storage_inf():
    r = db.session.query(Warehouse.warehouse_name, Container.container_number, Product.product_code, Product.product_name, Storage.quantity, Product.unit, Storage.container_id, Storage.product_id).join(
            Product, Storage.product_id == Product.product_id).join(
            Container, Storage.container_id == Container.container_id).join(
            Warehouse, Container.warehouse_id == Warehouse.warehouse_id).order_by(Warehouse.warehouse_name, Container.container_number).all()
    return r

def get_update_text(container_id, product_id):
    r = db.session.query(Warehouse.warehouse_name, Container.container_number, Product.product_name, Product.product_code, Storage.quantity, Storage.container_id, Storage.product_id).join(
                Product, Storage.product_id == Product.product_id).join(
                Container, Storage.container_id == Container.container_id).join(
                Warehouse, Container.warehouse_id == Warehouse.warehouse_id).filter((Storage.container_id == container_id) & (Storage.product_id == product_id)).all()
    return r
