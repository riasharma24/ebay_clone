from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *

from .models import User


def index(request):
    listings=Listing.objects.filter(activity=True)
    return render(request, "auctions/index.html",{
        'listings':listings,
        
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



def addListing(request):
    if request.method=='GET':
     return render(request,'auctions/addListing.html',{
         'category_list': Category.objects.all()
     })
    if request.method=='POST':
        name_of_listing=request.POST['Listing_name']
        desc_of_listing=request.POST['Listing_desc']
        img_url=request.POST['Listing_url']
        ini_price=request.POST['Listing_ini_bid']
        ini_bid=Bid(buyer=request.user,bid_price=ini_price)
        ini_bid.save()
        category_of_listing=request.POST['Listing_category']
        category_obj=Category.objects.get(name=category_of_listing)
        add_user=request.user
        l1=Listing(
            title=name_of_listing,
            description=desc_of_listing,
            imageUrl=img_url,
            initial_bid=ini_bid,
            activity=True,
            seller=add_user,
            category=category_obj
        )
        l1.save()
        return HttpResponseRedirect(reverse('index'))
        

def show_categories(request):
    categories=Category.objects.all()
    return render(request, 'auctions/categories.html',{
        'categories':categories
    })

def show_watchlist(request):
    reqUser=request.user
    listings=reqUser.listing_watchlist.all()
    return render(request, 'auctions/watchlist.html',{
        'listings':listings
    })

def displayCategoryListings(request,category):
    categoryObj=Category.objects.get(name=category)
    listings=Listing.objects.filter(activity=True,category=categoryObj)
    return render(request, "auctions/categoryListings.html",{
        'categories':listings
    })

def getDetails(request,listing_id):
    if request.method=='GET':
        listing=Listing.objects.get(id=listing_id)
        isAuthor=request.user.username==listing.seller.username
        isAdded=request.user in listing.watchlist.all()
        comments=Comments.objects.filter(forListing=listing)
        return render(request, "auctions/listing.html",{
            'listing':listing,
            'isAdded':isAdded,
            'dedicatedComments':comments,
            'isAuthor':isAuthor,
            'winner':request.user == listing.initial_bid.buyer
        })
    

def addToWatchlist(request,list_id):
    listingObj=Listing.objects.get(id=list_id)
    reqUser=request.user
    listingObj.watchlist.add(reqUser)
    return HttpResponseRedirect(reverse(getDetails, args=(list_id, )))

def removeFromWatchlist(request,list_id):
    listingObj=Listing.objects.get(id=list_id)
    reqUser=request.user
    listingObj.watchlist.remove(reqUser)
    return HttpResponseRedirect(reverse(getDetails, args=(list_id, )))



def commentOnListing(request,list_id):
    if request.method=='POST':
      reqUser=request.user
      listingObj=Listing.objects.get(id=list_id)
      text=request.POST['addedComment']

      new_comment=Comments(username=reqUser,text=text,forListing=listingObj)
      new_comment.save()

      return HttpResponseRedirect(reverse(getDetails, args=(list_id, )))
    
def bidOnListing(request,list_id):
    newBid=request.POST['addedBid']
    listingObj=Listing.objects.get(id=list_id)
    isAuthor=request.user.username==listingObj.seller.username
    if int(newBid)>listingObj.initial_bid.bid_price:
        currentBid=Bid(buyer=request.user,bid_price=int(newBid))
        currentBid.save()
        listingObj.initial_bid=currentBid
        listingObj.save()
        return render(request,'auctions/listing.html',{
            'listing':listingObj,
            'message':"Bid placed successfully!",
            'isAdded':listingObj.activity,
            'dedicatedComments':Comments.objects.filter(forListing=listingObj),
            'isAuthor':isAuthor
        })
    else:
        return render(request,'auctions/listing.html',{
            'listing':listingObj,
            'message':"Sorry! Could not place the bid.",
            'isAdded':listingObj.activity,
            'dedicatedComments':Comments.objects.filter(forListing=listingObj),
            'isAuthor':isAuthor

        })
    

def declareWinner(request, list_id):
    listingObj=Listing.objects.get(id=list_id)
    listingObj.activity=False
    listingObj.save()
    isAuthor=request.user.username==listingObj.seller.username
    return render(request,'auctions/listing.html',{
            'listing':listingObj,
            'message':"Auction closed!",
            'isAdded':listingObj.activity,
            'dedicatedComments':Comments.objects.filter(forListing=listingObj),
            'isAuthor':isAuthor
        })