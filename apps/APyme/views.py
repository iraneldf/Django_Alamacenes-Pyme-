from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import *

from apps.APyme.forms import AlmacenForm, BuscandoForm, AlmacenFormRoot, BuscandoFormRoot, TelefonoFormRoot, \
    TelefonoForm, SociosForm, DomiciliosForm, CorreoForm, SitiosForm, WhatsappFormRoot, SociosFormRoot, \
    DomiciliosFormRoot, CorreoFormRoot, SitiosFormRoot, WhatsappForm
from apps.APyme.models import *
from apps.account.forms import UnidadMedidaForm


def get_qs(self, qs):
    # ELIMINAR FILTROS
    if self.request.GET.get('clear_filter'):
        if 'nombre' in self.request.session:
            del self.request.session['nombre']
        if 'almacen_producto' in self.request.session:
            del self.request.session['almacen_producto']
        if 'buscando_producto' in self.request.session:
            del self.request.session['buscando_producto']
        if 'almacen_cantidad' in self.request.session:
            del self.request.session['almacen_cantidad']
        if 'buscando_cantidad' in self.request.session:
            del self.request.session['buscando_cantidad']
        if 'almacen_precio' in self.request.session:
            del self.request.session['almacen_precio']
        if 'buscando_precio' in self.request.session:
            del self.request.session['buscando_precio']

    if self.request.GET.get('nombre') is "":
        if 'nombre' in self.request.session:
            del self.request.session['nombre']

    if self.request.GET.get('almacen_producto') is "":
        if 'almacen_producto' in self.request.session:
            del self.request.session['almacen_producto']

    if self.request.GET.get('buscando_producto') is "":
        if 'buscando_producto' in self.request.session:
            del self.request.session['buscando_producto']

    if self.request.GET.get('almacen_cantidad') is "":
        if 'almacen_cantidad' in self.request.session:
            del self.request.session['almacen_cantidad']

    if self.request.GET.get('buscando_cantidad') is "":
        if 'buscando_cantidad' in self.request.session:
            del self.request.session['buscando_cantidad']

    if self.request.GET.get('almacen_precio') is "":
        if 'almacen_precio' in self.request.session:
            del self.request.session['almacen_precio']

    if self.request.GET.get('buscando_precio') is "":
        if 'buscando_precio' in self.request.session:
            del self.request.session['buscando_precio']

    # FILTRAR POR NOMBRE EMPRESA
    if self.request.GET.get('nombre'):
        self.request.session['nombre'] = self.request.GET.get('nombre')

    if 'nombre' in self.request.session:
        nom = self.request.session['nombre']
        qs = qs.filter(username__icontains=nom)

    # FILTRAR POR ALMACEN
    if self.request.GET.get('almacen_producto'):
        self.request.session['almacen_producto'] = self.request.GET.get('almacen_producto')

    if self.request.GET.get('almacen_cantidad'):
        self.request.session['almacen_cantidad'] = self.request.GET.get('almacen_cantidad')

    if self.request.GET.get('almacen_precio'):
        self.request.session['almacen_precio'] = self.request.GET.get('almacen_precio')

    if 'almacen_producto' in self.request.session:
        prodA = self.request.session['almacen_producto']
        p = User.objects.filter(usuario_almacen__producto__icontains=prodA)
        print(p)
        if 'almacen_cantidad' in self.request.session:
            ac = self.request.session['almacen_cantidad']
            p = p.filter(usuario_almacen__producto__icontains=prodA, usuario_almacen__cantidad__gte=ac)

        if 'almacen_precio' in self.request.session:
            ap = self.request.session['almacen_precio']
            p = p.filter(usuario_almacen__producto__icontains=prodA, usuario_almacen__precio__lte=ap)

        qs = qs.filter(id__in=p)

    # FILTRAR POR BUSCANDO
    if self.request.GET.get('buscando_producto'):
        self.request.session['buscando_producto'] = self.request.GET.get('buscando_producto')

    if self.request.GET.get('buscando_cantidad'):
        self.request.session['buscando_cantidad'] = self.request.GET.get('buscando_cantidad')

    if self.request.GET.get('buscando_precio'):
        self.request.session['buscando_precio'] = self.request.GET.get('buscando_precio')

    if 'buscando_producto' in self.request.session:
        prodB = self.request.session['buscando_producto']
        p = User.objects.filter(usuario_buscando__producto__icontains=prodB)

        if 'buscando_cantidad' in self.request.session:
            bc = self.request.session['buscando_cantidad']
            p = p.filter(usuario_buscando__producto__icontains=prodB, usuario_buscando__cantidad__gte=bc)

        if 'buscando_precio' in self.request.session:
            bp = self.request.session['buscando_precio']
            p = p.filter(usuario_buscando__producto__icontains=prodB, usuario_buscando__precio__lte=bp)

        qs = qs.filter(id__in=p)
    return qs


