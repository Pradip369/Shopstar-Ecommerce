from django.shortcuts import render, redirect
from .models import CarouselOffer,HomePageOffer,Category,Product,HomePageCarouselOffer
from order_detail.models import Order,OrderItem,MyOrder,LikeProduct
from user_detail.models import ShippingAddress,Profile
from user_detail.forms import Shippingaddress
from website_detail.models import Bugreport,Contact
from website_detail.form import Bug_report
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect
import time
import hashlib
import hmac
import base64
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from shopstar import settings
from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives
from django.db.models.query_utils import Q 
import json
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView, FormView, CreateView
from django.utils.decorators import method_decorator
from django.urls.base import reverse_lazy, reverse
from django import forms
from django.views.decorators.http import require_POST


def home(request):
    carouseloffer = CarouselOffer.objects.all().order_by("-id")
    homepageoffer = HomePageOffer.objects.all().order_by("-id")
    homepagecarouseloffer = HomePageCarouselOffer.objects.all().order_by("-id")
    return render(request,'home.html',{"carouseloffer":carouseloffer,"homepageoffer":homepageoffer,"homepagecarouseloffer":homepagecarouseloffer})

def home_offer(request,pk,event,slug):
    category = Category.objects.get(pk=pk)
        
    if event == "low_to_high":
        product = Product.objects.filter(category=category).order_by('price')
    elif event == "hight_to_low":
        product = Product.objects.filter(category=category).order_by('-price')
    elif event == "randomly":
        product = Product.objects.filter(category=category).order_by('?')
    elif event == "no":
        product = Product.objects.filter(category=category).order_by('-id')

    return render(request,'category_product.html',{"category":category,"product":product})

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
      
        order = Order.objects.filter(customer=customer,complete=False).exists()
        if order:
                order = Order.objects.get(customer=customer,complete=False)
                items = OrderItem.objects.filter(order=order)
        else:
                order = {'get_total_price':0,'get_total_item':0}
                items = []
        
    else:
        items = [] 
        order = {'get_total_price':0,'get_total_item':0}
    return render(request,"cart.html",{"items":items,"order":order})

@login_required
def checkout(request):
    
    customer = request.user
    order = Order.objects.filter(customer=customer,complete=False).exists()
    
    if order:
        order = Order.objects.get(customer=customer,complete=False)

        items = OrderItem.objects.filter(order=order)
            
        sa = ShippingAddress.objects.filter(customer=customer).exists()
        
        for it in items:
            if it.quantity > it.product.total_quantity:  
                ort = OrderItem.objects.filter(product = it.product)
                
                if it.product.total_quantity == 0:
                    ort.delete()
                else:
                    quantity = it.quantity - it.product.total_quantity
                    ort.update(quantity = quantity)
                messages.add_message(request,messages.SUCCESS, f'Sorry..Something went wrong..TRY AGAIN!!')  
                return redirect(request.META['HTTP_REFERER'])

                
        if request.method == "POST":
            fm=Shippingaddress(request.POST)
            
            if fm.is_valid():
                house_no = fm.cleaned_data["house_no"]
                full_address = fm.cleaned_data["full_address"]
                nearest_landmark = fm.cleaned_data["nearest_landmark"]
                country = fm.cleaned_data['country']
                city = fm.cleaned_data["city"]
                state = fm.cleaned_data["state"]
                zipcode = fm.cleaned_data["zipcode"]
                phone_no = fm.cleaned_data["phone_no"]
                
                if sa:
                    sa2 = ShippingAddress.objects.filter(customer=customer)
                    
                    sa2.update(
                    customer = customer,
                    country = country,
                    house_no = house_no,
                    full_address = full_address,
                    nearest_landmark = nearest_landmark,
                    city = city,
                    state = state,
                    zipcode = zipcode,
                    phone_no = phone_no)
                    
                                                
                    return HttpResponseRedirect('/place_order/')
                else:
                    data = ShippingAddress.objects.create(
                                customer = customer,
                                order = order,
                                country = country,
                                house_no = house_no,
                                full_address = full_address,
                                nearest_landmark = nearest_landmark,
                                city = city,
                                state = state,
                                zipcode = zipcode,
                                phone_no = phone_no
                                                        )
                    data.save()
                    return HttpResponseRedirect('/place_order/')
            else:
                messages.add_message(request,messages.SUCCESS, 'Please fill the currect or sufficient shipping address information!!')  
                return HttpResponseRedirect(redirect_to = '/checkout/#')
        elif sa:
            sd = ShippingAddress.objects.get(customer=customer)
            fm = Shippingaddress(instance=sd)
        else:
            fm = Shippingaddress()        
        
        delvery_india = float(settings.INDIA_DELIVERY)
        delvery_foreign = float(settings.FOREIGN_DELIVERY)
        
        return render(request,"checkout.html",{"items":items,"order":order,"fm":fm,"delvery_india" : delvery_india,"delvery_foreign" : delvery_foreign})
    else:
        messages.add_message(request,messages.SUCCESS, 'Please do Order first and then go to checkout page!!!')          
        return HttpResponseRedirect('/')
    
    
