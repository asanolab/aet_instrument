int8 do_id   # 0:measure blank, 1: measure target, 2: calc and save
int8 f       # dielectrometer_id(frequency). 0,1,2(10, 28, 40GHz)
float32 g    # guess param of dielectric constant
float32 t    # thickness of polymer film sample [mm]
bool switch  # true is necessary for the current dielectrometer
string name  # name of sample for result csv
string file  # path of result csv