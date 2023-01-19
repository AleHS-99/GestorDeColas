from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, FormView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .models import *
# Create your views here.

class HomePage(ListView):
    model = ColaModel
    template_name = 'index.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        a = ColaModel.objects.filter(creada_por=request.user)
        for i in a:
            if not request.user in i.usuarios_acceso.all():
                b = []
                for j in i.usuarios_acceso.all():
                    b.append(j)
                b.append(i.creada_por)
                i.usuarios_acceso.set(User.objects.filter(username__in=b))
                i.save()
        return super().dispatch(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = ColaModel.objects.filter(usuarios_acceso=self.request.user)
        return context

class LoginFormView(LoginView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

class CreateUserForm(FormView):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,*args,**kwargs)

    def form_valid(self, form):
        form.save()
        return redirect('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class AddCola(CreateView):
    template_name = 'addCola.html'
    form_class = ColaForm
    model = ColaModel
    success_url = reverse_lazy('HomePage')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request,*args,**kwargs)
    def form_valid(self, form):
        form.instance.creada_por = self.request.user
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']='Añadir Cola'
        return context

class EditCola(UpdateView):
    model = ColaModel
    form_class = ColaForm
    template_name = 'addCola.html'
    success_url = reverse_lazy('HomePage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']='Editar Cola'
        return context

class DeleteCola(DeleteView):
    model = ColaModel
    template_name = 'deleteCola.html'
    success_url = reverse_lazy('HomePage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']='Eliminar Cola'
        context['list_url'] = reverse_lazy('HomePage')
        return context

class List_Control(ListView):
    model = ColaItem
    template_name = 'list_control.html'

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.id = kwargs['pk']
        return super().dispatch(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'subir':
                codigo = request.POST['id']
                item = ColaItem.objects.get(cola=self.id,numero=codigo)
                n = 1
                if codigo == '1':
                    item.numero = len(ColaItem.objects.filter(cola=self.id))+1
                    item.save()
                    for i in ColaItem.objects.filter(cola=self.id).order_by('numero'):
                        i.numero = n
                        i.save()
                        n+=1
                else:
                    n = ColaItem.objects.get(cola=self.id,numero=item.numero-1)
                    n.numero = codigo
                    n.save()
                    item.numero = int(codigo)-1
                    item.save()
                data['hecho'] = 'hecho'
            else:
                data['error']="Ha ocurrido un error"
        except Exception as e:
            print(e)
            data['error']=str(e)
        return JsonResponse(data,safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list']=ColaItem.objects.filter(cola=self.id).order_by('numero')
        context['title']=ColaModel.objects.get(codigo=self.id)
        context['id'] = self.id
        return context

class AddColaItem(CreateView):
    template_name = 'addItem.html'
    form_class = ItemForm
    model = ColaItem

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.id = kwargs['pk']
        return super().dispatch(request,*args,**kwargs)

    def form_valid(self, form):
        form.instance.cola = ColaModel.objects.get(codigo=self.id)
        self.number = 1
        if ColaItem.objects.filter(cola=ColaModel.objects.get(codigo=self.id)):
            self.number=len(ColaItem.objects.filter(cola=ColaModel.objects.get(codigo=self.id)))
        else:
            self.number = 1
        while True:
            if ColaItem.objects.filter(cola=ColaModel.objects.get(codigo=self.id),numero=self.number):
                self.number+=1
            else:
                break
        form.instance.numero = self.number
        form.save()
        return redirect('ListControl',self.id)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']='Añadir Cola'
        context['id'] = self.id
        return context

class EditColaItem(UpdateView):
    model = ColaItem
    form_class = ItemForm
    template_name = 'addItem.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.id = kwargs['pk']
        self.pk = ColaItem.objects.get(codigo=self.id)
        self.codigo = self.pk.cola.codigo
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.num = ColaItem.objects.get(codigo=self.id)
        self.number = self.num.numero
        form.instance.numero = self.number
        form.save()
        return redirect('ListControl',self.codigo)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']='Editar Registro'
        return context

class DeleteColaItem(DeleteView):
    model = ColaItem
    template_name = 'deleteItem.html'

    def dispatch(self, request, *args, **kwargs):
        self.id = kwargs['pk']
        self.pk = ColaItem.objects.get(codigo=self.id)
        self.codigo = self.pk.cola.codigo
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.pk.delete()
        self.number = 1
        for a in ColaItem.objects.filter(cola=self.codigo).order_by('numero'):
            a.numero = self.number
            a.save()
            self.number+=1
        return redirect('ListControl',self.codigo)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Registro'
        context['id'] = self.codigo
        return context
