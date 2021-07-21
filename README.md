csv2djipilot creates a DJI kml file to be imported in a DJI Pilot waypoints.
Csvfile contains
```
point_name;lon;lat;height;heading;gimbal;speed;turnmode;actions_sequence
waypoint_A;2.2595689652949886;48.02450015337408;15.0;180;-30;5;1000.SHOOT.1000
waypoint_B;2.2596269016191606;48.02450001605067;22.98;180;-50;5;1000.REC
waypoint_C;2.2596653502913546;48.02450001248549;25.98;180;-60;5;STOPREC.2000.G40.SHOOT
```
speed between 0 to 15 m/s
turnmode is AUTO, C for clockwise or CC for counter clockwise
actions sequence is a list of actions separted by points without space. There could be no action, one or multiple actions.
H1000 => Hover 1000ms = 1s
SHOOT => take a picture 
G40 =>Gimbal a -40°
REC => start video recording
STOPREC => stop video recording
A-170 => turn aircraft to -170

usage: csv2djipilot.py [-h] [-o OUTPUT] [--onfinish {hover,gohome}] csvfile

positional arguments:
  csvfile               Specify csv input file

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Specify output file (default:stdout)
  --onfinish {hover,gohome}

ex: 
````
python3 csv2djipilot.py csvfile.csv -o output.kml
````

tested with DJI Matrice 210 RTK V2