@login_required
def placeOrder(request):

    # try:
    customer = User.objects.get(username=request.user)
    order = Order.objects.get(customer=customer,complete=False)    
    order_id = int(time.time()*1000.0)
    
    shipping_info = ShippingAddress.objects.get(customer=customer)
     
    if shipping_info.country.name == 'India':
        price_with_del = order.get_total_price + float(settings.INDIA_DELIVERY)
    else:
        price_with_del = order.get_total_price + float(settings.FOREIGN_DELIVERY)
        
    mode = settings.CASHFREE_MOD
    appId = settings.appId_cashfree
    return_link = request.build_absolute_uri(reverse('handle_payment', args=(order.id,)))
    
    postData = {
    "appId" : appId,
    "orderId" : str(order_id),
    "orderAmount" : str(price_with_del),
    "orderCurrency" : str(settings.CURRENCY),
    "orderNote" : "Pay Your Total Amount",
    "customerName" : str(request.user),
    "customerPhone" : str(shipping_info.phone_no),
    "customerEmail" : str(request.user.email),
    "returnUrl" : return_link,
    }
    
    sortedKeys = sorted(postData)
    signatureData = ""
    for key in sortedKeys:
        signatureData += key+postData[key]

    message = signatureData.encode('utf-8')
    
    secret_key = settings.secret_cashfree
    secret = secret_key.encode('utf-8')
    signature = base64.b64encode(hmac.new(secret, message,digestmod=hashlib.sha256).digest()).decode("utf-8")
    
    if mode == 'PROD': 
        url = "https://www.cashfree.com/checkout/post/submit"
    else: 
        url = "https://test.cashfree.com/billpay/checkout/post/submit"
        
        
    email_template1 = render_to_string('email_buyer.html',{"postData" : postData,"shipping_info":shipping_info})    
    mail_buyer = EmailMultiAlternatives(
                        "Your order detail", 
                        "Your order detail", 
                        settings.EMAIL_HOST_USER, 
                        [request.user.email], 
                    )
    mail_buyer.attach_alternative(email_template1, 'text/html')
    mail_buyer.send()

    return render(request,'cashfreeRequest.html',{'postData':postData,"signature":signature,"url":url})


def decQuantity(request,id,order,shipping_info,postData):
    
    orderitem1 = OrderItem.objects.filter(order = order)

    email_template3 = render_to_string('email_buyer3.html',{"postData" : postData,"shipping_info":shipping_info,"orderitem1":orderitem1,"user":order.customer.id})    
    mail_buyer3 = EmailMultiAlternatives(
                        "Order Completed", 
                        "Your order detail", 
                        settings.EMAIL_HOST_USER, 
                        [shipping_info.customer.email],
                    )
    mail_buyer3.attach_alternative(email_template3, 'text/html')
    mail_buyer3.send()
    
    for i in orderitem1:
        i.product.total_quantity -= i.quantity
        i.product.save()
        notification_Email = i.product.notification_email
        
        my_order = MyOrder.objects.create(
            username = order.customer.username,
            item = i.product.product_name,
            image = i.product.image,
            price = i.product.price,
            quantity = i.quantity,
            total = float(postData['orderAmount']),
            payment_status = postData['txStatus'],
            category = i.product.category.category_name,
            order_complete = i.order.complete,
            reference_id = postData['referenceId'],
            order_id = id,
            order_complete_id = i.order.order_complete_id,
            customer_detail = f'Address Info. : {shipping_info.house_no},{shipping_info.full_address},Nr.{shipping_info.nearest_landmark},city : {shipping_info.city},state : {shipping_info.state},zipcode : {shipping_info.zipcode},country : {shipping_info.country.name},\nMobile No. : {shipping_info.phone_no},\nEmail Address : {order.customer.email}'
        )
        
        email_template2 = render_to_string('email_admin.html',{'postData':postData,"product_name":i.product.product_name,"product_quantity":i.quantity,"product_price":i.product.price,"shipping_info":shipping_info,"user":order.customer.id})
        mail_admin = EmailMultiAlternatives(
                                "New order has been completed!!! Check order detail", 
                                "New order has been completed!!! Check order detail", 
                                settings.EMAIL_HOST_USER, 
                                ['kachhadiyapradip6@gmail.com',notification_Email], 
                                      )
        mail_admin.attach_alternative(email_template2, 'text/html')
        mail_admin.send()
        orderitem1.delete()

