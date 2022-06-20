#!/usr/bin/env python

import rospy, sys
import pandas as pd
import rospkg

# Main function
if __name__ == '__main__':
    rospy.init_node('evora_map')
    
    # READ FILES AS ARGUMENTS
    # csv_file_path = sys.argv[1]
    
    rp = rospkg.RosPack()
    pkg_path = rp.get_path('evora_topological_map')
    rospy.loginfo(pkg_path)

    csv_file_path = pkg_path + '/data/csv/'
    csv_file_left_panels = 'evora_topology_left_panels.csv'
    csv_file_right_panels = 'evora_topology_right_panels.csv'
    csv_file_central_corridor = 'evora_topology_central_corridor.csv'

    data_left_panels = pd.read_csv(csv_file_path + csv_file_left_panels, names=['LATITUDE', 'LONGITUDE'], sep=',')
    gps_data_left_panels = tuple(zip(data_left_panels['LATITUDE'].values, data_left_panels['LONGITUDE'].values))

    data_right_panels = pd.read_csv(csv_file_path + csv_file_right_panels, names=['LATITUDE', 'LONGITUDE'], sep=',')
    gps_data_right_panels = tuple(zip(data_right_panels['LATITUDE'].values, data_right_panels['LONGITUDE'].values))

    data_central_corridor = pd.read_csv(csv_file_path + csv_file_central_corridor, names=['LATITUDE', 'LONGITUDE'], sep=',')
    gps_data_central_corridor = tuple(zip(data_central_corridor['LATITUDE'].values, data_central_corridor['LONGITUDE'].values))

    param_evora_map_ns = "evora_map/"
    # print(len(gps_data_right_panels))

    if rospy.has_param(param_evora_map_ns):
      rospy.delete_param(param_evora_map_ns)

    # LEFT PANNELS MATRIX SIZE: 17 x 11
    row = 0
    column = 0
    for idx, point in enumerate(gps_data_left_panels):
        name = param_evora_map_ns + 'left_panels/row/' + str(row) + '/column/' + str(column)
        rospy.set_param(name, str(point[0]) + ',' + str(point[1]))
        column += 1
        if column == 11:
            row += 1
            column = 0
    
    # RIGHT PANNELS MATRIX SIZE: 18 x 11
    row = 0
    column = 0
    for idx, point in enumerate(gps_data_right_panels):
        name = param_evora_map_ns + 'right_panels/row/' + str(row) + '/column/' + str(column)
        rospy.set_param(name, str(point[0]) + ',' + str(point[1]))
        column += 1
        if column == 11:
            row += 1
            column = 0

    for idx, point in enumerate(gps_data_central_corridor):
        name = param_evora_map_ns + 'central_corridor/row/' + str(idx)
        rospy.set_param(name, str(point[0]) + ',' + str(point[1]))


