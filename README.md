# educafeweb
# educafe

https://www.youtube.com/watch?v=ttBWi5Qs_wQ

the app idea was conceived at HackHarvard 2022

EduCafe 

Welcome to EduCafé! We are so excited to be able to guide you through our mission of making university campuses more social and intellectually vibrant!.

EduCafé is a web application which serves to connect students and professors outside of the classroom setting and without the pressure of tense formality that too often plagues these sorts of interactions. We will achieve this mission with EduMeets, roundtable discussions posted and hosted by professors in search of a casual conversation with students. These EduMeets come in all shapes and sizes—from a meal at a large roundtable in Commons to an intimate one on one debate over coffee. 

Many professors we have spoken to this semester have expressed an interest in learning more about the interesting life-stories of the students at their institutions. To do so, now, is easier than ever. With EduCafé, all professors need to do is post an EduMeet on our website, after which all students from all fields of study will be able to browse and sign up for it. We expect a large eagerness among students to sign up for EduMeets, so the capacity of the EduMeet must be set to a certain limit by the hosting professor before it is posted.

Getting Started
We are so excited that you would like to get started with EduCafe. Before we get going, make sure, you have set up a virtual environment by command line in the terminal:
python3 -m venv venv

Activate virtual environment:
. venv/bin/activate

Install Flask:
pip install flask

Install flask_mail:
pip install flask_mail

Install requests:
pip install requests

Install flask_session:
pip install flask_session

Walkthrough
The whole website is made to be very accessible, user friendly, and as easy as possible to navigate.

On the main page of the website you can register if you are a first time user (you will be required to use your Yale email), login if you already have an account, learn more about what EduCafé is, or scroll through an easy guide on how to register for an EduMeet.

From here the user interface differs based on if you are a student or a professor. 

User Experience for Professors
When registering for the first time, you will be asked to fill out a quick form to create your profile. We are working hard to implement the possibility to take a picture on a web-camera, but for now please use an image that can be found online and paste its URL address in the relevant input field. Once the form has been filled out and the password fulfills all of the requirements, you will be redirected to a welcome page.

When logging in as an already existing user, you will be asked to provide your username and password, after which you will be redirected to a welcome page.

The welcome page offers you an easy and quick way to post an EduMeet–just click on “Post an EduMeet” or “Post and Host !”. Other than posting an EduMeet, you can also scroll down to learn more about what an EduMeet is, and how to post one. Click on “My EduMeets” in the header to view your previously posted EduMeets, hover over the pink user icon and then click on “Profile” to view your profile information, or “Logout” to logout and go back to the main page.

When you want to post an EduMeet, you will be asked to fill out a very brief and simple form (4 questions - Date and time, Location, Capacity, and Topic of Discussion - optional). We have purposefully drafted and written these questions to be as minimal yet effective as possible given the circumstances. We believe succinctly yet meaningfully answering them will create an inspiring EduMeet experience. You will see a draft of the EduMeet after submitting the form, and the last step is to confirm and post the EduMeet with the button “Post Now!”
And it’s done! You have posted an EduMeet which students will be able to see and sign up for!

User Experience for Students
When registering for the first time, you will be asked to fill out a quick form to create your profile. Once finished creating your profile you will be redirected to a “New EduMeets” page. 

When logging in as an already existing user, you will be asked to provide your username and password, after which you will be redirected to the “New EduMeets” page. 

On this page, you can swipe right or left on newly posted EduMeets. This is the core of EduCafé, and we are proud to say that it’s great fun! Swiping right will sign you up for the EduMeet,  but swiping left will simply act as a “pass” and allow you to see the next one. This system of signing up was implemented to stress the move away from the tense formality of students contacting professors with EduCafé. 

When you sign up for an EduMeet, a confirmation Email will be sent to the email address you provided, as a confirmation that you are signed up. The information provided about the EduMeet in the email is the Name of the Professor, Location of the EduMeet, and its scheduled Date and Time.

Once you have gone through all of the new EduMeets you will be redirected to the All EduMeets page, where you can see all previously posted EduMeets on the website. The EduMeets you are registered for will show “You are registered” at the bottom of them. You can click on EduMeets you are not registered for, to see more information and it gives you the possibility to register for it.

In the header you can go to your “Profile” page, to see your account information, logout, or navigate to the “My EduMeets” page, where you will be able to see all of the EduMeets you have signed up for. And that’s it! The only thing left is to attend the EduMeet/EduMeets you registered for!