@csrf_exempt
def handlepayment(request,pk):
      
    if request.method == 'POST':
        form = request.POST
        postData = {
                "orderId" : form['orderId'], 
                "orderAmount" : form['orderAmount'], 
                "referenceId" : form['referenceId'], 
                "txStatus" : form['txStatus'], 
                "paymentMode" : form['paymentMode'], 
                "txMsg" : form['txMsg'], 
                "signature" : form['signature'], 
                "txTime" : form['txTime'],
                }        
        signatureData = postData['orderId'] + postData['orderAmount'] + postData['referenceId'] + postData['txStatus'] + postData['paymentMode'] + postData['txMsg'] + postData['txTime']

        message = signatureData.encode('utf-8')
        
        secret_key = settings.secret_cashfree
        
        secret = secret_key.encode('utf-8')
        computedsignature = base64.b64encode(hmac.new(secret,message,digestmod=hashlib.sha256).digest()).decode('utf-8')
       
        if postData['signature'] == computedsignature:
            if postData['txStatus'] == 'CANCELLED':
                return redirect(to = '/cart/') 
            order = Order.objects.filter(id = pk,complete=False).exists()

            if order:
                order = Order.objects.get(id = pk,complete=False)
                shipping_info = ShippingAddress.objects.get(customer = order.customer.id)
                
                if shipping_info.country.name == 'India':
                    total_price = float(postData['orderAmount']) - float(settings.INDIA_DELIVERY)
                else:
                    total_price = float(postData['orderAmount']) - float(settings.FOREIGN_DELIVERY)
                
                if total_price == float(order.get_total_price):
                    order.complete = True
                    order.reference_Id = postData['referenceId']
                    order.order_complete_id = postData['orderId']
                    order.payment_status = postData['txStatus']
                    order.save()
                    order = Order.objects.get(id=pk,complete=True)
                    decQuantity(request,pk,order,shipping_info,postData)
                else:
                    return render(request,'cancelPayment.html')
                    
            else:
                HttpResponse("No data")
        return render(request,"paymentStatus.html",{'postData':postData,"computedsignature":computedsignature,"user":pk})

    else:
        return HttpResponseRedirect(redirect_to='/cart/')
        
@login_required
def updateItem(request,pk,event):
    customer = request.user
    product = Product.objects.get(pk=pk)
    order,created = Order.objects.get_or_create(customer=customer,complete=False)
    orderitem,created = OrderItem.objects.get_or_create(order=order,product=product)
    
    if event == 'add':
        
        product_quantity = product.total_quantity
       
        orderitem.quantity = (orderitem.quantity + 1)
                
        if orderitem.quantity <= product_quantity: 
            orderitem.save()
            messages.add_message(request,messages.SUCCESS, f'{product} has been successfully added.... (Total items: { order.get_total_item}) (Sub total: ${ order.get_total_price})')
        else: 
            messages.add_message(request,messages.SUCCESS, f'{product} no more quantity available.....(only {product_quantity} items are remains..)')

        
    if event == 'minus':
        orderitem.quantity = (orderitem.quantity - 1)
        orderitem.save()
        messages.add_message(request,messages.SUCCESS,f'{product} removed.... (Total items: { order.get_total_item}) (Sub total: ${ order.get_total_price})')

    if orderitem.quantity <= 0:
        orderitem.delete()
           
    return redirect(request.META['HTTP_REFERER'])


