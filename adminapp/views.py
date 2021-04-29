from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from django.contrib.auth.decorators import user_passes_test
from authapp.forms import ShopUserRegisterForm
from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.utils.decorators import method_decorator



# Create your views here.
'''
@user_passes_test(lambda u: u.is_superuser)
def users(request):
    title = 'админка / ползователи'
    users_list = ShopUser.objects.all()

    content = {'title': title, 'objects': users_list}
    return render(request, 'adminapp/users.html', content)
'''

class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return  super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка / ползователи'
        return context


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = 'ползователи / создать'

    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)

        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:users'))
    else:
        user_form = ShopUserRegisterForm()

    content = {'title': title, 'update_form': user_form}
    return render(request, 'adminapp/user_update.html', content)

@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    title = 'ползователи / редактировать'
    edit_user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:users'))
    else:
        edit_form = ShopUserAdminEditForm(instance=edit_user)

    content = {'title': title, 'update_form': edit_form}
    return render(request, 'adminapp/user_update.html', content)

@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    title = 'ползователи / удалить'
    user_item = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        if user_item.is_active:
            user_item.is_active = False
        else:
            user_item.is_active = True

        user_item.save()
        return HttpResponseRedirect(reverse('admin:users'))

    content = {'title': title, 'user_to_delete': user_item}
    return render(request, 'adminapp/user_delete.html', content)



@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'админка / категории'
    categories_list = ProductCategory.objects.all()
    
    content = {'title': title, 'objects': categories_list}
    return render(request, 'adminapp/categories.html', content)

'''
@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    title = 'категории / создать'

    if request.method == 'POST':
        category_form = ProductCategoryEditForm(request.POST)

        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin:categories'))
    else:
        category_form = ProductCategoryEditForm()

    content = {'title': title, 'update_form': category_form}
    return render(request, 'adminapp/category_update.html', content)
'''


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    form_class = ProductCategoryEditForm


'''
@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    title = 'категории / редактирование'
    edit_category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        category_form = ProductCategoryEditForm(request.POST, instance=edit_category)

        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin:categories'))
    else:
        category_form = ProductCategoryEditForm(instance=edit_category)

    content = {'title': title, 'update_form': category_form}
    return render(request, 'adminapp/category_update.html', content)
'''


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    form_class = ProductCategoryEditForm


'''
@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    title = 'категории / удалить'
    category_item = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        if category_item.is_active:
            category_item.is_active = False
        else:
            category_item.is_active = True

        category_item.save()
        return HttpResponseRedirect(reverse('admin:categories'))

    content = {'title': title, 'category_to_delete': category_item}
    return render(request, 'adminapp/category_delete.html', content)
'''


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.success_url)


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    title = 'админка / продукты'
    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    content = {'title': title, 'category': category, 'objects': products_list}
    return render(request, 'adminapp/products.html', content)

@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    title = 'продукт / добавить'
    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES)

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:products', args=[category.pk]))
    else:
        edit_form = ProductEditForm()

    content = {'title': title, 'update_form': edit_form, 'category': category}
    return render(request, 'adminapp/product_update.html', content)


'''
@user_passes_test(lambda u: u.is_superuser)
def product_read(request, pk):
    title = 'продукт / подробнее'
    product = get_object_or_404(Product, pk=pk)

    content = {'title': title, 'object': product}
    return render(request, 'adminapp/product_read.html', content)
'''

class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = 'продукт / редактировать'
    edit_product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:product_update', args=[edit_product.pk]))
    else:
        edit_form = ProductEditForm(instance=edit_product)

    content = {'title': title, 'update_form': edit_form, 'category': edit_product.category}
    return render(request, 'adminapp/product_update.html', content)

@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    title = 'продукт / удалить'
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.is_active = False
        product.save()
        return HttpResponseRedirect(reverse('admin:products', args=[product.category.pk]))

    content = {'title': title, 'product_to_delete': product}
    return render(request, 'adminapp/product_delete.html', content)






