from flask import Blueprint, jsonify, request
from app.models.operational_models import Purchase, PurchaseDetail, Sale, SaleDetail, Forecast, Inventory
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from app import db
import numpy as np
import datetime
from sqlalchemy.orm import joinedload

forecast_bp = Blueprint('forecast', __name__)

@forecast_bp.route('/forecast', methods=['GET'])
def get_forecast():
    forecast = Forecast.query.order_by(Forecast.date.desc()).first()
    if forecast:
        return jsonify({
            'purchase_forecast': forecast.purchase_forecast,
            'sale_forecast': forecast.sale_forecast
        })
    else:
        forecast = perform_forecast(days=7)
        return jsonify({
            'purchase_forecast': forecast.purchase_forecast,
            'sale_forecast': forecast.sale_forecast
        })

def prepare_data(data, past_date):
    if not data:
        return np.array([]).reshape(-1, 1), np.array([])
    dates = [(d[0] - past_date).days for d in data]
    quantities = [d[1] for d in data]
    return np.array(dates).reshape(-1, 1), np.array(quantities)

def perform_forecast(days=7):
    today = datetime.date.today()
    past_date = today - datetime.timedelta(days=days)
    past_datetime = datetime.datetime.combine(past_date, datetime.time.min)

    purchase_details = (
        db.session.query(PurchaseDetail, Purchase)
        .join(Purchase, PurchaseDetail.purchase_id == Purchase.id)
        .filter(Purchase.purchase_date >= past_datetime)
        .all()
    )
    sale_details = (
        db.session.query(SaleDetail, Sale)
        .join(Sale, SaleDetail.sale_id == Sale.id)
        .filter(Sale.sale_date >= past_datetime)
        .all()
    )

    purchase_data = [(purchase.purchase_date, detail.quantity) for detail, purchase in purchase_details]
    sale_data = [(sale.sale_date, detail.quantity) for detail, sale in sale_details]

    purchase_dates, purchase_quantities = prepare_data(purchase_data, past_datetime)
    sale_dates, sale_quantities = prepare_data(sale_data, past_datetime)

    purchase_forecast, sale_forecast = 0, 0
    model = LinearRegression()

    if len(purchase_dates) > 0 and len(purchase_quantities) > 0:
        model.fit(purchase_dates, purchase_quantities)
        purchase_forecast = float(model.predict(np.array([[days]]))[0])

    if len(sale_dates) > 0 and len(sale_quantities) > 0:
        model.fit(sale_dates, sale_quantities)
        sale_forecast = float(model.predict(np.array([[days]]))[0])

    forecast = Forecast(
        date=today,
        purchase_forecast=purchase_forecast,
        sale_forecast=sale_forecast
    )

    try:
        db.session.add(forecast)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

    return forecast

@forecast_bp.route('/items', methods=['GET'])
def get_item_forecast():
    items = Inventory.query.all()
    forecasts = {}
    for item in items:
        forecasts[item.name] = perform_item_forecast(item.id, days=7)
    return jsonify(forecasts)

def perform_item_forecast(item_id, days=7):
    today = datetime.date.today()
    past_date = today - datetime.timedelta(days=days)
    past_datetime = datetime.datetime.combine(past_date, datetime.time.min)

    purchase_details = (
        db.session.query(PurchaseDetail, Purchase)
        .join(Purchase, PurchaseDetail.purchase_id == Purchase.id)
        .filter(Purchase.purchase_date >= past_datetime, PurchaseDetail.item_id == item_id)
        .all()
    )
    sale_details = (
        db.session.query(SaleDetail, Sale)
        .join(Sale, SaleDetail.sale_id == Sale.id)
        .filter(Sale.sale_date >= past_datetime, SaleDetail.item_id == item_id)
        .all()
    )

    purchase_data = [(purchase.purchase_date, detail.quantity) for detail, purchase in purchase_details]
    sale_data = [(sale.sale_date, detail.quantity) for detail, sale in sale_details]

    purchase_dates, purchase_quantities = prepare_data(purchase_data, past_datetime)
    sale_dates, sale_quantities = prepare_data(sale_data, past_datetime)

    purchase_forecast, sale_forecast = 0, 0
    model = LinearRegression()

    if len(purchase_dates) > 0 and len(purchase_quantities) > 0:
        model.fit(purchase_dates, purchase_quantities)
        purchase_forecast = float(model.predict(np.array([[days]]))[0])

    if len(sale_dates) > 0 and len(sale_quantities) > 0:
        model.fit(sale_dates, sale_quantities)
        sale_forecast = float(model.predict(np.array([[days]]))[0])

    return {
        'purchase_forecast': purchase_forecast,
        'sale_forecast': sale_forecast
    }

@forecast_bp.route('/clusters', methods=['GET'])
def get_item_clusters():
    sale_details = SaleDetail.query.all()
    item_quantities = {}

    for detail in sale_details:
        if detail.sale_id not in item_quantities:
            item_quantities[detail.sale_id] = {}
        if detail.item_id not in item_quantities[detail.sale_id]:
            item_quantities[detail.sale_id][detail.item_id] = 0
        item_quantities[detail.sale_id][detail.item_id] += detail.quantity

    transactions = list(item_quantities.values())
    item_ids = list(set(item_id for transaction in transactions for item_id in transaction.keys()))
    item_index = {item_id: idx for idx, item_id in enumerate(item_ids)}

    data = np.zeros((len(transactions), len(item_ids)))
    for i, transaction in enumerate(transactions):
        for item_id, quantity in transaction.items():
            data[i, item_index[item_id]] = quantity

    kmeans = KMeans(n_clusters=5)
    kmeans.fit(data)
    clusters = kmeans.labels_

    item_names = {item.id: item.name for item in Inventory.query.filter(Inventory.id.in_(item_ids)).all()}
    cluster_data = [[] for _ in range(5)]
    for idx, item_id in enumerate(item_ids):
        cluster = clusters[idx]
        item_name = item_names.get(item_id, f"Item {item_id}")
        cluster_data[cluster].append(item_name)

    return jsonify({
        'clusters': cluster_data
    })