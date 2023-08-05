from apps.APyme.models import *

almacen = Almacen.objects.all().order_by('user')
buscando = Buscando.objects.all().order_by('user')
empresas = User.objects.all()


def crearAlarma(userMatch, userBuscando, productos):
    print("Funcion CREAR ALARMA, LOS PRODUCTOS SON: ")
    print(productos)
    try:
        alarma = Alarmas.objects.get(user=userMatch, user2=userBuscando)
        print('Existe ya con datos nuevos')
        for p in productos:
            AA = alarmas_almacenes(alarma=alarma, almacen=p['producto'], buscando=p['buscado'])
            AA.save()
        print('Productos añadidos a la alarma ya existente: ', alarma)
    except Exception as e:
        print(e)
        print('Se crea la Alarma')
        print(productos)
        alarmaa = Alarmas(user=userMatch, user2=userBuscando)
        alarmaa.save()

        for p in productos:
            AA = alarmas_almacenes(alarma=alarmaa, almacen=p['producto'], buscando=p['buscado'])
            AA.save()


def VerificarHash(e, p, b):
    try:
        hash = Hash(
            hash=f"{str(e.id)} | {str(p.user_id)} | {str(b.id)} |"
                 f" {str(p.id)} | {str(p.updated_at)} | {str(b.updated_at)} | {str(p.producto)} ")
        hash.save()
    except:
        print('Ya esta en HASH')
        return False

    else:
        print('No esta en HASH, se procede')
        return True


def prueba():
    for e in empresas:
        print('EMPRESA ', e, " BUSCANDO: ")
        productosMatch = []

        for b in buscando.filter(user=e):
            producto = b.producto
            cantidad = b.cantidad
            precio = b.precio
            unidad = b.unidad
            print(b, "|", b.cantidad, "|", b.precio)
            # Buscar matches de la empresa e
            almacenMatch = almacen.filter(producto__icontains=producto).exclude(
                user=e)

            if cantidad != 0 and precio != 0:
                print('if 1')
                almacenMatch = almacenMatch.filter(cantidad__gte=cantidad, precio__lte=precio, unidad=unidad)
                print("matches: ", almacenMatch)

            if cantidad != 0 and precio == 0:
                print('if 2')
                almacenMatch = almacenMatch.filter(cantidad__gte=cantidad, unidad=unidad)
                print("matches: ", almacenMatch)

            if cantidad == 0 and precio != 0:
                print('if 3')
                almacenMatch = almacenMatch.filter(precio__lte=precio)
                print("matches: ", almacenMatch)

            for p in almacenMatch:
                if VerificarHash(e, p, b):
                    dic = {'producto': p, 'buscado': b}
                    productosMatch.append(dic)

        if productosMatch:
            # buscar los usuarios e2 q posean esos matches
            for e2 in empresas.exclude(id=e.id):
                pf = []
                for pr in productosMatch:
                    if pr['producto'].user == e2:
                        pf.append(pr)

                        print(pr)

                if pf:
                    crearAlarma(e2, e, pf)

        print('FIN BUSCAR PARA ', e)
        print("")

    print("FIN")
    print('\n')


def ppp():
    pass
