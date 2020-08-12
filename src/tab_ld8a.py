NC0_B = None
NC1_B = None

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/TAB_LD8A.C#L21
hamwindow = [2621,  2623,  2629,  2638,  2651,  2668,  2689,  2713,  2741,  2772,
             2808,  2847,  2890,  2936,  2986,  3040,  3097,  3158,  3223,  3291,
             3363,  3438,  3517,  3599,  3685,  3774,  3867,  3963,  4063,  4166,
             4272,  4382,  4495,  4611,  4731,  4853,  4979,  5108,  5240,  5376,
             5514,  5655,  5800,  5947,  6097,  6250,  6406,  6565,  6726,  6890,
             7057,  7227,  7399,  7573,  7750,  7930,  8112,  8296,  8483,  8672,
             8863,  9057,  9252,  9450,  9650,  9852, 10055, 10261, 10468, 10677,
             10888, 11101, 11315, 11531, 11748, 11967, 12187, 12409, 12632, 12856,
             13082, 13308, 13536, 13764, 13994, 14225, 14456, 14688, 14921, 15155,
             15389, 15624, 15859, 16095, 16331, 16568, 16805, 17042, 17279, 17516,
             17754, 17991, 18228, 18465, 18702, 18939, 19175, 19411, 19647, 19882,
             20117, 20350, 20584, 20816, 21048, 21279, 21509, 21738, 21967, 22194,
             22420, 22644, 22868, 23090, 23311, 23531, 23749, 23965, 24181, 24394,
             24606, 24816, 25024, 25231, 25435, 25638, 25839, 26037, 26234, 26428,
             26621, 26811, 26999, 27184, 27368, 27548, 27727, 27903, 28076, 28247,
             28415, 28581, 28743, 28903, 29061, 29215, 29367, 29515, 29661, 29804,
             29944, 30081, 30214, 30345, 30472, 30597, 30718, 30836, 30950, 31062,
             31170, 31274, 31376, 31474, 31568, 31659, 31747, 31831, 31911, 31988,
             32062, 32132, 32198, 32261, 32320, 32376, 32428, 32476, 32521, 32561,
             32599, 32632, 32662, 32688, 32711, 32729, 32744, 32755, 32763, 32767,
             32767, 32741, 32665, 32537, 32359, 32129, 31850, 31521, 31143, 30716,
             30242, 29720, 29151, 28538, 27879, 27177, 26433, 25647, 24821, 23957,
             23055, 22117, 21145, 20139, 19102, 18036, 16941, 15820, 14674, 13505,
             12315, 11106,  9879,  8637,  7381,  6114,  4838,  3554,  2264,   971]

lag_h = [32728,
         32619,
         32438,
         32187,
         31867,
         31480,
         31029,
         30517,
         29946,
         29321]

lag_l = [11904,
         17280,
         30720,
         25856,
         24192,
         28992,
         24384,
         7360,
         19520,
         14784]

table = [32767,  32729,  32610,  32413,  32138,  31786,  31357,  30853,
         30274,  29622,  28899,  28106,  27246,  26320,  25330,  24279,
         23170,  22006,  20788,  19520,  18205,  16846,  15447,  14010,
         12540,  11039,   9512,   7962,   6393,   4808,   3212,   1608,
         0,  -1608,  -3212,  -4808,  -6393,  -7962,  -9512, -11039,
         -12540, -14010, -15447, -16846, -18205, -19520, -20788, -22006,
         -23170, -24279, -25330, -26320, -27246, -28106, -28899, -29622,
         -30274, -30853, -31357, -31786, -32138, -32413, -32610, -32729,
         -32768]

slope = [-26887,  -8812,  -5323,  -3813,  -2979,  -2444,  -2081,  -1811,
         -1608,  -1450,  -1322,  -1219,  -1132,  -1059,   -998,   -946,
         -901,   -861,   -827,   -797,   -772,   -750,   -730,   -713,
         -699,   -687,   -677,   -668,   -662,   -657,   -654,   -652,
         -652,   -654,   -657,   -662,   -668,   -677,   -687,   -699,
         -713,   -730,   -750,   -772,   -797,   -827,   -861,   -901,
         -946,   -998,  -1059,  -1132,  -1219,  -1322,  -1450,  -1608,
         -1811,  -2081,  -2444,  -2979,  -3813,  -5323,  -8812, -26887]

