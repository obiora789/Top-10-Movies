<h1>Top-10-Movies</h1>
<p>This is my personal blog of my top ten movies of all time. Feel free to add more than 10 movies. Enjoy!!</p>
<p>Simply put, this blog ranks your favourite movies of all time based on the movie ratings you provide, and shows them to the whole world.</p>
<p>The route "http://localhost:5000/" is the homepage and diaplays all the movies already in the database. If there are no movies, only the "Add Movie button" is displayed.</p>
<p>The route "http://localhost:5000/add" is activated when you click "Add Movie" button. Here, you can type the name of the movie you love.</p>
<p>The "/select" route is activated immediately you submit the movie you would like to add. This route displays the likely movies (and the year they were produced) that may have a similar name to the movie you requested. You can then manually select the correct movie to be added to your collection.</p> 
<p>The "/edit" route provides you the opportunity to personally rate the movie as well as add a review to be displayed on the homepage. <br>
The "/edit" route is either automatically triggered when adding a movie for the first time, or manually triggered when you click the "Update" button.</p>
<p>The "/delete" route deletes a movie from both your list of movies and from the database permanently.</p>


<h2>Requirements</h2>
<ul>
  <li>Python 3.8 or higher.</li>
  <li>Pycharm 2022.3.2 or higher.</li>
  <li>Flask</li>
  <li>SqlAlchemy</li>
  <li>WTForms</li>
  <li>I have already added requirements.txt to this code.</li>
</ul>
<hr>
<h3>What to do</h3>
<ol>
  <li>Fork this Git and clone to your local PC.</li>
  <li>To install all modules required for this program, click "Install Requirements" when prompted by your code editor</li>
  <li>Ensure you have updated Pycharm or other good updated IDE. I used Pycharm 2022.3.2 (Community Edition).</li>
  <li>Populate the environment variables as stated below</li>
  <ul>
    <li>API_KEY=keyToAccessTheMovieDatabase</li>
    <li>APP_SECRET=secretSessionKey</li>
  </ul>
  <li>That's all you need to do for now.😉</li>
</ol>

<hr>
<h3>Results</h3>
<img src="https://github.com/obiora789/Top-10-Movies/blob/ecacbda745b9e5a1dc5e32a42a8d9584d3ea3785/Screenshot%202023-04-16%20at%2019.26.49.png" alt="addMovieScreenshot">
<img src="https://github.com/obiora789/Top-10-Movies/blob/ecacbda745b9e5a1dc5e32a42a8d9584d3ea3785/Screenshot%202023-04-16%20at%2019.26.55.png" alt="selectMovie">
<img src="https://github.com/obiora789/Top-10-Movies/blob/ecacbda745b9e5a1dc5e32a42a8d9584d3ea3785/Screenshot%202023-04-16%20at%2019.27.29.png" alt="updateRatingsAndReviews">
<img src="https://github.com/obiora789/Top-10-Movies/blob/ecacbda745b9e5a1dc5e32a42a8d9584d3ea3785/Screenshot%202023-04-16%20at%2019.27.39.png" alt="homepage">
<hr>
<h3>Bugs</h3>
<p>None as at the time of this report.</p>
