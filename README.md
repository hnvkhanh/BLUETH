# BLUETH: A web application that helps you learn new words via flashcards
#### Video Demo:  https://youtu.be/zVeybSKQGvk
#### Description:
**BLUETH** is a web application that helps everyone learn vocabulary by using the same idea as flashcard. It provides a website where users can create and practice with virtual flashcards. The flashcards are ordered by users' fluency, when users practice with their flashcards, flashcards with words that users more fluent will appear last.
The front-end of this project uses HTML, CSS, and Bootstrap 4.5. The back-end is written in Python (using framework Flask).
This project contains following files: application.py, style.css, add.html, index.html, layout.html, login.html, register.html, setting.html, language.csv, project.db.
1. application.py:
    - This is the back-end of **BLUETH**, written in Python. It is responsible to input new data from users to database, send specific data to users, process information received from users and send responses.
    - application.py contains these following main functions that responsible for most of web's work: `index`, `login`, `logout`, `register`, `add`, `setting`.
        - `index` is the first function to be called when users visit **BLUETH**, it will redirect users to route /login if users have not logged in. When users have logged in, `index` will take data from database, which is users' flashcard(s), and send them to index.html. Besides that, `index` also keep track of users' fluency when they practice, but users have to reload the page for newly updated fluency in next time they practice.
        - `login` take usernames and passwords provided by users then look at database to make sure if that information is valid. If valid, login will redirect users to homepage.
        - `logout` redirect users to /login and log out users' account.
        - `register` input new users’ information to database.
        - `add` is function that adds new flashcards to users' list of flashcards. Flashcard’s details are inputted by users via a form.
        - `setting` will either delete users' card, users' account, change username or password when it receives signal from setting.html.
    - I have also reused a function, written by CS50 staffs, from Problem Set 9:
    ```
    def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
    ```
2. style.css: The aesthetic of **BLUETH** is decided by this file.
3. index.html: This is **BLUETH**'s homepage, where users can see their flashcards and practice with them.
4. login.html: This file displays the *Login* page, users send their username(s) and passwords via this page.
5. register.html: Where users register for new account if they have not had one.
6. setting.html: Users can delete their list of cards, their account, or change their username (or password) here.
7. layout.html: Help display repeated contains throughout other pages.
8. language.csv: Contain languages' name and their ISO-639-1 Code. This file is used in add.html for the sake of searching via [Google Translate](https://translate.google.com/). I decided to use Google Translate URL as a tool to search for words' meaning when I notice it has the same spirit as searching by https://www.google.com/, you can pass something to URL and let Google Translate does the other works. In this case, that is ISO-639-1 Code. I have copied the list of ISO-639-1 Code from [this](https://cloud.google.com/translate/docs/languages) to Excel then saved it as a csv file (after having removed some unnecessary parts).
9. project.db: Have two tables, `users` and `cards`.
    - `users`: Contain users' information such as their username, password, id, ...
    - `cards`: Contain cards' information, which is entered by users themself, such as what the word is, type of the word, it's meaning, ...
#### How to Use:
You need to log in with your account first, if you do not have any you have to register for one. After logged in you will see **BLUETH** homepage, where all your added cards displayed. If you are new user, then there are not any cards yet, instead you will see a plus button, click that button to add new words.
    
At the homepage you can practice with your flashcard(s), click the yellow play button to start practicing. A modal with (new) word (series of modals) will pop up, there are three options correspond with how fluent you are with that word, your choice will affect the order of words next time you practice (words that you are more fluent will appear later in the queue). If you want to practice again right after you finished, you should reload the page for newly updated order. The length of modal series is the number of words you have added. You can quit half-way by click on x button. Click trash bin button on the card to delete it.
    
To add new words to your account, click the button at the top-left choose *Add new card*. Two forms will appear, use the first form to add new word (*note* and *example* part is optional), if you just know the word but have no idea about its meaning then use the second one to search for it. You can also use the second form to find out how to say something in other language.
    
To make some changes on your account, click the button at the top-left, choose *Setting*. 
    
If you want to return to homepage, click **BLUETH** logo.
You can log out your account at any page of the web just by clicking *log out* at the top-right.
### Thanks a lot for reading!

