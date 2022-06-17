# evora_topological_map
The package in this repository topologically generates waypoint coordinates for the Evora solar farm.

![evora topology map](https://raw.githubusercontent.com/durable-ist/evora_topological_map/master/data/imgs/evora_farm_matrix.png)


## Running the code
Running the following launch file
```
$ roslaunch evora_topological_map evora_topology.launch
```

will add all coordinates of the farm as ROS parameters. To access them just type
```
$ rosparam list
```

and you will get the parameters/coordiantes as shown below. 

```
/evora_map/right_panels/row/0/column/2
/evora_map/right_panels/row/0/column/3
/evora_map/right_panels/row/0/column/4
...
/evora_map/left_panels/row/9/column/8
/evora_map/left_panels/row/9/column/9
...
/evora_map/central_corridor/row/8
/evora_map/central_corridor/row/9
```

To get actual coordinates, one must run the following command to get the latitude and longitude of one point

```
$ rosparam get /evora_map/right_panels/row/9/column/9
38.54098562306518,-7.960679494830838
```
