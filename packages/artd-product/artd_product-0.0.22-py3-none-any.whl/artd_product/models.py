"""
 * Copyright (C) ArtD SAS - All Rights Reserved
 * Unauthorized copying of this file, via any medium is strictly prohibited
 * Proprietary and confidential
 * Written by Jonathan Favian Urzola Maldonado <jonathan@artd.com.co>, 2023
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from artd_partner.models import Partner


class ProductBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField("status", default=True)

    class Meta:
        abstract = True


UNITS_OF_MEASURE = [
    ("kg", _("Kilogram")),
    ("g", _("Gram")),
    ("l", _("Liter")),
    ("ml", _("Milliliter")),
    ("m", _("Meter")),
    ("cm", _("Centimeter")),
    ("mm", _("Millimeter")),
    ("in", _("Inch")),
    ("ft", _("Foot")),
    ("yd", _("Yard")),
    ("mi", _("Mile")),
    ("oz", _("Ounce")),
    ("lb", _("Pound")),
    ("st", _("Stone")),
    ("t", _("Ton")),
    ("gal", _("Gallon")),
    ("pt", _("Pint")),
    ("qt", _("Quart")),
    ("cup", _("Cup")),
    ("pc", _("Piece")),
    ("set", _("Set")),
    ("pair", _("Pair")),
    ("doz", _("Dozen")),
    ("box", _("Box")),
    ("pack", _("Pack")),
    ("roll", _("Roll")),
    ("bag", _("Bag")),
    ("bottle", _("Bottle")),
    ("tube", _("Tube")),
    ("can", _("Can")),
    ("jar", _("Jar")),
    ("case", _("Case")),
    ("other", _("Other")),
]
PRODUCT_TYPE = [
    ("service", _("Service")),
    ("physical", _("Physical")),
    ("virtual", _("Virtual")),
]


class SearchEngine(models.Model):
    url_key = models.SlugField(
        _("Url key"),
        help_text=_("Enter the url key of the search engine"),
        max_length=250,
    )
    meta_title = models.CharField(
        _("Meta title"),
        help_text=_("Enter the meta title of the search engine"),
        max_length=250,
    )
    meta_description = models.CharField(
        _("Meta description"),
        help_text=_("Enter the meta description of the search engine"),
        max_length=250,
    )
    meta_keywords = models.CharField(
        _("Meta keywords"),
        help_text=_("Enter the meta keywords of the search engine"),
        max_length=250,
    )

    class Meta:
        abstract = True


class Tax(ProductBaseModel):
    """Model definition for Tax."""

    name = models.CharField(
        _("Name"),
        help_text=_("Enter the name of the tax"),
        max_length=250,
    )
    percentage = models.DecimalField(
        _("Percentage"),
        help_text=_("Enter the percentage of the tax"),
        max_digits=5,
        decimal_places=2,
    )

    class Meta:
        """Meta definition for Tax."""

        verbose_name = _("Tax")
        verbose_name_plural = _("Taxes")

    def __str__(self):
        """Unicode representation of Tax."""
        return self.name


class Brand(ProductBaseModel, SearchEngine):
    """Model definition for Brand."""

    name = models.CharField(
        _("Name"),
        help_text=_("Enter the name of the brand"),
        max_length=250,
    )

    class Meta:
        """Meta definition for Brand."""

        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

    def __str__(self):
        """Unicode representation of Brand."""
        return self.name


class RootCategory(ProductBaseModel, SearchEngine):
    """Model definition for RootCategory."""

    name = models.CharField(
        _("Name"),
        help_text=_("Enter the name of the root category"),
        max_length=250,
    )
    json_data = models.JSONField(
        _("Json data"),
        help_text=_("Enter the json data of the root category"),
        null=True,
        blank=True,
        default=dict,
    )
    partner = models.ForeignKey(
        Partner,
        verbose_name=_("Partner"),
        help_text=_("Select the partner"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        """Meta definition for RootCategory."""

        verbose_name = _("Root Category")
        verbose_name_plural = _("Root Categories")

    def __str__(self):
        """Unicode representation of RootCategory."""
        return self.name


class Category(ProductBaseModel, SearchEngine):
    """Model definition for Category."""

    name = models.CharField(
        _("Name"),
        help_text=_("Enter the name of the category"),
        max_length=250,
    )
    root_category = models.ForeignKey(
        RootCategory,
        verbose_name=_("Root category"),
        help_text=_("Select the root category"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    partner = models.ForeignKey(
        Partner,
        verbose_name=_("Partner"),
        help_text=_("Select the partner"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    parent = models.ForeignKey(
        "self",
        verbose_name=_("Parent category"),
        help_text=_("Select the Parent category"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        """Meta definition for Category."""

        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        """Unicode representation of Category."""
        return self.name

    # Create a function to get the children of a category in a tree structure
    def get_children(self):
        return self.get_children_count() > 0


class Product(ProductBaseModel, SearchEngine):
    """Model definition for Product."""

    url_key = models.SlugField(
        _("Url key"),
        help_text=_("Enter the url key of the product"),
        max_length=250,
        null=True,
        blank=True,
    )
    type = models.CharField(
        _("Type"),
        help_text=_("Select the type of the product"),
        max_length=250,
        choices=PRODUCT_TYPE,
        default="physical",
    )
    name = models.CharField(
        _("Name"),
        help_text=_("Enter the name of the product"),
        max_length=250,
    )
    sku = models.SlugField(
        _("Sku"),
        help_text=_("Enter the sku of the product"),
        max_length=250,
    )
    description = models.TextField(
        _("Description"),
        help_text=_("Enter the description of the product"),
    )
    short_description = models.TextField(
        _("Short description"),
        help_text=_("Enter the short description of the product"),
    )
    brand = models.ForeignKey(
        Brand,
        verbose_name=_("brand"),
        help_text=_("Select the brand"),
        on_delete=models.CASCADE,
    )
    categories = models.ManyToManyField(
        Category,
        verbose_name=_("Category"),
        help_text=_("Select the category"),
    )
    tax = models.ForeignKey(
        Tax,
        verbose_name=_("Tax"),
        help_text=_("Select the tax"),
        on_delete=models.CASCADE,
    )
    weight = models.DecimalField(
        _("Weight"),
        help_text=_("Enter the weight of the product"),
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    unit_of_measure = models.CharField(
        _("Unit of measure"),
        help_text=_("Select the unit of measure of the product"),
        max_length=250,
        choices=UNITS_OF_MEASURE,
        default="kg",
    )
    measure = models.DecimalField(
        _("Measure"),
        help_text=_("Enter the measure of the product"),
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )

    class Meta:
        """Meta definition for Product."""

        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        """Unicode representation of Product."""
        return self.name


class ProductImage(ProductBaseModel):
    """Model definition for ProductImage."""

    url_key = models.SlugField(
        _("Url key"),
        help_text=_("Enter the url key of the product"),
        max_length=250,
        null=True,
        blank=True,
    )
    product = models.ForeignKey(
        Product,
        verbose_name=_("Product"),
        help_text=_("Select the product"),
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        _("Image"),
        help_text=_("Select the image"),
        upload_to="product/images/",
    )
    alt = models.CharField(
        _("Alt"),
        help_text=_("Enter the alt of the image"),
        max_length=250,
    )

    class Meta:
        """Meta definition for ProductImage."""

        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

    def __str__(self):
        """Unicode representation of ProductImage."""
        return self.product.name


class GroupedProduct(ProductBaseModel, SearchEngine):
    """Model definition for GroupedProduct."""

    url_key = models.SlugField(
        _("Url key"),
        help_text=_("Enter the url key of the product"),
        max_length=250,
        null=True,
        blank=True,
    )
    name = models.CharField(
        _("Name"),
        help_text=_("Enter the name of the grouped product"),
        max_length=250,
    )
    sku = models.SlugField(
        _("Sku"),
        help_text=_("Enter the sku of the grouped product"),
        max_length=250,
    )
    description = models.TextField(
        _("Description"),
        help_text=_("Enter the description of the grouped product"),
    )
    short_description = models.TextField(
        _("Short_description"),
        help_text=_("Enter the short description of the grouped product"),
    )
    products = models.ManyToManyField(
        Product,
        verbose_name=_("Product"),
        help_text=_("Select the product"),
    )

    class Meta:
        """Meta definition for GroupedProduct."""

        verbose_name = _("Grouped Product")
        verbose_name_plural = _("Grouped Products")

    def __str__(self):
        """Unicode representation of GroupedProduct."""
        return self.name
