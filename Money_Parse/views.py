from django.shortcuts import render
def home(request):
     return render(request,'about.html',{})
def about(request):
     return render(request, 'about.html',{}) #brackets at the end allow us to pass in stuff during render
# Create your views here.
