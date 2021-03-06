# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-09 00:35
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_prices.models
import satchless.item
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('etrans', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('discount', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('status', models.CharField(choices=[('open', 'Open - currently active'), ('payment', 'Waiting for payment'), ('saved', 'Saved - for items to be purchased later'), ('ordered', 'Submitted - an order was placed'), ('checkout', 'Checkout - processed in checkout'), ('canceled', 'Canceled - canceled by user')], default='open', max_length=32)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_status_change', models.DateTimeField(auto_now_add=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('token', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('checkout_data', django.contrib.postgres.fields.jsonb.JSONField(editable=False, null=True)),
                ('total', django_prices.models.PriceField(currency='FCFA', decimal_places=2, default=0, max_digits=12)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='carts', to=settings.AUTH_USER_MODEL)),
                ('voucher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='discount.Voucher')),
            ],
            options={
                'ordering': ('-last_status_change',),
            },
        ),
        migrations.CreateModel(
            name='CartLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(999)])),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={})),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='cart.Cart')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='etrans.ProductVariant')),
            ],
            bases=(models.Model, satchless.item.ItemLine),
        ),
        migrations.AlterUniqueTogether(
            name='cartline',
            unique_together=set([('cart', 'variant', 'data')]),
        ),
    ]
