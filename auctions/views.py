from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Watchlist

from django.contrib.auth.decorators import login_required


def index(request):
    print("WATCHLIST ITEMS:", Listing.objects.filter(active=True).all())
    print(Listing.objects.filter(active=True).all())
    return render(request, "auctions/index.html",{
        "listings": Listing.objects.filter(active=True).all(),
        "page_heading": "ACTIVE LISTINGS"
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
    listing = Listing.objects.get(pk=listing_id)
    try:
        highest_bid = Bid.objects.filter(item=listing).order_by('-bid')[0]
    except IndexError:
        highest_bid = None

    watchlist = False
    try:
        user = User.objects.get(username = request.user.get_username())
        print(user)
        #print("USERNAME",user)
        try:
            watchlist_obj = Watchlist.objects.filter(wisher=user, item=listing)
            if watchlist_obj.count() != 0:
                watchlist = True
        except:
            pass

    except:
        pass

    print("Watchlist = ",watchlist)
        #print("No user")

    return render(request, "auctions/listing.html",{
        "listing": listing,
        "min_bid": listing.current_price+1,
        "highest_bid": highest_bid,
        "watchlist": watchlist
    })


@login_required
def watchlist(request):
    if request.method == "POST":
        wisher = User.objects.get(username = request.POST["user"])
        item = Listing.objects.get(title = request.POST["watch_item"])
        exe = request.POST["watchlist_exe"]

        if exe == "add":
            watch = Watchlist()
            watch.wisher = wisher
            watch.item = item
            watch.save()

        if exe == "remove":
            watch = Watchlist.objects.filter(wisher=wisher, item=item).delete()

        url = "listing/" + str(item.id)
        return HttpResponseRedirect(url)

    watchlist = Watchlist.objects.filter(wisher=User.objects.get(username = request.user.get_username())).values('item')
    watchlist_items = Listing.objects.filter(pk__in=watchlist).all()
    print("WATCHLIST ITEMS:", watchlist_items)
    return render(request, "auctions/index.html",{
        "listings": watchlist_items,
        "page_heading": "WATCHLIST LISTINGS",
        "watchlist_items_count": watchlist_items.count()
    })

@login_required
def bid(request):
    if request.method == "POST":
        listing = Listing.objects.get(title = request.POST["item"])
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
