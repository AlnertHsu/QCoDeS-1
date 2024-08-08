from qcodes.dataset.measurements import Measurement
import numpy as np
from qcodes.instrument.specialized_parameters import ElapsedTimeParameter
from time import sleep
from tqdm.notebook import tqdm

def do1d(param_set, start, stop, num_points, delay, *param_meas):
    meas = Measurement()
    meas.register_parameter(param_set)  # register the first independent parameter
    output = []
    param_set.post_delay = delay
    # do1D enforces a simple relationship between measured parameters
    # and set parameters. For anything more complicated this should be reimplemented from scratch
    for parameter in param_meas:
        meas.register_parameter(parameter, setpoints=(param_set,))
        output.append([parameter, None])

    with meas.run() as datasaver:
        for set_point in tqdm(np.linspace(start, stop, num_points)):
            param_set.set(set_point)
            for i, parameter in enumerate(param_meas):
                output[i][1] = parameter.get()
            datasaver.add_result((param_set, set_point),
                                 *output)
    dataid = datasaver.run_id  # convenient to have for plotting
    return dataid

def do1d_hysterisis(param_set, start, stop, num_points, delay, *param_meas):
    meas = Measurement()
    meas.register_parameter(param_set)  # register the first independent parameter
    output = []
    param_set.post_delay = delay
    # do1D enforces a simple relationship between measured parameters
    # and set parameters. For anything more complicated this should be reimplemented from scratch
    for parameter in param_meas:
        meas.register_parameter(parameter, setpoints=(param_set,))
        output.append([parameter, None])
        
    whole_set=np.linspace(0, start, (num_points-1)/2)
    whole_set = np.append(whole_set,np.linspace(start, stop, num_points))
    whole_set = np.append(whole_set,np.linspace(stop, 0, (num_points-1)/2))
    
    with meas.run() as datasaver:
        for set_point in tqdm(whole_set):
            param_set.set(set_point)
            for i, parameter in enumerate(param_meas):
                output[i][1] = parameter.get()
            datasaver.add_result((param_set, set_point),
                                 *output)
    dataid = datasaver.run_id  # convenient to have for plotting
    return dataid

def do2d_dyn(param_set1, start1, stop1, num_points1, delay1, dyn_param, dyn_value1,dyn_value2,
         param_set2, start2, stop2, num_points2, delay2,
         *param_meas):
    # And then run an experiment

    meas = Measurement()
    meas.register_parameter(param_set1)
    meas.register_parameter(dyn_param)
    param_set1.post_delay = delay1
    meas.register_parameter(param_set2)
    param_set2.post_delay = delay2
    output = []
    for parameter in param_meas:
        meas.register_parameter(parameter, setpoints=(param_set1,param_set2))
        output.append([parameter, None])

    with meas.run() as datasaver:
        for set_point1 in tqdm(np.linspace(start1, stop1, num_points1), desc='first parameter'):
            param_set1.set(set_point1)
            dyn_set = set_point1*dyn_value1+dyn_value2
            dyn_param.set(dyn_set)
            for set_point2 in  tqdm(np.linspace(start2, stop2, num_points2), desc='nested  parameter', leave=False):
                param_set2.set(set_point2)
                for i, parameter in enumerate(param_meas):
                    output[i][1] = parameter.get()
                datasaver.add_result((param_set1, set_point1),
                                     (dyn_param, dyn_set),
                                     (param_set2, set_point2),
                                     *output)
            param_set2.set(start2)
    dataid = datasaver.run_id  # convenient to have for plotting
    return dataid

def do1d_dyn(param_set, start, stop, num_points, delay, dyn_param, dyn_value1, dyn_value2, *param_meas):
    meas = Measurement()
    meas.register_parameter(param_set)  # register the first independent parameter
    meas.register_parameter(dyn_param)
    output = []
    param_set.post_delay = delay
    # do1D enforces a simple relationship between measured parameters
    # and set parameters. For anything more complicated this should be reimplemented from scratch
    for parameter in param_meas:
        meas.register_parameter(parameter, setpoints=(param_set,))
        output.append([parameter, None])

    with meas.run() as datasaver:
        for set_point in tqdm(np.linspace(start, stop, num_points)):
            param_set.set(set_point)
            sleep(delay)
            dyn_set = set_point*dyn_value1+dyn_value2
            dyn_param.set(dyn_set)
            for i, parameter in enumerate(param_meas):
                output[i][1] = parameter.get()
            datasaver.add_result((param_set, set_point),
                                 (dyn_param, dyn_set),
                                 *output)
    dataid = datasaver.run_id  # convenient to have for plotting
    return dataid

def do2d_dyn_b(param_set1, start1, stop1, num_points1, delay1,
         param_set2, start2, stop2, num_points2, delay2,dyn_param, dyn_value1,dyn_value2,
         *param_meas):
    # And then run an experiment

    meas = Measurement()
    meas.register_parameter(param_set1)
    meas.register_parameter(dyn_param)
    param_set1.post_delay = delay1
    meas.register_parameter(param_set2)
    param_set2.post_delay = delay2
    output = []
    for parameter in param_meas:
        meas.register_parameter(parameter, setpoints=(param_set1,param_set2))
        output.append([parameter, None])

    with meas.run() as datasaver:
        for set_point1 in tqdm(np.linspace(start1, stop1, num_points1), desc='first parameter'):
            param_set1.set(set_point1)

            for set_point2 in  tqdm(np.linspace(start2, stop2, num_points2), desc='nested  parameter', leave=False):
                param_set2.set(set_point2)
                dyn_set = set_point2*dyn_value1+dyn_value2
                dyn_param.set(dyn_set)
                for i, parameter in enumerate(param_meas):
                    output[i][1] = parameter.get()
                datasaver.add_result((param_set1, set_point1), 
                                     (param_set2, set_point2),
                                     (dyn_param, dyn_set),
                                     *output)
            param_set2.set(start2)
    dataid = datasaver.run_id  # convenient to have for plotting
    return dataid


