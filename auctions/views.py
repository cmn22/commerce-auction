from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Watchlist

from django.contrib.auth.decorators import login_required

#Home/Index Page
def index(request):

    # Display Active Listings
    print(f"ACTIVE LISTING PAGE")
    print(f"ACTIVE LISTINGS: {Listing.objects.filter(active=True).all()}")

    return render(request, "auctions/index.html",{
        "listings": Listing.objects.filter(active=True).all(),
        "page_heading": "ACTIVE LISTINGS"
    })


#Login
def login_view(request):

    # On getting a "POST" request
    if request.method == "POST":

        # Attempt to sign user in
        print(f"ATTEMPTING TO LOGIN...")

        # Retriving the user input from the form
        username = request.POST["username"]
        password = request.POST["password"]

        # To check if authentication is successful
        user = authenticate(request, username=username, password=password)

        print(f"AUTHETICATING USER...")

        # To detect why user wasn't authenticated
        if user is not None:
            # If user exists
            login(request, user)
            print(f"\'{user}\' LOGGED IN SUCCESSFULLY")

            return HttpResponseRedirect(reverse("index"))

        else:
            # If authentication error occurs
            print(f"LOGIN UNSUCCESSFULL")

            print(f"REDIRECTING TO LOGIN PAGE...")
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })

    # On getting a "GET" request
    else:
        print(f"LOGIN PAGE")

        return render(request, "auctions/login.html")


#Logout
def logout_view(request):
    print(f"LOGGING OUT \'{request.user.get_username()}\'")

    logout(request)

    print("REDIRECTING TO INDEX PAGE...")

    return HttpResponseRedirect(reverse("index"))


#Register
def register(request):

    # On getting a "POST" request
    if request.method == "POST":

        # Retriving user information from the form
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        print(f"VALIDATING ENTERED FORM...")

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            print(f"PASSWORD CONFIRMATION FAILED")

            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempting to create new user
        try:
            print(f"CREATING A NEW USER...")

            user = User.objects.create_user(username, email, password)
            user.save()

            print(f"NEW USER \'{user}\' CREATED")

        except IntegrityError:
            print(f"COULD NOT CREATE NEW USER")
            print(f"REDIRECTING TO REGISTRATION PAGE...")

            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })

        # New User Created
        login(request, user)

        print(f"REDIRECTING TO INDEX PAGE...")
        return HttpResponseRedirect(reverse("index"))

    # On getting a "GET" request
    else:
        return render(request, "auctions/register.html")


#Create New Listing
@login_required
def create_listing(request):

    # On getting a "POST" request
    if request.method == "POST":

        print(f"CREATING NEW LISTING")

        listing = Listing()
        listing.owner = User.objects.get(username = request.user.get_username())
        listing.title = request.POST["title"]
        listing.description = request.POST["description"]
        listing.base_price = request.POST["base_price"]
        listing.current_price = listing.base_price
        if not request.POST["img_url"]:
            listing.image = "/static/auctions/images/no_image.png"
        else:
            listing.image = request.POST["img_url"]
        listing.category = request.POST["category"]
        listing.active = True
        listing.save()

        print(f"NEW LISTING \'{listing}\' CREATED")

        print(f"REDIRECTING TO NEWLY CREATED LISTING PAGE...")
        url = "listing/" + str(listing.id)
        return HttpResponseRedirect(url)

    # On getting a "GET" request
    else:
        return render(request, "auctions/create.html")


#Listing Page
def listing(request, listing_id):

    listing = Listing.objects.get(pk=listing_id)

    print(f"LISTING PAGE OF \'{listing.title}\'")

    # To find highest bid if any
    try:
        highest_bid = Bid.objects.filter(item=listing).order_by('-bid')[0]
    except IndexError:
        highest_bid = None

    # To check if listing is in user's (if logged in) watchlist
    watchlist = False
    try:
        # To check if a user is logged in
        user = User.objects.get(username = request.user.get_username())

        # If user is logged in, then try
        try:
            watchlist_obj = Watchlist.objects.filter(wisher=user, item=listing)

            # To check if listing present in Watchlist
            if watchlist_obj.count() != 0:
                watchlist = True

        except:
            pass

    # If user is not logged in
    except:
        pass

    # To retrive comments for the listing
    comments = Comment.objects.filter(item=listing).all()

    return render(request, "auctions/listing.html",{
        "listing": listing,
        "min_bid": listing.current_price+1,
        "highest_bid": highest_bid,
        "watchlist": watchlist,
        "comments": comments
    })


