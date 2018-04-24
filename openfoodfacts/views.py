from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404, JsonResponse
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

from .forms import SignUpForm, EmailChangeForm
from .models import Products, Substitutes, User

IMG = 'https://authentic-visit.jp/wp-content/uploads/2017/12/gregoire-jeanneau-1451361.jpg'


def index(request):
    """Home page."""
    context = {
        "page_title": "Accueil"
    }
    return render(request, 'openfoodfacts/index.html', context)


def search(request):
    """Return a list of products with a nutriscore at least equivalent of the product."""
    try:
        id_prod = request.GET.get('id_product')
        origin = Products.objects.get(id_product=id_prod)
    except Products.DoesNotExist:
        raise Http404
    else:
        sub_list = Products.objects.filter(category=origin.category)
        sub_list = sub_list.filter(nutriscore__lte=origin.nutriscore)
        sub_list = sub_list.order_by('nutriscore')
        sub_list = sub_list.exclude(pk=id_prod)

        if request.user.is_authenticated:
            # Remove products already in the user list
            for sub in sub_list:
                listed = Substitutes.objects.filter(
                    origin=id_prod,
                    replacement=sub.id_product,
                    user=request.user
                    )
                if listed:
                    sub_list = sub_list.exclude(pk=sub.id_product)

    # user want to save a product
    if request.method == 'POST':
        origin = request.POST.get('origin')
        replacement = request.POST.get('replacement')

        origin = Products.objects.get(pk=origin)
        replacement = Products.objects.get(pk=replacement)

        Substitutes.objects.create(
            origin=origin,
            replacement=replacement,
            user=request.user
            )
        sub_list = sub_list.exclude(pk=replacement.id_product)

    # Slices pages
    paginator = Paginator(sub_list, 9)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'paginate': True,
        'query': id_prod,
        'title': origin.product_name,
        'img': origin.img,
        'query_prod': id_prod,
        "page_title": "Résultats"
    }

    return render(request, 'openfoodfacts/search.html', context)


def detail(request, id_product):
    """ Detail the product with nutiscore, and nutrient quantity for 100g."""
    # if product doesn't exists raise error 404
    product = get_object_or_404(Products, pk=id_product)

    fat_index_img = ""
    saturated_fat_index_img = ""
    salt_index_img = ""
    sugar_index_img = ""
    url = "https://static.openfoodfacts.org/images/misc/"

    # Image based on the qantity of nutrients
    if product.fat is not None:
        if 0 <= product.fat < 3:
            fat_index_img = url + "low_30.png"
        elif 3 <= product.fat <= 20:
            fat_index_img = url + "moderate_30.png"
        else:
            fat_index_img = url + "high_30.png"

    if product.saturated_fat is not None:
        if 0 <= product.saturated_fat < 1.5:
            saturated_fat_index_img = url + "low_30.png"
        elif 1.5 <= product.saturated_fat <= 5:
            saturated_fat_index_img = url + "moderate_30.png"
        else:
            saturated_fat_index_img = url + "high_30.png"

    if product.salt is not None:
        if 0 <= product.salt < 0.3:
            salt_index_img = url + "low_30.png"
        elif 0.3 <= product.salt <= 1.5:
            salt_index_img = url + "moderate_30.png"
        else:
            salt_index_img = url + "high_30.png"

    if product.sugar is not None:
        if 0 <= product.sugar < 5:
            sugar_index_img = url + "low_30.png"
        elif 5 <= product.sugar <= 12.5:
            sugar_index_img = url + "moderate_30.png"
        else:
            sugar_index_img = url + "high_30.png"

    context = {
        "product": product.product_name,
        "img": product.img,
        "nutriscore": product.nutriscore,
        "fat": product.fat,
        "saturated_fat": product.saturated_fat,
        "salt": product.salt,
        "sugar": product.sugar,
        "fat_index_img": fat_index_img,
        "saturated_fat_index_img": saturated_fat_index_img,
        "salt_index_img": salt_index_img,
        "sugar_index_img": sugar_index_img,
        "redirection": product.url,
        "page_title": product.product_name
    }
    return render(request, 'openfoodfacts/detail.html', context)


