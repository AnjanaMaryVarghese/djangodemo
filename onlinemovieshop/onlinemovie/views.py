from django.shortcuts import render,redirect

# Create your views here.
from onlinemovie.models import Movie
def home(request): #Home view
    k = Movie.objects.all()  # select * from Movie reads all records from table Movie
    context = {'movie': k}  # passes data from views to html file. Context is dictionary type.
    return render(request, 'home.html', context)

def addmovies(request): #Add movies view
    if (request.method == "POST"):  # After submitting the form
        ti = request.POST['ti']
        d = request.POST['d']
        la = request.POST['la']
        yr = request.POST['yr']
        im = request.FILES['im']
        m = Movie.objects.create(title=ti, description=d, language=la, year=yr, image=im)  # creates a new record
        m.save()  # saves the record inside the table movie
        return redirect('home')
    return render(request,'add.html')

def detail(request,p):  #detail page
    m=Movie.objects.get(id=p)
    context={'movie':m}
    return render(request,'details.html',context)
def delete(request,p):
    m=Movie.objects.get(id=p)
    m.delete()
    return redirect('home')
def update(request,p):  #detail page
    # return render(request,'edit.html')
    m=Movie.objects.get(id=p)
    if (request.method == "POST"):  # After submitting the form
        m.title = request.POST['ti']
        m.description = request.POST['d']
        m.language = request.POST['la']
        m.year = request.POST['yr']
        if(request.FILES.get('im')==None):
            m.save()
        else:
            m.image=request.FILES.get('im')
        m.save()
        return redirect('home')
    context = {'movie': m}
    return render(request, 'edit.html', context)