table2 = [32767,  32729,  32610,  32413,  32138,  31786,  31357,  30853,
          30274,  29622,  28899,  28106,  27246,  26320,  25330,  24279,
          23170,  22006,  20788,  19520,  18205,  16846,  15447,  14010,
          12540,  11039,   9512,   7962,   6393,   4808,   3212,   1608,
          0,  -1608,  -3212,  -4808,  -6393,  -7962,  -9512, -11039,
          -12540, -14010, -15447, -16846, -18205, -19520, -20788, -22006,
          -23170, -24279, -25330, -26320, -27246, -28106, -28899, -29622,
          -30274, -30853, -31357, -31786, -32138, -32413, -32610, -32729]

slope_cos = [-632,  -1893,  -3150,  -4399,  -5638,  -6863,  -8072,  -9261,
             -10428, -11570, -12684, -13767, -14817, -15832, -16808, -17744,
             -18637, -19486, -20287, -21039, -21741, -22390, -22986, -23526,
             -24009, -24435, -24801, -25108, -25354, -25540, -25664, -25726,
             -25726, -25664, -25540, -25354, -25108, -24801, -24435, -24009,
             -23526, -22986, -22390, -21741, -21039, -20287, -19486, -18637,
             -17744, -16808, -15832, -14817, -13767, -12684, -11570, -10428,
             -9261,  -8072,  -6863,  -5638,  -4399,  -3150,  -1893,   -632]

slope_acos = [-26887,  -8812,  -5323,  -3813,  -2979,  -2444,  -2081,  -1811,
              -1608,  -1450,  -1322,  -1219,  -1132,  -1059,   -998,   -946,
              -901,   -861,   -827,   -797,   -772,   -750,   -730,   -713,
              -699,   -687,   -677,   -668,   -662,   -657,   -654,   -652,
              -652,   -654,   -657,   -662,   -668,   -677,   -687,   -699,
              -713,   -730,   -750,   -772,   -797,   -827,   -861,   -901,
              -946,   -998,  -1059,  -1132,  -1219,  -1322,  -1450,  -1608,
              -1811,  -2081,  -2444,  -2979,  -3813,  -5323,  -8812, -26887]