@login_required
def buyNow(request,pk,event):
    updateItem(request,pk,event)
    return HttpResponseRedirect(redirect_to = '/checkout/')
    

@login_required
def removeItem(request,pk):
    customer = request.user
    product = Product.objects.get(pk=pk)
    order,created = Order.objects.get_or_create(customer=customer,complete=False)
    orderitem,created = OrderItem.objects.get_or_create(order=order,product=product)
    orderitem.delete()
    return redirect(request.META['HTTP_REFERER'])

def myorder(request):
    
    if request.user.is_authenticated:
        order = MyOrder.objects.filter(username = request.user,order_complete = True).order_by('-id')
        if not order:
            return render(request,'myorder.html',{"orderitem":0})
        else:
            return render(request,'myorder.html',{"orderitem":order})
    else:
        return render(request,'myorder.html',{"orderitem":0})
    
from .pdf import Render
from django.utils import timezone

def order_to_pdf(request,pk):
    obj = MyOrder.objects.get(id = pk)
    today = timezone.now()
    params = {
        'today' : today,
        'obj' : obj
    }
    return Render.render('order_pdf.html', params)

def product_view(request,pk,slug):
    
    product = Product.objects.get(pk = pk)
    if request.user.is_authenticated:
        lk = LikeProduct.objects.filter(product=product,liked_by=request.user)        
    else:
        lk = False
    if product.total_quantity == 0:
        messages.error(request,"Apologize!!This item is currently out of stock..Please(press ❤) add this item in your wish list..")
    might_like = Product.objects.filter(category = product.category).exclude(pk=pk).order_by("?")
    
    return render(request,"product_detailview.html",{"product":product,"product_like":might_like,"lk":lk})

