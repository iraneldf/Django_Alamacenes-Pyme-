from django.urls import path

from apps.APyme.views import *

urlpatterns = [
    path('', ListAlarmas.as_view(), name='alarmas'),
    path('verEmpresa/<int:pk>', DetailsEmpresa.as_view(), name='DetailsEmpresa'),
    path('informacion/', Informacion.as_view(), name='informacion'),
    path('empresas/', ListEmpresas.as_view(), name='ListEmpresas'),
    path('empresas/details/<int:pk>', DetailsRoot.as_view(), name='DetailsRoot'),

    path('informacion/create/telefonos', CreateTelefono.as_view(), name='CreateTelefono'),
    path('informacion/edit/telefonos/<int:pk>', TelefonosUpdateView.as_view(), name='EditTelefono'),
    path('informacion/delete/telefonos/<int:pk>', DeleteTelefono.as_view(), name='DeleteTelefono'),

    path('informacion/create/whatsapp', CreateWhastapp.as_view(), name='CreateWhastapp'),
    path('informacion/edit/whatsapp/<int:pk>', WhatsappUpdateView.as_view(), name='EditWhatsapp'),
    path('informacion/delete/whatsapp/<int:pk>', DeleteWhastapp.as_view(), name='DeleteWhastapp'),

    path('informacion/create/socios', CreateSocio.as_view(), name='CreateSocio'),
    path('informacion/edit/socios/<int:pk>', SociosUpdateView.as_view(), name='EditSocios'),
    path('informacion/delete/socios/<int:pk>', DeleteSocio.as_view(), name='DeleteSocio'),

    path('informacion/create/domicilio', CreateDomicilios.as_view(), name='CreateDomicilios'),
    path('informacion/edit/domicilio/<int:pk>', DomiciliosUpdateView.as_view(), name='EditDomicilios'),
    path('informacion/delete/domicilio/<int:pk>', DeleteDomicilios.as_view(), name='DeleteDomicilios'),

    path('informacion/create/email', CreateCorreo.as_view(), name='CreateCorreo'),
    path('informacion/edit/email/<int:pk>', CorreoUpdateView.as_view(), name='EditEmail'),
    path('informacion/delete/email/<int:pk>', DeleteCorreo.as_view(), name='DeleteCorreo'),

    path('informacion/create/web', CreateSitios.as_view(), name='CreateSitios'),
    path('informacion/edit/web/<int:pk>', SitiosUpdateView.as_view(), name='EditSitios'),
    path('informacion/delete/web/<int:pk>', DeleteSitios.as_view(), name='DeleteSitios'),

    path('almacen/', ListAlmacen.as_view(), name='almacen'),
    path('almacen/create', CreateAlmacen.as_view(), name='CreateAlmacen'),
    path('almacen/edit/<int:pk>', UpdateAlmacen.as_view(), name='EditAlmacen'),
    path('almacen/delete/<int:pk>', DeleteAlmacen.as_view(), name='DeleteAlmacen'),

    path('buscando/', ListBuscando.as_view(), name='buscando'),
    path('buscando/create', CreateBuscando.as_view(), name='CreateBuscando'),
    path('buscando/edit/<int:pk>', UpdateBuscando.as_view(), name='EditBuscando'),
    path('buscando/delete/<int:pk>', DeleteBuscando.as_view(), name='DeleteBuscando'),

    path('alarmas/delete/<int:pk>', DeleteAlarma.as_view(), name='DeleteAlarma'),

    # ROOT
    path('root/eliminar-usuario/<int:pk>/', EliminarUsuario.as_view(), name='eliminar_usuario'),
    path('root/almacen/create/<int:pk>', CreateAlmacenRoot.as_view(), name='CreateAlmacenRoot'),
    path('root/almacen/edit/<int:pk>/<int:user>', EditAlmacenRoot, name='EditAlmacenRoot'),
    path('root/buscando/create/<int:pk>', CreateBuscandoRoot, name='CreateBuscandoRoot'),
    path('root/buscando/edit/<int:pk>/<int:user>', EditBuscandoRoot, name='EditBuscandoRoot'),

    path('root/create/telefonos/<int:user>', CreateTelefonoRoot, name='CreateTelefonoRoot'),

    path('root/create/whatsapp/<int:user>', CreateWhatsappRoot, name='CreateWhastappRoot'),

    path('root/create/socios/<int:user>', CreateSociosRoot, name='CreateSocioRoot'),

    path('root/create/domicilio/<int:user>', CreateDomiciliosRoot, name='CreateDomiciliosRoot'),

    path('root/create/email/<int:user>', CreateEmailsRoot, name='CreateCorreoRoot'),

    path('root/create/web/<int:user>', CreateSitiosRoot, name='CreateSitiosRoot'),

    path('root/unidades', unidad_list, name='Lista_unidades'),
    path('root/unidades/create', unidad_create, name='Crear_unidad'),
    path('root/unidades/edit/<int:pk>', unidad_edit, name='Editar_unidad'),
    path('root/unidades/delete/<int:pk>', unidad_delete, name='Borrar_unidad'),

]
