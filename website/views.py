from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm, AddOrderForm
from .models import Record, Order

def home(request):
    records = Record.objects.all()
    
    # Check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.success(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': records})


def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out...")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            
            messages.success(request, "You Have Successfully Registered! Welcome!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        # Look Up Records
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully...")
        return redirect('home')
    else:
        messages.success(request, "You Must Be Logged In To Do That...")
        return redirect('home')


def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added...")
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Has Been Updated!")
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')



def add_order(request):
    form = AddOrderForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                order = form.save(commit=False)
                order.record = form.cleaned_data['record']
                order.save()
                messages.success(request, "Order Added...")
                return redirect('home')
        return render(request, 'add_order.html', {'form': form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')



def update_order(request, order_id):
    if request.user.is_authenticated:
        current_order = Order.objects.get(id=order_id)
        form = AddOrderForm(request.POST or None, instance=current_order)
        if form.is_valid():
            form.save()
            messages.success(request, "Order Has Been Updated!")
            return redirect('customer_record', pk=current_order.record.id)
        return render(request, 'update_order.html', {'form': form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


def delete_order(request, order_id):
    if request.user.is_authenticated:
        delete_order = Order.objects.get(id=order_id)
        record_id = delete_order.record.id
        delete_order.delete()
        messages.success(request, "Order Deleted Successfully...")
        return redirect('customer_record', pk=record_id)
    else:
        messages.success(request, "You Must Be Logged In To Do That...")
        return redirect('home')
    
def all_orders(request):
    if request.user.is_authenticated:
        all_orders_list = Order.objects.all()
        return render(request, 'all_orders.html', {'all_orders_list': all_orders_list})
    else:
        messages.success(request, "You Must Be Logged In To View All Orders...")
        return redirect('home')
    
def all_records(request):
    if request.user.is_authenticated:
        records = Record.objects.all()
        return render(request, 'all_records.html', {'records': records})
    else:
        messages.success(request, "You Must Be Logged In To View All Records...")
        return redirect('home')        
	
   		 	

