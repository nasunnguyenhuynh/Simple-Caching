from main import redis, Product
import time

key = 'order_completed'
group = 'inventory-group'

try:  # Create consumer group
    redis.xgroup_create(key, group)
except:
    print('Group already exist!')

while True:
    try:
        results = redis.xreadgroup(group, key, {key: '>'}, None)
        # print(results)
        if results != []:
            for result in results:
                obj = result[1][0][1]
                try:  # Resolve user payment after products are empty
                    product = Product.get(obj['product_id'])
                    # print(product)
                    product.quantity = product.quantity - int(obj['quantity'])
                    product.save()
                except:
                    redis.xadd('refund_order', obj, '*')
    except Exception as e:
        print(str(e))
    time.sleep(1)  # Chờ trước khi đọc event mới trong Stream
