from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Watchlist, Bid, Comments

@login_required(login_url="/login")
def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings" : listings
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
            watchlist = Watchlist(user=user)
            watchlist.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def search(request):
    pass

@login_required(login_url="/login")
def list(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        category = request.POST["category"]
        image = request.POST["image"]
        
        listing = Listing(user = request.user,title=title, description=description, price=price, category=category,image=image)
        listing.save()
        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/list.html")

@login_required(login_url="/login")
def details(request, listing_id):
    return render(request, "auctions/details.html", {
        "listing" : Listing.objects.get(pk=listing_id),
        "bids_count" : Listing.objects.get(pk=listing_id).item_bids.count(),
        "watchlist" : Watchlist.objects.get(user=request.user).listings.all(),
        "listing_user" : Listing.objects.get(pk=listing_id).user,
        "winner" : Bid.objects.filter(item=Listing.objects.get(pk=listing_id)).order_by("-value").first(),
        "comments" : Listing.objects.get(pk=listing_id).item_comments.all()
    })

@login_required(login_url="/login")
def watchlist(request):
    if request.method == "POST":
        add_listing_id = request.POST.get('watchlist_add', None)
        remove_listing_id = request.POST.get('watchlist_remove', None)
        if add_listing_id:
            listing = Listing.objects.get(pk=add_listing_id)
            watchlist = Watchlist.objects.filter(user=request.user).first()
            if not watchlist:
                watchlist = Watchlist(user=request.user)
                watchlist.save()
            watchlist.listings.add(listing)
        if remove_listing_id:
            listing = Listing.objects.get(pk=remove_listing_id)
            watchlist = Watchlist.objects.filter(user=request.user).first()
            if not watchlist:
                watchlist = Watchlist(user=request.user)
                watchlist.save()
            watchlist.listings.remove(listing)

        return render(request, "auctions/watchlist.html", {
            "listings" : watchlist.listings.all()
        })
    watchlist = Watchlist.objects.filter(user=request.user).first()
    if not watchlist:
        watchlist = Watchlist(user=request.user)
        watchlist.save()
    return render(request, "auctions/watchlist.html", {
        "listings" : watchlist.listings.all()
    })

@login_required(login_url="/login")
def place_bid(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        bid = request.POST["bid"]
        listing_price = Listing.objects.get(pk=listing_id).price
        highest_bid = Bid.objects.filter(item=Listing.objects.get(pk=listing_id)).order_by("-value").first()
        if highest_bid:
            highest_bid = Bid.objects.filter(item=Listing.objects.get(pk=listing_id)).order_by("-value").first().value

        else:
            highest_bid = 0
        if (int(bid) < int(listing_price)) or (int(bid) < int(highest_bid)):
            return HttpResponse(f"Error bid must be higher than {highest_bid}")
        else:
            user_bid = Bid(user=request.user, item=Listing.objects.get(pk=listing_id), value=bid)
            user_bid.save()
            return HttpResponseRedirect(reverse("details", args=[listing_id]))
        
    else:
        return HttpResponseRedirect(reverse("index"))
    
@login_required(login_url="/login")
def close_bid(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        listing = Listing.objects.get(pk=listing_id)
        listing.active = False
        listing.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))
    
@login_required(login_url="/login")
def comment(request):
    if request.method == "POST":
        user_comment = request.POST["comment"]
        listing_id = request.POST["listing_id"]
        
        comment = Comments(user=request.user, item=Listing.objects.get(pk=listing_id), comment=user_comment)
        comment.save()

        return HttpResponseRedirect(reverse("details", args=[listing_id]))
    
    return HttpResponseRedirect(reverse("details", args=[listing_id]))

@login_required(login_url="/login")
def category(request):
    return render(request, "auctions/category.html", {
        "categories" : Listing.objects.values_list("category", flat=True).distinct()
    })

@login_required(login_url="/login")
def category_list(request, category):
    return render(request, "auctions/category_list.html", {
        "category" : category,
        "listings" : Listing.objects.filter(category=category)
    })

