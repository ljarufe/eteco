from mantenimiento.models import MantenimientoPreventivo, MantenimientoCorrectivo


def do_script():
    for item in MantenimientoPreventivo.objects.all():
        if not item.costo:
            item.costo = 0
            item.save()

    for item in MantenimientoCorrectivo.objects.all():
        if not item.costo:
            item.costo = 0
            item.save()