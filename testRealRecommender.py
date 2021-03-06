#Beya5od el question wel closest users w yesheel el question men 3and el user w ye7seb el closest neighbors tany
import pandas as pd
import numpy as np
import math
import realRecommender
# import commonQues_wUser
# from commonQues_wUser import *

data = pd.read_csv("example.csv")
problem_data = pd.read_csv("problem_sample.csv")
missing = {'tags':'mcq', 'level_type': 'N'}
problem_data.fillna(value = missing, inplace = True)
#User targetted vars
data = data.sort_values(by=['user_id'])
users = data['user_id'].unique().tolist()

# questions_to_predict = [2283, 542, 2472, 1966, 164, 542, 2472, 1421, 137, 1879, 2382, 1879, 542, 164, 70, 2605, 2472, 2472, 18, 2472, 1421, 2704, 2472, 2084, 81, 2605, 2283, 2472, 2472, 1966, 164, 1705, 1879, 1830, 2472, 542, 137, 1734, 1421, 1047, 542, 1879, 304, 1705, 304, 718, 542, 164, 81, 304, 95, 2472, 2382, 127, 948, 718, 1879, 2472, 1879, 2472, 1887, 2094, 1966, 718, 21, 1177, 137, 304, 1734, 718, 70, 1887, 2472, 718, 2472, 1705, 718, 2059, 1705, 53, 213, 963, 1705, 2472, 718, 2472, 137, 542, 2472, 1481, 53, 1047, 1887, 1734, 542, 1481, 2084, 49, 1966, 542, 2776, 155, 1734, 1966, 1879, 1879, 1705, 2084, 542, 53, 1887, 542, 2472, 757, 1879, 1705, 542, 718, 542, 1734, 304, 1705, 2472, 1734, 542, 2472, 2472, 1734, 1899, 2472, 1421, 137, 542, 542, 137, 2084, 1879, 2605, 2472, 542, 2472, 2472, 2624, 2472, 1510, 199, 2472, 542, 2012, 1705, 1421, 2472, 542, 2085, 583, 2472, 542, 53, 542, 304, 2283, 1742, 1421, 1266, 2472, 988, 2472, 510, 542, 2472, 2077, 2472, 1966, 542, 304, 304, 542, 1421, 2472, 2605, 2472, 53, 304, 1705, 718, 713, 2472, 2472, 2472, 718, 1625, 1421, 542, 137, 137, 1879, 1510, 336, 304, 53, 2385, 53, 304, 1421, 2283, 1887, 53, 590, 747, 2472, 2472, 542, 304, 2472, 1705, 304, 542, 2472, 2776, 2472, 2472, 1966, 137, 2472, 2472, 542, 1421, 2472, 2207, 1625, 963, 1966, 542, 1705, 1887, 1742, 1734, 542, 1421, 2472, 2472, 53, 1705, 1734, 2472, 1625, 1734, 1705, 1879, 81, 2472, 253, 1421, 2084, 1734, 2472, 2472, 542, 542, 1899, 542, 718, 2472, 1879, 70, 542, 81, 542, 2472, 2472, 1734, 164, 2780, 81, 304, 2472, 713, 2710, 53, 2084, 1879, 2472, 2472, 1705, 718, 2472, 1966, 2283, 542, 1734, 1481, 581, 718, 1421, 1421, 1421, 2472, 2084, 2472, 2472, 542, 542, 1879, 1421, 542, 2472, 137, 1879, 542, 1705, 2472, 1879, 611, 304, 1966, 542, 705, 2822, 1705, 1966, 542, 2472, 2472, 2472, 542, 988, 1421, 1482, 1734, 1094, 542, 304, 948, 542, 1705, 988, 211, 713, 1266, 137, 742, 2472, 2472, 718, 542, 542, 2472, 2472, 1481, 21, 581, 2472, 2472, 542, 21, 972, 542, 137, 1966, 1899, 1705, 1879, 1481, 542, 2472, 542, 2776, 70, 2472, 713, 1966, 164, 137, 542, 1549, 2472, 304, 2472, 1705, 542, 53, 137, 1966, 1421, 1966, 718, 1625, 2472, 1887, 850, 1887, 1705, 2472, 2084, 2472, 2472, 2084, 2472, 718, 53, 304, 1734, 304, 211, 581, 2466, 2084, 2315, 713, 605, 1879, 1816, 1421, 1154, 21, 1899, 2084, 713, 137, 1421, 972, 1481, 2472, 688, 1966, 1481, 542, 542, 1421, 2472, 49, 542, 542, 542, 2084, 304, 2472, 2472, 1510, 2472, 2472, 542, 1481, 1421, 2704, 472, 2472, 137, 1421, 246, 304, 81, 1705, 1266, 1899, 542, 542, 542, 2298, 1705, 2472, 2472, 137, 1879, 2472, 2472, 2472, 2059, 1966, 1510, 542, 542, 542, 1705, 70, 542, 1705, 53, 304, 1742, 2084, 542, 2472, 542, 1705, 81, 542, 304, 2472, 53, 542, 1705, 1421, 2472, 1421, 304, 1266, 2321, 1076, 80, 2472, 989, 304, 542, 1734, 1705, 948, 1421, 1510, 1887, 850, 1705, 542, 304, 2472, 2472, 2472, 1966, 963, 2472, 542, 1705, 1481, 53, 1966, 80, 2084, 2472, 137, 1705, 2472, 2472, 1966, 611, 2084, 542, 1879, 1887, 2472, 2472, 1421, 1421, 1705, 1734, 2472, 2472, 81, 53, 542, 1421, 304, 137, 2472, 81, 1421, 2472, 1705, 137, 2312, 2472, 1879, 53, 1899, 2472, 304, 137, 718, 53, 1421, 1966, 1966, 542, 81, 1421, 1481, 304, 542, 2264, 611, 1481, 1879, 1510, 2472, 137, 1734, 2059, 2472, 2472, 542, 2472, 1705, 1421, 2605, 1742, 137, 304, 304, 2472, 542, 2472, 1899, 2472, 718, 1879, 49, 2776, 2605, 80, 53, 304, 1879, 2472, 542, 1966, 2472, 1734, 2472, 2776, 2382, 137, 2472, 1909, 2382, 1966, 2605, 80, 542, 2472, 1421, 2472, 304, 2472, 304, 1705, 1266, 304, 137, 1076, 1879, 1899, 989, 718, 2605, 1421, 1481, 53, 53, 2472, 1481, 542, 583, 137, 1705, 542, 542, 1705, 1510, 2776, 164, 81, 542, 164, 377, 2466, 1510, 2084, 2059, 757, 53, 2472, 1737, 1705, 1879, 21, 2472, 70, 1481, 1966, 1879, 2321, 1734, 2472, 1421, 2084, 2472, 53, 2472, 1966, 137, 1734, 2605, 1705, 611, 1421, 2472, 164, 1705, 963, 542, 1076, 1966, 2472, 2472, 2472, 1510, 963, 2472, 2269, 1966, 2472, 53, 137, 542, 1481, 718, 1966, 304, 1879, 1421, 304, 542, 2472, 2472, 1705, 53, 542, 1705, 1734, 53, 542, 1421, 542, 2552, 1705, 304, 164, 2472, 641, 1879, 1734, 542, 137, 611, 1966, 2207, 1421, 304, 2472, 542, 2472, 1177, 1481, 1510, 1421, 542, 2472, 1510, 2472, 542, 2472, 2472, 304, 2472, 85, 2084, 2472, 2472, 53, 1705, 1421, 2472, 542, 246, 542, 542, 2605, 1734, 1481, 742, 1510, 2472, 2472, 542, 542, 1705, 718, 542, 53, 1879, 1705, 850, 137, 542, 2283, 542, 164, 2472, 2472, 137, 164, 2472, 2472, 1887, 1705, 2472, 1966, 542, 1966, 304, 2283, 304, 70, 2472, 1266, 2059, 1966, 1737, 2472, 2228, 1266, 1966, 53, 137, 542, 137, 2472, 2472, 2472, 53, 2228, 1742, 137, 1421, 2472, 2472, 542, 1705, 2925, 1481, 81, 2472, 1887, 2605, 164, 713, 1421, 1510, 1734, 2472, 1734, 542, 1734, 2472, 85, 304, 1966, 1887, 1705, 2472, 2776, 2472, 1421, 2472, 1879, 246, 542, 2758, 713, 137, 137, 718, 2753, 1510, 542, 164, 2472, 1742, 542, 1266, 53, 1899, 2472, 542, 304, 1705, 1094, 1421, 53, 2472, 1266, 53, 2472, 1966, 757, 2472, 137, 53, 718, 2472, 2472, 542, 1705, 713, 2472, 1481, 1966, 542, 2472, 2472, 713, 1879, 1887, 2472, 542, 1421, 542, 2900, 1887, 246, 2472, 354, 2472, 1705, 2472, 304, 1421, 1421, 2472, 53, 211, 2472, 718, 2472, 2605, 1510, 70, 304, 2084, 2472, 2472, 1421, 963, 963, 1879, 137, 611, 2472, 1887, 2472, 2472, 2472, 1421, 948, 70, 304, 304, 1705, 542, 2776, 1015, 1421, 542, 2472, 114, 1481, 2928, 1421, 70, 1705, 137, 1734, 2084, 304, 2472, 2472, 81, 1510, 2472, 2472, 1899, 542, 2472, 1421, 1374, 271, 53, 963, 137, 2472, 742, 1966, 304, 53, 1482, 1421, 1946, 304, 2472, 189, 2382, 53, 304, 718, 1734, 2472, 2472, 542, 2472, 2366, 317, 542, 542, 2472, 542, 137, 1481, 2472, 2472, 2472, 2472, 53, 1734, 1868, 1899, 2472, 2298, 1879, 1966, 2472, 1705, 542, 542, 2472, 1734, 713, 164, 1879, 713, 80, 1481, 542, 304, 164, 2712, 304, 2605, 2472, 70, 81, 2472, 1421, 85, 2472, 2298, 542, 1899, 542, 2472, 53, 2472, 1266, 1625, 2605, 542, 81, 1879, 2472, 2472, 21, 137, 127, 1421, 542, 1481, 2283, 1705, 1421, 542, 542, 2605, 542, 1421, 2472, 1266, 81, 1705, 590, 542, 542, 1705, 1705, 21, 583, 1481, 1734, 1421, 2315, 1510, 1966, 2472, 1625, 1421, 713, 2298, 611, 2494, 2315, 969, 948, 668, 542, 2171, 542, 164, 1481, 718, 2084, 1482, 713, 1482, 2382, 2472, 542, 542, 1887, 304, 2472, 583, 1879, 2776, 137, 53, 988, 2321, 1887, 2472, 1879, 53, 1705, 1421, 2472, 1076, 542, 1421, 1421, 2472, 1421, 836, 581, 1705, 53, 2283, 2472, 2776, 304, 2472, 164, 53, 137, 2472, 137, 1421, 2472, 1266, 164, 80, 2472, 2605, 1887, 611, 2472, 2472, 83, 2315, 53, 542, 2283, 2084, 1482, 2472, 739, 542, 2321, 542, 542, 583, 1705, 1966, 1734, 713, 542, 1879, 196, 2472, 2472, 1879, 542, 137, 304, 2858, 1421, 542, 1705, 1966, 542, 81, 1076, 2472, 1734, 713, 304, 1705, 211, 713, 21, 611, 2472, 2472, 1879, 2472, 2472, 21, 304, 542, 542, 2472, 304, 2472, 2472, 1481, 304, 21, 1705, 1705, 542, 989, 1421, 542, 164, 1887, 1094, 864, 718, 1705, 2472, 53, 718, 1421, 53, 85, 137, 542, 542, 542, 1705, 542, 2605, 1421, 81, 2472, 304, 1816, 81, 2472, 718, 2472, 53, 2472, 2472, 2472, 1266, 53, 304, 137, 1481, 137, 1421, 2472, 1705, 1966, 542, 127, 81, 164, 1899, 21, 1966, 1421, 542, 2605, 304, 1481, 1705, 1421, 2283, 1266, 972, 542, 1421, 1879, 2472, 1510, 542, 304, 1966, 1705, 542, 2472, 1510, 2605, 1421, 53, 542, 542, 1734, 164, 1421, 2472, 2472, 1966, 2472, 542, 542, 542, 2472, 1705, 542, 718, 542, 542, 718, 2114, 1966, 1734, 1966, 2283, 2472, 2472, 2472, 1742, 1266, 1510, 542, 2472, 53, 137, 1800, 718, 542, 1705, 304, 21, 2472, 1767, 1887, 1705, 1705, 2472, 304, 2472, 164, 2472, 2472, 137, 2472, 1966, 1887, 583, 53, 542, 2472, 2472, 2472, 542, 137, 1966, 718, 611, 2472, 164, 1879, 2472, 718, 1966, 611, 304, 2472, 137, 164, 1421, 2472, 1705, 137, 1742, 2059, 734, 304, 542, 1879, 1966, 2472, 1481, 1742, 1705, 542, 2472, 718, 1705, 2472, 1705, 21, 1266, 2758, 137, 1734, 2472, 1734, 304, 2472, 137, 2472, 2472, 2472, 81, 137, 1421, 1457, 137, 53, 53, 1421, 2472, 542, 718, 2472, 1421, 53, 542, 21, 1879, 702, 2776, 742, 1879, 2472, 1705, 137, 1879, 1421, 1705, 137, 1966, 1266, 2472, 1705, 1966, 1705, 1887, 1421, 2605, 542, 304, 304, 542, 542, 2472, 1734, 1705, 542, 1887, 137, 304, 718, 1705, 1481, 53, 2946, 2094, 542, 1705, 2264, 2776, 1734, 1421, 1421, 581, 2472, 53, 2084, 1879, 542, 611, 137, 1421, 1734, 542, 542, 718, 2472, 1421, 542, 2472, 1966, 2269, 718, 53, 1510, 81, 1734, 2472, 137, 1879, 304, 542, 2472, 53, 2472, 2472, 542, 53, 2929, 81, 2084, 742, 2472, 1915, 1887, 1510, 80, 2472, 2084, 542, 2059, 137, 1510, 2472, 1899, 2776, 1266, 304, 53, 1421, 211, 1966, 1421, 137, 2321, 81, 388, 542, 1879, 542, 164, 1705, 718, 1421, 718, 757, 2472, 2472, 963, 164, 2472, 2758, 1879, 611, 713, 542, 53, 81, 304, 1734, 304, 1481, 53, 2321, 542, 1966, 2472, 1705, 1266, 988, 2472, 246, 542, 2472, 1421, 2269, 127, 1421, 1481, 718, 1887, 2472, 2466, 304, 542, 1510, 2472, 85, 2472, 1824, 2472, 304, 542, 2269, 2472, 2472, 2472, 542, 542, 611, 718, 1481, 2472, 1421, 542, 21, 2762, 1510, 1421, 2776, 137, 1421, 600, 1966, 2472, 988, 1734, 137, 2472, 1481, 542, 1481, 1734, 963, 1481, 1899, 1625, 1966, 718, 1266, 542, 542, 542, 1966, 21, 542, 137, 2472, 1966, 304, 304, 2472, 304, 137, 2472, 1899, 1421, 1481, 718, 1705, 304, 2605, 2283, 1481, 164, 2472, 53, 1966, 2472, 1421, 2472, 81, 757, 53, 1742, 1879, 2776, 1481, 2472, 81, 1470, 542, 2472, 211, 1481, 1481, 542, 81, 1421, 304, 81, 1705, 2472, 48, 137, 81, 1879, 1665, 1421, 2472, 1510, 1421, 1421, 1481, 2179, 988, 304, 2472, 1705, 164, 304, 2283, 2472, 2084, 2472, 2472, 2472, 1966, 1705, 2869, 2472, 2472, 2472, 2542, 2472, 2776, 1421, 542, 542, 542, 718, 542, 1966, 1879, 542, 1421, 2472, 74, 1861, 304, 1421, 1705, 49, 2283, 1015, 1510, 2472, 2472, 542, 199, 1705, 542, 2472, 1625, 2472, 2472, 2472, 542, 1705, 304, 2472, 2472, 164, 361, 2472, 1421, 1705, 2900, 1879, 1705, 2472, 542, 1421, 304, 542, 542, 2472, 2472, 1966, 137, 1421, 2472, 2605, 81, 718, 1421, 1421, 1966, 542, 1421, 1734, 2472, 70, 1879, 53, 53, 81, 542, 1625, 1421, 1734, 2472, 137, 1705, 1966, 1705, 2472, 53, 1266, 53, 2605, 757, 81, 2472, 304, 1625, 542, 53, 2084, 53, 542, 137, 53, 2472, 542, 2472, 542, 718, 1705, 137, 1879, 1421, 1879, 542, 2472, 1899, 211, 2094, 1705, 1421, 2472, 1705, 2472, 1966, 2472, 1705, 2605, 1066, 2472, 2472, 2472, 1481, 2472, 1879, 1266, 1705, 2472, 2472, 2059, 2472, 304, 137, 1266, 542, 581, 1879, 542, 542, 2472, 137, 1481, 1421, 583, 211, 1887, 2472, 2472, 542, 137, 304, 2472, 581, 304, 2605, 53, 304, 2472, 2472, 137, 1421, 718, 542, 70, 1734, 542, 2472, 2228, 542, 2704, 21, 2925, 2472, 2472, 542, 1879, 542, 2605, 304, 542, 137, 164, 542, 2552, 1705, 1966, 2472, 53, 2472, 713, 2472, 713, 1421, 1705, 2472, 1705, 581, 2776, 1421, 2472, 246, 1705, 1734, 137, 2472, 542, 542, 1705, 1481, 1421, 2472, 2472, 2321, 137, 21, 304, 2472, 1879, 2472, 2472, 2472, 542, 1887, 1705, 137, 1421, 2472, 351, 718, 713, 1705, 2472, 668, 1266, 1899, 542, 542, 137, 2472, 2605, 421, 542, 1705, 2472, 2472, 1887, 542, 542, 2472, 21, 1705, 53, 2321, 1734, 2472, 1879, 718, 1705, 1625, 421, 1899, 2472, 2472, 1705, 53, 542, 1421, 542, 1705, 2472, 1705, 542, 1625, 304, 53, 1879, 1481, 2084, 2946, 542, 1966, 2084, 2472, 304, 1421, 21, 2472, 137, 757, 1705, 1734, 2283, 2472, 2472, 137, 137, 2472, 2605, 1879, 1625, 53, 1625, 1266, 53, 718, 542, 53, 1879, 304, 292, 2472, 742, 1705, 1734, 1705, 1879, 2472, 542, 1771, 2472, 1734, 1892, 542, 1421, 1879, 1966, 542, 304, 53, 718, 718, 21, 1879, 1705, 718, 164, 2472, 70, 1421, 542, 2472, 1879, 542, 1879, 1742, 2472, 2472, 1705, 304, 2472, 1879, 505, 718, 1421, 713, 1879, 2228, 2776, 2776, 1625, 611, 542, 137, 542, 2928, 1734, 542, 2762, 542, 53, 2084, 542, 1879, 542, 304, 581, 1879, 542, 1705, 1705, 1966, 2472, 2472, 542, 542, 542, 542, 304, 2472, 1734, 2472, 1705, 2472, 1734, 2472, 2472, 1482, 137, 1742, 81, 581, 583, 114, 317, 2472, 2472, 2472, 1510, 2472, 1966, 713, 542, 1481, 2283, 2472,70, 1879, 1879, 1705, 2605, 542, 718, 542]
# old_questions = [1358, 133, 713, 2142, 1397, 699, 2663, 2284, 1716, 2946, 1767, 2083, 1311, 1740, 0, 190, 713, 713, 2472, 2340, 1154, 1149, 713, 2171, 1592, 783, 304, 2340, 322, 2721, 740, 164, 2946, 196, 2605, 1311, 1304, 668, 1767, 2121, 2264, 81, 1891, 2602, 484, 2171, 1311, 2264, 522, 2398, 0, 2171, 2199, 334, 388, 2472, 1675, 1636, 1675, 2710, 2171, 2152, 2721, 2472, 0, 2272, 1716, 1372, 783, 842, 0, 1976, 322, 2171, 713, 164, 2472, 137, 887, 1771, 0, 740, 668, 1550, 2360, 246, 1000, 1699, 2218, 740, 1812, 1457, 2991, 1592, 887, 668, 2171, 0, 1868, 740, 842, 0, 1537, 1625, 1675, 2946, 1625, 1899, 887, 964, 1902, 1086, 2710, 2776, 53, 2903, 1537, 1577, 1482, 2052, 18, 164, 2605, 740, 2284, 713, 713, 2949, 2171, 2605, 2777, 522, 2264, 32, 334, 2171, 2946, 2824, 713, 887, 254, 713, 0, 713, 190, 2754, 1550, 2747, 0, 1152, 2777, 757, 307, 0, 612, 2605, 887, 1421, 1811, 281, 0, 510, 1767, 1421, 2605, 164, 2605, 574, 1675, 2605, 0, 1051, 1625, 2090, 1930, 2086, 740, 211, 254, 1675, 713, 1154, 862, 668, 2472, 246, 1334, 2171, 713, 2472, 2491, 2454, 2403, 1621, 1688, 1675, 190, 0, 1851, 821, 0, 0, 524, 2284, 2080, 2174, 2957, 1051, 0, 2710, 713, 2022, 524, 361, 101, 1551, 740, 713, 2472, 254, 757, 1559, 2804, 713, 2605, 1675, 972, 2977, 1555, 821, 742, 2721, 1533, 887, 2374, 1460, 668, 1583, 918, 2605, 713, 583, 1625, 668, 2605, 164, 668, 887, 1675, 1592, 2605, 774, 2284, 2773, 668, 713, 1051, 887, 1482, 336, 1675, 2472, 246, 1675, 0, 1273, 522, 114, 1051, 620, 812, 902, 1318, 1592, 2049, 713, 2171, 713, 583, 2171, 1675, 2605, 2605, 1625, 0, 713, 2654, 304, 1311, 1689, 2605, 1543, 1043, 1899, 2284, 2284, 2084, 1899, 1636, 2605, 1311, 1460, 1942, 972, 2090, 2171, 1827, 81, 887, 164, 590, 1094, 2121, 920, 1868, 114, 164, 1397, 887, 1559, 1311, 246, 879, 2605, 1311, 668, 53, 1942, 783, 1675, 1675, 2321, 1830, 32, 1170, 668, 1183, 2171, 53, 318, 1698, 1577, 1357, 2472, 887, 2264, 1577, 1914, 668, 0, 2957, 713, 2340, 32, 0, 1154, 1311, 127, 2142, 2171, 887, 1675, 703, 1675, 2171, 1675, 842, 0, 2340, 2171, 1716, 1311, 2721, 1675, 1974, 879, 758, 2605, 1152, 1273, 583, 1304, 421, 2284, 1625, 842, 887, 1636, 2171, 1076, 2640, 1170, 757, 2663, 1561, 2340, 1899, 2710, 2472, 1583, 1676, 1689, 1358, 1183, 2389, 2754, 243, 739, 1561, 1675, 1942, 0, 2284, 626, 0, 2084, 1899, 1051, 522, 1655, 1154, 668, 713, 0, 1625, 2920, 1675, 2747, 1154, 713, 0, 1460, 1311, 32, 2171, 862, 2605, 1550, 2777, 361, 1914, 1311, 703, 1975, 0, 713, 718, 334, 2284, 2171, 524, 1675, 1625, 1066, 1183, 1218, 2939, 2022, 542, 887, 1561, 713, 1026, 81, 713, 713, 2340, 916, 1868, 574, 1273, 887, 1675, 1740, 0, 887, 1625, 1968, 281, 963, 2218, 2022, 1334, 1482, 1170, 2594, 114, 2449, 2403, 740, 1311, 1625, 2221, 246, 211, 31, 1066, 1837, 2240, 0, 2125, 2156, 1487, 2264, 1689, 1625, 718, 1154, 583, 2994, 69, 1710, 32, 281, 322, 2710, 718, 1559, 1218, 1383, 32, 1170, 703, 1172, 1625, 0, 1899, 2710, 2791, 668, 2605, 2605, 2721, 1311, 1899, 1273, 2946, 2994, 713, 2718, 972, 211, 164, 522, 842, 713, 812, 1734, 2264, 2284, 524, 127, 713, 522, 845, 1051, 1625, 318, 0, 1550, 1675, 2583, 254, 1636, 862, 1716, 2472, 1421, 2153, 1625, 1625, 1675, 522, 972, 740, 862, 32, 1675, 988, 2605, 1675, 190, 1561, 95, 740, 2132, 2605, 1334, 114, 2605, 1170, 761, 1689, 1311, 1298, 1487, 862, 1281, 32, 246, 254, 246, 2171, 2946, 0, 842, 2630, 0, 334, 747, 1493, 1334, 740, 2491, 1561, 697, 713, 842, 0, 522, 255, 2334, 655, 1559, 190, 0, 1482, 2718, 1273, 713, 1358, 2605, 862, 164, 1421, 281, 2791, 2240, 1675, 869, 0, 2472, 612, 972, 2605, 190, 583, 2605, 668, 1675, 1510, 1868, 1170, 740, 32, 164, 2228, 2472, 1625, 1592, 1218, 1625, 0, 0, 2848, 2171, 137, 62, 2221, 2605, 148, 164, 81, 0, 246, 0, 2605, 1559, 1675, 952, 2068, 713, 88, 2171, 2605, 740, 2171, 1625, 29, 783, 1428, 164, 2936, 972, 713, 1922, 2048, 1742, 1218, 1151, 1625, 2546, 2605, 246, 1776, 1772, 2340, 1311, 1625, 2340, 581, 2920, 1543, 1140, 842, 1625, 2321, 1675, 23, 281, 2022, 2605, 1334, 164, 190, 937, 164, 2052, 334, 2022, 1273, 699, 0, 1152, 895, 1811, 1550, 0, 2946, 2343, 1547, 334, 988, 1625, 2712, 23, 788, 842, 740, 2340, 2494, 1516, 190, 972, 1675, 2605, 190, 2100, 1482, 1636, 713, 2321, 675, 0, 2773, 2340, 1051, 1675, 887, 1273, 713, 114, 1095, 1311, 2022, 612, 2471, 2272, 779, 944, 713, 713, 2022, 1228, 1152, 2977, 2264, 1861, 2946, 668, 1076, 121, 1675, 304, 1311, 1247, 2605, 1550, 127, 332, 2340, 2171, 2528, 164, 2605, 1792, 1218, 1625, 2321, 304, 1487, 0, 2605, 1899, 2685, 1625, 1272, 897, 2121, 617, 1625, 2691, 1621, 740, 2791, 713, 1561, 713, 821, 1510, 1311, 1019, 2284, 2206, 713, 2284, 1710, 0, 1689, 1592, 713, 2059, 612, 1955, 1051, 740, 190, 1689, 246, 668, 1482, 668, 2605, 0, 1891, 937, 1421, 1170, 713, 2472, 2693, 2284, 2171, 81, 1929, 1560, 1457, 2171, 1688, 1000, 757, 0, 1311, 1675, 1705, 1334, 2948, 1482, 1279, 2957, 2403, 2605, 2240, 2321, 1710, 1675, 972, 2957, 246, 53, 740, 1550, 1625, 842, 713, 703, 2240, 757, 1550, 1051, 2939, 1170, 2817, 2605, 703, 2142, 142, 2605, 713, 1051, 1675, 510, 1383, 2421, 2284, 2463, 611, 2630, 1095, 713, 2111, 2218, 668, 713, 1851, 1154, 740, 12, 190, 2298, 2605, 2663, 2605, 1154, 190, 0, 811, 2171, 246, 2171, 1154, 29, 2847, 1270, 1716, 988, 2171, 71, 246, 322, 1636, 972, 2298, 0, 2321, 281, 887, 2849, 2472, 0, 2284, 1273, 2605, 0, 164, 0, 972, 0, 1170, 1298, 740, 2385, 2321, 1636, 1051, 812, 574, 713, 713, 2171, 1675, 713, 821, 0, 0, 1929, 740, 127, 2605, 1698, 522, 2938, 1580, 334, 88, 2665, 281, 322, 0, 964, 740, 1280, 2977, 2699, 1550, 879, 1181, 246, 0, 0, 2240, 887, 713, 114, 1621, 740, 879, 2503, 62, 62, 1270, 1167, 1625, 675, 2605, 2979, 53, 2142, 70, 1170, 32, 1273, 2171, 2605, 254, 32, 1675, 757, 0, 2605, 779, 2664, 1043, 2776, 1891, 1675, 2605, 0, 1879, 1051, 2284, 0, 2100, 902, 1482, 2171, 2284, 713, 1812, 2605, 2374, 2565, 190, 32, 2501, 1675, 2605, 2206, 0, 2791, 338, 2284, 1675, 668, 0, 1625, 2218, 1460, 307, 1675, 740, 2174, 2100, 2497, 1592, 1170, 2472, 1311, 1311, 668, 1710, 0, 2052, 627, 1689, 2374, 0, 1776, 2142, 2125, 777, 688, 1051, 1695, 1311, 1047, 739, 0, 1887, 1625, 1836, 0, 2284, 32, 1516, 2472, 842, 1675, 2171, 1580, 1128, 2605, 1311, 1482, 1254, 1891, 2403, 1510, 1675, 2472, 703, 583, 668, 2863, 2783, 2605, 81, 334, 668, 1154, 2710, 148, 729, 211, 2171, 2693, 1887, 0, 390, 2903, 2686, 1358, 713, 2403, 1851, 2171, 32, 211, 1716, 2605, 2920, 2171, 2084, 1421, 887, 0, 2084, 190, 2305, 1705, 2171, 2605, 1160, 1006, 1734, 1311, 1358, 2171, 1273, 2776, 0, 699, 2477, 1482, 1675, 1311, 1625, 1625, 668, 1550, 32, 1675, 2214, 2693, 1199, 53, 740, 121, 1891, 647, 740, 2022, 164, 1868, 1383, 522, 148, 246, 522, 2403, 1891, 1625, 1421, 2340, 0, 1705, 1084, 2776, 1675, 1636, 713, 0, 1833, 740, 1675, 2605, 1891, 713, 2340, 1516, 2748, 0, 668, 1152, 2022, 0, 2454, 1675, 1311, 2497, 81, 0, 2472, 887, 713, 740, 2171, 2284, 2630, 0, 127, 114, 1482, 2264, 164, 1218, 51, 2630, 812, 713, 281, 0, 1537, 713, 1877, 713, 2686, 254, 713, 713, 2374, 1421, 1889, 2791, 2920, 1537, 2153, 322, 1625, 1625, 887, 1537, 1537, 1170, 2218, 0, 2142, 1459, 887, 190, 1280, 2605, 164, 1846, 304, 1421, 1273, 1675, 2284, 1675, 713, 190, 1311, 1635, 1559, 668, 2747, 1051, 361, 244, 972, 2957, 1482, 1675, 1689, 1710, 2284, 2710, 1322, 2142, 2909, 1311, 2240, 2090, 713, 1170, 32, 757, 2240, 2463, 2472, 0, 1625, 2605, 2142, 304, 713, 246, 2605, 779, 53, 2848, 1311, 2605, 972, 334, 0, 1877, 1675, 1170, 1891, 0, 1051, 390, 1254, 887, 164, 2605, 436, 2605, 1705, 2605, 2710, 2334, 2340, 2142, 2305, 1510, 334, 887, 2710, 2084, 246, 32, 1868, 1625, 2472, 2936, 2605, 1705, 1675, 2693, 2171, 1625, 1181, 862, 2605, 1621, 1894, 972, 2977, 2501, 334, 779, 2754, 668, 2938, 2022, 81, 1625, 2693, 334, 963, 668, 1311, 675, 842, 1170, 156, 164, 0, 779, 1397, 334, 668, 246, 1710, 1891, 246, 2756, 246, 2605, 2605, 1592, 127, 1154, 0, 2872, 1675, 583, 2284, 2605, 1482, 2403, 1051, 88, 1846, 2264, 0, 1094, 0, 2663, 1218, 1675, 879, 887, 1304, 1675, 1740, 1625, 114, 1625, 779, 1550, 1170, 1625, 887, 2374, 972, 1428, 887, 895, 2321, 1311, 740, 1550, 1236, 1710, 887, 2059, 2110, 2321, 1877, 164, 334, 1272, 1675, 1592, 114, 101, 2939, 842, 74, 2777, 2284, 1390, 2605, 1812, 1899, 1675, 2264, 0, 1621, 2374, 2949, 2939, 2460, 2171, 713, 2284, 1675, 2605, 1625, 1460, 2171, 2583, 574, 1094, 668, 713, 522, 1675, 533, 2022, 2340, 0, 2605, 2605, 2443, 583, 0, 1675, 2663, 779, 62, 0, 2374, 190, 1362, 713, 842, 1311, 211, 2756, 2777, 1929, 2171, 2472, 53, 1425, 190, 2153, 1183, 1625, 2284, 1621, 2863, 2501, 0, 1675, 1675, 1218, 2090, 2501, 2472, 972, 2472, 246, 2605, 713, 740, 1152, 1561, 1397, 1256, 2121, 1051, 32, 452, 1592, 705, 668, 1425, 2920, 583, 207, 2264, 1625, 2605, 668, 617, 668, 1051, 1095, 1181, 2605, 2284, 1975, 2499, 1663, 668, 1577, 2528, 1051, 534, 2969, 1273, 2848, 713, 0, 1334, 0, 2340, 2321, 1273, 963, 246, 2605, 246, 32, 740, 1579, 2171, 2334, 2403, 2100, 1675, 0, 2654, 190, 1266, 2472, 1716, 2740, 0, 2142, 2605, 668, 2052, 95, 2693, 2920, 114, 334, 668, 1218, 2920, 2403, 821, 1625, 757, 2374, 1218, 2180, 32, 1625, 0, 887, 334, 2605, 937, 895, 2321, 246, 2321, 717, 2171, 2773, 2777, 668, 1877, 164, 2321, 1710, 304, 740, 1181, 1636, 1272, 1559, 246, 211, 713, 812, 246, 2421, 601, 1675, 253, 332, 2171, 1592, 0, 887, 2909, 1154, 668, 668, 1311, 2501, 2762, 1891, 1879, 164, 1561, 0, 334, 2501, 1094, 0, 1273, 2718, 574, 2284, 2284, 668, 0, 668, 895, 713, 887, 887, 2988, 304, 2605, 1899, 254, 2340, 1550, 840, 516, 0, 675, 2745, 2605, 0, 1561, 2453, 2777, 2312, 740, 32, 842, 1311, 1625, 2946, 740, 2777, 2100, 0, 0, 1891, 655, 668, 0, 304, 0, 190, 1636, 2605, 779, 0, 887, 114, 2605, 777, 713, 713, 2605, 1460, 164, 2321, 2605, 2605, 1955, 0, 713, 740, 668, 133, 1942, 887, 675, 1311, 630, 2748, 887, 1675, 2605, 1275, 2142, 127, 1655, 713, 190, 1384, 2472, 1154, 1154, 1625, 1311, 1471, 668, 713, 0, 81, 1583, 1846, 1592, 1482, 2654, 1390, 668, 62, 1019, 1170, 2491, 2903, 2605, 756, 2472, 972, 81, 2171, 1675, 842, 2321, 1311, 1311, 1812, 842, 190, 32, 2602, 740, 2340, 114, 2605, 1311, 2472, 164, 522, 1675, 2630, 2686, 32, 2693, 1183, 694, 1675, 2501, 740, 713, 1625, 1550, 2654, 2605, 1170, 2295, 0, 879, 246, 1636, 2920, 254, 1675, 53, 1625, 2605, 246, 137, 2340, 862, 334, 617, 2022, 1390, 1580, 1218, 32, 2340, 234, 2499, 972, 1510, 53, 2640, 897, 1636, 172, 2920, 2854, 713, 1390, 2321, 190, 2163, 2321, 675, 713, 703, 23, 2171, 2264, 0, 668, 1537, 2340, 2121, 2939, 1861, 0, 0, 2605, 713, 1311, 1675, 740, 1675, 1591, 1460, 1298, 32, 1086, 0, 887, 1625, 2718, 2528, 1561, 2100, 713, 246, 2454, 164, 246, 887, 2957, 842, 53, 246, 1095, 1625, 612, 2920, 713, 32, 1311, 164, 783, 1154, 713, 713, 2509, 703, 0, 281, 70, 1675, 2340, 2605, 2605, 1311, 1942, 1338, 127, 1154, 713, 1311, 1043, 1561, 1660, 2171, 164, 53, 254, 1699, 2460, 1621, 2605, 1675, 53, 114, 668, 2605, 2340, 71, 1675, 1482, 1550, 0, 157, 334, 498, 1689, 1128, 1675, 1877, 887, 1181, 211, 879, 2340, 879, 1710, 1734, 114, 2640, 1942, 1152, 675, 668, 1273, 1705, 281, 791, 1675, 703, 2171, 583, 887, 1868, 2171, 713, 2682, 88, 0, 1636, 2791, 1550, 887, 2605, 1197, 2340, 713, 1896, 334, 2605, 1675, 1675, 777, 779, 777, 2704, 1543, 757, 114, 740, 2946, 1358, 2042, 713, 740, 1625, 783, 164, 1942, 2605, 887, 0, 2605, 1689, 0, 32, 1154, 1675, 1868, 1922, 2854, 2496, 2171, 2472, 0, 1675, 887, 2472, 1625, 2340, 0, 1942, 1095, 1051, 1942, 1460, 81, 1619, 1051, 1636, 1625, 2321, 713, 870, 0, 2472, 53, 1051, 1675, 1510, 842, 2472, 1955, 1311, 1460, 1397, 1218, 0, 1592, 887, 821, 2284, 1272, 2403, 1311, 1675, 740, 2321, 684, 2934, 1482, 1625, 887, 1625, 2605, 2605, 887, 114, 1218, 1675, 2321, 713, 1714, 2340, 1170, 2605, 164, 2171, 713, 334, 318, 1311, 2501, 43, 190, 1675, 0, 2663, 2605, 713, 1640, 246, 1625, 2693, 1675, 783, 304, 2340, 0, 1675, 53, 164, 1154, 114, 2171, 1273]
questions_to_predict = realRecommender.problemsToPredict
old_questions = realRecommender.previousProblems
non_existing_users = 0
no_similarity_users = 0
close_to_real = 0
far_from_real = 0
del data['Unnamed: 0']
print(data)
x = 0
while x < len(users):

	if old_questions[x] == 0:
		no_similarity_users = no_similarity_users + 1
		x = x + 1
		continue
	problems_of_first_user = []
	common_rating_first_user = 0
	sum_for_first_user_mean = 0
	changed = False
	current_user = users[x]
	index_for_first_user = data.index[data['user_id'] == current_user] 
	user1_table = data.loc[index_for_first_user]
	if user1_table.empty == True:
		continue
	user1_table_size = user1_table.size//4 # .........................

	#equation & similarity vars
	sum1_for_pearson = 0 
	sum2_for_pearson = 0
	sum3_for_pearson = 0
	similarity = 0
	target_question = questions_to_predict[x]
	
	#NN vars
	found_question = False
	closest_seventeen = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	closest_seventeen_ids = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	second_mean_count = 0 
	second_user_mean = 0
	second_mean_flag = False
	occurrence = 0 #represents the num of users who have a problem in common
	solvedBy = []
	solvedBy_similarity = []
	solvedBy_ratings = []
	i = 0

	for index, row in data.iterrows(): #To get the mean of the 1st user and the problems he/she solved
	    if row['user_id'] == current_user and changed == False and row['status'] == 'Accepted' :
	    	changed = True
	    	sum_for_first_user_mean = sum_for_first_user_mean + row['attempts_range']
	    	i = i + 1
	    	problems_of_first_user.append(row['problem_id'])
	    elif row['user_id'] == current_user and changed == True and row['status'] == 'Accepted' : 
	    	sum_for_first_user_mean = sum_for_first_user_mean + row['attempts_range']
	    	i = i + 1
	    	problems_of_first_user.append(row['problem_id'])
	    elif row['user_id'] > current_user:
	    	break
	mean_of_first_user = sum_for_first_user_mean/i
	second_user = 0
	i = 0
	j = 0
	print(users[x])
	count_till_end_of_user = 0 #Skipping every row of the user 
	first_time = False #3shan law 5allas 2, ye7seb 3and 3 awel marra bas
	question_exists = False
	for index, row in data.iterrows():
		
		if current_user == 1 and row['user_id'] == 1:
			continue
		if row['user_id'] == current_user and first_time == True and count_till_end_of_user < user1_table_size:
			second_mean_flag = False
			count_till_end_of_user = count_till_end_of_user + 1
			if count_till_end_of_user == user1_table_size - 1:
				first_time = False
			continue
		if row['user_id'] > second_user and second_mean_flag == False: #For when the 2nd user appears for the 1st time
			second_user = row['user_id']
			index_for_sec_user = data.index[data['user_id'] == row['user_id']] 
			temp_user = data.loc[index_for_sec_user] #Getting a sub dataset for the 2nd user
			for index2, row2 in temp_user.iterrows(): #Calculating the sum 
				if row2['problem_id'] == target_question:
					question_exists = True
				if row2['status'] == 'Accepted':
					second_mean_count = second_mean_count + row2['attempts_range']
				j = j + 1
			second_user_mean = second_mean_count/j
			j = 0
			second_mean_flag = True
			if row['problem_id'] in problems_of_first_user and question_exists == True and row['status'] == 'Accepted':
				index_for_first_user_prob = data.index[data['user_id'] == current_user]
				temp_user = data.loc[index_for_first_user_prob]
				real_index = temp_user.index[temp_user['problem_id'] == row['problem_id']]
				real_temp = temp_user.loc[real_index]
				for index2, row2 in real_temp.iterrows():
					common_rating_first_user = row2['attempts_range']
				sum1_for_pearson = sum1_for_pearson + ((common_rating_first_user - mean_of_first_user) * (row['attempts_range'] - second_user_mean))
				sum2_for_pearson = sum2_for_pearson + (common_rating_first_user - mean_of_first_user)**2
				sum3_for_pearson = sum3_for_pearson + (row['attempts_range'] - second_user_mean)**2

		elif row['user_id'] == second_user and second_mean_flag == True and question_exists == True and row['status'] == 'Accepted': #If the following entry is the same user
			second_user = row['user_id']
			if row['problem_id'] in problems_of_first_user:
				index_for_first_user_prob = data.index[data['user_id'] == current_user]
				temp_user = data.loc[index_for_first_user_prob]
				real_index = temp_user.index[temp_user['problem_id'] == row['problem_id']]
				real_temp = temp_user.loc[real_index]
				for index2, row2 in real_temp.iterrows():
					index = real_temp.index[real_temp['problem_id'] == row['problem_id']].tolist()
					common_rating_first_user = real_temp.at[index[0],'attempts_range']
				sum1_for_pearson = sum1_for_pearson + ((common_rating_first_user - mean_of_first_user) * (row['attempts_range'] - second_user_mean))
				sum2_for_pearson = sum2_for_pearson + (common_rating_first_user - mean_of_first_user)**2
				sum3_for_pearson = sum3_for_pearson + (row['attempts_range'] - second_user_mean)**2

		elif row['user_id'] > second_user and second_mean_flag == True and first_time == False : #When the 2nd user changes
			second_mean_flag = False	
			similarity_check = math.sqrt(sum2_for_pearson)*math.sqrt(sum3_for_pearson)
			if(similarity_check != 0):
				similarity = sum1_for_pearson/(math.sqrt(sum2_for_pearson) * math.sqrt(sum3_for_pearson))
			else:
				similarity = 0
			smallest = 100.0
			for num in closest_seventeen:
				if num < smallest:
					smallest = num		
			
			k = closest_seventeen.index(smallest)
			if  similarity > 0.49 and similarity > smallest:
				closest_seventeen[k] = similarity
				closest_seventeen_ids[k] = second_user
				
			question_exists = False
			sum1_for_pearson = 0
			sum2_for_pearson = 0
			sum3_for_pearson = 0
			second_mean_count = 0
			second_user_mean = 0
			j = 0
			second_user = row['user_id']
			index_for_sec_user = data.index[data['user_id'] == row['user_id']]
			temp_user = data.loc[index_for_sec_user]
			if row['user_id'] == current_user:
				first_time = True
			else:
				for index2, row2 in temp_user.iterrows():
					if row2['problem_id'] == target_question:
						question_exists = True
					if row2['status'] == 'Accepted':
						second_mean_count = second_mean_count + row2['attempts_range']
					j = j + 1
				second_mean_flag = True
				second_user_mean = second_mean_count/j
				j = 0
				if row['problem_id'] in problems_of_first_user and question_exists == True and row['status'] == 'Accepted':
					index_for_first_user_prob = data.index[data['user_id'] == current_user]
					temp_user = data.loc[index_for_first_user_prob]
					real_index = temp_user.index[temp_user['problem_id'] == row['problem_id']]
					real_temp = temp_user.loc[real_index]
					for row2, index2 in real_temp.iterrows():
						index = real_temp.index[real_temp['problem_id'] == row['problem_id']].tolist()
						common_rating_first_user = real_temp.at[index[0],'attempts_range']
					sum1_for_pearson = sum1_for_pearson + ((common_rating_first_user - mean_of_first_user) * (row['attempts_range'] - second_user_mean))
					sum2_for_pearson = sum2_for_pearson + (common_rating_first_user - mean_of_first_user)**2
					sum3_for_pearson = sum3_for_pearson + (row['attempts_range'] - second_user_mean)**2

	current_problem = 0
	l = 0
	numerator = 0
	denomenator = 0
	if closest_seventeen[0] == 0:
		no_similarity_users = no_similarity_users + 1
		x = x + 1
		continue

	for eachOne in closest_seventeen:
		if eachOne == 0 or eachOne == 0.0:
			break
		index = data.index[data['user_id'] == closest_seventeen_ids[l]]
		temp_user = data.loc[index]
		real_index = temp_user.index[temp_user['problem_id'] == target_question]
		real_temp = temp_user.loc[real_index]
		for i, r in real_temp.iterrows():
			val = float(r['attempts_range'])
			# print(eachOne)
			numerator = numerator + (eachOne*val)
		denomenator = denomenator + eachOne

	prediction_test = mean_of_first_user + (numerator/denomenator)
	if math.isnan(prediction_test) == True:
		print("1")
		x = x + 1
		continue

	prediction_test = round(prediction_test)
	index_to_check = data.index[data['user_id'] == x + 1]
	temp_user = data.loc[index_to_check]
	index_for_question = temp_user.index[temp_user['problem_id'] == old_questions[x]]
	row_of_question = temp_user.loc[index_for_question]
	difficulty_index_for_question2 = problem_data.index[problem_data['problem_id'] == questions_to_predict[x]]
	difficulty_row_of_question2 = problem_data.loc[difficulty_index_for_question2]
	difficulty_index_for_question1 = problem_data.index[problem_data['problem_id'] == old_questions[x]]
	difficulty_row_of_question1 = problem_data.loc[difficulty_index_for_question1]
	for i, r in difficulty_row_of_question1.iterrows():
		difficulty1 = r['level_type']
	for i, r in difficulty_row_of_question2.iterrows():
		difficulty2 = r['level_type']
	for i, r in real_temp.iterrows():
		real_value = r['attempts_range']
	if old_questions[x] != 0:
		if ord(difficulty1) < ord(difficulty2): #Ely a5ado as-hal
			difference = prediction_test - real_value
			if difference >= 0:
				close_to_real = close_to_real + 1
				data = data.append({'user_id' : users[x] , 'problem_id' : questions_to_predict[x], 'attempts_range': prediction_test,'status':'Accepted'}, ignore_index=True)
			else:
				far_from_real = far_from_real + 1
				data = data.append({'user_id' : users[x] , 'problem_id' : questions_to_predict[x], 'attempts_range': prediction_test,'status':'Rejected'}, ignore_index=True)
		elif ord(difficulty1) > ord(difficulty2):
			difference = prediction_test - real_value
			if difference <= 0:
				close_to_real = close_to_real + 1
				data = data.append({'user_id' : users[x] , 'problem_id' : questions_to_predict[x], 'attempts_range': prediction_test,'status':'Accepted'}, ignore_index=True)
			else:
				far_from_real = far_from_real + 1
				data = data.append({'user_id' : users[x] , 'problem_id' : questions_to_predict[x], 'attempts_range': prediction_test,'status':'Rejected'}, ignore_index=True)
		else:
			difference = abs(prediction_test - real_value)
			if difference >= 0 and difference <= 1:
				close_to_real = close_to_real + 1
				data = data.append({'user_id' : users[x] , 'problem_id' : questions_to_predict[x], 'attempts_range': prediction_test,'status':'Accepted'}, ignore_index=True)
			else:
				far_from_real = far_from_real + 1
				data = data.append({'user_id' : users[x] , 'problem_id' : questions_to_predict[x], 'attempts_range': prediction_test,'status':'Rejected'}, ignore_index=True)
	else:
		data = data.append({'user_id' : users[x] , 'problem_id' : questions_to_predict[x], 'attempts_range': prediction_test,'status':'Rejected'}, ignore_index=True)
	x = x + 1
	print("Close: " + str(close_to_real))
	print("Far: " + str(far_from_real))

data.to_csv('example.csv')
print("Close: " + str(close_to_real))
print("Far: " + str(far_from_real))
# print("Don't exist " + str(non_existing_users))
# print("Not similar " + str(no_similarity_users))
