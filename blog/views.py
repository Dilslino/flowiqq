from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Category, Comment
from django.db.models import Q
from .forms import CommentForm, ContactForm, NewsletterForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

# Create your views here.

def home(request):
    featured_posts = Post.objects.filter(status='published', is_featured=True).order_by('-created_on')[:6]
    latest_posts = Post.objects.filter(status='published').order_by('-created_on')[:6]
    
    featured_posts_count = Post.objects.filter(status='published', is_featured=True).count()
    latest_posts_count = Post.objects.filter(status='published').count()
    
    newsletter_form = NewsletterForm()
    
    context = {
        'featured_posts': featured_posts,
        'latest_posts': latest_posts,
        'featured_posts_count': featured_posts_count,
        'latest_posts_count': latest_posts_count,
        'newsletter_form': newsletter_form,
    }
    return render(request, 'blog/home.html', context)

def post_list(request):
    featured = request.GET.get('featured')
    if featured:
        posts = Post.objects.filter(status='published', is_featured=True).order_by('-created_on')
    else:
        posts = Post.objects.filter(status='published').order_by('-created_on')
    
    paginator = Paginator(posts, 6)  # Menampilkan 6 postingan per halaman
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(request, 'blog/post_list.html', {'posts': posts, 'featured': featured})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.active = True
            new_comment.save()
            print(f"Komentar baru disimpan: {new_comment}")  # Tambahkan ini
            return redirect('post_detail', slug=post.slug)
        else:
            print(f"Form tidak valid: {comment_form.errors}")  # Tambahkan ini
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    })

def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published').order_by('-created_on')
    
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(request, 'blog/category_posts.html', {'category': category, 'posts': posts})

def search_posts(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct().order_by('-created_on')
    else:
        posts = Post.objects.none()
    
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(request, 'blog/search_results.html', {'posts': posts, 'query': query})

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Proses form (misalnya, kirim email)
            messages.success(request, 'Pesan Anda telah terkirim. Terima kasih!')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'blog/contact.html', {'form': form})

def newsletter_signup(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Anda berhasil berlangganan newsletter kami!')
        else:
            messages.error(request, 'Email sudah terdaftar atau tidak valid.')
    return redirect('home')