def do2d_dyn_c(param_set1, start1, stop1, num_points1, delay1,dyn_param1, dyn1_value1,dyn1_value2,
         param_set2, start2, stop2, num_points2, delay2,dyn_param2, dyn2_value1,dyn2_value2,
         *param_meas):
    # And then run an experiment

    meas = Measurement()
    meas.register_parameter(param_set1)
    meas.register_parameter(dyn_param1)
    meas.register_parameter(dyn_param2)
    meas.register_parameter(param_set2)

    param_set1.post_delay = delay1
    param_set2.post_delay = delay2
    output = []
    for parameter in param_meas:
        meas.register_parameter(parameter, setpoints=(param_set1,param_set2))
        output.append([parameter, None])

    with meas.run() as datasaver:
        for set_point1 in tqdm(np.linspace(start1, stop1, num_points1), desc='first parameter'):
            param_set1.set(set_point1)
            dyn_set1 = set_point1*dyn1_value1+dyn1_value2
            dyn_param1.set(dyn_set1)
            for set_point2 in  tqdm(np.linspace(start2, stop2, num_points2), desc='nested  parameter', leave=False):
                param_set2.set(set_point2)
                dyn_set2 = set_point2*dyn2_value1+dyn2_value2
                dyn_param2.set(dyn_set2)
                for i, parameter in enumerate(param_meas):
                    output[i][1] = parameter.get()
                datasaver.add_result((param_set1, set_point1),
                                      (dyn_param1, dyn_set1),
                                     (param_set2, set_point2),
                                     (dyn_param2, dyn_set2),
                                     *output)
            param_set2.set(start2)
    dataid = datasaver.run_id  # convenient to have for plotting
    return dataid

def do2d_vert_field(param_set1, start1, stop1, num_points1, delay1, dyn_param, dyn_value1,dyn_value2,
         param_set2, start2, stop2, num_points2, delay2,
         *param_meas):
    # And then run an experiment

    meas = Measurement()
    meas.register_parameter(param_set1)
    meas.register_parameter(dyn_param)
    param_set1.post_delay = delay1
    meas.register_parameter(param_set2)
    param_set2.post_delay = delay2
    output = []
    for parameter in param_meas:
        meas.register_parameter(parameter, setpoints=(param_set1,param_set2))
        output.append([parameter, None])

    with meas.run() as datasaver:
        for set_point1 in tqdm(np.linspace(start1, stop1, num_points1), desc='first parameter'):
            param_set1.set(set_point1)
            dyn_set = set_point1*dyn_value1+dyn_value2
            dyn_param.set(dyn_set)
            for set_point2 in  tqdm(np.linspace(start2, stop2, num_points2), desc='nested  parameter', leave=False):
                param_set2.set(set_point2)
                for i, parameter in enumerate(param_meas):
                    output[i][1] = parameter.get()
                datasaver.add_result((param_set1, set_point1),
                                     (dyn_param, dyn_set),
                                     (param_set2, set_point2),
                                     *output)
            param_set2.set(start2)
    dataid = datasaver.run_id  # convenient to have for plotting
    return dataid
    
def do2d_sens(param_set1, start1, stop1, num_points1, delay1,
         param_set2, start2, stop2, num_points2, delay2,
         lockin_device, *param_meas):
    # And then run an experiment
    # keep in mind the change of impededance of lockin circuit, the extra logic operations dwelling time and the abrupt change of data values

    meas = Measurement()
    meas.register_parameter(param_set1)
    param_set1.post_delay = delay1
    meas.register_parameter(param_set2)
    param_set2.post_delay = delay2
    output = []
    for parameter in param_meas:
        meas.register_parameter(parameter, setpoints=(param_set1,param_set2))
        output.append([parameter, None])

    with meas.run() as datasaver:
        for set_point1 in tqdm(np.linspace(start1, stop1, num_points1), desc='first parameter'):
            param_set1.set(set_point1)
            lockin_readings = np.zeroes(num_points2)
            for idx_2, set_point2 in enumerate(tqdm(np.linspace(start2, stop2, num_points2), desc='nested  parameter', leave=False)):
                param_set2.set(set_point2)
                lockin_readings[idx_2] = lockin_device.X()
                for i, parameter in enumerate(param_meas):
                    output[i][1] = parameter.get()
                datasaver.add_result((param_set1, set_point1),
                                     (param_set2, set_point2),
                                     *output)
            param_set2.set(start2)
            if np.max > 
            # add the sensitivity check and determine the optimal sensitivity for which the maximum lockin values < optlim (0.7 by default)
            optlim = 0.7
            lockin1_reading = output



    dataid = datasaver.run_id  # convenient to have for plotting
    return dataid