def autocompleteModel(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = Product.objects.filter(Q(product_name__icontains=q) | Q(price__icontains=q) | Q(Product_description__icontains = q) | Q(category__category_name__icontains = q))
        results = []
        for r in search_qs:
            results.append(r.category.category_name)
            results.append(r.product_name)
        data = json.dumps(list(set(results)))
    else:
        data = json.dumps('No Result found!!')
    mimetype = 'application/json'
    return HttpResponse(data,mimetype)

def search(request):
    
    if request.method == 'POST':
        data = request.POST
        q = data['txtSearch']
        search_qs = Product.objects.filter(Q(product_name__icontains=q) | Q(price__icontains=q) | Q(Product_description__icontains = q) | Q(category__category_name__icontains = q))
        if not search_qs:
            messages.error(request,"Oops!! No results found try another keywords...")
            return redirect(request.META['HTTP_REFERER'])
        return render(request,'search.html',{"search_qs" : search_qs})
    else:
        return render(request,'search.html',{"search_qs" : "no"})

@login_required
def myProfile(request,pk):
    profile_data = Profile.objects.get(pk = pk)
    return render(request,'myprofile.html',{"profile_data":profile_data})

@method_decorator(login_required,name="dispatch")     
class Changeusername(SuccessMessageMixin,UpdateView):
    model = User
    fields = ['username']
    template_name = 'change_username.html'
    success_message = "Your username successfully updated!!"
    
    
    def get_success_url(self):
        profile_id=self.request.user.profile.id
        return reverse_lazy('my_profile', kwargs={'pk': profile_id})
    
@method_decorator(login_required,name="dispatch") 
class ProfileUpdateview(SuccessMessageMixin,UpdateView):
    model = Profile
    template_name = 'profile_form.html'
    fields = ["full_name","gender","age","phone_no","profile_pic"]
    success_message = "Your profile successfully updated!!!!"
    
    def get_form(self):
        form = super().get_form()
        form.fields["full_name"].widget = forms.TextInput(attrs={'class':'text-success form-control my-3','placeholder':"Name and Surname"})
        form.fields["gender"].widget = forms.RadioSelect(attrs={'class':'ml-4 mr-1 my-3'},choices=[('Male','Male'),('Female','Female')])
        form.fields["age"].widget = forms.NumberInput(attrs={'class':'text-info form-control my-3','placeholder':"Enter Your Age.."})
        form.fields["profile_pic"].widget = forms.FileInput(attrs={'class':'btn-dark btn btn-sm my-3','id':'profile_pic_hash'})
        form.fields["phone_no"].widget = forms.NumberInput(attrs={'class':'text-info form-control my-3','placeholder':"Enter Mobile No.."})
        return form

    def get_success_url(self):
        user_id=self.kwargs['pk']
        return reverse_lazy('my_profile', kwargs={'pk': user_id})

@login_required
@require_POST
def like(request,pk):
    if request.method == 'POST':
        product = Product.objects.get(pk=pk)
        new_like, created = LikeProduct.objects.get_or_create(product=product, liked_by=request.user)
        message = "Like"
        
        if not created:
            LikeProduct.objects.filter(product = product,liked_by = request.user).delete()
            message = "Dislike"
            
    ctx = {'message': message}
    return HttpResponse(json.dumps(ctx), content_type='application/json')

def myWishlist(request,event):
    
    if request.user.is_authenticated:
        like_list = LikeProduct.objects.filter(liked_by = request.user).exists()
        if like_list:
            like_list = LikeProduct.objects.filter(liked_by = request.user)
        else:
            like_list = 0
            
        if event == 'remove':
            LikeProduct.objects.filter(liked_by = request.user).delete()
            like_list = 0
    else:
        like_list = 0
        
    return render(request,'mywish_list.html',{"like_list":like_list})

class BugreportView(SuccessMessageMixin,FormView):
    model = Bugreport
    form_class = Bug_report
    template_name = 'bugreport.html'
    success_message = "Your response was successfully submitted!!!!"
    success_url = '/'
    
    def get_form(self):
        form = super().get_form()
        form.fields["name"].widget = forms.TextInput(attrs={'class':'my-1 form-control','placeholder':"Your Full Name"})
        form.fields["email"].widget = forms.EmailInput(attrs={'class':'my-1 form-control','placeholder':"Email Address"})
        form.fields["bug_detail"].widget = forms.Textarea(attrs={'rows':5, 'cols':40,'class':'my-1 form-control','placeholder':"Describe the complete bug...."})
        return form
    
    def form_valid(self, form):
        name = form.cleaned_data["name"]
        email = form.cleaned_data["email"]
        bug_detail = form.cleaned_data["bug_detail"]
        Bugreport.objects.create(name=name,email=email,bug_detail=bug_detail)
        return super(BugreportView, self).form_valid(form)

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible

class Contactus(SuccessMessageMixin,CreateView):
    model = Contact
    fields = ["f_type","email369","mobile_no","name","feedback","captcha"]
    success_message = "Your response successfully submitted!!!!"
    context_object_name = "ct"
    template_name = 'contact_form.html'

    def get_form(self):
        form = super().get_form()
        form.fields["email369"].widget = forms.EmailInput(attrs={'class':'my-1 form-control','placeholder':"Email Address"})
        form.fields["mobile_no"].widget = forms.NumberInput(attrs={'class':'my-1 form-control','placeholder':"Mobile Number"})
        form.fields["name"].widget = forms.TextInput(attrs={'class':'my-1 form-control','placeholder':"Your Name"})
        form.fields["f_type"].widget = forms.RadioSelect(attrs={'class':'list-unstyled px-2'},choices=[('Feedback','Feedback'),("Help","Get Help"),("Contact us","Contact us")])
        form.fields["feedback"].widget = forms.Textarea(attrs={'rows':4, 'cols':40,'class':'my-1 form-control','placeholder':"Enter your Feedback or Help or Contact topic here....."})
        form.fields["captcha"] = ReCaptchaField(widget=ReCaptchaV2Invisible)
        return form    
    def get_success_url(self):
        return reverse_lazy('contact_us')

@login_required
def chage_order_status(request):
    if request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST':
            ref_id = request.POST.get('ref_id')
            status = request.POST.get('status')
            my_order = MyOrder.objects.filter(reference_id = ref_id)
            if not my_order.exists():
                messages.add_message(request,messages.SUCCESS, f'No any order found for given this "{ref_id}" reference Id....')                  
            for ot in my_order:
                ot.order_status = status
                ot.save(update_fields=['order_status'])
                messages.add_message(request,messages.SUCCESS, f'[{ot.username}---{ot.item}---status({status})] updated successfuly...')  
            return redirect(request.META['HTTP_REFERER'])
        else:
            return render(request,'chage_order_status.html')
    else:
        return redirect(to = '/')