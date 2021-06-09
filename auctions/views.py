from typing import List
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import Http404
from django.shortcuts import render
from django.urls import reverse
from django.utils.html import urlize

from .models import Bid, Comment, Listing, User
from .forms import *
from .utils import *

from django.contrib.auth.decorators import login_required


def index(request):
    auctions = get_auctions(Listing.objects.all())

    return render(request, "auctions/index.html", {
        "auctions": auctions
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
def create_view(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            # Attempt to create new listing
            try:
                newListing = form.save(commit=False)
                newListing.seller = request.user
                #newListing.current_bid = Bid.objects.create(amount=newListing.starting_bid, bidder=request.user)
                newListing.save()
                return HttpResponseRedirect(reverse("listing", args=[newListing.id])) # Change this later to redirect to Listing Page
            except:
                return render(request, "auctions/create.html", {
                    "message": "An unexpected error has occurred.",
                    "form": form
                })
        else:
            return render(request, "auctions/create.html", {
                "message": "The data entered is not valid.",
                "form": form
            })
    else:
        return render(request, "auctions/create.html", {
            "form": ListingForm(),
        })

def listing(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        current_bid = get_current_bid(listing.auctions.filter(listing=listing_id))
        bidForm = BidForm(request.POST)
        if bidForm.is_valid():
            #Attempt to place bid
            try:
                new_bid = bidForm.cleaned_data["amount"]
                if new_bid >= listing.starting_bid and (len(Bid.objects.filter(listing=listing)) == 0 or new_bid > current_bid.amount):
                    newBid = bidForm.save(commit=False)
                    newBid.bidder = request.user
                    newBid.listing = listing
                    newBid.save()
                    listing.save()
                    return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "current_bid": get_current_bid(listing.auctions.filter(listing=listing_id)),
                        "comments": listing.users_comments.all(),
                        "num_bids": len(Bid.objects.filter(listing=listing)),
                        "bidForm": BidForm(),
                        "success_message": "Success! Your bid is the current bid."
                    })
                else:
                    return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "current_bid": current_bid,
                        "comments": listing.users_comments.all(),
                        "num_bids": len(Bid.objects.filter(listing=listing)),
                        "bidForm": BidForm(),
                        "failure_message": "Failure! Your bid is very small"
                    })
            except:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "current_bid": get_current_bid(Bid.objects.filter(listing=listing)),
                    "comments": listing.users_comments.all(),
                    "num_bids": len(Bid.objects.filter(listing=listing)),
                    "bidForm": BidForm(),
                    "error_message": "An unexpected error has occurred.",
                })
        else:
            listing.status = False
            listing.winner = current_bid.bidder
            listing.save()
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "current_bid": get_current_bid(Bid.objects.filter(listing=listing)),
                "comments": listing.users_comments.all(),
                "num_bids": len(Bid.objects.filter(listing=listing)),
                "bidForm": bidForm,
                "error_message": "The data entered is not correct",
            })
    else:
        try:
            listing = Listing.objects.get(id=listing_id)
        except Listing.DoesNotExist:
            raise Http404("Listing not found.")
        return render (request, "auctions/listing.html", {
            "listing": listing,
            "current_bid": get_current_bid(Bid.objects.filter(listing=listing)),
            "comments": listing.users_comments.all(),
            "num_bids": len(Bid.objects.filter(listing=listing)),
            "bidForm": BidForm(),
        })