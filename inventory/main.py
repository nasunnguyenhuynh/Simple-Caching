from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()
app.add_middleware(  # Cơ chế giới hạn tài nguyên được yêu cầu truy cập từ domain khác
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*'],
)

redis = get_redis_connection(
    host='redis-18894.c311.eu-central-1-1.ec2.cloud.redislabs.com',
    port=18894,
    password='AzFmbGKmaFPxwwnt5cgH4hi1pDLs2UVS',
    decode_responses=True  # Giải mã dữ liệu trả về của Redis từ byte -> string
)


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:  # Chỉ dịnh dữ liệu của redis dùng cho lớp Product
        database = redis


@app.get('/products')
def all():
    return [format(pk) for pk in Product.all_pks()]


def format(pk: str):
    product = Product.get(pk)
    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }


@app.post('/products')
def create(product: Product):
    return product.save()


@app.get('/products/{pk}')
def get(pk: str):
    return Product.get(pk)


@app.delete('/products/{pk}')
def delete(pk: str):
    return Product.delete(pk)
