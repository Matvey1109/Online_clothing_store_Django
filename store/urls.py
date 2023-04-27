from django.urls import path
from . import views

urlpatterns = [
	path('', views.main, name="main"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('categories/', views.categories, name="categories"),
	path('liked/', views.liked, name="liked"),
	path('profile/', views.profile, name="profile"),
	path('login/',views.LoginUser.as_view(), name="login"),
	path('register/',views.RegisterUser.as_view(), name="register"),
	path('logout/',views.logout_user, name="logout"),
	path('product/<slug:product_slug>/', views.product, name="product"),
	path('add_to_cart/<slug:product_slug>',views.add_to_cart,name="add_to_cart"),
	path('change_quantity/<int:order_product_pk>/<int:plus>',views.change_quantity,name = "change_quantity"),
	path('success/', views.successPayment,name="success"),
	path('cancel/', views.cancelPayment,name="cancel"),
	path('get_address/',views.get_address,name = 'get_address'),
	path('create-checkout-session/<int:order_id>/', views.CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
	path('landing/<int:order_id>/',views.ProductLandingPageView.as_view(),name = 'landing'),
	path('<slug:gender_slug>/', views.gender, name = "gender"),
	path('<slug:gender_slug>/<slug:category_slug>',views.category, name="category"),
	path('webhooks/stripe/', views.stripe_webhook, name='stripe-webhook'),
]