from crum import get_current_user

from apps.APyme.models import Buscando, Almacen, Alarmas, User


def ctx_dict(request):
    if request.user.is_authenticated:
        return {
            'buscandosC': Buscando.objects.filter(user=get_current_user()),
            'almacenesC': Almacen.objects.filter(user=get_current_user()),
            'alarmasC': Alarmas.objects.filter(user2=get_current_user()),
            'empresasC': User.objects.exclude(is_superuser=True),
        }
    else:
        return {
            'buscandos': None,
            'almacenes': None,
            'alarmas': None,
        }
