# https://github.com/tisljaricleo/GPS-visualization-Python
from gps_class import GPSVis
import simplekml as skml
import pandas as pd
import rospkg

class FilesPath:
    def __init__(self):
        self.package_path = pkg_path + '/'
        self.csv_path = 'data/csv/'
        self.kml_path = 'data/kml/'

        self.data_file_measures = 'evora_data.csv'
        self.data_file_left = 'evora_data_lats_left.csv'
        self.data_file_right = 'evora_data_lats_right.csv'

        self.map_path = 'data/imgs/evora_map.png'

        self.data_file_write_all = 'evora_topology_all.csv'
        self.data_file_write_left = 'evora_topology_left_panels.csv'
        self.data_file_write_right = 'evora_topology_right_panels.csv'
        self.data_file_write_central = 'evora_topology_central_corridor.csv'


rp = rospkg.RosPack()
pkg_path = rp.get_path('evora_topological_map')

current_paths = FilesPath()

vis = GPSVis(current_paths, points=(38.54184, -7.96304, 38.54023, -7.96044))

vis.create_image(color=(0, 0, 0), width=3)
# vis.plot_map(output='save')
vis.plot_map(output='not_save')

# GPS TO KML
csv_to_convert = []
csv_to_convert.append(current_paths.package_path + current_paths.csv_path + current_paths.data_file_write_all)
csv_to_convert.append(current_paths.package_path + current_paths.csv_path + current_paths.data_file_write_left)
csv_to_convert.append(current_paths.package_path + current_paths.csv_path + current_paths.data_file_write_right)
csv_to_convert.append(current_paths.package_path + current_paths.csv_path + current_paths.data_file_write_central)

for file in csv_to_convert:
    data_pd = pd.read_csv(file, names= ['latitude','longitude'], sep=',')
    data = data_pd.values
    
    print(len(data))

    k = skml.Kml()
    k.document.name = file.replace(".csv", '')

    sharedstyle = skml.Style()
    sharedstyle.iconstyle.color = 'ff0000ff'  # Red   
    # sharedstyle.iconstyle.color = skml.Color.blue  # Blue
    sharedstyle.iconstyle.scale = 0.3
    sharedstyle.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/road_shield3.png'

    for row in data:
        if len(row) <= 3:
            pnt = k.newpoint(coords=[(row[1], row[0])])
        elif len(row) == 4:
            pnt = k.newpoint(coords=[(row[2], row[1])])
        pnt.style = sharedstyle

    wfile = file.replace('/csv/', '/kml/')
    k.save(wfile.replace(".csv", '') + ".kml")
