# E-Commerce Auction Management

![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=darkgreen) ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green) ![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) ![CSS](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white) ![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white) ![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)


<br/>  
<br/>  


## Table Of Contents
- [Introduction](#introduction)
- [Setup](#setup)
- [About the Application](#about-the-application)
  - [Models](#models)
  - [Home Page](#home-page)
  - [Registration Page](#registration-page)
  - [Login Page](#login)
  - [Logout](#logout)
  - [Create Listing](#create-listing)
  - [Listing Page](#listing-page)
  - [Bids](#bids)
  - [Comments](#comments)
  - [Watchlist Page](#watchlist)
  - [My Listing Page](#my-listing-page)
  - [Closed Listing Page](#closed-listing-page)
  - [Closed Listing](#closed-listing)
  - [Category](#category)
  - [About Us Page](#about-us-page)
- [Author](#author)



<br/>  
<br/>  


<div name="introduction">

## Introduction
Creating an E-Commerce Auction web application where users can publish listings, add listings to their watchlist, bid on a listing and even comment on them.


<br/>  
<br/>  


<div name="setup">

## Setup

### Cloning the Repository
You can clone this repository by either downloading a zip file or by using the following command.
```
git clone https://github.com/cmn22/mail
```

<br/>

### Creating a virtual environment 

#### For Unix/macOS
1. Installing virtualenv
    ```
    pip3 install virtualenv
    ```
2. Creating a virtual environment
    ```
    virtualenv env
    ```
3. Activating the virtual environment
    ```
    source env/bin/activate
    ```
<br>    

#### For Windows
1. Installing virtualenv
    ```
    pip3 install virtualenv
    ```
2. Creating a virtual environment
    ```
    virtualenv env
    ```
3. Activating the virtual environment
    ```
    .\env\Scripts\activate
    ```

<br/>
<br/>

### Installing required dependencies
NOTE: Use Python3.9 to mitigate package version issues.

Install the required packages as stated in requirements.txt file
```
pip3 install -r requirements.txt
```

<br/>
<br/>

### Running the application
1. Make Migrations 
    ```
    python3 manage.py makemigrations
    ```
2. Migrate
    ```
    python3 manage.py migrate
    ```
3. Collect Static
    ```
    python3 manage.py collectstatic
    ```
4. Runserver (on port 8000)
    ```
    python3 manage.py runserver 0.0.0.0:8000
    ```
5. Open the corresponding address on a web browser and your application should be up and running.


<br/>
<br/>


<div name="about">

## About the Application

<div name="models">

### Models (Database Structure)

The web application uses 5 models as follows:  
1. **User:** This is a predefined Django model who's username, email-id and password field we will be using in this web application.  

2. **Listing**: This model will store information regarding a listing. The fields are title, description, base price, current price, image(to save image URL of listing), category(type of listing), owner(Foreign Key to User), active(status of the listing), date.  

3. **Bid:** This model is used to register bids made by users. It contains information such as bidder(who is bidding - Foreign Key to User), bid(bid amount) and item(on which bid is being made - Foreign Key to Listing)  

4. **Comment:** This model stores all the comments made by various users on the listings. It stores listing(on which comment is made - Foreign Key to Listing), commentor(who made the comment - Foreign Key to User), comment, date(of comment).  

5. **Watchlist:** This models helps in keep tracking of the watchlist listings for users. It does so by storing the wisher(who is watching the listing) and the item(the listing that is being watched).  

<img src="auctions/static/auctions/images/ss_models.png" width=100%> 
<br/>
<br/>

<br/>


<div name="home-page">

### Home Page: (/)
The **Home Page** has a two sticky navigation bars which help in navigating throughout the web application. This main page displays all the active listings as cards. On hovering over a particular listing, the listing card becomes more pronounced.

<img src="auctions/static/auctions/images/ss_home.png" width=100%> 
<br/>
<br/>  


<br/>  


<div name="registration-page">

### Registration Page: (/register)
The **Register Page** helps a new user to create a new account so that he can avail all the features of the website such as commenting, bidding and adding listings to a watchlist.

<img src="auctions/static/auctions/images/ss_register.png" width=100%> 
<br/>
<br/>  


<br/>  


<div name="login-page">

### Login Page: (/login)
The **Login Page** helps the user to login in so that he can avail login specific features such as commenting on listings, bidding on listings and adding listings to watchlists. If the user does not have a account, he can create one using the register option. 

<img src="auctions/static/auctions/images/ss_login.png" width=100%>  
<br/>
<br/>  


<br/>  


<div name="logout">

### Logout: (/logout)
The **Logout** option is only available to a logged in user. A user can logout by clicking on the user icon on the top right of any page and then clicking on the _"LOGOUT"_ option.

<img src="auctions/static/auctions/images/ss_login.png" width=100%>  
<br/>
<br/>  


<br/> 


<div name="create-listing">

### Create Listing: (/create)
The **Create Listing** option is only available to a logged in user. A user can create a new listing by click on the _"Create Listing"_ in the secondary navigation bar.  

The create listing page prompts the user to enter details such as title, description, starting price, image URL(optional) and category of the new listing. On clicking on _"Post Item"_, the listing gets saved in the database and the user is redirected to the newly created listing page.

<img src="auctions/static/auctions/images/ss_create.png" width=100%>  
<br/>
<br/>  


<br/> 


<div name="listing-page">

### Listing Page: (/listing/\<listing_id\>)
The **Listing Page** can be reached on clicking a particular listing. The listing page shows detailed information of a particular listing. Information such as the current highest bidder, comments on the listing etc are present on this page.

#### **NO USER**
If no logged in user is present, then the following page is displayed wherein there is prompt to login so that the user can interact with the item:

<img src="auctions/static/auctions/images/ss_listing_nouser.png" width=100%>  
<br/>
<br/>  


<br/> 

#### **LOGGED USER**
If a user is logged in, the user can interact with the listing in various ways. The user can add the listing to his watchlist so that he can quickly access the listing for later reference. The user can make bids on the listings which is the main purpose of this web application, provided that the user isn't the owner of the listing. If a user is the owner of a listing, he/she is provided with the option of closing the auction. Also a logged in users can make comments on a listing.  

<img src="auctions/static/auctions/images/ss_listing_logged.png" width=100%>
<br/>
<br/>  


<br/> 


<div name="bids">

### Bids:
**Bidding** is the primary use case of this web application. All bids are saved in the database using the _"Bid"_ models that we have created.  
The first bid on any listing can be equal to or greater than the _"Base Price"_ of the listing. For any further bids, the bid amount must be greater than the _"Current Price"_ i.e the preivious bid.
 
<br/>
<br/>  


<br/>


<div name="comments">

### Comments:
**Comments** about of listing is visible on the _"Listing Page"_ of a listing below the information.

#### **NO USER**
If no logged in user is present, then the user cannot make any comment on the listing though he can still see the comments made by other user. It looks as follows:

<img src="auctions/static/auctions/images/ss_comment_nouser.png" width=100%>  
<br/>
<br/>  


<br/> 

#### **LOGGED USER**
If a user is logged in, the user can make comments along with being able to view other comments. It looks as follows:

<img src="auctions/static/auctions/images/ss_comment_logged.png" width=100%>
<br/>
<br/>  


<br/> 


<div name="watchlist">

### Watchlist Page: (/watchlist)
The **Watchlist Page** is only available to users who are logged into their account. It can be accessed by clicking on the user icon and then clicking on _"My Watchlist"_. A page with all the watched listings is presented as in Active Listings Page.  

To add or remove a listing from the watchlist, the user can click on **Star** present besides the title of the listing on the listing page. If the page shows a _"Yellow Star"_, then the listing is already in the watchlist of the user. On clicking on this _"Yellow Star"_, the star turns into a transparent _"Black Bordered Star"_ which represents that the listing is not in the watchlist.
 
<br/>
<br/>  


<br/>


<div name="my-listing-page">

### My Listing Page: (/mylistings)
The **My Listing Page** is only available to users who are logged into their account. It can be accessed by clicking on the user icon and then clicking on _"My Listings"_. A page with all the listings that have been posted by the user is presented just like in the Active Listings Page.  
 
<br/>
<br/>  


<br/>


<div name="closed-listing-page">

### Closed Listing Page: (/closedlistings)
The **Closed Listings Page** displays all those listings who have been closed i.e listings which are _"Inactive"_.
 
<br/>
<br/>  


<br/>


<div name="closed-listing">

### Closed Listing: (/listing/\<listing_id\>)
The **Listing Page** of a closed listing is displayed differently depending if the user is the owner, winner or some other user.

<br/>  
<br/>  

#### **OWNER**
<img src="auctions/static/auctions/images/ss_closed_owner.png" width=100%> 
<br/>  
<br/>   

#### **WINNER**
<img src="auctions/static/auctions/images/ss_closed_winner.png" width=100%>  
<br/>  
<br/>  

#### **OTHER USERS**
<img src="auctions/static/auctions/images/ss_closed_user.png" width=100%>
<br/>
<br/> 


<br/>  
  

<div name="category">

### Category: (/category/\<category_name\>)
The **Category Page** displays all possible listings present for a particular category. Listings of particular category can be accessed by clicking on the _"CATEGORIES"_ option in the secondary navigation bar and then clicking on a particular _"\<category_name\>"_ option to get results for a particular category. All listings are categorized into Fashion, Furniture, Electronics, Collectibles, Games & Toys, Motor Vehicle, Property or as None.  

<img src="auctions/static/auctions/images/ss_categories.png" width=100%>  
<br/>
<br/>  


<br/> 


<div name="about-us-page">

### About Us Page: (/about)
The **About Us Page** displays basic information about the web application as well as the developer.  

In short, this website is about a online auction bidding site, wherein users can publish listings of the items they want to sell.

For demonstration and usage of this website, kindly watch this [YouTube](LINK) video.

<img src="auctions/static/auctions/images/ss_about.png" width=100%>   
<br/>
<br/>  


<br/> 


<div name="author">

## Author 

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](
https://www.linkedin.com/in/chaitanya-malani/) 
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/cmn22) [![FaceBook](https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white)](https://www.facebook.com/itsme.cmn22) [![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/ChaitanyaMalani) [![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/itsme.cmn22/)

This project has been made by Chaitanya Malani 

Demonstration of this project can be viewed on [YouTube](https://youtu.be/FUzSQ6Zw2vo)

I am an aspiring software engineer who is currently studying Computer Science in Mumbai, India. I love to code and explore various fields within computers. Also I am a very big football enthusiast and I love supporting Manchester United F.C.