def sign_up(request):
    """Sign up view with buil in django form."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/openfoodfacts/account')
    else:
        form = SignUpForm()

    context = {
        "form": form,
        "title": "S'enregistrer",
        "img": IMG,
        "page_title": "S'enregistrer"
    }
    return render(request, 'openfoodfacts/sign_up.html', context)


@login_required
def account(request):
    context = {
        "user": request.user,
        "img": IMG,
        "page_title": 'Votre compte',
        "passwd_form": PasswordChangeForm(user=request.user),
        "email_form": EmailChangeForm()
    }
    return render(request, 'openfoodfacts/account.html', context)


def validate_changemail(request):
    """AJAX view for changing user e-mail."""
    data = dict()

    if request.method == 'POST':
        email_form = EmailChangeForm(data=request.POST)

        if email_form.is_valid():
            new_mail = email_form.cleaned_data['new_email']

            u = User.objects.get(username=request.user)
            if new_mail != u.email:
                u.email = new_mail
                u.save()
                print(u.email)
                data['form_is_valid'] = True
            else:
                data['form_is_valid'] = False

        return JsonResponse(data)


def validate_change_passwd(request):
    """AJAX view for changing user password."""
    data = dict()

    if request.method == 'POST':
        passwd_form = PasswordChangeForm(
            request.user,
            request.POST
            )
        if passwd_form.is_valid():
            passwd_form.save()
            update_session_auth_hash(request, passwd_form.user)
            data['msg'] = 'Votre mot de passe a bien été changé !'
            data['form_is_valid'] = True
        else:
            data['msg'] = 'Impossible de changer votre mot de passe. Réessayez!'
            data['form_is_valid'] = False
    return JsonResponse(data)



def contacts(request):
    context = {
        "title": 'Contacts',
        "img": IMG,
        'page_title': 'Nous contacter'
        }
    return render(request, 'openfoodfacts/contacts.html', context)


def legals(request):

    context = {
        "title": "Mentions légales",
        "img": IMG,
        "page_title": "Mentions légales"
    }
    return render(request, 'openfoodfacts/legals.html', context)


@login_required
def saved(request):
    """
    Products saved by the user.
    User can delete a product by using POST request.
    """

    products_saved = Substitutes.objects.filter(user=request.user)

    if request.method == 'POST':
        origin = request.POST.get('origin')
        replacement = request.POST.get('replacement')

        origin = Products.objects.get(pk=origin)
        replacement = Products.objects.get(pk=replacement)

        Substitutes.objects.get(
            origin=origin,
            replacement=replacement,
            user=request.user
            ).delete()

    # Slices pages
    paginator = Paginator(products_saved, 5)
    page = request.GET.get('page')

    try:
        products_saved = paginator.page(page)
    except PageNotAnInteger:
        products_saved = paginator.page(1)
    except EmptyPage:
        products_saved = paginator.page(paginator.num_pages)

    context = {
        "title": "Vos aliments sauvegardés",
        "img": IMG,
        "products_saved": products_saved,
        "paginate": True,
        "page_title": "Vos aliments sauvegardés"
    }
    return render(request, 'openfoodfacts/saved.html', context)


class ProductsListView(ListView):
    """Return a product list based on the product name and matching query."""
    model = Products

    def get_queryset(self):
        """Get the query parameter."""
        self.query = self.request.GET.get('query')

        if not self.query:
            return redirect(index)

        # query match product_name
        queryset = Products.objects.filter(
            product_name__iexact=self.query
            )

        # query doesn't match exactly but can match product_name
        queryset = Products.objects.filter(
            product_name__icontains=self.query
            )

        # filter distinct categories in the queryset
        categories = queryset.distinct('category')
        self.categories = {}
        # keep the last category
        for category in categories:
            c = "".join(
                str(category.category).split(',')[-1:]).replace('[', '').replace('\'', '').replace(']', '')
            self.categories[category] = c
        queryset = queryset.order_by('nutriscore')
        if not queryset:
            raise Http404
        else:
            return queryset

    def get_context_data(self, **kwargs):
        """Contains essential data for the page."""
        data = super(ProductsListView, self).get_context_data(**kwargs)

        data['page_title'] = 'Produit à remplacer'
        data['img'] = IMG
        data['query'] = self.query
        data['categories'] = self.categories
        return data
