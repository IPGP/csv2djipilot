csv2djipilot creates a DJI kml file to be imported in a DJI Pilot waypoints.
Csvfile contains
```
point_name;lon;lat;height;heading;gimbal
waypoint_A;2.2595689652949886;48.02450015337408;15.0;180;-30
waypoint_B;2.2596269016191606;48.02450001605067;22.98;180;-50
waypoint_C;2.2596653502913546;48.02450001248549;25.98;180;-60
```

usage: csv2djipilot.py [-h] [-o OUTPUT] csvfile

ex: 
````
python3 csv2djipilot.py csvfile.csv -o output.kml
````

tested with DJI Matrice 210 RTK V2

To do :
- [ ] User interface to change actions for the waypoints or colums for actions in the csv
- [ ] specific speed for each waypoint in the csv. It is the speed between current point to next one (or the speed to reach current point ? )
