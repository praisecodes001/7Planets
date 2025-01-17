from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static
from .forms import CreateUserForm, PostForm 
from django.views import View
from django.shortcuts import render,  get_object_or_404 , redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum
from django.core.mail import send_mail
from django.http import JsonResponse
from decimal import Decimal
from .models import Post, Cart, CartItem,Order,OrderItem
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    
    return render(request,'planetapp/home.html')
def conditions(request):
    
    return render(request,'planetapp/conditions.txt')


@login_required(login_url='login')
def product(request):
    posts = Post.objects.all()
    cart_item_count = 0  # Default to 0 if no cart exists
    
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()  # Get the cart for the logged-in user
        if cart:
            cart_item_count = cart.items.aggregate(Sum('quantity'))['quantity__sum'] or 0

    context = {
        'posts': posts,
        'cart_item_count': cart_item_count,
    }
    return render(request, 'planetapp/product.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('product')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Registration successful, Login ' + user)

                return redirect('login')

        context = {'form': form}
    
    return render(request,'planetapp/register.htm', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('product')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('product')
            else:
                messages.info(request, 'Username OR Password is incorrect')

        context = {}
    return render(request, 'planetapp/login.html')

def logoutUser(request):
    logout(request)
    messages.info(request, 'Logout successfull')
    return redirect('login')



@login_required(login_url='login')
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        post = get_object_or_404(Post, id=product_id)

        # Get or create the user's cart
        cart, _ = Cart.objects.get_or_create(user=request.user)

        # Add or update the cart item
        cart_item, created = CartItem.objects.get_or_create(cart=cart, post=post)
        if not created:
            cart_item.quantity += quantity
        cart_item.save()

        # Add a success message
        messages.success(request, f"{post.name} has been added to your cart!")

        # Redirect back to the products page
        return redirect('product')  # Ensure 'product' matches the URL name for your products.html page

    messages.error(request, "Invalid request. Please try again.")
    return redirect('product')


@login_required(login_url='login')
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'planetapp/cart.html', {'cart': cart})


@login_required(login_url='login')
def List(request):
    posts = []
    for post in Post.objects.all():
          
        post = {
            'name': post.name,
            'price': post.price,
            'image': post.image.url,
        }
        posts.append(post)
        context ={
            'posts': Post.objects.all(),
        }
    return render(request, 'planetapp/product.html', {'posts': posts})

class PostListView(ListView):
    model = Post
    template_name = 'planetapp/product.html'
    context_object_name = 'posts'
    ordering = ['?']


class PostDetailView(DetailView):
    model = Post

@login_required(login_url='login')
def remove_from_cart(request, post_id):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        cart_item = get_object_or_404(CartItem, id=item_id, post_id=post_id)

        # Remove the item from the cart
        cart_item.delete()

        # Optionally, add a success message
        messages.success(request, f'Item has been removed from your cart.')

    # Redirect back to the cart page
    return redirect('cart_view')  # Replace 'cart' with the name of your cart view

@login_required(login_url='login')
def checkout(request):
    if request.method == "POST":
        user = request.user
        cart = Cart.objects.get(user=user)  # Get the user's cart
        size = request.POST.get("size")
        phone_number = request.POST.get("num")
        email = request.POST.get("email")
        address = request.POST.get("address")

        # Calculate the total price (call the method, not reference it)
        total_price = Decimal(cart.total_price())

        # Create the order
        order = Order.objects.create(
            user=user,
            size=size,
            phone_number=phone_number,
            email=email,
            address=address,
            total_price=total_price
        )

        # Create order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                post=cart_item.post,
                quantity=cart_item.quantity,
                price=cart_item.post.price
            )

        # Clear the cart
        cart.items.all().delete()

        return redirect('order_success')  # Redirect to success page


def order_success(request):

    return render(request, "planetapp/order_success.html")    

# Restrict access to staff users or superusers
def owner_check(user):
    return user.is_staff or user.is_superuser

@user_passes_test(owner_check)
def dashboard(request):
    orders = Order.objects.all().order_by('-created_at')  # Fetch all orders, newest first
    return render(request, 'planetapp/dashboard.html', {'orders': orders})

@user_passes_test(owner_check)
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'planetapp/order_detail.html', {'order': order})


def update_order_status(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get("status")
        order.status = new_status
        order.save()
        return redirect("order_detail", order_id=order.id)    
    