# City Weather GUI

This project is a simple GUI based weather application created in python using the tkinter module, incorporating MySQL connectivity.

 Users can input the name of a city and request information on its weather at that moment. The data received include the temperature of the place (in °C), the weather description and the time of the place for which the information corresponds to. This request is done using API calls with the OpenWeather API. This information can then be saved to the MySQL database for future reference. Weather data from API calls are updated every ten minutes. Duplicate entries are prevented using primary key constraints in the SQL table.

Users have the option to delete any of the saved records by using the display & delete button. 
The program also contains a graphing feature for comparison purposes using the matplotlib library to plot a line graph between temperature and timestamp of various cities from the saved records present in the MySQL database. The graph is annotated with the weather descriptions of the cities and users can hover the mouse cursor over the graph to display more annotations.
