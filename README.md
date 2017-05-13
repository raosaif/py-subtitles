# py-subtitles

py-subtitles automates boring and time-consuming task into a single click action and saves your precious time. 
Subtitles are great especially when video is done in a language that you do not understand. If you are French and want to share videos with people who only understand English, you will have to add subtitles to your video. 

Description
----------

py-subtitles and py-subtitles-click are python scripts to download subtitles for a movie with a movie name provided or single right click on movie file. Right click on a movie file and download the subtitle. If there is no exact subtitle then this script will download a subtitle from an exisiting pool of priority subtitles. You can edit the prirority list and add your own preffered list to download the subtitles.

![alt text](https://github.com/raosaif/py-subtitles/blob/master/images/right-click.jpg)

Subscene
--------
The search for subtitles in this site is very simple once you know the right name and title. Furthermore, you will have the choice of using language to sieve your results to a manageable number. 

Process
-------
There are two scripts

* py-subttitles.py is a script which can be used from a command line with a movie name provided
* py-subtitles-click.py is a script which can be made right click based action using Nautilus-Action configuration tools.

If there is no exact subtitle for the movie name and format then py-subtitles will download movie subtitle which matched a tag from priority list. You can edit this list from the script

priority_list = ['axxo','YIFY','RARBG','FXG','DIAMOND','iNTERNAL']

Adding Right Click Context Menu Options
---------------------------------------
Nautilus-Actions is easy to create custom context menu options for Ubuntu’s Nautilus file manager. Nautilus-Actions is simple to use – much simpler than editing the Windows registry to add Windows Explorer context menu options. All you really have to do is name your option and specify a command or script to run.

![alt text](https://github.com/raosaif/py-subtitles/blob/master/images/nautilus-actions.jpg)


* ![How to Easily Add Custom Right-Click Options to Ubuntu’s File Manager] (https://www.howtogeek.com/116807/how-to-easily-add-custom-right-click-options-to-ubuntus-file-manager/)

Features
--------
* Saves you a lot of time and frustrations: right click on the movie and everything automagically works!
* It is lightweight and fast
* It is actively developed and we try to listen our users.

Comman-Line Example
-------------------
You need to add geckodriver to your path 

    $ export PATH=$PATH:/path/to/geckdriver/directory/
    $ ./py-subtitles -b movieName #command-line utility to download subtitles for a movie file
    $ ./py-subtitles-click #context menu option to download subtitles of a movie file
    