#Watchlist
@login_required
def watchlist(request):

    # On getting a "POST" request
    if request.method == "POST":

        wisher = User.objects.get(username = request.POST["user"])
        item = Listing.objects.get(title = request.POST["watch_item"])
        exe = request.POST["watchlist_exe"]

        # Adding listing to Watchlist
        if exe == "add":
            watch = Watchlist()
            watch.wisher = wisher
            watch.item = item
            watch.save()

            print(f"\'{item.title}\' ADDED TO WATCHLIST OF \'{wisher.username}\'")

        # Removing listing from Watchlist
        if exe == "remove":
            watch = Watchlist.objects.filter(wisher=wisher, item=item).delete()

            print(f"\'{item.title}\' REMOVED FROM WATCHLIST OF \'{wisher.username}\'")

        print(f"REDIRECTING TO LISTING PAGE...")

        url = "listing/" + str(item.id)
        return HttpResponseRedirect(url)

    # On getting a "GET" request
    else:
        # To display the watchlist items for a user
        watchlist = Watchlist.objects.filter(wisher=User.objects.get(username = request.user.get_username())).values('item')
        watchlist_items = Listing.objects.filter(pk__in=watchlist).all()

        print(f"WATCHLIST PAGE FOR {request.user.get_username()}")
        print(f"WATCHLIST LISTINGS: {watchlist_items}")

        return render(request, "auctions/index.html",{
            "listings": watchlist_items,
            "page_heading": "WATCHLIST LISTINGS",
            "watchlist_items_count": watchlist_items.count()
        })


#My Listings Page
@login_required
def mylistings(request):

    mylistings = Listing.objects.filter(owner=User.objects.get(username = request.user.get_username())).all()

    print(f"MY LISTINGS PAGE FOR {request.user.get_username()}")
    print(f"MY LISTINGS: {mylistings}")

    return render(request, "auctions/index.html",{
        "listings": mylistings,
        "page_heading": "MY LISTINGS"
    })


#Bidding
@login_required
def bid(request):

    # On getting a "POST" request
    if request.method == "POST":

        print(f"PROCESSING THE BID...")

        listing = Listing.objects.get(title = request.POST["item"])

        # Updating current price of listing
        listing.current_price = request.POST["bid"]
        listing.save()
        print(f"CUREENT PRICE OF \'{listing.title}\' UPDATED TO \'{listing.current_price}\' ")

        # Registring the bid
        bid = Bid()
        bid.bid = request.POST["bid"]
        bid.item = Listing.objects.get(title = request.POST["item"])
        bid.bidder = User.objects.get(username = request.POST["bidder"])
        bid.save()
        print(f"BID OF Rs.{bid.bid} ON \'{bid.item.title}\' BY \'{bid.bidder.username}\' HAS BEEN REGISTERED")

        # Redirecting to listing page
        print(f"REDIRECTING TO LISTING PAGE...")
        url = "listing/" + str(listing.id)
        return HttpResponseRedirect(url)

    # On getting a "GET" request
    else:
        print(f"GET REQUEST FOR BID DENIED")
        return render(request, "auctions/error.html",{
            "message": "You cannot access this URL using a GET request."
        })


#Close Listing
@login_required
def close(request):

    # On getting a "POST" request
    if request.method == "POST":

        listing = Listing.objects.get(title = request.POST["item"])

        # Update the status of the listing
        listing.active = False
        listing.save()

        print(f"AUCTION FOR \'{listing.title}\' HAS BEEN CLOSED")

        print(f"REDIRECTING TO LISTING PAGE...")
        url = "listing/" + str(listing.id)
        return HttpResponseRedirect(url)

    # On getting a "GET" request
    else:
        print(f"GET REQUEST FOR CLOSING AUCTION DENIED")
        return render(request, "auctions/error.html",{
            "message": "You cannot access this URL using a GET request."
        })


#Category Listing Page
def category(request, category_name):
    print(f"CATEGORY LISTING PAGE FOR \'{category_name}\'")

    category_items = Listing.objects.filter(category__iexact=category_name).all()

    print(f"LISTINGS FOR \'{category_name}\': {category_items}")

    return render(request, "auctions/index.html",{
        "listings": category_items,
        "page_heading": category_name,
        "type": "CATEGORY_LISTING",
        "category_listing_count": category_items.count()
    })


#Closed/In-Active Listings
def closed(request):
    print(f"CLOSED LISTING PAGE")

    closed_listings = Listing.objects.filter(active=False).all()

    print(f"CLOSED LISTINGS: {closed_listings}")

    return render(request, "auctions/index.html",{
        "listings": closed_listings,
        "page_heading": "CLOSED LISTINGS"
    })


#Comments
@login_required
def comment(request):

    # On getting a "POST" request
    if request.method == "POST":

        print(f"PROCESSING NEW COMMENT...")

        listing = Listing.objects.get(title = request.POST["item"])
        commentor = User.objects.get(username = request.POST["commentor"])

        # Registring a new comment
        new_comment = Comment()
        new_comment.item = listing
        new_comment.commentor = commentor
        new_comment.comment = request.POST["comment"]
        new_comment.save()
        print(f"\'{new_comment.commentor.username}\'s\' COMMENT ON \'{new_comment.item.title}\' HAS BEEN SAVED SUCCESSFULLY")

        print(f"REDIRECTING TO LISTING PAGE...")
        url = "listing/" + str(listing.id)
        return HttpResponseRedirect(url)

    # On getting a "GET" request
    else:
        print(f"GET REQUEST FOR COMMENT DENIED")
        return render(request, "auctions/error.html",{
            "message": "You cannot access this URL using a GET request."
        })


#About Page
def about(request):
    print(f"ABOUT PAGE")
    return render(request, "auctions/about.html")
