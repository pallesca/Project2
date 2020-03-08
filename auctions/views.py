from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse


#get = get form
#post = sending data
#put = create
#add new models
from .models import User, Listing, Comment
#import form
from .forms import ListingForm, CommentForm

#active listings
def index(request):
    listings = Listing.objects.all()
    if request.user.is_authenticated:
        return render(request, "auctions/index.html", {"listings": listings})
    else:
        return render(request, "auctions/index.html", {"listings": listings})

#listings
def listing(request, title):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    listing = Listing.objects.filter(title=title)
    if len(listing) > 0:
        listing = list(listing)[0]
    context={
        'listing': listing
    }
    print(context)
    return render(request, "auctions/listing.html", context)

#create listing
def create_listing(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    form = ListingForm(request.POST or None)
    form.owner = request.user
    if form.is_valid():
        form.save()
        form = ListingForm()

    context = {
        'form': form
    }
    return render(request, "auctions/create_listing.html", context)

# *************************************************************************
# view watchlist
@login_required
def watchlist(request, user_id):
    user_watchlist = User.objects.get(pk=int(user_id)).watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": user_watchlist,
        "title": "Watchlist"
    })

# *************************************************************************
#add to watchlist
@login_required
def add_watchlist(request):
    if request.method == "POST":
        listing = get_object_or_404(Listing, pk=int(request.POST["listing_id"]))
        request.user.watchlist.add(listing)
        return HttpResponseRedirect(reverse("listing", args = (listing.id,)))

    #first try
    # if request.method == "POST":
    #     listing = get_object_or_404(Listing, pk=int(request.POST["listing_id"]))
    #     request.user.watchlist.add(listing)
    #     return HttpResponseRedirect(reverse("listing", args = (listing.id,)))
    #     return HttpResponseRedirect(reverse("watchlist", args = [listing]))
    #     return render(request, "auctions/watchlist.html")
    # else: 
    #     return render(request, "auctions/index.html", {"listings": listings})
    #     listing = Listing.objects.get(pk=listing)
    #     return HttpResponseRedirect(reverse("watchlist", args=(user_id)))


# *************************************************************************
@login_required
def delete_watchlist(request): 
    if request.method == "POST":
        listing = get_object_or_404(Listing, pk=int(request.POST["listing_id"]))
        # Listing.objects.get(pk=request.POST["listing_id"])
        request.user.watchlist.remove(listing)
        return HttpResponseRedirect(reverse("listing", args = (listing.id,)))
# *************************************************************************
#filter category
@login_required
def category_detail(request, slug):
    template = 'auctions/category_detail.html'

    category = get_object_or_404(Category, slug=slug)
    listing = Post.objects.filter(category=category)

    context = {
        'category': category,
        'listing' : listing
    }
    return render(request, template, context)


# *************************************************************************
#Comment
@login_required
def add_comment(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    form = CommentForm(request.Post or None)
    form.owner = request.user
    if form.is_valid():
        form.save()
        form = CommentForm()
    context = {
        'form': form
    }
    return render(request, "auctions/index.html", context)

# *************************************************************************

# def bid(request, listing_id):
#     amount = 
#     listing = 
# if seller = owner then error
# if amount is less than starting bid then error 

# create variable to store bid amount


# *************************************************************************
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
