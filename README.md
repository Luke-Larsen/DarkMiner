# DarkMiner
 A program to use idle computer time to run other programs

# This project is for legal use only
 I wish to repeat this, I have not created this program so that you go out there and use it for a botnet or something like that.
 It will not work for that purpose. It is constructed and developed to use idle time of your own personal computers when they are running
 to do downtime processes like mine cryptocurrency or join render farms.

# Different versions
There are two different versions. One which is developed in c++ and was the original code for this script. Python is the new version that I have been developing. I changed over to python as it is easy to prototype and quick to develop cross-platform solutions. It was also just a good first project to learn python with. The CNC folder is for the command and control server which can be used if you need to administer a few different computers.

# Dependencies
    ** Windows: **
        Python 3.8x
    ** Linux: **
        Python 3.8x
        https://github.com/g0hl1n/xprintidle

# Basic set up
The set-up is relatively easy. The most difficult part is to set up the command and control server. 
## CnC
To set up the command and control server you will need a web server. You can create this with a vps or just get a web host. I won't be going into how to do this here. The next thing you need to do is set up the MySQL table. In the CnC folder there is a file called Work.sql you need to import this into your mysql database. After that just upload all of your CnC files to the server and change the config.php to the proper MySQL settings. It should then be up and running, and you can log into it with the default password of *MySecurePassword*. Realize if there are any problems this is a beta version and I haven't gone through and created an installation script. Something may mess up or be different on your installation. Stack Overflow is your friend in these cases.
## Python install
In order for the python script to run you will need python 3.8x. In general this is an easy process there are some dependencies at the moment depending on what kind of machine you are running. Check the README in the python version folder for more information. Past that point just run the main.py, and it will walk you through the installation.
## C++ install
This currently only works for windows, but given that it uses all standard libraries there is no need for any dependencies. All you need to do is compile the c++ and run the EXE.

# Licensing 
 This program is licensed under the MIT license. There are some programs i.e. sheepit, xprintidle that are licensed under GPL and their restrictive license. I have read and researched this license and while I am not a legal expert have ascertained that if I use piping between the two programs it should be allowed, although it seems to be a bit of an undefined gray area. In the event that any of these groups wants me to remove the pipes to their code please reach out to me, and I'm sure we can work something out.
 https://www.gnu.org/licenses/gpl-faq.en.html#MereAggregation