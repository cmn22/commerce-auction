from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment

from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "auctions/index.html",{
        "listings": Listing.objects.filter(active=True).all()
    })


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


@login_required
def create_listing(request):
    if request.method == "POST":
        listing = Listing()
        listing.owner = User.objects.get(username = request.user.get_username())
        listing.title = request.POST["title"]
        listing.description = request.POST["description"]
        listing.base_price = request.POST["base_price"]
        listing.current_price = listing.base_price
        listing.image = request.POST["img_url"]
        listing.category = request.POST["category"]
        listing.active = True
        listing.save()

    return render(request, "auctions/create.html")


def listing(request, listing_id):
    print(listing_id)
    listing = Listing.objects.get(pk=listing_id)
    try:
        highest_bid = Bid.objects.filter(item=listing).order_by('-bid')[0]
    except IndexError:
        highest_bid = None
    print("HEY THERE", highest_bid)
    return render(request, "auctions/listing.html",{
        "listing": listing,
        "min_bid": listing.current_price+1,
        "highest_bid": highest_bid
    })


@login_required
def bid(request):
    if request.method == "POST":
        listing = Listing.objects.get(title=request.POST["item"])
        listing.current_price = request.POST["bid"]
        listing.save()
        bid = Bid()
        bid.bid = request.POST["bid"]
        bid.item = Listing.objects.get(title = request.POST["item"])
        bid.bidder = User.objects.get(username = request.POST["bidder"])
        bid.save()
        url = "listing/" + str(listing.id)
        return HttpResponseRedirect(url)

    return render(request, "auctions/error.html",{
        "message": "You cannot access this URL using a GET request."
    })
