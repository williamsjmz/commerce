from .models import Bid, Comment, Listing, User

def get_current_bid(list):
    if len(list) > 0:
        return list[len(list) - 1]


def get_auctions(listings):
    listing_and_current_bid = []
    auctions = []
    for listing in listings:
        listing_and_current_bid.append(listing)
        listing_and_current_bid.append(get_current_bid(Bid.objects.filter(listing=listing)))
        auctions.append(listing_and_current_bid)
        listing_and_current_bid = []
    print(auctions)
    return auctions

