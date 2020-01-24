## Anurag Vaiyda
CSCI 204: Data Structures and Algorithms 
Final Project: Chicago Crime Analysis 
12/10/2019

The aim of this project was to read ~ 7 million crime reports from Chicago from the last decade and create a
data driven system that will tell the police department to send patrols to areas that require the most attention. 
The code utilizes different data structures like dictionaries, BST, AVL trees, and Heaps to efficiecntly store the 
data and algorithms to optimize the data processing. We also use Bridges API to create visualizations of our 
trees and heaps. Finally, we also use google maps to create a heat map of the crime intensity in Chicago. The project was done in three phases. Here are their brief descriptions:

1. Phase 1: This phase involved setting up a pipeline to load the data set and create BST for crimes and locations of crimes
2. Phase 2: A function was written to handle dispatch requests. Three scenarios were handled
	* A new 911 dispatch call is made and a patrol needs to be sent
	* No 911 call is made but there is a queue of dispatches (stored as a priority queue in a min heap) that need to be handled
	* No 911 call is made and no backlog of dispatches. A general dispatch is sent based on areas of high risk (stored in an   AVL tree)
3. Phase 3: This phase involved doing background readings on racial bias in police and assigning priorities to crime and location in a socially cognizant way. 

Main data structures used: Queues, Priority queues, BST, AVL trees, heaps

For more details, continue reading ahead. 

## Phase 1

__________________________________________________________________________________________________________
#### Before you run the code, you will have to install the bridges package. Follow the following instructions:

1. Navigate to the folder where you have stored the files.
2. Run the following command in terminal.
	* "python3 -m venv p3"
3. Activate the virtual environment 
	* "source p3/bin/activate"
4. Install the bridges API
	* "pip install bridges"

Once bridges API is installed, you can run the program. _The API does not allow for multiple links to be created one after the other_, so only the location priority tree visualization link is created by default. In order to create the visualization link for the crime priority tree, comment out the location priority tree code and uncomment the appropriate crime tree visualization code.

In both the trees, the color of the node represents the _priority_. More **red** means higher priority, and the more **green/ blue** is lower priority. Hovering over the node gives more information about the node. 

__________________________________________________________________________________________________________

## Phase 2
__________________________________________________________________________________________________________

#### This phase generated two new visualizations :
1. We improved our Phase 1 visualization by translating the data to a heat map
In this heat map we plot the **location** of each crime and then google maps visualization software gives it a green color. When the density of dots crosses a threshold, the map shows the color red. You can visualize the heat map by opening **heatmap_CAN.html**.
#### If you wish to recreate this visualization, follow these steps:
   1. Run the following command:
		- "pip install gmaps"
		- "pip install gmplot"
   2. Run the **Heatmap_CAN.py**

2. We used the Bridges API to create a visualization of the dispatch queue minHeap
We used the test code to create the dispatch queue visualization 
   1. You can look at the visualization at the following link: <http://bridges-cs.herokuapp.com/assignments/2/ajv012>

##### We tested the code in small parts:
1. We first tested the insert and extract method for the min heap 
2. We then tested the heap sort method
3. Once the heap class and heap sort modules were working, we created a bunch of test dispatch strings and added them to the dispatch queue
4. Then we called our next patrol function sometimes with a new request and sometimes without a new request 
5. Once the test code was provided by Prof. Dancy, we tested our functions using that code 
6. We also used the bridges API constantly to check our heaps 

##### Creative aspects:
- We created a heat map to better our visualizations from the first phase 
- We broke down the big problem of creating the get next patrol method into three different scenarios
  * We handled the three scenarios intelligently (for example sending a patrol to the location of the crime and not adding the dispatch to the dispatch queue)
- We created a smart system for finding overall priority
  * We added the priorities of the crimes and then divided by the count to get the overall priority
  * We used this priority for all the sorting purposes 
  * We realized that it would be hard for the user to understand fractional priorities, so we created a map that translated the fractional priorities to whole numbers, which is what is displayed in the dispatch queue heap

__________________________________________________________________________________________________________

## Phase 3
__________________________________________________________________________________________________________
#### To run our code you need to follow the previous instructions issued for Phase 1 and Phase 2.

