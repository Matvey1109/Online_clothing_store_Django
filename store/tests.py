from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase,Client
from django.urls import reverse
import json
from .models import *


class TestViews(TestCase):

    def setUp(self):

        user = get_user_model()
        self.user = user.objects.create_user(username="Dmitry")
        self.client1 = Client()
        self.client1.force_login(self.user)
        self.testgender = Gender.objects.create(name="TestGender", slug="TestGender")
        self.testcategory = Category.objects.create(name="TestCategory", slug="TestCategory")
        self.testgender.categories_id.add(self.testcategory)
        photo =  (
            b'\x13\x14\x15\x15\x15\x15\x15\x15'

        )
        upl_photo = SimpleUploadedFile(name="testphoto",content=photo)
        self.testproduct = Product.objects.create(name="TestProduct",slug="TestProduct",price=20,cat=self.testcategory,gender=self.testgender,price_discount=40,discount=True,photo=upl_photo)
        self.testproduct.gender = self.testgender
        self.testsize = Size.objects.create(name="TestSize")


    def test_main(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[0].template_name, 'store/main.html')
        self.assertEqual(response.context[0].dicts[3]['gender_selected'], -1)
        self.assertEqual(response.context[0].dicts[3]['cat_selected'], -1)
        self.assertEqual(response.context[0].dicts[3]['ordered'], 0)
    def test_cart(self):
        response = self.client1.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[0].template_name, 'store/cart.html')
        self.assertEqual(response.context[0].dicts[3]['gender_selected'], -1)
        self.assertEqual(response.context[0].dicts[3]['cat_selected'], -1)
        self.assertEqual(response.context[0].dicts[3]['ordered'], 0)

    def test_cart_redirect(self):
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')

    # def test_checkout(self):
    #     print(reverse('checkout'))
    #     response = self.client1.get(reverse('checkout'))
    #     #self.assertEqual(response.status_code, 200)

    def test_liked(self):
        response = self.client1.get(reverse('liked'))
        self.assertEqual(response.context[0].template_name, 'store/liked.html')
        #self.assertTrue(isinstance(response.context[0].dicts[3]['favorite'], Favorite))
        self.assertIsInstance(response.context[0].dicts[3]['favorite'], Favorite)

    def test_liked_redirect(self):
        response = self.client.get(reverse('liked'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')

    def test_register(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/register.html')

    def test_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/login.html')

    def test_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')

    def test_gender(self):
        response = self.client.get(reverse('gender', kwargs={'gender_slug': self.testgender.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/gender.html')
        self.assertEqual(response.context[0].dicts[3]['cats'][0].name,'TestCategory')
        self.assertEqual(response.context[0].dicts[3]['gender_selected'].name, 'TestGender')
        self.assertEqual(response.context[0].dicts[3]['cat_selected'], -1)

    def test_category(self):
        response = self.client.get(reverse('category', kwargs={'gender_slug': self.testgender.slug,'category_slug':self.testcategory.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/category.html')
        self.assertEqual(response.context[0].dicts[3]['cats'][0].name, 'TestCategory')
        self.assertEqual(response.context[0].dicts[3]['gender_selected'].name, 'TestGender')
        self.assertEqual(response.context[0].dicts[3]['cat_selected'].name, 'TestCategory')

    def test_add_to_cart(self):
        response = self.client1.get(reverse('add_to_cart',kwargs={'product_slug':self.testproduct.slug,'size_name':self.testsize.name}))
        order = Order.objects.last()
        orderproduct = OrderProduct.objects.last()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/cart/')
        self.assertEqual(order.user.username,"Dmitry")
        self.assertEqual(orderproduct.product.name, "TestProduct")

    def test_change_quantity_plus(self):

        order_product = OrderProduct.objects.create(user=self.user,product=self.testproduct)
        order_product.save()
        quantity_old = order_product.quantity
        response = self.client1.get(reverse('change_quantity', kwargs={'order_product_pk':order_product.pk, 'plus': 1}))
        order_product = OrderProduct.objects.get(pk=order_product.pk)
        quantity_new = order_product.quantity
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/cart/')
        self.assertEqual(quantity_new-quantity_old,1)

    def test_change_quantity_minus(self):

        order_product = OrderProduct.objects.create(user=self.user,product=self.testproduct,quantity=2)
        order_product.save()
        quantity_old = order_product.quantity
        response = self.client1.get(reverse('change_quantity', kwargs={'order_product_pk':order_product.pk, 'plus': 0}))
        order_product = OrderProduct.objects.get(pk=order_product.pk)
        quantity_new = order_product.quantity
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/cart/')
        self.assertEqual(quantity_new-quantity_old,-1)

    def test_change_quantity_delete(self):
        order_product = OrderProduct.objects.create(user=self.user, product=self.testproduct)
        order_product.save()
        response = self.client1.get(
            reverse('change_quantity', kwargs={'order_product_pk': order_product.pk, 'plus': 0}))
        order_product = OrderProduct.objects.filter(pk=order_product.pk)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/cart/')
        self.assertEqual(len(order_product), 0)

    def test_create_checkout_session(self):
        order = Order.objects.create(user=self.user)
        order_product = OrderProduct.objects.create(user=self.user, product=self.testproduct)
        order.products.add(order_product)
        response = self.client1.post(reverse('create-checkout-session',kwargs={'order_id':order.pk}))
        self.assertEqual(response.status_code, 200)

    def test_success_payment(self):
        response = self.client1.get(reverse('success'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[0].template_name, 'store/successpayment.html')

    def test_cancel_payment(self):
        response = self.client1.get(reverse('cancel'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[0].template_name, 'store/cancelpayment.html')

    def test_product_landing(self):
        order = Order.objects.create(user=self.user)
        order_product = OrderProduct.objects.create(user=self.user, product=self.testproduct)
        order.products.add(order_product)
        response = self.client1.get(reverse('landing', kwargs={'order_id': order.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[0].template_name, 'store/checkout.html')
        self.assertEqual(response.context[0].dicts[3]['order_id'],order.pk)

    def test_get_adress(self):
        order = Order.objects.create(user=self.user)
        order.save()
        data = '{"address": "Testadress","city": "city","state": "state","zipcode": "zipcode","order_id": 1}'
        response = self.client1.generic('POST', reverse('get_address'), data)
        order = Order.objects.get(user=self.user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(order.address.address,"Testadress")
        self.assertEqual(order.address.city, "city")
        self.assertEqual(order.address.state, "state")
        self.assertEqual(order.address.zipcode, "zipcode")

    def test_product(self):
        response = self.client1.get(reverse('product', kwargs={'product_slug': self.testproduct.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[0].template_name, 'store/product.html')
        self.assertEqual(response.context[0].dicts[3]['product'], self.testproduct)

    def test_add_to_favorite(self):
        response = self.client1.get(
            reverse('add_to_favorite', kwargs={'product_slug': self.testproduct.slug}))
        favorite = Favorite.objects.last()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/liked/')
        self.assertEqual(favorite.user.username, "Dmitry")
        self.assertEqual(favorite.products.last().name, "TestProduct")

    def test_delete_from_favorite(self):
        favorite = Favorite.objects.create(user=self.user)
        favorite.products.add(self.testproduct)
        favorite.save()
        response = self.client1.get(
            reverse('delete_from_favorite', kwargs={'product_pk': self.testproduct.pk}))
        favorite = Favorite.objects.filter(user=self.user)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/liked/')
        self.assertEqual(favorite[0].products.count(), 0)

    def test_add_to_favorite_redirect(self):
        response = self.client.get(reverse('add_to_favorite', kwargs={'product_slug': self.testproduct.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')



