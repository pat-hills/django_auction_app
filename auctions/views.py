from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import date, datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Max

from .models import User
from .models import Auction,Bidding,Comments,Watchlist


def index(request):
    return render(request, "auctions/index.html", {
       # "bids": Bidding.objects.all()
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            request.session["user_id"] = user.id
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
       #contact = request.POST["contact"]

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
        request.session["user_id"] = user.id   
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def createaution(request):
    
   
    if request.method == "POST":
      
        user_id = request.session["user_id"]
        user = User.objects.get(id=user_id)
        item_name = request.POST["item_name"]
        item_title = request.POST["item_title"]
        item_bid_price = request.POST["item_bid_price"]
        item_description = request.POST["item_description"]
        item_category = request.POST["item_category"]
        item_image_url = request.FILES["item_image_url"]

        #Auction.user = User()
        #Auction.item_name = item_name
        #Auction.item_bid_price = item_bid_price
        #Auction.item_title = item_title
        #Auction.item_description = item_description
        #Auction.item_category = item_category
        #Auction.save()

       # a = Auction.user

        auction = Auction.objects.create(item_name=item_name,item_title=item_title,item_bid_price=item_bid_price,
        item_description=item_description,item_category=item_category,item_image_url = item_image_url,user=user
        )
        auction.save()
       

    return render(request, "auctions/auction.html", {
  })


def auctionlisting(request):
    return render(request, "auctions/auctionListing.html",{
          "auctions": Auction.objects.filter(is_deleted=False , is_sold=False)
 })
        
@login_required(login_url="login")
def viewauction(request, auction_id):
    user_id = request.session["user_id"]
    users = User.objects.get(id=user_id)
    userCreatedby = users.username
    auction = Auction.objects.get(id=auction_id)
    listedby = auction.user.username
    count_bidding = Bidding.objects.filter(is_deleted=False, auctionbid=auction.id).count()
    all_bids = Bidding.objects.filter(is_deleted=False, auctionbid=auction.id)
    new_bid = Bidding.objects.latest('date_created')
    current_bidder = new_bid.auctionbid.user
    allComments = Comments.objects.filter(is_deleted=False , auctionbc=auction.id)
    userWatchlistRecords = Watchlist.objects.filter(is_deleted=False , userw=users)
    countUsersWatchList = Watchlist.objects.filter(is_deleted=False,userw=users).count()
    request.session['countUsersWatchList'] = countUsersWatchList
    #countList = userWatchlistLatestCheck.userw.username


    
   
    

    return render(request, "auctions/singleAuction.html", {
        "auction": auction,
        "listedby": listedby,
        "count_bidding": count_bidding,
        "current_bidder": current_bidder,
        "allComments": allComments,
        "userWatchlistRecords": userWatchlistRecords,
        "countUsersWatchList": countUsersWatchList,
        "userCreatedby": userCreatedby,
        "all_bids": all_bids,

    })

@login_required(login_url="login")
def bid(request, auction_id):

    errorcode = 1

    
    if request.method == "POST":

        user_id = request.session["user_id"]
        users = User.objects.get(id=user_id)
        #bid_amount = request.POST["bid_amount"]
        bid_amount = float(request.POST.get("bid_amount"))
        auctionbid = Auction.objects.get(pk=auction_id)
        bid_amount_old =  auctionbid.item_bid_price 

        if bid_amount <= float(bid_amount_old):
            return render(request, "auctions/errorprice.html", {
            "message": "Bidding amount should be greater than current bid price!!!!."
        })



        auctionbid.item_bid_price = bid_amount
        
        
        bid = Bidding.objects.create(bid_amount=bid_amount,auctionbid=auctionbid,userb=users)
        
        bid.save()
        auctionbid.save()
        

    return HttpResponseRedirect(reverse("viewauction", args=(auctionbid.id,)))



@login_required(login_url="login")
def addcomment(request, auction_id):

    
    if request.method == "POST":

        user_id = request.session["user_id"]
        users = User.objects.get(id=user_id)
        title = request.POST["title"]
        message = request.POST["message"]
        auctionbid = Auction.objects.get(pk=auction_id)
        
        comm = Comments.objects.create(title=title,comments=message,auctionbc=auctionbid,userc=users)
        
        comm.save()
        

    return HttpResponseRedirect(reverse("viewauction", args=(auctionbid.id,)))        

 
@login_required(login_url="login")
def watchlist(request, auction_id):

    
    if request.method == "POST":

        user_id = request.session["user_id"]
        users = User.objects.get(id=user_id)
        auctionbid = Auction.objects.get(pk=auction_id)
        
        comm = Watchlist.objects.create(auctionbw=auctionbid,userw=users)
        
        comm.save()
        

    return HttpResponseRedirect(reverse("viewauction", args=(auctionbid.id,))) 



@login_required(login_url="login")
def viewuserswatchlist(request):


    user_id = request.session["user_id"]
    users = User.objects.get(id=user_id)
    userWatchlistRecords = Watchlist.objects.filter(is_deleted=False , userw=users)
    countUsersWatchList = Watchlist.objects.filter(is_deleted=False,userw=users).count()
        
    return render(request, "auctions/watchlisting.html", {
        "userWatchlistRecords": userWatchlistRecords,
        "countUsersWatchList": countUsersWatchList,

    })


@login_required(login_url="login")
def singlewatchlistview(request,watchlist_id):
    user_id = request.session["user_id"]
    users = User.objects.get(id=user_id)
    #auction = Auction.objects.get(id=auction_id)
    usersinglewatchlist = Watchlist.objects.get(id=watchlist_id,is_deleted=False)
    viewAuctionForUser = usersinglewatchlist

    return render(request, "auctions/viewwatchlist.html", {
        "usersinglewatchlist": viewAuctionForUser,

    }) 




@login_required(login_url="login")
def removewatchlistitem(request, watchlist_id):

    
    if request.method == "POST":
        itemOnWatchlist = Watchlist.objects.get(pk=watchlist_id)
        
        itemOnWatchlist.is_deleted = True
        
        itemOnWatchlist.save()
        

    return HttpResponseRedirect(reverse("viewuserswatchlist")) 




def categories(request):

    auctions = Auction.objects.get(is_deleted=False , is_sold=False)
    auctions = auctions.item_category.distinct()

    #category_list = Auction.objects.values_list('item_category', flat=True).distinct()
     
    return render(request, "auctions/layout.html",{
    "auctions": auctions
 })



def listcategory(request,category):

    #category_item = request.get["category"]
    #category_item = request.POST.get('category')

    return render(request, "auctions/listcategory.html",{
          "listcategories": Auction.objects.filter(item_category=category,is_deleted=False),
          "category" : category
 })


@login_required(login_url="login")
def closedbid(request, auction_id):

    
    if request.method == "POST":
        closedAuction = Auction.objects.get(pk=auction_id)
        
        closedAuction.is_sold = True
        
        closedAuction.save()
        

    return HttpResponseRedirect(reverse("auctionlisting"))



def closedbidlisting(request):

    closedbids = Auction.objects.filter(is_sold=True)
     

    return render(request, "auctions/closedbidlisting.html",{
          "closedbids": closedbids
 })


@login_required(login_url="login")
def viewwinner(request,auction_id,fbid_amount):


    user_id = request.session["user_id"]
    authdetails = User.objects.get(id=user_id)
    authUser = authdetails.username
    auction = Auction.objects.get(id=auction_id)
    listedby = auction.user.username
    #obj= Model.objects.filter(testfield=12).latest('testfield')
    #Student.objects.filter(subject='Math').aggregate(Max('marks'))
    #Entry.objects.latest('pub_date', '-expire_date')
    #highestBid = Bidding.objects.filter(is_deleted=False, userb=authdetails, auctionbid = auction.id).aggregate(bid_amount=Max('bid_amount'))['bid_amount']
    #highestBid = Bidding.objects.filter(is_deleted=False, userb=authdetails, auctionbid = auction.id,bid_amount=fbid_amount)

    allComments = Comments.objects.filter(is_deleted=False , auctionbc=auction.id)
    all_bids = Bidding.objects.filter(is_deleted=False, auctionbid=auction.id)

    try:
        winnerDetails = Bidding.objects.get(bid_amount=fbid_amount,auctionbid = auction.id,userb=authdetails)
    except Bidding.DoesNotExist:
        winnerDetails = None
    
     

     

    #res = Image.objects.filter().aggregate(max_id=Max('pk'))
    #res.get('max_id')
    #latestBidWinner = Bidding.objects.latest('bid_amount','date_created').filter(userb=authUser)
    
     

    return render(request, "auctions/winner.html",{
          "auction": auction,
          "allComments": allComments,
          "all_bids": all_bids,
          "listedby": listedby,
          "authUser": authUser,
          "winnerDetails": winnerDetails,
          "fbid_amount": fbid_amount,
 }) 


    
      
 

      

 