lspcb1 = [
    [1486,  2168,  3751,  9074, 12134, 13944, 17983, 19173, 21190, 21820],
    [1730,  2640,  3450,  4870,  6126,  7876, 15644, 17817, 20294, 21902],
    [1568,  2256,  3088,  4874, 11063, 13393, 18307, 19293, 21109, 21741],
    [1733,  2512,  3357,  4708,  6977, 10296, 17024, 17956, 19145, 20350],
    [1744,  2436,  3308,  8731, 10432, 12007, 15614, 16639, 21359, 21913],
    [1786,  2369,  3372,  4521,  6795, 12963, 17674, 18988, 20855, 21640],
    [1631,  2433,  3361,  6328, 10709, 12013, 13277, 13904, 19441, 21088],
    [1489,  2364,  3291,  6250,  9227, 10403, 13843, 15278, 17721, 21451],
    [1869,  2533,  3475,  4365,  9152, 14513, 15908, 17022, 20611, 21411],
    [2070,  3025,  4333,  5854,  7805,  9231, 10597, 16047, 20109, 21834],
    [1910,  2673,  3419,  4261, 11168, 15111, 16577, 17591, 19310, 20265],
    [1141,  1815,  2624,  4623,  6495,  9588, 13968, 16428, 19351, 21286],
    [2192,  3171,  4707,  5808, 10904, 12500, 14162, 15664, 21124, 21789],
    [1286,  1907,  2548,  3453,  9574, 11964, 15978, 17344, 19691, 22495],
    [1921,  2720,  4604,  6684, 11503, 12992, 14350, 15262, 16997, 20791],
    [2052,  2759,  3897,  5246,  6638, 10267, 15834, 16814, 18149, 21675],
    [1798,  2497,  5617, 11449, 13189, 14711, 17050, 18195, 20307, 21182],
    [1009,  1647,  2889,  5709,  9541, 12354, 15231, 18494, 20966, 22033],
    [3016,  3794,  5406,  7469, 12488, 13984, 15328, 16334, 19952, 20791],
    [2203,  3040,  3796,  5442, 11987, 13512, 14931, 16370, 17856, 18803],
    [2912,  4292,  7988,  9572, 11562, 13244, 14556, 16529, 20004, 21073],
    [2861,  3607,  5923,  7034,  9234, 12054, 13729, 18056, 20262, 20974],
    [3069,  4311,  5967,  7367, 11482, 12699, 14309, 16233, 18333, 19172],
    [2434,  3661,  4866,  5798, 10383, 11722, 13049, 15668, 18862, 19831],
    [2020,  2605,  3860,  9241, 13275, 14644, 16010, 17099, 19268, 20251],
    [1877,  2809,  3590,  4707, 11056, 12441, 15622, 17168, 18761, 19907],
    [2107,  2873,  3673,  5799, 13579, 14687, 15938, 17077, 18890, 19831],
    [1612,  2284,  2944,  3572,  8219, 13959, 15924, 17239, 18592, 20117],
    [2420,  3156,  6542, 10215, 12061, 13534, 15305, 16452, 18717, 19880],
    [1667,  2612,  3534,  5237, 10513, 11696, 12940, 16798, 18058, 19378],
    [2388,  3017,  4839,  9333, 11413, 12730, 15024, 16248, 17449, 18677],
    [1875,  2786,  4231,  6320,  8694, 10149, 11785, 17013, 18608, 19960],
    [679,  1411,  4654,  8006, 11446, 13249, 15763, 18127, 20361, 21567],
    [1838,  2596,  3578,  4608,  5650, 11274, 14355, 15886, 20579, 21754],
    [1303,  1955,  2395,  3322, 12023, 13764, 15883, 18077, 20180, 21232],
    [1438,  2102,  2663,  3462,  8328, 10362, 13763, 17248, 19732, 22344],
    [860,  1904,  6098,  7775,  9815, 12007, 14821, 16709, 19787, 21132],
    [1673,  2723,  3704,  6125,  7668,  9447, 13683, 14443, 20538, 21731],
    [1246,  1849,  2902,  4508,  7221, 12710, 14835, 16314, 19335, 22720],
    [1525,  2260,  3862,  5659,  7342, 11748, 13370, 14442, 18044, 21334],
    [1196,  1846,  3104,  7063, 10972, 12905, 14814, 17037, 19922, 22636],
    [2147,  3106,  4475,  6511,  8227,  9765, 10984, 12161, 18971, 21300],
    [1585,  2405,  2994,  4036, 11481, 13177, 14519, 15431, 19967, 21275],
    [1778,  2688,  3614,  4680,  9465, 11064, 12473, 16320, 19742, 20800],
    [1862,  2586,  3492,  6719, 11708, 13012, 14364, 16128, 19610, 20425],
    [1395,  2156,  2669,  3386, 10607, 12125, 13614, 16705, 18976, 21367],
    [1444,  2117,  3286,  6233,  9423, 12981, 14998, 15853, 17188, 21857],
    [2004,  2895,  3783,  4897,  6168,  7297, 12609, 16445, 19297, 21465],
    [1495,  2863,  6360,  8100, 11399, 14271, 15902, 17711, 20479, 22061],
    [2484,  3114,  5718,  7097,  8400, 12616, 14073, 14847, 20535, 21396],
    [2424,  3277,  5296,  6284, 11290, 12903, 16022, 17508, 19333, 20283],
    [2565,  3778,  5360,  6989,  8782, 10428, 14390, 15742, 17770, 21734],
    [2727,  3384,  6613,  9254, 10542, 12236, 14651, 15687, 20074, 21102],
    [1916,  2953,  6274,  8088,  9710, 10925, 12392, 16434, 20010, 21183],
    [3384,  4366,  5349,  7667, 11180, 12605, 13921, 15324, 19901, 20754],
    [3075,  4283,  5951,  7619,  9604, 11010, 12384, 14006, 20658, 21497],
    [1751,  2455,  5147,  9966, 11621, 13176, 14739, 16470, 20788, 21756],
    [1442,  2188,  3330,  6813,  8929, 12135, 14476, 15306, 19635, 20544],
    [2294,  2895,  4070,  8035, 12233, 13416, 14762, 17367, 18952, 19688],
    [1937,  2659,  4602,  6697,  9071, 12863, 14197, 15230, 16047, 18877],
    [2071,  2663,  4216,  9445, 10887, 12292, 13949, 14909, 19236, 20341],
    [1740,  2491,  3488,  8138,  9656, 11153, 13206, 14688, 20896, 21907],
    [2199,  2881,  4675,  8527, 10051, 11408, 14435, 15463, 17190, 20597],
    [1943,  2988,  4177,  6039,  7478,  8536, 14181, 15551, 17622, 21579],
    [1825,  3175,  7062,  9818, 12824, 15450, 18330, 19856, 21830, 22412],
    [2464,  3046,  4822,  5977,  7696, 15398, 16730, 17646, 20588, 21320],
    [2550,  3393,  5305,  6920, 10235, 14083, 18143, 19195, 20681, 21336],
    [3003,  3799,  5321,  6437,  7919, 11643, 15810, 16846, 18119, 18980],
    [3455,  4157,  6838,  8199,  9877, 12314, 15905, 16826, 19949, 20892],
    [3052,  3769,  4891,  5810,  6977, 10126, 14788, 15990, 19773, 20904],
    [3671,  4356,  5827,  6997,  8460, 12084, 14154, 14939, 19247, 20423],
    [2716,  3684,  5246,  6686,  8463, 10001, 12394, 14131, 16150, 19776],
    [1945,  2638,  4130,  7995, 14338, 15576, 17057, 18206, 20225, 20997],
    [2304,  2928,  4122,  4824,  5640, 13139, 15825, 16938, 20108, 21054],
    [1800,  2516,  3350,  5219, 13406, 15948, 17618, 18540, 20531, 21252],
    [1436,  2224,  2753,  4546,  9657, 11245, 15177, 16317, 17489, 19135],
    [2319,  2899,  4980,  6936,  8404, 13489, 15554, 16281, 20270, 20911],
    [2187,  2919,  4610,  5875,  7390, 12556, 14033, 16794, 20998, 21769],
    [2235,  2923,  5121,  6259,  8099, 13589, 15340, 16340, 17927, 20159],
    [1765,  2638,  3751,  5730,  7883, 10108, 13633, 15419, 16808, 18574],
    [3460,  5741,  9596, 11742, 14413, 16080, 18173, 19090, 20845, 21601],
    [3735,  4426,  6199,  7363,  9250, 14489, 16035, 17026, 19873, 20876],
    [3521,  4778,  6887,  8680, 12717, 14322, 15950, 18050, 20166, 21145],
    [2141,  2968,  6865,  8051, 10010, 13159, 14813, 15861, 17528, 18655],
    [4148,  6128,  9028, 10871, 12686, 14005, 15976, 17208, 19587, 20595],
    [4403,  5367,  6634,  8371, 10163, 11599, 14963, 16331, 17982, 18768],
    [4091,  5386,  6852,  8770, 11563, 13290, 15728, 16930, 19056, 20102],
    [2746,  3625,  5299,  7504, 10262, 11432, 13172, 15490, 16875, 17514],
    [2248,  3556,  8539, 10590, 12665, 14696, 16515, 17824, 20268, 21247],
    [1279,  1960,  3920,  7793, 10153, 14753, 16646, 18139, 20679, 21466],
    [2440,  3475,  6737,  8654, 12190, 14588, 17119, 17925, 19110, 19979],
    [1879,  2514,  4497,  7572, 10017, 14948, 16141, 16897, 18397, 19376],
    [2804,  3688,  7490, 10086, 11218, 12711, 16307, 17470, 20077, 21126],
    [2023,  2682,  3873,  8268, 10255, 11645, 15187, 17102, 18965, 19788],
    [2823,  3605,  5815,  8595, 10085, 11469, 16568, 17462, 18754, 19876],
    [2851,  3681,  5280,  7648,  9173, 10338, 14961, 16148, 17559, 18474],
    [1348,  2645,  5826,  8785, 10620, 12831, 16255, 18319, 21133, 22586],
    [2141,  3036,  4293,  6082,  7593, 10629, 17158, 18033, 21466, 22084],
    [1608,  2375,  3384,  6878,  9970, 11227, 16928, 17650, 20185, 21120],
    [2774,  3616,  5014,  6557,  7788,  8959, 17068, 18302, 19537, 20542],
    [1934,  4813,  6204,  7212,  8979, 11665, 15989, 17811, 20426, 21703],
    [2288,  3507,  5037,  6841,  8278,  9638, 15066, 16481, 21653, 22214],
    [2951,  3771,  4878,  7578,  9016, 10298, 14490, 15242, 20223, 20990],
    [3256,  4791,  6601,  7521,  8644,  9707, 13398, 16078, 19102, 20249],
    [1827,  2614,  3486,  6039, 12149, 13823, 16191, 17282, 21423, 22041],
    [1000,  1704,  3002,  6335,  8471, 10500, 14878, 16979, 20026, 22427],
    [1646,  2286,  3109,  7245, 11493, 12791, 16824, 17667, 18981, 20222],
    [1708,  2501,  3315,  6737,  8729,  9924, 16089, 17097, 18374, 19917],
    [2623,  3510,  4478,  5645,  9862, 11115, 15219, 18067, 19583, 20382],
    [2518,  3434,  4728,  6388,  8082,  9285, 13162, 18383, 19819, 20552],
    [1726,  2383,  4090,  6303,  7805, 12845, 14612, 17608, 19269, 20181],
    [2860,  3735,  4838,  6044,  7254,  8402, 14031, 16381, 18037, 19410],
    [4247,  5993,  7952,  9792, 12342, 14653, 17527, 18774, 20831, 21699],
    [3502,  4051,  5680,  6805,  8146, 11945, 16649, 17444, 20390, 21564],
    [3151,  4893,  5899,  7198, 11418, 13073, 15124, 17673, 20520, 21861],
    [3960,  4848,  5926,  7259,  8811, 10529, 15661, 16560, 18196, 20183],
    [4499,  6604,  8036,  9251, 10804, 12627, 15880, 17512, 20020, 21046],
    [4251,  5541,  6654,  8318,  9900, 11686, 15100, 17093, 20572, 21687],
    [3769,  5327,  7865,  9360, 10684, 11818, 13660, 15366, 18733, 19882],
    [3083,  3969,  6248,  8121,  9798, 10994, 12393, 13686, 17888, 19105],
    [2731,  4670,  7063,  9201, 11346, 13735, 16875, 18797, 20787, 22360],
    [1187,  2227,  4737,  7214,  9622, 12633, 15404, 17968, 20262, 23533],
    [1911,  2477,  3915, 10098, 11616, 12955, 16223, 17138, 19270, 20729],
    [1764,  2519,  3887,  6944,  9150, 12590, 16258, 16984, 17924, 18435],
    [1400,  3674,  7131,  8718, 10688, 12508, 15708, 17711, 19720, 21068],
    [2322,  3073,  4287,  8108,  9407, 10628, 15862, 16693, 19714, 21474],
    [2630,  3339,  4758,  8360, 10274, 11333, 12880, 17374, 19221, 19936],
    [1721,  2577,  5553,  7195,  8651, 10686, 15069, 16953, 18703, 19929]
]

