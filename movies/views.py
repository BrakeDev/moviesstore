from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Movie, Review, Report

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html',
                  {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)

    report_count = {}

    # superuser sees all reviews, regular only sees filtered
    if request.user and request.user.is_superuser:
        # get all the reviews 
        reviews = Review.objects.filter(movie=movie)
    else:
        reviews = Review.objects.filter(movie=movie, report__isnull=True)
    

    # template data and rendering
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    template_data['report_count'] = report_count
    return render(request, 'movies/show.html',
                  {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html',
            {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

@login_required
def report_review(request, id, review_id):

    # create report from info
    report = Report()
    report.user = request.user
    report.movie = get_object_or_404(Movie, id=id)
    report.review = get_object_or_404(Review, id=review_id)

    # check if user already reported this review
    if Report.objects.filter(review=report.review):
        return redirect('movies.show', id=id)

    # save report if the user hasn't already filed it
    report.save()

    return redirect('movies.show', id=id)

@login_required
def clear_reports(request, id, review_id):
    
    # can't clear reports if not superuser
    if not request.user.is_superuser:
        return redirect('movies.show', id=id)
    
    review = get_object_or_404(Review, id=review_id)

    Report.objects.filter(review=review).delete()

    return redirect('movies.show', id=id)