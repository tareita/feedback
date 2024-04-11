1. Install Node.js at https://nodejs.org/en/download/
   Follow the instructions at https://phoenixnap.com/kb/install-node-js-npm-on-windows
   Ensure npm (node package manager) is installed

2. cd into the feedback-app directory (or unzip the source code folder)
   install dependencies by running:

```
npm install
```

3. Run the app

```
npm start
```

4. Open http://localhost:3000 to view it in the browser.

Using the application

1. Upload documents using the Choose files button,
   Select all 5 pdf files within the Week 1 Module Documents folder in the root folder. feedback-app\Week 1 Module Documents
   Select all 5 pdf files and click open.
   It should now say '5 files' next to the button.

2. Input answers to the questions in the quiz.

3. Once done, submit the quiz by scrolling down and clicking the Finish Attempt.. button, and confirming by clicking Submit on the pop-up
   modal.

4. The feedback will start to generate under each question, and a review section will pop up on the right hand side.

5. Refresh if you want to reattempt the quiz. Note: You will have to upload the documents again.

6. Click submit.

7. The results will be displayed in the console.

TESTING

run the following command to run the test suite:

```
npm test
```
