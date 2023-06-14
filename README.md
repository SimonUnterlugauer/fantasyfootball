# fantasyfootball

## With this code i wanted to simulate a fantasy football draft for the upcoming season. The goal was to get the best possible lineup to win as many games as possible in the upcoming season. To achieve this, we used several sources (e.g. Historical Data from current players, predictions for next season, common draft-techniques ,etc.) 

## Data

### The data was selected from various sources (....) 
### and was preprocessed and saved into a postgres database. The database is hosted on ....

## Code

### -> helpers:
#### helperfunctions to provide the basic functionality for 
##### - drafting
##### - creating the best possible lineup for upcoming game week
##### - simulate the draft with 10 teams with each 15 players to select from

### -> databasehandlers:
#### functions to migrate different tables to one to have a better summary and better insights of the data

### -> optimization Models
#### PULP-Optimization Models for:
##### - Finding the best players in every draft situation
##### - Selecting the best possible lineup out of the available/existing players that we have drafted in the beginning of the season

### -> simulation
#### Simulation - Scenarios:
##### - simulate complete draft with xx-teams and xx-players to be selected of every team (default values that are presented in the research paper being 10 teams in the league with each team being able to select 15 players)
##### - simulate game (to be continued)
