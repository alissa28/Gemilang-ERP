from app.models.operational_models import Purchase, SaleDetail, PurchaseDetail
from sqlalchemy import and_, desc
from datetime import datetime

def calculate_profit(sale_id):
    """
    Calculates profit by using the last purchase price as the cost basis
    """
    sale_details = SaleDetail.query.filter_by(sale_id=sale_id).all()
    total_revenue = 0
    total_cost = 0

    for detail in sale_details:
        # Calculate revenue
        revenue = detail.quantity * float(detail.unit_price)
        total_revenue += revenue
        
        # Get the most recent purchase price for this item
        last_purchase = PurchaseDetail.query.join(Purchase)\
            .filter(PurchaseDetail.item_id == detail.item_id)\
            .order_by(desc(Purchase.purchase_date))\
            .first()
            
        if last_purchase:
            cost = detail.quantity * float(last_purchase.unit_price)
        else:
            # Fallback if no purchase history
            cost = 0
            
        total_cost += cost

    return total_revenue - total_cost


def get_item_cogs(item_id, quantity, before_date=None):
    """
    Helper function to calculate COGS for a specific item quantity using FIFO
    """
    if before_date is None:
        before_date = datetime.now()

    # Get relevant purchases
    purchases = PurchaseDetail.query.join(PurchaseDetail.purchase).filter(
        and_(
            PurchaseDetail.item_id == item_id,
            Purchase.purchase_date <= before_date
        )
    ).order_by(Purchase.purchase_date.asc()).all()

    cogs = 0
    remaining_quantity = quantity

    for purchase in purchases:
        if remaining_quantity <= 0:
            break

        quantity_from_purchase = min(remaining_quantity, purchase.quantity)
        purchase_cost = quantity_from_purchase * float(purchase.unit_price)  # Calculate total cost
        cogs += purchase_cost
        remaining_quantity -= quantity_from_purchase

    # Handle any remaining quantity using the latest purchase price
    if remaining_quantity > 0 and purchases:
        latest_purchase = purchases[-1]
        cogs += remaining_quantity * float(latest_purchase.unit_price)

    return cogs
