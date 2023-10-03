from django.test import TestCase
from artd_product.models import (
    Tax,
    Brand,
    RootCategory,
    Category,
    Product,
    ProductImage,
    GroupedProduct,
)
from artd_product.data.taxes import TAXES


# Create test for Tax model
class TestProductModles(TestCase):
    def setUp(self):
        for tax in TAXES:
            Tax.objects.create(
                name=tax[0],
                percentage=tax[1],
            )
        self.tax = Tax.objects.first()
        self.brand = Brand.objects.create(
            name="Test Brand",
            status=True,
            url_key="test-brand",
            meta_title="Test Brand",
            meta_description="Test Brand",
            meta_keywords="Test Brand",
        )
        self.root_category = RootCategory.objects.create(
            name="Test Root Category",
            status=True,
            url_key="test-root-category",
            meta_title="Test Root Category",
            meta_description="Test Root Category",
            meta_keywords="Test Root Category",
        )
        self.category = Category.objects.create(
            name="Test Category",
            status=True,
            url_key="test-category",
            meta_title="Test Category",
            meta_description="Test Category",
            meta_keywords="Test Category",
            parent=self.root_category,
        )
        self.product = Product.objects.create(
            name="Test Product",
            sku="test-product",
            description="Test Product",
            short_description="Test Product",
            price=100,
            special_price_from="2021-01-01 00:00:00",
            special_price_to="2021-01-01 00:00:00",
            url_key="test-product",
            meta_title="Test Product",
            meta_description="Test Product",
            meta_keywords="Test Product",
            brand=self.brand,
            tax=self.tax,
        )
        self.product.categories.add(self.category)
        self.product_image = ProductImage.objects.create(
            image="test-image.jpg",
            product=self.product,
            alt="Test Image",
        )
        self.grouped_product = GroupedProduct.objects.create(
            name="Test Product",
            sku="test-product",
            description="Test Product",
            short_description="Test Product",
            url_key="test-product",
            meta_title="Test Product",
            meta_description="Test Product",
            meta_keywords="Test Product",
        )
        self.grouped_product.products.add(self.product)

    def test_tax_created(self):
        assert len(TAXES) == Tax.objects.count()

    def test_brand_created(self):
        assert Brand.objects.count() == 1

    def test_root_category_created(self):
        assert RootCategory.objects.count() == 1

    def test_category_created(self):
        assert Category.objects.count() == 1

    def test_product_created(self):
        assert Product.objects.count() == 1

    def test_product_image_created(self):
        assert ProductImage.objects.count() == 1

    def test_grouped_product_created(self):
        assert GroupedProduct.objects.count() == 1