# ALARMAS
class ListAlarmas(ListView):
    template_name = 'alarmas.html'
    context_object_name = 'productos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['path'] = 'alarmas'
        context['titulo'] = 'Alarmas'
        context['texto'] = 'En esta pantalla podrá ver las empresas que tienen' \
                           ' existencias en aquellos productos que está buscando'

        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Busqueda de alarmas
        return Alarmas.objects.filter(user2=self.request.user)


class DetailsEmpresa(DetailView):
    template_name = 'CRUD/detailEmpresa.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['telefonos'] = Telefonos.objects.filter(perfil=self.object)
        context['socios'] = Socios.objects.filter(perfil=self.object)
        context['whats'] = Whastapp.objects.filter(perfil=self.object)
        context['socios'] = Socios.objects.filter(perfil=self.object)
        context['domicilios'] = Domicilios.objects.filter(perfil=self.object)
        context['emails'] = Emails.objects.filter(perfil=self.object)
        context['webs'] = Sitios.objects.filter(perfil=self.object)
        context['almacen'] = Almacen.objects.filter(user=self.object)
        context['path'] = 'detallesEmpresa'
        context['titulo'] = f"Información sobre {self.object}"
        context['alarmas'] = Alarmas.objects.filter(user=self.object)
        return context


class DeleteAlarma(DeleteView):
    model = Alarmas
    template_name = 'CRUD/deleteAlarma.html'
    success_url = reverse_lazy('alarmas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['succes_url'] = self.success_url
        return context


#  INFORMACION
class Informacion(TemplateView):
    template_name = 'informacion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['path'] = 'informacion'
        context['titulo'] = 'Información'
        context['texto'] = 'En esta pantalla podra rellenar toda la informacion de su empresa.'
        context['telefonos'] = Telefonos.objects.filter(perfil=self.request.user)
        context['whats'] = Whastapp.objects.filter(perfil=self.request.user)
        context['socios'] = Socios.objects.filter(perfil=self.request.user)
        context['domicilios'] = Domicilios.objects.filter(perfil=self.request.user)
        context['emails'] = Emails.objects.filter(perfil=self.request.user)
        context['webs'] = Sitios.objects.filter(perfil=self.request.user)
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class CreateTelefono(CreateView):
    model = Telefonos
    form_class = TelefonoForm
    template_name = 'CRUD/createOtros.html'
    success_url = reverse_lazy('informacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['header'] = 'Añadir un telefono'
        context['boton'] = 'Añadir'

        return context


class DeleteTelefono(DeleteView):
    model = Telefonos
    template_name = 'CRUD/deleteOtros.html'
    success_url = reverse_lazy('informacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['succes_url'] = self.success_url
        context['header'] = 'Teléfono'
        return context

    def get_success_url(self):
        if self.request.GET.get("user"):
            print('Root')
            user = self.request.GET.get("user")
            return reverse('DetailsRoot', kwargs={'pk': user})
        else:
            print('Normal')
            return reverse('informacion')


class CreateWhastapp(CreateView):
    model = Whastapp
    form_class = WhatsappForm
    template_name = 'CRUD/createOtros.html'
    success_url = reverse_lazy('informacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['header'] = 'Añadir un whastapp'
        context['boton'] = 'Añadir'

        return context


class DeleteWhastapp(DeleteView):
    model = Whastapp
    template_name = 'CRUD/deleteOtros.html'
    success_url = reverse_lazy('informacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['succes_url'] = self.success_url
        context['header'] = 'Whastapp'
        return context


class CreateSocio(CreateView):
    model = Socios
    form_class = SociosForm
    template_name = 'CRUD/createOtros.html'
    success_url = reverse_lazy('informacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['header'] = 'Añadir un  nombres de socio'
        context['boton'] = 'Añadir'

        return context


class DeleteSocio(DeleteView):
    model = Socios
    template_name = 'CRUD/deleteOtros.html'
    success_url = reverse_lazy('informacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['succes_url'] = self.success_url
        context['header'] = 'Socio'
        return context


class CreateDomicilios(CreateView):
    model = Domicilios
    form_class = DomiciliosForm
    template_name = 'CRUD/createOtros.html'
    success_url = reverse_lazy('informacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['header'] = 'Añadir un domicilio social'
        context['boton'] = 'Añadir'

        return context


class DeleteDomicilios(DeleteView):
    model = Domicilios
    template_name = 'CRUD/deleteOtros.html'
    success_url = reverse_lazy('informacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['succes_url'] = self.success_url
        context['header'] = 'Domicilio'
        return context


class CreateCorreo(CreateView):
    model = Emails
    form_class = CorreoForm
    template_name = 'CRUD/createOtros.html'
    success_url = reverse_lazy('informacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['header'] = 'Añadir un correo electrónico'
        context['boton'] = 'Añadir'

        return context


class DeleteCorreo(DeleteView):
    model = Emails
    template_name = 'CRUD/deleteOtros.html'
    success_url = reverse_lazy('informacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['succes_url'] = self.success_url
        context['header'] = 'Correo'
        return context


class CreateSitios(CreateView):
    model = Sitios
    form_class = SitiosForm
    template_name = 'CRUD/createOtros.html'
    success_url = reverse_lazy('informacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['header'] = 'Añadir un sitio web'
        context['boton'] = 'Añadir'

        return context


class DeleteSitios(DeleteView):
    model = Sitios
    template_name = 'CRUD/deleteOtros.html'
    success_url = reverse_lazy('informacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['succes_url'] = self.success_url
        context['header'] = 'Sitio'
        return context


# ALMACEN
class ListAlmacen(ListView):
    template_name = 'almacen.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['path'] = 'almacen'
        context['titulo'] = 'Almacén'
        context['texto'] = 'En esta pantalla podrá indicar los productos que su empresa' \
                           ' tiene en existencia así como el precio y la cantidad.'

        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Almacen.objects.filter(user=self.request.user)


class CreateAlmacen(CreateView):
    model = Almacen
    form_class = AlmacenForm
    template_name = 'CRUD/createProducto.html'
    success_url = reverse_lazy('almacen')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Añadir producto a Almacén'
        context['boton'] = 'Añadir'
        context['header'] = 'Añada un producto'
        context['success_url'] = self.success_url
        context['unidades'] = Unidad.objects.all()
        return context


class UpdateAlmacen(UpdateView):
    model = Almacen
    form_class = AlmacenForm
    template_name = 'CRUD/createProducto.html'
    success_url = reverse_lazy('almacen')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar producto en Almacén'
        context['header'] = 'Editar producto'
        context['boton'] = 'Actualizar datos'
        context['unidades'] = Unidad.objects.all()
        context['success_url'] = self.success_url
        return context


class DeleteAlmacen(DeleteView):
    model = Almacen
    template_name = 'CRUD/Delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['succes_url'] = self.get_success_url()
        return context

    def get_success_url(self):

        if self.request.GET.get("user"):
            print('Root')
            user = self.request.GET.get("user")
            return reverse('DetailsRoot', kwargs={'pk': user})
        else:
            print('Normal')
            return reverse('almacen')


# BUSCANDO
class ListBuscando(ListView):
    template_name = 'buscando.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['path'] = 'buscando'
        context['titulo'] = 'Buscando'
        context[
            'texto'] = 'En esta pantalla podrá indicar aquellos productos que está buscando así como opcionalmente el precio y la cantidad. Si deja el valor de la casilla precio o cantidad en 0 estos criterios no se tendrán en cuenta para las búsquedas. Una vez alguna empresa agregue a su almacén algún producto de los que esta buscando, se le enviará una notificación por email y se pondrá una tarjeta en Alarmas donde podrá inspeccionar' \
                       ' la empresa en cuestión y los productos que coincidieron con su busqueda.'
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Buscando.objects.filter(user=self.request.user)


class CreateBuscando(CreateView):
    model = Buscando
    form_class = BuscandoForm
    template_name = 'CRUD/createProducto.html'
    success_url = reverse_lazy('buscando')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Añadir producto a Buscando'
        context['header'] = 'Añada un producto'
        context['boton'] = 'Añadir'
        uni = Almacen.objects.values_list('unidad')
        context['unidades'] = Unidad.objects.filter(unidad__in=uni)
        context['success_url'] = self.success_url
        return context


class UpdateBuscando(UpdateView):
    model = Buscando
    form_class = BuscandoForm
    template_name = 'CRUD/createProducto.html'
    success_url = reverse_lazy('buscando')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar producto en Buscando'
        context['header'] = 'Editar producto'
        context['boton'] = 'Actualizar datos'
        uni = Almacen.objects.values_list('unidad')
        context['unidades'] = Unidad.objects.filter(unidad__in=uni)
        context['success_url'] = self.success_url
        return context


class DeleteBuscando(DeleteView):
    model = Buscando
    template_name = 'CRUD/Delete.html'

    def get_success_url(self):

        if self.request.GET.get("user"):
            print('Root')
            user = self.request.GET.get("user")
            return reverse('DetailsRoot', kwargs={'pk': user})
        else:
            print('Normal')
            return reverse('buscando')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['succes_url'] = self.get_success_url()
        return context


# Root
class ListEmpresas(ListView):
    template_name = 'Root/empresas.html'
    queryset = User.objects.exclude(is_superuser=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['path'] = 'Root'
        context['titulo'] = 'Empresas'

        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(ListEmpresas, self).get_queryset()

        return get_qs(self, qs)


class DetailsRoot(DetailView):
    template_name = 'Root/VerEmpresa.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['telefonos'] = Telefonos.objects.filter(perfil=self.object)
        context['socios'] = Socios.objects.filter(perfil=self.object)
        context['whats'] = Whastapp.objects.filter(perfil=self.object)
        context['socios'] = Socios.objects.filter(perfil=self.object)
        context['domicilios'] = Domicilios.objects.filter(perfil=self.object)
        context['emails'] = Emails.objects.filter(perfil=self.object)
        context['webs'] = Sitios.objects.filter(perfil=self.object)
        context['almacen'] = Almacen.objects.filter(user=self.object)
        context['path'] = 'detallesRoot'
        context['titulo'] = f"Información sobre {self.object}"
        context['alarmas'] = Alarmas.objects.filter(user=self.object)
        return context


class EliminarUsuario(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'CRUD/deleteOtros.html'
    success_url = reverse_lazy('ListEmpresas')

    def test_func(self):
        # Verifica que el usuario autenticado tenga los permisos necesarios para eliminar un usuario
        usuario_a_eliminar = self.get_object()
        return self.request.user != usuario_a_eliminar

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['succes_url'] = reverse('DetailsRoot', kwargs={'pk': self.kwargs['pk']})
        context['header'] = 'Eliminar usuario'
        context['mensaje'] = '¿Estás seguro de que deseas eliminar este usuario?'
        return context


# def CreateAlmacenRoot(request, pk):
#     if request.method == 'POST':
#         form = AlmacenFormRoot(data=request.POST)
#         if form.is_valid():
#             form.instance.user_id = pk
#             form.save()
#             return HttpResponseRedirect(reverse('DetailsRoot', kwargs={'pk': pk}))
#
#     return render(request, 'Root/createProductoRoot.html', {
#         'form': AlmacenFormRoot(),
#         'empresa': User.objects.get(id=pk),
#         'header': 'Almacén de:',
#         'boton': 'Añadir',
#     })

class CreateAlmacenRoot(CreateView):
    model = Almacen
    form_class = AlmacenFormRoot
    template_name = 'Root/createProductoRoot.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Añadir producto a Almacén'
        context['boton'] = 'Añadir'
        context['header'] = 'Añada un producto'
        context['success_url'] = self.get_success_url()
        context['unidades'] = Unidad.objects.all()
        return context

    def get_success_url(self):
        print(self.kwargs)
        if 'pk' in self.kwargs:
            user = self.kwargs['pk']
        else:
            user = self.request.user
        return reverse('DetailsRoot', kwargs={'pk': user})

    def form_valid(self, form):
        print('adfaf ', form.instance.precio)
        user = self.kwargs['pk']
        form.instance.user_id = user
        form.save()
        return HttpResponseRedirect(reverse('DetailsRoot', kwargs={'pk': user}))


def EditAlmacenRoot(request, pk, user):
    alm = get_object_or_404(Almacen, pk=pk)

    if request.method == 'POST':
        form = AlmacenFormRoot(instance=alm, data=request.POST)
        if form.is_valid():
            form.instance.user_id = user
            form.save()
            return HttpResponseRedirect(reverse('DetailsRoot', kwargs={'pk': user}))

    return render(request, 'Root/createProductoRoot.html', {
        'almacen': alm,
        'form': AlmacenFormRoot(instance=alm),
        'empresa': User.objects.get(id=user),
        'header': 'Editar Almacén de:',
        'boton': 'Guardar cambios',
        'unidades': Unidad.objects.all(),
        'success_url': reverse('DetailsRoot', kwargs={'pk': user}),
    })


def CreateBuscandoRoot(request, pk):
    if request.method == 'POST':
        form = BuscandoFormRoot(data=request.POST)
        if form.is_valid():
            form.instance.user_id = pk
            form.save()
            return HttpResponseRedirect(reverse('DetailsRoot', kwargs={'pk': pk}))
    uni = Almacen.objects.values_list('unidad')
    return render(request, 'Root/createProductoRoot.html', {
        'form': BuscandoFormRoot(),
        'empresa': User.objects.get(id=pk),
        'header': 'Buscando de:',
        'boton': 'Añadir',
        'unidades': Unidad.objects.filter(unidad__in=uni),
        'success_url': reverse('DetailsRoot', kwargs={'pk': pk}),
    })


def EditBuscandoRoot(request, pk, user):
    busc = get_object_or_404(Buscando, pk=pk)

    if request.method == 'POST':
        form = BuscandoFormRoot(instance=busc, data=request.POST)
        if form.is_valid():
            form.instance.user_id = user
            form.save()
            return HttpResponseRedirect(reverse('DetailsRoot', kwargs={'pk': user}))
    uni = Almacen.objects.values_list('unidad')
    return render(request, 'Root/createProductoRoot.html', {
        'buscando': busc,
        'form': BuscandoFormRoot(instance=busc),
        'empresa': User.objects.get(id=user),
        'header': 'Editar Buscando de:',
        'boton': 'Guardar cambios',
        'unidades': Unidad.objects.filter(unidad__in=uni),
        'success_url': reverse('DetailsRoot', kwargs={'pk': user}),
    })


def CreateTelefonoRoot(request, user):
    if request.method == 'POST':
        form = TelefonoFormRoot(data=request.POST)
        print(request.POST)
        if form.is_valid():
            form.instance.perfil_id = user
            form.save()
            return HttpResponseRedirect(reverse('DetailsRoot', kwargs={'pk': user}))

    return render(request, 'CRUD/createOtros.html', {
        'form': TelefonoFormRoot(),
        'boton': 'Añadir'
    })


def CreateWhatsappRoot(request, user):
    if request.method == 'POST':
        form = WhatsappFormRoot(data=request.POST)
        print(request.POST)
        if form.is_valid():
            form.instance.perfil_id = user
            form.save()
            return HttpResponseRedirect(reverse('DetailsRoot', kwargs={'pk': user}))

    return render(request, 'CRUD/createOtros.html', {
        'form': WhatsappFormRoot(),
        'boton': 'Añadir'
    })


def CreateSociosRoot(request, user):
    if request.method == 'POST':
        form = SociosFormRoot(data=request.POST)
        print(request.POST)
        if form.is_valid():
            form.instance.perfil_id = user
            form.save()
            return HttpResponseRedirect(reverse('DetailsRoot', kwargs={'pk': user}))

    return render(request, 'CRUD/createOtros.html', {
        'form': SociosFormRoot(),
        'boton': 'Añadir'
    })


def CreateDomiciliosRoot(request, user):
    if request.method == 'POST':
        form = DomiciliosFormRoot(data=request.POST)
        print(request.POST)
        if form.is_valid():
            form.instance.perfil_id = user
            form.save()
            return HttpResponseRedirect(reverse('DetailsRoot', kwargs={'pk': user}))

    return render(request, 'CRUD/createOtros.html', {
        'form': DomiciliosFormRoot(),
        'boton': 'Añadir'
    })


def CreateEmailsRoot(request, user):
    if request.method == 'POST':
        form = CorreoFormRoot(data=request.POST)
        print(request.POST)
        if form.is_valid():
            form.instance.perfil_id = user
            form.save()
            return HttpResponseRedirect(reverse('DetailsRoot', kwargs={'pk': user}))

    return render(request, 'CRUD/createOtros.html', {
        'form': CorreoFormRoot(),
        'boton': 'Añadir'
    })


def CreateSitiosRoot(request, user):
    if request.method == 'POST':
        form = SitiosFormRoot(data=request.POST)
        print(request.POST)
        if form.is_valid():
            form.instance.perfil_id = user
            form.save()
            return HttpResponseRedirect(reverse('DetailsRoot', kwargs={'pk': user}))

    return render(request, 'CRUD/createOtros.html', {
        'form': SitiosFormRoot(),
        'boton': 'Añadir'
    })


class TelefonosUpdateView(UpdateView):
    model = Telefonos
    template_name = 'CRUD/createOtros.html'
    success_url = reverse_lazy('informacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Editar telefono'
        context['boton'] = 'Actualizar datos'
        return context

    def get_form_class(self):
        if self.request.GET.get("user"):
            print('Root')

            return TelefonoFormRoot
        else:
            print('Normal')
            return TelefonoForm

    def get_success_url(self):
        if self.request.GET.get("user"):
            print('Root')
            user = self.request.GET.get("user")
            return reverse('DetailsRoot', kwargs={'pk': user})
        else:
            print('Normal')
            return reverse('informacion')


class WhatsappUpdateView(UpdateView):
    model = Whastapp
    form_class = WhatsappForm
    template_name = 'CRUD/createOtros.html'
    success_url = reverse_lazy('informacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Editar whatsapp'
        context['boton'] = 'Actualizar datos'
        return context

    def get_form_class(self):
        if self.request.GET.get("user"):
            print('Root')

            return WhatsappFormRoot
        else:
            print('Normal')
            return WhatsappForm

    def get_success_url(self):
        if self.request.GET.get("user"):
            print('Root')
            user = self.request.GET.get("user")
            return reverse('DetailsRoot', kwargs={'pk': user})
        else:
            print('Normal')
            return reverse('informacion')


class SociosUpdateView(UpdateView):
    model = Socios
    form_class = SociosForm
    template_name = 'CRUD/createOtros.html'
    success_url = reverse_lazy('informacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Editar socio'
        context['boton'] = 'Actualizar datos'
        return context

    def get_form_class(self):
        if self.request.GET.get("user"):
            print('Root')

            return SociosFormRoot
        else:
            print('Normal')
            return SociosForm

    def get_success_url(self):
        if self.request.GET.get("user"):
            print('Root')
            user = self.request.GET.get("user")
            return reverse('DetailsRoot', kwargs={'pk': user})
        else:
            print('Normal')
            return reverse('informacion')


class DomiciliosUpdateView(UpdateView):
    model = Domicilios
    form_class = DomiciliosForm
    template_name = 'CRUD/createOtros.html'
    success_url = reverse_lazy('informacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Editar domicilios'
        context['boton'] = 'Actualizar datos'
        return context

    def get_form_class(self):
        if self.request.GET.get("user"):
            print('Root')

            return DomiciliosFormRoot
        else:
            print('Normal')
            return DomiciliosForm

    def get_success_url(self):
        if self.request.GET.get("user"):
            print('Root')
            user = self.request.GET.get("user")
            return reverse('DetailsRoot', kwargs={'pk': user})
        else:
            print('Normal')
            return reverse('informacion')


class CorreoUpdateView(UpdateView):
    model = Emails
    form_class = CorreoForm
    template_name = 'CRUD/createOtros.html'
    success_url = reverse_lazy('informacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Editar correo'
        context['boton'] = 'Actualizar datos'
        return context

    def get_form_class(self):
        if self.request.GET.get("user"):
            print('Root')

            return CorreoFormRoot
        else:
            print('Normal')
            return CorreoForm

    def get_success_url(self):
        if self.request.GET.get("user"):
            print('Root')
            user = self.request.GET.get("user")
            return reverse('DetailsRoot', kwargs={'pk': user})
        else:
            print('Normal')
            return reverse('informacion')


class SitiosUpdateView(UpdateView):
    model = Sitios
    form_class = SitiosForm
    template_name = 'CRUD/createOtros.html'
    success_url = reverse_lazy('informacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Editar sitio'
        context['boton'] = 'Actualizar datos'
        return context

    def get_form_class(self):
        if self.request.GET.get("user"):
            print('Root')

            return SitiosFormRoot
        else:
            print('Normal')
            return SitiosForm

    def get_success_url(self):
        if self.request.GET.get("user"):
            print('Root')
            user = self.request.GET.get("user")
            return reverse('DetailsRoot', kwargs={'pk': user})
        else:
            print('Normal')
            return reverse('informacion')


def unidad_list(request):
    unidades = Unidad.objects.all()
    return render(request, 'Root/unidad_list.html', {'unidades': unidades, 'path': 'unidades', 'titulo': 'Unidades'})


def unidad_create(request):
    if request.method == 'POST':
        form = UnidadMedidaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Lista_unidades')
    else:
        form = UnidadMedidaForm()
    return render(request, 'CRUD/createOtros.html', {'form': form, 'boton': 'Agregar'})


def unidad_edit(request, pk):
    unidad = get_object_or_404(Unidad, pk=pk)
    if request.method == 'POST':
        form = UnidadMedidaForm(request.POST, instance=unidad)
        if form.is_valid():
            form.save()
            return redirect('Lista_unidades')
    else:
        form = UnidadMedidaForm(instance=unidad)
    return render(request, 'CRUD/createOtros.html', {'form': form, 'boton': 'Guardar cambios'})


def unidad_delete(request, pk):
    unidad = get_object_or_404(Unidad, pk=pk)

    try:
        unidad.delete()
    except ProtectedError:
        messages.error(request,
                       'No se puede eliminar esta instancia porque hay uno o más registros relacionados con ella.')

    return redirect('Lista_unidades')
