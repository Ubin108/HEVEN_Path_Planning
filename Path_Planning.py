'''
#################### PATH PLAN TEAM ####################

## ABOUT
- target point에 따른 path를 반환해주는 코드.

## INPUT & OUTPUT
- Input: Combine에서 받은 target, map
- Output: 제어에 넘길 Path
'''

from Combine import Combine
from hybrid_astar.hybrid_a_star import HybridAStar
from hybrid_astar.car import Car
from hybrid_astar.mapinfo import MapInfo
import numpy as np
from Database import Database

import matplotlib.pyplot as plt

#세로 35pixel
#가로 37pixel

class Path_Planning:  # Mission으로부터 mission number를 받아 그에 맞는 제어에 넘겨줄 list를 반환해줌.
    def __init__(self, mission_number,db):  # 초기화
        self.db = db
        self.combine = Combine(mission_number,self.db)
        self.radius = 150
        self.car_size = [45, 80]
        self.__local_target = self.combine.target
        self.__map = self.combine.map
        self.__path = [(0,0,0)]

    def make_path(self):
            m = MapInfo(800, 600)
            vehicle = Car(self.car_size[0], self.car_size[1])
            start = (350,50,np.pi/2)
            end = (400,400,np.pi/2)#self.__local_target
            m.start = start
            m.end = end

            m.obstacle = self.combine.update_map()
            
            vehicle.set_position(m.start)
            plan = HybridAStar(m.start, m.end, m, vehicle, r= self.radius, r_step = 50, grid_step=30)

            if plan.run(False):
                xs,ys,yaws = plan.reconstruct_path()
                path = []
                
                plt.scatter(xs,ys)
                plt.show()
                
                gx,gy = float(self.db.gps.data[1]), float(self.db.gps.data[3])
                theta = float(self.db.imu.data[2]) / 180 * np.pi
                
                xs = np.array(xs)
                ys = np.array(ys)

                x = np.cos(theta) * xs - np.sin(theta) * ys + gx
                y = np.sin(theta) * xs + np.cos(theta) * ys + gy
            
                for cord in zip(x,y):
                    path.append(cord)
            
            print(path)
            self.__path = path

    @property
    def path(self):
        return self.__path
     
if __name__ == "__main__":
    #db = Database()
    #db.start()

    Path = Path_Planning(0,1)
    Path.make_path()
    p = Path.path
    #db.path.generate_path = p
    
    plt.plot(p)
    plt.show()

#    db.join()