lspcb2 = [
    [-435,  -815,  -742,  1033,  -518,   582, -1201,   829,    86,   385],
    [-833,  -891,   463,    -8, -1251,  1450,    72,  -231,   864,   661],
    [-1021,   231,  -306,   321,  -220,  -163,  -526,  -754, -1633,   267],
    [57,  -198,  -339,   -33, -1468,   573,   796,  -169,  -631,   816],
    [171,  -350,   294,  1660,   453,   519,   291,   159,  -640, -1296],
    [-701,  -842,   -58,   950,   892,  1549,   715,   527,  -714,  -193],
    [584,    31,  -289,   356,  -333,  -457,   612,  -283, -1381,  -741],
    [-109,  -808,   231,    77,   -87,  -344,  1341,  1087,  -654,  -569],
    [-859,  1236,   550,   854,   714,  -543, -1752,  -195,   -98,  -276],
    [-877,  -954, -1248,  -299,   212,  -235,  -728,   949,  1517,   895],
    [-77,   344,  -620,   763,   413,   502,  -362,  -960,  -483,  1386],
    [-314,  -307,  -256, -1260,  -429,   450,  -466,  -108,  1010,  2223],
    [711,   693,   521,   650,  1305,   -28,  -378,   744, -1005,   240],
    [-112,  -271,  -500,   946,  1733,   271,   -15,   909,  -259,  1688],
    [575,   -10,  -468,  -199,  1101, -1011,   581,   -53,  -747,   878],
    [145,  -285, -1280,  -398,    36,  -498, -1377,    18,  -444,  1483],
    [-1133,  -835,  1350,  1284,   -95,  1015,  -222,   443,   372,  -354],
    [-1459, -1237,   416,  -213,   466,   669,   659,  1640,   932,   534],
    [-15,    66,   468,  1019,  -748,  1385,  -182,  -907,  -721,  -262],
    [-338,   148,  1445,    75,  -760,   569,  1247,   337,   416,  -121],
    [389,   239,  1568,   981,   113,   369, -1003,  -507,  -587,  -904],
    [-312,   -98,   949,    31,  1104,    72,  -141,  1465,    63,  -785],
    [1127,   584,   835,   277, -1159,   208,   301,  -882,   117,  -404],
    [539,  -114,   856,  -493,   223,  -912,   623,   -76,   276,  -440],
    [2197,  2337,  1268,   670,   304,  -267,  -525,   140,   882,  -139],
    [-1596,   550,   801,  -456,   -56,  -697,   865,  1060,   413,   446],
    [1154,   593,   -77,  1237,   -31,   581, -1037,  -895,   669,   297],
    [397,   558,   203,  -797,  -919,     3,   692,  -292,  1050,   782],
    [334,  1475,   632,   -80,    48, -1061,  -484,   362,  -597,  -852],
    [-545,  -330,  -429,  -680,  1133, -1182,  -744,  1340,   262,    63],
    [1320,   827,  -398,  -576,   341,  -774,  -483, -1247,   -70,    98],
    [-163,   674,   -11,  -886,   531, -1125,  -265,  -242,   724,   934]
]

