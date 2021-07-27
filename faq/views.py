from django.contrib.auth.decorators import login_required,permission_required,user_passes_test
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .models import ImageUpload, Komen, Pertanyaan
from .forms import KomenForm, PertanyaanForm,NewUserForm,DocumentForm
from django.db.models import Q
from django.conf import settings
from django.core.files.storage import FileSystemStorage
@user_passes_test(lambda u: u.is_authenticated, login_url='faq:login')
def create_post(request):
    new_form = None
    if request.method == 'POST':
        form = PertanyaanForm(data=request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            return redirect("faq:index")
    else:
        form = PertanyaanForm()
    return render(request, 'faq/create.html', {'form_pertanyaan':form })    

@user_passes_test(lambda u: u.is_authenticated, login_url='faq:login')
def model_form_upload(request):
    new_form = None
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            return redirect('faq:profile')
    else:
        form = DocumentForm()
    images = ImageUpload.objects.order_by('-pub_date')
    return render(request, 'faq/model_form_upload.html', {
        'form': form,
        'images':images,
    })

@user_passes_test(lambda u: u.is_authenticated, login_url='faq:login')
def search_profile(request,profile_id):
    
    obj = get_object_or_404(User, pk=profile_id)
    new_form = None
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            return redirect('faq:search-profile', profile_id)
    else:
        form = DocumentForm()

    images = ImageUpload.objects.filter(user=profile_id).order_by('-pub_date')

    return render(request, "faq/model_form_upload.html", {'obj':obj, 'images':images, 'form':form})


@user_passes_test(lambda u: u.is_authenticated, login_url='faq:login')
def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'simple_upload.html')

@user_passes_test(lambda u: u.is_authenticated, login_url='faq:login')
def serach_user(request):
    search_post = request.GET.get('search')
    
    if search_post:
        #data = User.objects.filter(Q(username__icontains=search_post))
        data = User.objects.filter(Q(username=search_post))
    else:
        data = None
    return render(request, 'faq/check.html', {'data':data})

@user_passes_test(lambda u: u.is_authenticated, login_url='faq:login')
def delete(request, pertanyaan_id):
    context = {}
    obj = get_object_or_404(Pertanyaan, pk=pertanyaan_id)
    if request.method == "POST":
        obj.delete()
        return redirect("faq:index")
    return render(request, "faq/index.html", context)

@user_passes_test(lambda u: u.is_authenticated, login_url='faq:login')
def index(request):
    search_post = request.GET.get('search')
    if search_post:
        pertanyaan = Pertanyaan.objects.filter(Q(pertanyaan_text__icontains=search_post))
    else:
        pertanyaan = Pertanyaan.objects.order_by('-pub_date')
    new_form = None
    if request.method == 'POST':
        form = PertanyaanForm(data=request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            return redirect("faq:index")
    else:
        form = PertanyaanForm()
    images = ImageUpload.objects.order_by('-pub_date')
    return render(request, 'faq/index.html', {
        'form_pertanyaan':form,
        'pertanyaans': pertanyaan,
        'images':images,
    })

@user_passes_test(lambda u: u.is_authenticated, login_url='faq:login')
def detail(request, pertanyaan_id):
    pertanyaan_list=get_object_or_404(Pertanyaan, pk=pertanyaan_id)
    komenan=Komen.objects.filter(pertanyaan=pertanyaan_list.pk)
    komen_form=None
    if request.method == 'POST':
        form=KomenForm(request.POST)
        if form.is_valid():
            komen_form=form.save(commit=False)
            komen_form.pertanyaan = pertanyaan_list
            komen_form.user = request.user
            komen_form.save()
            return redirect("faq:detail", pertanyaan_id)
    else:
        form=KomenForm()
    images = ImageUpload.objects.order_by('-pub_date')
    return render(request, 'faq/detail.html', {'pertanyaan': pertanyaan_list, 'form': form, 'komenan': komenan,'images':images })

@user_passes_test(lambda u: u.is_authenticated, login_url='faq:login')
def results(request, pertanyaan_id):
    pertanyaan=get_object_or_404(Pertanyaan, pk=pertanyaan_id)
    return render(request, 'faq/results.html', {'pertanyaan': pertanyaan})

@user_passes_test(lambda u: u.is_authenticated, login_url='faq:login')
def vote(request, pertanyaan_id):
    pertanyaan=get_object_or_404(Pertanyaan, pk=pertanyaan_id)
    pertanyaan.votes += 1
    pertanyaan.save()
    return redirect("faq:index")

@user_passes_test(lambda u: u.is_authenticated, login_url='faq:login')
def vote_komen(request, pertanyaan_id, komen_id):
    komen=get_object_or_404(Komen, pk=pertanyaan_id)
    komen.votes += 1
    komen.save()
    return redirect("faq:detail", komen_id)

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("faq:index")

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("faq:index")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})

@user_passes_test(lambda u: u.is_authenticated, login_url='faq:login')
def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("faq:index")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request, "register.html",context={"register_form":form})

'''
    search_post = request.GET.get('search')
    
    if search_post:
        pertanyaan = Pertanyaan.objects.filter(Q(pertanyaan_text__icontains=search_post))
    else:
        pertanyaan = Pertanyaan.objects.order_by('-pub_date')
    
'''