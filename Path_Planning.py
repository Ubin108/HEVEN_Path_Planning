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
import Database

class Path_Planning:  # Mission으로부터 mission number를 받아 그에 맞는 제어에 넘겨줄 list를 반환해줌.
    def __init__(self, mission_number):  # 초기화
        self.db = Database()
        self.combine = Combine(mission_number,self.db)
        self.radius = 5
        self.car_size = [0.5, 1]
        self.__local_target = self.combine.target
        self.__map = self.combine.map
        self.__path = [(0,0,0)]

    def make_path(self):
            m = MapInfo(80, 60)
            vehicle = Car( self.car_size[0], self.car_size[1])
            start = (0,0,np.pi/2)
            end = self.__local_target
            m.start = start
            m.end = end

            m.obstacle = self.combine.update_map
            
            vehicle.set_position(m.start)
            plan = HybridAStar(m.start, m.end, m, vehicle, r=self.radius)
            plan.run(False)
            xs,ys,yaws = plan.reconstruct_path()
            path = []
            
            for cord in zip(xs,ys,yaws):
                path.append(cord)
            
            self.__path = path

    @property
    def path(self):
        return self.__path
     
if __name__ == "__main__":
    Path = Path_Planning(0)
    Path.make_path()
    p = Path.path