fg = [
    [
        [8421,  9109,  9175,  8965,  9034,  9057,  8765,  8775,  9106,  8673],
        [7018,  7189,  7638,  7307,  7444,  7379,  7038,  6956,  6930,  6868],
        [5472,  4990,  5134,  5177,  5246,  5141,  5206,  5095,  4830,  5147],
        [4056,  3031,  2614,  3024,  2916,  2713,  3309,  3237,  2857,  3473]
    ],
    [
        [7733,  7880,  8188,  8175,  8247,  8490,  8637,  8601,  8359,  7569],
        [4210,  3031,  2552,  3473,  3876,  3853,  4184,  4154,  3909,  3968],
        [3214,  1930,  1313,  2143,  2493,  2385,  2755,  2706,  2542,  2919],
        [3024,  1592,   940,  1631,  1723,  1579,  2034,  2084,  1913,  2601]
    ]
]

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/TAB_LD8A.C#L344
fg_sum = [
    [7798,  8447,  8205,  8293,  8126,  8477,  8447,  8703,  9043,  8604],
    [14585, 18333, 19772, 17344, 16426, 16459, 15155, 15220, 16043, 15708]
]

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/TAB_LD8A.C#L348
fg_sum_inv = [
    [17210, 15888, 16357, 16183, 16516, 15833, 15888, 15421, 14840, 15597],
    [9202,  7320,  6788,  7738,  8170,  8154,  8856,  8818,  8366,  8544]
]

