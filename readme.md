#Goodshare, the Goodreads and Bookshare desktop client, in early alpha
##About Goodshare

Goodshare is intended to act as a goodreads client, much like the website, but with the more native desktop app "feel", as well as integration with bookshare and a few tools that are made possible by the entegration of the 2.

##So where is goodshare at currently, as far as development?

In very... Verry early alpha.
So far, I've got authorization with the [python goodreads API wrapper](https://github.com/sefakilic/goodreads),using OAuth done, secure storage of app and user spesific keys and tokens is handled by [Secure config](https://bitbucket.org/nthmost/python-secureconfig), and I still need to build the ui with [WX Python](http://http://www.wxpython.org/).

##What features are planned?

As stated above, Goodshare will be able to do the same things you can do with the Goodreads and Bookshare web interfaces.

Spesifically, with goodreads, a few things you'll be able to do are:
*View, add books to, and remove books from you're shelves
*Rate and comment on books
*Create and destroy shelves.
*Search for books, authors, groups, etc just like on Goodreads.

Group support will most likely be coming, but... Well. I don't use many groups so it won't be next on the list :p


Things you'll be able to do with bookshare:
*View you're book history and download any of them
*search for books and authors
*Download books (did you really think I wouldn't put this in?)
*View categories such as latest, popular, etc
*quickly rate any book on Goodreads, probably with a right click menu
*quickly add a book to a goodreads shelf, again with a right click menu

##Contributing

If you would like to help with this project, by all means, PULL REQUEST!
Especially if you're good with WX... 