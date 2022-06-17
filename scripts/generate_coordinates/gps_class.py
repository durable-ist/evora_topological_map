from hashlib import new
from pickle import FALSE
from turtle import right
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw


class GPSVis(object):
    """
        Class for GPS data visualization using pre-downloaded OSM map in image format.
    """
    def __init__(self, cp, points):
        """
        :param data_path: Path to file containing GPS records.
        :param map_path: Path to pre-downloaded OSM map in image format.
        :param points: Upper-left, and lower-right GPS points of the map (lat1, lon1, lat2, lon2).
        """
        self.data_path = cp.package_path + cp.csv_path + cp.data_file_measures
        self.data_path_2 = cp.package_path + cp.csv_path + cp.data_file_left
        self.data_path_3 = cp.package_path + cp.csv_path + cp.data_file_right

        self.points = points
        self.map_path = cp.package_path + cp.map_path

        self.write_all = cp.package_path + cp.csv_path + cp.data_file_write_all
        self.write_left_panels = cp.package_path + cp.csv_path + cp.data_file_write_left
        self.write_right_panels = cp.package_path + cp.csv_path + cp.data_file_write_right
        self.write_central_corridor = cp.package_path + cp.csv_path + cp.data_file_write_central

        self.result_image = Image
        self.x_ticks = []
        self.y_ticks = []

        self.latitudeOffset = -0.00001206293
        self.latitudeOffsetvar = True

    def plot_map(self, output='save', save_as='resultMap.png'):
        """
        Method for plotting the map. You can choose to save it in file or to plot it.
        :param output: Type 'plot' to show the map or 'save' to save it.
        :param save_as: Name and type of the resulting image.
        :return:
        """
        self.get_ticks()
        fig, axis1 = plt.subplots(figsize=(10, 10))
        axis1.imshow(self.result_image)
        axis1.set_xlabel('Longitude')
        axis1.set_ylabel('Latitude')
        axis1.set_xticklabels(self.x_ticks)
        axis1.set_yticklabels(self.y_ticks)
        axis1.grid()
        if output == 'save':
            plt.savefig(save_as)
        else:
            plt.show()

    def create_image(self, color, width=2):
        """
        Create the image that contains the original map and the GPS records.
        :param color: Color of the GPS records.
        :param width: Width of the drawn GPS records.
        :return:
        """
        data = pd.read_csv(self.data_path, names=['LATITUDE', 'LONGITUDE'], sep=',')

        self.result_image = Image.open(self.map_path, 'r')
        img_points = []
        gps_data = tuple(zip(data['LATITUDE'].values, data['LONGITUDE'].values))

        distance_beetween_pannels_lon = gps_data[0][1] - gps_data[1][1]

        new_gps_data = []

        # GET COORDINATES FOR THE LEFT SIDE AND MIDDLE CORRIDOR
        data_2 = pd.read_csv(self.data_path_2, names=['LATITUDE', 'LONGITUDE'], sep=',')
        gps_data_2 = tuple(zip(data_2['LATITUDE'].values, data_2['LONGITUDE'].values))

        central_corridor = []
        left_pannels = []
        right_pannels = []
        
        for point in gps_data_2:
            coord_arr = []
            for j in range(0, 12):
                if j == 0:
                    if self.latitudeOffsetvar:
                        coord_arr.append((point[0] + self.latitudeOffset, point[1]))
                    else:
                        coord_arr.append(point)
                elif j == 10:
                    if self.latitudeOffsetvar:
                        coord_arr.append((point[0] + self.latitudeOffset, coord_arr[j - 1][1] - distance_beetween_pannels_lon*0.75))
                    else:
                        coord_arr.append((point[0], coord_arr[j - 1][1] - distance_beetween_pannels_lon*0.75))
                elif j == 11:
                    if self.latitudeOffsetvar:
                        central_corridor.append((point[0] + self.latitudeOffset, coord_arr[j - 1][1] - distance_beetween_pannels_lon*0.42))
                    else:
                        central_corridor.append((point[0], coord_arr[j - 1][1] - distance_beetween_pannels_lon*0.42))
                else:
                    if self.latitudeOffsetvar:
                        coord_arr.append((point[0] + self.latitudeOffset, coord_arr[j - 1][1] - distance_beetween_pannels_lon))
                    else:
                        coord_arr.append((point[0], coord_arr[j - 1][1] - distance_beetween_pannels_lon))

            new_gps_data += coord_arr
            left_pannels += coord_arr

        # APPEND COORDINATES OF THE CENTRAL CORRIDOR
        new_gps_data += central_corridor
       
        # GET COORDINATES FOR THE RIGHT SIDE
        data_3 = pd.read_csv(self.data_path_3, names=['LATITUDE', 'LONGITUDE'], sep=',')
        gps_data_3 = tuple(zip(data_3['LATITUDE'].values, data_3['LONGITUDE'].values))

        for point in gps_data_3:
            coord_arr = []
            for j in range(0, 11):
                if j == 0:
                    if self.latitudeOffsetvar:
                        coord_arr.append((point[0] + self.latitudeOffset, point[1] + distance_beetween_pannels_lon*0.65))
                    else:
                        coord_arr.append((point[0], point[1] + distance_beetween_pannels_lon*0.65))
                elif j == 1:
                    if self.latitudeOffsetvar:
                        coord_arr.append((point[0] + self.latitudeOffset, point[1]))
                    else:
                        coord_arr.append(point)
                else:
                    if self.latitudeOffsetvar:
                        coord_arr.append((point[0] + self.latitudeOffset, coord_arr[j - 1][1] - distance_beetween_pannels_lon))
                    else:
                        coord_arr.append((point[0], coord_arr[j - 1][1] - distance_beetween_pannels_lon))

            new_gps_data += coord_arr
            right_pannels += coord_arr

        # WRITE TO CSV FILES
        pd.DataFrame(new_gps_data).to_csv(self.write_all, index=False, header=False)
        pd.DataFrame(left_pannels).to_csv(self.write_left_panels, index=False, header=False)
        pd.DataFrame(central_corridor).to_csv(self.write_central_corridor, index=False, header=False)
        pd.DataFrame(right_pannels).to_csv(self.write_right_panels, index=False, header=False)

        # DRAW POINTS INTO THE MAP IMAGE
        for d in new_gps_data:
            x1, y1 = self.scale_to_img(d, (self.result_image.size[0], self.result_image.size[1]))
            img_points.append((x1, y1))
        draw = ImageDraw.Draw(self.result_image)
        # draw.line(img_points, fill=color, width=width)
        draw.point(img_points, fill=color)



    def scale_to_img(self, lat_lon, h_w):
        """
        Conversion from latitude and longitude to the image pixels.
        It is used for drawing the GPS records on the map image.
        :param lat_lon: GPS record to draw (lat1, lon1).
        :param h_w: Size of the map image (w, h).
        :return: Tuple containing x and y coordinates to draw on map image.
        """
        # https://gamedev.stackexchange.com/questions/33441/how-to-convert-a-number-from-one-min-max-set-to-another-min-max-set/33445
        old = (self.points[2], self.points[0])
        new = (0, h_w[1])
        y = ((lat_lon[0] - old[0]) * (new[1] - new[0]) / (old[1] - old[0])) + new[0]
        old = (self.points[1], self.points[3])
        new = (0, h_w[0])
        x = ((lat_lon[1] - old[0]) * (new[1] - new[0]) / (old[1] - old[0])) + new[0]
        # y must be reversed because the orientation of the image in the matplotlib.
        # image - (0, 0) in upper left corner; coordinate system - (0, 0) in lower left corner
        return int(x), h_w[1] - int(y)

    def get_ticks(self):
        """
        Generates custom ticks based on the GPS coordinates of the map for the matplotlib output.
        :return:
        """
        self.x_ticks = map(
            lambda x: round(x, 4),
            np.linspace(self.points[1], self.points[3], num=7))
        y_ticks = map(
            lambda x: round(x, 4),
            np.linspace(self.points[2], self.points[0], num=8))
        # Ticks must be reversed because the orientation of the image in the matplotlib.
        # image - (0, 0) in upper left corner; coordinate system - (0, 0) in lower left corner
        self.y_ticks = sorted(y_ticks, reverse=True)