grid = [
    32760,     32703,     32509,     32187,     31738,     31164,
    30466,     29649,     28714,     27666,     26509,     25248,
    23886,     22431,     20887,     19260,     17557,     15786,
    13951,     12062,     10125,      8149,      6140,      4106,
    2057,         0,     -2057,     -4106,     -6140,     -8149,
    -10125,    -12062,    -13951,    -15786,    -17557,    -19260,
    -20887,    -22431,    -23886,    -25248,    -26509,    -27666,
    -28714,    -29649,    -30466,    -31164,    -31738,    -32187,
    -32509,    -32703,    -32760]

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/TAB_LD8A.C#L383
inter_3l = [
    29443,
    25207,   14701,    3143,
    -4402,   -5850,   -2783,
    1211,    3130,    2259,
    0,   -1652,   -1666,
    -464,     756,    1099,
    550,    -245,    -634,
    -451,       0,     308,
    296,      78,    -120,
    -165,     -79,      34,
    91,      70,       0]

# https://github.com/opentelecoms-org/codecs/blob/master/g729/ITU-samples-200701/Soft/g729AnnexA/c_code/TAB_LD8A.C#L416
pred[4] = [5571, 4751, 2785, 1556]

gbk1 = [
    [1,  1516],
    [1551,  2425],
    [1831,  5022],
    [57,  5404],
    [1921,  9291],
    [3242,  9949],
    [356, 14756],
    [2678, 27162]
]

