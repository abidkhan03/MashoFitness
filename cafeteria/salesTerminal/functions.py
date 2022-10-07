
# from ast import Invert
from cafeteria.Items.models import Items, NonStock
from cafeteria.purchases.models import Inventory, Purchases
from cafeteria.salesTerminal.models import Order, OrderHistory



def CostomSerializer(item_name):
    # if stock is None:
    #     stock=Items.objects.all()
    #     nonstock=NonStock.objects.all()
    data=list()
    if Items.objects.filter(item_name__icontains=item_name).exists():
        for i in Inventory.objects.filter(inventory_item_id__item_name__icontains=item_name):
            
            data.append(
                    {
                'id':i.id,
                'item_name':i.inventory_item_id.item_name,
                'item_price':i.inventory_item_id.item_selling_price,
                'item_category':i.inventory_item_id.item_category,
                'item_image':i.inventory_item_id.item_image.url,
                'item_stock':i.inventory_stock_available,
            }
            )
    if NonStock.objects.filter(nonStock_item_name__icontains=item_name).exists():
        for i in NonStock.objects.filter(nonStock_item_name__icontains=item_name):
            data.append(
                    {
                'id':i.id,
                'item_name':i.nonStock_item_name,
                'item_price':i.nonStock_item_selling_price,
                'item_category':i.nonStock_item_category,
                'item_image':i.nonStock_item_image.url,
                'item_stock':str('inf'),
            }
            )
    if not data:
        return False
    else:
        return data

    # for i in nonstock:
        
    #     data.append(
    #         {
    #         'id':i.id,
    #         'item_name':i.nonStock_item_name,
    #         'item_price':i.nonStock_item_selling_price,
    #         'item_category':i.nonStock_item_category,
    #         'item_image':i.nonStock_item_image.url,
    #     }
    #     )
    # return data


def OrderPlaced(dictonary:dict,order:Order):
    """
    {
        'itemName': 'juice',
        'quantity': '1',
        'discount': '', 
        'totalPrice': '200'
    }
    """
    if Items.objects.filter(item_name=dictonary["itemName"]).exists():
        inventory=Inventory.objects.get(inventory_item_id=Items.objects.get(item_name=dictonary["itemName"]))
        inventory.inventory_purchased_quantity-=int(dictonary["quantity"])
        inventory.inventory_stock_available-=int(dictonary["quantity"])
        # inventory.inventory_stock_available-=int(dictonary["quantity"])
        inventory.save()

        purchases=Purchases.objects.get(purchases_order_number=inventory.inventory_order_number)
        purchases.purchases_stock_available -=int(dictonary["quantity"])
        purchases.save()
    elif NonStock.objects.filter(nonStock_item_name=dictonary["itemName"]).exists():
        pass
    discount=int(dictonary["discount"]) if dictonary["discount"] else 0
    price=int(dictonary["totalPrice"]) if dictonary["totalPrice"] else 0
    quantity=int(dictonary["quantity"]) if dictonary["quantity"] else 0
    price=(price+discount)//quantity
    total=(price*quantity)-discount
    # print(price,quantity,discount,total)
    OrderHistory.objects.create(
        order_id=order,
        order_item_name=dictonary["itemName"],
        order_item_quantity=quantity,
        order_item_discount=discount,
        order_item_price=price,
        order_item_total=total,
    )