##### This includes:
1. **Installing the bridges package** in order to run our visualizations.
   1. Navigate to the folder where you have stored the files 
   2. Run the following command in terminal 
	* "python3 -m venv p3"
   3. Activate the virtual environment 
	* "source p3/bin/activate"
   4. Install the bridges API
	* "pip install bridges"
2. **Installing gmaps and gmplot** if you want to create the heat map from Phase 2
   1. Run the following command:
		- "pip install gmaps"
		- "pip install gmplot"
   2. Run the **Heatmap_CAN.py**

##### Alternatively, links for the AVL tree visualizations are given below:

#### Visualizations (old):

- [Location AVL Tree](http://bridges-cs.herokuapp.com/assignments/0/ajv012 "Phase 1 Location AVL Tree")
- [Crime AVL Tree](http://bridges-cs.herokuapp.com/assignments/1/ajv012 "Phase 1 Crime AVL Tree")




#### Visualizations (new):

- [Location AVL Tree](http://bridges-cs.herokuapp.com/assignments/2/ajv012 "Phase 3 Location AVL Tree")
- [Crime AVL Tree](http://bridges-cs.herokuapp.com/assignments/3/ajv012 "Phase 3 Crime AVL Tree")

##### How we tested our code:
1. We tested our code by discussing and experimenting with different weights for both the location and crime priorities.
2. Based on the deviations between location and crime priorities, we adjusted the weights of the priorities so that they both evenly contributed to overall priority. 
3. Overall our goal was to make sure both location and crime had equal impact on determining the final priority for dispatch. 

#### Overall Creative Aspects of Our Assignment:
- We created a heat map to better our visualizations from the first phase 
- We used many of the tools in the Bridges API
  * Color coded nodes based on priority 
  * Attached node labels and titles 
- We broke down the big problem of creating the get next patrol method into three different scenarios
  * We handled the three scenarios intelligently (for example sending a patrol to the location of the crime and not adding the dispatch to the dispatch queue)
- We created a smart system for finding overall priority
  * We attached weights to different crimes and made decisions based on location and arrest rates to determine priority for locations and crimes.
  * We used this priority for all the sorting purposes 
  * We realized that it would be hard for the user to understand fractional priorities, so we created a map that translated the fractional priorities to whole numbers, which is what is displayed in the dispatch queue heap

#### Police Station Placement Design 

- Overall we decided that police stations should be placed in areas with the greatest crime frequency. However, we learned in the past phases that frequency on its own isn't an accurate representation of priority. 
- Instead, we decided to use the crime priority list, which is the list of all the beats and their overall priority (overall priority being the sum of crime and location priority), to create another, more accurate heat map. 
- Using this heat map we will be able to decide where we wanted to place initial police stations.
- We start by placing 4-5 police stations in the areas that showed the highest priorities on our heat map
- From there, we will have a function that, when necessary, can be called to decide where the next police station should be located.
    * The function will work by adding potential police stations to a priority queue. 
    * This function will take into consideration several variables to determine priority: 
      * The crime priority list to give us priorities for different beats.
      * Proximity to existing police stations to make sure dispatch can cover a good area. 
- The function can be called whenever the police commissioner 
    
   
#### Code Refactoring and Revisions 

##### Based on the readings and suggestions we decided to make a few crucial changes to our implementation.
1. We reviewed and revised our code so that everything was named and formatted appropriately and professionally.
    * i.e. Changing the name of our main function from **~~'ChicagoCrimeFun"~~** to 
**"ChicagoCrimeAnalysis"**.
2. After considering the topics discussed in the readings we changed the way we determined priority.
    * Originally, crime priority was determined exclusively by its frequency and location priority was determined by the amount of crimes committed in each beat.
    * We revised **crime priority** so now it takes into account three different variables.
      * What crime division the crime falls under (accounts for **60%** of the priority)
      * Crime frequency (**20%**)
      * Arrest rate of that crime (**20%**)
    * We revised **location priority** to take into account two variables
      * Weighted crime count (**70%**)
      * What community area the crime was committed in (**30%**)


