from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.views import View
import django_tables2 as tables
from django_tables2 import SingleTableView

from .models import Transaction, Account
from .forms import LoginForm
from .tables import TransactionsTable
from datetime import datetime
from django.contrib.auth import authenticate, login, logout

class LoginView(View):
    template_name = 'login/index.html'
    form_class = LoginForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            print(f'Logging in as {username}')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                print("We logged in!")

                # Create the account object if we do not have
                Account.objects.get_or_create(
                    user_id=user.id,
                    username=username
                )
                
                return HttpResponseRedirect('/')
            else:
                print("Access denied!")

        return render(request, self.template_name, locals())

    def get(self, request):
        form = LoginForm()
        
        if request.user.is_authenticated:
            print('User is already logged in, redirecting to /')
            return HttpResponseRedirect('/')

        return render(request, self.template_name, locals())

class LogoutView(View):
    template_name = 'logout/index.html'

    def get(self, request):
        if request.user.is_authenticated:
            print('We have a user to logut')
            logout(request)
            return HttpResponseRedirect('/login/')
        else:
            print('No user is logged in, redirect to /login')
            return HttpResponseRedirect('/login/')
        
        return render(request, self.template_name, locals())

class HomeView(View):
    template_name = 'home/index.html'

    def get(self, request):
        nbar = 'home'
        return render(request, self.template_name, locals())

class TransactionsView(SingleTableView):
    model = Transaction
    table_class = TransactionsTable
    template_name = 'transactions/index.html'

    def get(self, request):
        if not request.user.is_authenticated:
            print('Someone is not logged in!')
            print('No user is logged in, redirect to /login')
            return HttpResponseRedirect('/login/')
        
        nbar = 'transactions'

        # Create the account object if we do not have
        account = Account.objects.get(
            user_id=request.user.id
        )
        
        user_transactions = Transaction.objects.filter(user_id=account.user_id)
        transaction_table = TransactionsTable(user_transactions)

        return render(request, self.template_name, locals())

class PortfolioView(View):
    template_name = 'portfolio/index.html'

    def get(self, request):

        nbar = 'Portfolio'
        # Data variables
        portfolio_data = Transaction.objects.filter(ticker='BTC')
        
        # Template variables
        portfolio = portfolio_data

        return render(request, self.template_name, locals())