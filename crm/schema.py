import graphene
from graphene_django import DjangoObjectType
from crm.models import Product, Customer, Order
from django.db.models import Sum

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ('id', 'name', 'stock')

class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass

    success = graphene.Boolean()
    message = graphene.String()
    updated_products = graphene.List(ProductType)

    def mutate(self, info):
        low_stock_products = Product.objects.filter(stock__lt=10)
        updated_products = []
        for product in low_stock_products:
            product.stock += 10
            product.save()
            updated_products.append(product)
        return UpdateLowStockProducts(
            success=True,
            message="Low stock products updated successfully.",
            updated_products=updated_products
        )

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()

class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello, world!")
    total_customers = graphene.Int()
    total_orders = graphene.Int()
    total_revenue = graphene.Float()

    def resolve_total_customers(self, info):
        return Customer.objects.count()

    def resolve_total_orders(self, info):
        return Order.objects.count()

    def resolve_total_revenue(self, info):
        return Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0

schema = graphene.Schema(query=Query, mutation=Mutation)