gbk2 = [
    [826,  2005],
    [1994,     0],
    [5142,   592],
    [6160,  2395],
    [8091,  4861],
    [9120,   525],
    [10573,  2966],
    [11569,  1196],
    [13260,  3256],
    [14194,  1630],
    [15132,  4914],
    [15161, 14276],
    [15434,   237],
    [16112,  3392],
    [17299,  1861],
    [18973,  5935]
]

map1 = [
    5, 1, 4, 7, 3, 0, 6, 2
]

map2 = [
    4, 6, 0, 2, 12, 14, 8, 10, 15, 11, 9, 13, 7, 3, 1, 5
]

coef = [
    [31881, 26416],
    [31548, 27816]
]

L_coef = [
    [2089405952, 1731217536],
    [2067549984, 1822990272]
]

thr1 = [
    10808,
    12374,
    19778,
    32567
]

thr2 = [
    14087,
    16188,
    20274,
    21321,
    23525,
    25232,
    27873,
    30542
]

imap1 = [
    5, 1, 7, 4, 2, 0, 6, 3
]

imap2 = [
    2, 14, 3, 13, 0, 15, 1, 12, 6, 10, 7, 9, 4, 11, 5, 8
]

b100 = [7699, -15398, 7699]
a100 = [8192, 15836, -7667]

b140 = [1899, -3798, 1899]
a140 = [4096, 7807, -3733]

bitsno = [1 + NC0_B,
          NC1_B * 2,
          8, 1, 13, 4, 7,
          5,    13, 4, 7]

tabpow = [
    16384, 16743, 17109, 17484, 17867, 18258, 18658, 19066, 19484, 19911,
    20347, 20792, 21247, 21713, 22188, 22674, 23170, 23678, 24196, 24726,
    25268, 25821, 26386, 26964, 27554, 28158, 28774, 29405, 30048, 30706,
    31379, 32066, 32767]

tablog = [
    0,  1455,  2866,  4236,  5568,  6863,  8124,  9352, 10549, 11716,
    12855, 13967, 15054, 16117, 17156, 18172, 19167, 20142, 21097, 22033,
    22951, 23852, 24735, 25603, 26455, 27291, 28113, 28922, 29716, 30497,
    31266, 32023, 32767]

tabsqr = [

    32767, 31790, 30894, 30070, 29309, 28602, 27945, 27330, 26755, 26214,
    25705, 25225, 24770, 24339, 23930, 23541, 23170, 22817, 22479, 22155,
    21845, 21548, 21263, 20988, 20724, 20470, 20225, 19988, 19760, 19539,
    19326, 19119, 18919, 18725, 18536, 18354, 18176, 18004, 17837, 17674,
    17515, 17361, 17211, 17064, 16921, 16782, 16646, 16514, 16384]

tab_zone = [

    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
    3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
