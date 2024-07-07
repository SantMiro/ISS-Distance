# International Space Station Distance Calculator


This Flask app will return the distance from the International Space Station (ISS) to your position. This app was deployed in GCP.

The code simply retrieves the current position of the ISS via its open [API](http://open-notify.org/Open-Notify-API/ISS-Location-Now/). It also requests from the user to provide a valid Google Maps address that gets converted to coordinates using GCP API credentials. The code calculates the distance from the user's coordinates to the ISS applying the [Haversine](https://en.wikipedia.org/wiki/Haversine_formula) formula.

As an additional feauture if the code, if the ISS and user are on the same country, the code returns the estimated time of drive to get to the prejected position of the ISS. 

This app was created by Santiago Miro.
