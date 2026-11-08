from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("productos", "0004_alter_producto_proveedor"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cliente",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=100)),
                ("telefono", models.CharField(max_length=15, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "clientes_venta",
                "ordering": ["nombre", "id"],
                "verbose_name": "Cliente de venta",
                "verbose_name_plural": "Clientes de venta",
            },
        ),
        migrations.CreateModel(
            name="Venta",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tipo", models.CharField(choices=[("CONTADO", "Pagada"), ("FIADO", "Fiada")], db_index=True, max_length=10)),
                ("total", models.PositiveBigIntegerField()),
                ("fecha", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("cliente", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="ventas", to="ventas.cliente")),
            ],
            options={
                "db_table": "ventas",
                "ordering": ["-fecha", "-id"],
            },
        ),
        migrations.CreateModel(
            name="DetalleVenta",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("cantidad", models.PositiveIntegerField()),
                ("precio_unitario", models.PositiveBigIntegerField()),
                ("producto", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="detalles_venta", to="productos.producto")),
                ("venta", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="ventas.venta")),
            ],
            options={
                "db_table": "ventas_detalle",
                "constraints": [
                    models.UniqueConstraint(fields=("venta", "producto"), name="venta_producto_unico"),
                    models.CheckConstraint(check=models.Q(("cantidad__gt", 0)), name="detalle_cantidad_positiva"),
                ],
            },
        ),
        migrations.CreateModel(
            name="Abono",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("monto", models.PositiveBigIntegerField()),
                ("fecha", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("venta", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="abonos", to="ventas.venta")),
            ],
            options={
                "db_table": "ventas_abonos",
                "ordering": ["-fecha", "-id"],
                "constraints": [
                    models.CheckConstraint(check=models.Q(("monto__gt", 0)), name="abono_monto_positivo"),
                ],
            },
        ),
    ]
