
import json
from datetime import datetime
from aind_data_schema_models.organizations import Organization
from aind_data_schema.core.rig import Rig

from aind_data_schema.components.coordinates import RelativePosition, Translation3dTransform, Rotation3dTransform,Axis,AxisName
from aind_data_schema.core.rig import Rig
from aind_data_schema.components.devices import (
    Calibration,
    Camera,
    CameraAssembly,
    CameraTarget,
    DAQChannel,
    Disc,
    EphysAssembly,
    EphysProbe,
    HarpDevice,
    Laser,
    LaserAssembly,
    Lens,
    Manipulator,
    ProbeModel,
    FilterType,
    Filter,
    Tube,
    RewardDelivery,
    MotorizedStage,
    SpoutSide,
    RewardSpout,
    Speaker,
    Device,
    DataInterface,
    NeuropixelsBasestation,
    DAQDevice,
    ProbePort,
    Lamp,
    LightEmittingDiode
)
from aind_data_schema_models.harp_types import HarpDeviceType
from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization,NewScaleTechnologies
from aind_data_schema_models.units import FrequencyUnit, PowerUnit, SizeUnit
from local_devices import Cameras_class,Filter_class,Lens_class,Probes_class,Stimulus_devices_class,daq_class,Mouse_platform_class,Light_sources_laser_class,Light_sources_led_class

from foraging_gui.Visualization import PlotWaterCalibration

class generate_rig_metadata:
    '''
    Used to generate metadata for the rig. 

    Parameters:
    output_folder: Optional. The folder where the metadata file will be saved.
    json_file: Optional. The json file containing information used to generate the metadata. 
    object_name: Optional. Dictionary  containing information used to generate the metadata.

    Output:
    A json file containing the metadata for the rig.
    '''
    def __init__(self, output_folder=None,json_file=None,obj=None):
        self.metadata = {}
        if json_file==None and obj==None:
            raise ValueError('Please provide either a json file or a dictionary object')
        if json_file!=None:
            self.obj = json.load(open(json_file))
        elif obj!=None:
            self.obj = obj

        if output_folder==None:
            if 'output_folder' in self.obj:
                self.output_folder = self.obj['output_folder']
            else:
                raise ValueError('output_folder not found in json file')
        else:
            self.output_folder = output_folder

        self._mapper()
        self.generate_rig_metadata()
        
    def _mapper(self):
        '''
        Name mapping
        '''
        self.name_mapper = {
            'laser_name_mapper':{
                'Oxxius_Lasers_473_1': 'Blue', 
                'Oxxius_Lasers_473_2': 'Blue', 
                'Oxxius_Lasers_561_1': 'Yellow',
                'Oxxius_Lasers_561_2': 'Yellow',
                'Oxxius_Lasers_638_1': 'Red',
                'Oxxius_Lasers_638_2': 'Red',
            },# laser name in the rig metadata and the corresponding color used in the behavior GUI
            'laser_tags':[1,2], # laser tags corresponding to Laser_1 and Laser_2
            'sides':['Left','Right'], # lick spouts
            'lick_spouts_distance':5000, # distance between the two lick spouts in um; this value shoud be directly extracted from the rig metadata
            'camera_list':['SideCameraLeft','SideCameraRight','BottomCamera','BodyCamera'], # camera names in the settings_box.csv
            'camera_name_mapper':{
                'SideCameraLeft': "Face side left",
                'SideCameraRight': "Face side right",
                'BottomCamera': "Bottom",
                'BodyCamera': "Body"
            }, # camera names in the settings_box.csv and the corresponding names in the rig metadata
        }
        
    def generate_rig_metadata(self):

        self._get_ephys_assemblies()
        self._get_stick_microscopes()
        self._get_high_speed_cameras()
        self._get_stimulus_devices()
        self._get_light_sources()
        self._get_mouse_platform()
        self._get_daqs()
        self._get_calibration()
        self._get_modalities()

        self.rig = Rig(
            rig_id=self.obj['rig_id'],
            modification_date=datetime.strptime(self.obj['rig_id'][-10:], "%Y-%m-%d").date(),
            modalities=self.modalities,
            ephys_assemblies=self.ephys_assemblies,
            cameras=self.high_speed_cameras,
            stick_microscopes=self.stick_microscopes,
            mouse_platform=self.mouse_platform,
            calibrations=self.calibrations,
            stimulus_devices=self.stimulus_devices,
            patch_cords=[],
            daqs=self.daqs,
            light_sources=self.light_sources,
            notes=self.obj['notes'],
        )

        self.rig.write_standard_file(self.output_folder,suffix=self.obj['rig_id']+'.json')


    def _get_light_sources(self):
        '''
        get the light sources metadata
        '''
        self.light_sources=[]
        for light_source in self.obj['light_sources_laser']:
            light_source_params=getattr(Light_sources_laser_class,light_source)
            self.light_sources.append(Laser(**light_source_params))

        for light_source in self.obj['light_sources_led']:
            light_source_params=getattr(Light_sources_led_class,light_source['model_name'])
            light_source_params['name']=light_source['name']
            light_source_params['serial_number']=light_source['serial_number']
            self.light_sources.append(LightEmittingDiode(**light_source_params))
            

    def _get_calibration(self):
        '''
        generate the calibration metadata
        '''
        self.calibrations=[]
        self._get_water_calibration()
        self._get_opto_calibration()
        self.calibrations=self.water_calibration+self.opto_calibration

    def _get_opto_calibration(self):
        '''
        Make the optogenetic (Laser or LED) calibration metadata
        '''
        if not 'laser_calibration_file' in self.obj:
            self.opto_calibration =[]
            return
        # load the optogenetic calibration json
        self.OptoCalibrationResults=json.load(open(self.obj['laser_calibration_file']))

        self._parse_opto_calibration() 
        self.opto_calibration=[]
        for current_calibration in self.parsed_optocalibration:
                description= f'Optogenetic calibration for {current_calibration["laser name"]} {current_calibration["Color"]} Laser_{current_calibration["Laser tag"]}. Protocol: {current_calibration["Protocol"]}. Frequency: {current_calibration["Frequency"]}.'
                self.opto_calibration.append(Calibration(
                calibration_date=datetime.strptime(current_calibration['latest_calibration_date'], '%Y-%m-%d').date(),
                device_name=current_calibration['laser name'],
                description=description,
                input= {'input voltage (v)':current_calibration['Voltage']},
                output={'laser power (mw)':current_calibration['Power']} ,
                ))

    def _parse_opto_calibration(self):
        '''
        Parse the optogenetic calibration information from the behavior json file
        '''
        self.parsed_optocalibration=[]
        self._get_laser_names()
        for laser in self.laser_names:
                Color=self.name_mapper['laser_name_mapper'][laser]
                latest_calibration_date=self._FindLatestCalibrationDate(Color)
                if latest_calibration_date=='NA':
                    RecentLaserCalibration={}
                else:
                    RecentLaserCalibration=self.OptoCalibrationResults[latest_calibration_date]
                no_calibration=False
                if not RecentLaserCalibration=={}:
                    if Color in RecentLaserCalibration.keys():
                        for Protocol in RecentLaserCalibration[Color]:
                            if Protocol=='Sine': 
                                for Frequency in RecentLaserCalibration[Color][Protocol]:
                                    for laser_tag in self.name_mapper['laser_tags']:
                                        voltage=[]
                                        power=[]
                                        for i in range(len(RecentLaserCalibration[Color][Protocol][Frequency][f"Laser_{laser_tag}"]['LaserPowerVoltage'])):
                                            laser_voltage_power=eval(str(RecentLaserCalibration[Color][Protocol][Frequency][f"Laser_{laser_tag}"]['LaserPowerVoltage'][i]))
                                            voltage.append(laser_voltage_power[0])
                                            power.append(laser_voltage_power[1])
                                        voltage, power = zip(*sorted(zip(voltage, power), key=lambda x: x[0]))
                                        self.parsed_optocalibration.append({'laser name':laser,'latest_calibration_date':latest_calibration_date,'Color':Color, 'Protocol':Protocol, 'Frequency':Frequency, 'Laser tag':laser_tag, 'Voltage':voltage, 'Power':power})
                            elif Protocol=='Constant' or Protocol=='Pulse':
                                for laser_tag in self.name_mapper['laser_tags']:
                                    voltage=[]
                                    power=[]
                                    for i in range(len(RecentLaserCalibration[Color][Protocol][f"Laser_{laser_tag}"]['LaserPowerVoltage'])):
                                        laser_voltage_power=eval(str(RecentLaserCalibration[Color][Protocol][f"Laser_{laser_tag}"]['LaserPowerVoltage'][i]))
                                        voltage.append(laser_voltage_power[0])
                                        power.append(laser_voltage_power[1])
                                    voltage, power = zip(*sorted(zip(voltage, power), key=lambda x: x[0]))
                                    self.parsed_optocalibration.append({'laser name':laser,'latest_calibration_date':latest_calibration_date,'Color':Color, 'Protocol':Protocol, 'Frequency':'None', 'Laser tag':laser_tag, 'Voltage':voltage, 'Power':power})
                        else:
                            no_calibration=True
                    else:
                        no_calibration=True
                else:
                    no_calibration=True
    
    def _FindLatestCalibrationDate(self,Laser):
        '''find the latest calibration date for the selected laser'''

        Dates=[]
        for Date in self.OptoCalibrationResults:
            if Laser in self.OptoCalibrationResults[Date].keys():
                Dates.append(Date)
        sorted_dates = sorted(Dates)
        if sorted_dates==[]:
            return 'NA'
        else:
            return sorted_dates[-1]
        
    def _get_laser_names(self):
        ''' 
        get the laser names
        '''
        self.laser_names=[]
        for stimulus_device in self.obj['stimulus_devices']:
            if 'Lasers' in stimulus_device:
                self.laser_names.append(stimulus_device)

    def _get_water_calibration(self):
        '''
        Make water calibration metadata
        '''

        if not 'water_calibration_file' in self.obj:
            self.water_calibration =[]
            return
        # load the water calibration json
        self.WaterCalibrationResults=json.load(open(self.obj['water_calibration_file']))

        self.water_calibration =[]
        self._parse_water_calibration()
        for side in self.parsed_watercalibration.keys():
            if side == 'Left':
                device_name = 'Lick spout Left'
            elif side == 'Right':
                device_name = 'Lick spout Right'
            description= f'Water calibration for {device_name}. The input is the valve open time in second and the output is the volume of water delivered in microliters.'
            self.water_calibration.append(Calibration(
                calibration_date=datetime.strptime(self.RecentWaterCalibrationDate, '%Y-%m-%d').date(),
                device_name=device_name,
                description=description ,
                input= {'valve open time (s)':self.parsed_watercalibration[side]['X']},
                output={'water volume (ul)':self.parsed_watercalibration[side]['Y']} ,
            ))

    def _parse_water_calibration(self):
        '''
        Parse the water calibration information from the json file
        '''
        sorted_dates = sorted(self.WaterCalibrationResults.keys(), key=self._custom_sort_key)
        self.RecentWaterCalibration=self.WaterCalibrationResults[sorted_dates[-1]]
        self.RecentWaterCalibrationDate=sorted_dates[-1]

        sides=self.name_mapper['sides']
        self.parsed_watercalibration={}
        for side in sides:
            self.parsed_watercalibration[side]={}
            sorted_X,sorted_Y=PlotWaterCalibration._GetWaterCalibration(self,self.WaterCalibrationResults,self.RecentWaterCalibrationDate,side)
            self.parsed_watercalibration[side]['X']=sorted_X
            self.parsed_watercalibration[side]['Y']=sorted_Y


    def _get_daqs(self):
        '''
        generate the daqs metadata
        '''
        self.daqs=[]
        for index, daq in enumerate(self.obj['daqs']):
            computer_name=self.obj[self.obj['daq_computer_name'][index]]
            if 'harp' in daq:
                harp_params=getattr(daq_class,daq)
                harp_params['computer_name']=computer_name
                self.daqs.append(HarpDevice(**harp_params))
            elif 'neuropixels' in daq:
                neuropixels_params=getattr(daq_class,daq)
                neuropixels_params['computer_name']=computer_name
                self._get_ports()
                neuropixels_params['ports']=self.ports
                self.daqs.append(NeuropixelsBasestation(**neuropixels_params))
            elif 'optogenetics' in daq:
                optogenetics_params=getattr(daq_class,daq)
                optogenetics_params['computer_name']=computer_name
                self.daqs.append(DAQDevice(**optogenetics_params))

    def _get_ports(self):
        '''
        get the probe ports related to neuropixels basestation
        '''
        self.ports=[]

        for probe in self.obj['probes']:
            self.ports.append(ProbePort(
                probes=[probe['probe_name']],
                index=probe['port_index'],
            ))

    def _get_mouse_platform(self):
        '''
        generate the mouse platform metadata
        '''
        platform_parameters=getattr(Mouse_platform_class,self.obj['mouse_platform'])
        self.mouse_platform=Tube(**platform_parameters)

    def _get_stimulus_devices(self):
        '''
        generate the stimulus devices metadata
        '''
        self.stimulus_devices=[]
        for stimulus_device in self.obj['stimulus_devices']:
            if 'reward_delivery' in stimulus_device:
                reward_delivery_params=getattr(Stimulus_devices_class,stimulus_device)
                self.stimulus_devices.append(RewardDelivery(**reward_delivery_params))
            elif 'speaker' in stimulus_device:
                speaker_params=getattr(Stimulus_devices_class,stimulus_device)
                self.stimulus_devices.append(Speaker(**speaker_params))


    def _get_stick_microscopes(self):
        '''
        generate the stick microscope metadata
        '''
        self.stick_microscopes=[]

        for ind, camera in enumerate(self.obj['stick_microscopes']):
            current_camera=self._get_camera(camera)
            current_lens=self._get_lens(camera['lens_model'])
            self.stick_microscopes.append(CameraAssembly(
                name=camera['camera_name'],
                camera=current_camera,
                camera_target=getattr(CameraTarget,camera['camera_target']),
                lens=current_lens,
            ))

    def _get_high_speed_cameras(self):
        '''
        generate the high speed camera metadata
        '''
        self.high_speed_cameras=[]

        for ind, camera in enumerate(self.obj['high_speed_cameras']):
            current_camera=self._get_camera(camera)
            current_lens=self._get_lens(camera['lens_model'])
            current_filter=self._get_filter(camera['filter_model'])
            self.high_speed_cameras.append(CameraAssembly(
                name=camera['camera_name'],
                camera=current_camera,
                camera_target=getattr(CameraTarget,camera['camera_target']),
                lens=current_lens,
                filter=current_filter
            ))

    
    def _get_filter(self,filter_model):
        '''
        get the filter metadata
        '''
        filter_parameters=getattr(Filter_class(),filter_model)
        return Filter(**filter_parameters)
    
    def _get_camera(self,current_camera):
        ''' 
        get the camera metadata
        '''
        camera_parameters=getattr(Cameras_class(),current_camera['camera_model'])
        camera_parameters['serial_number']=current_camera['serial_number']
        camera_parameters['computer_name']=self.obj[current_camera['computer_name']]
        camera_parameters['name']=current_camera['camera_name']
        return Camera(**camera_parameters)
    
    
    def _get_lens(self,lens_model):
        '''
        get the lens metadata
        '''
        lens_parameters=getattr(Lens_class(),lens_model)
        return Lens(**lens_parameters)

    def _get_modalities(self):
        '''
        generate the modalities metadata
        '''
        self.modalities = []
        for modality in self.obj['modalities']:
            self.modalities.append(getattr(Modality,modality))

    def _get_ephys_assemblies(self):
        '''
        generate the ephys assemblies metadata
        '''
        self.ephys_assemblies=[]

        for ind_probe, probe in enumerate(self.obj['probes']):
            ephys_probe=self._get_ephys_probe(probe=probe)
            self.ephys_assemblies.append(EphysAssembly(
                name='Probe Assembly '+str(ind_probe+1),
                manipulator=Manipulator(
                    name=probe['probe_name']+' Manipulator',
                    device_type="Manipulator",
                    manufacturer=NewScaleTechnologies(),
                    serial_number=probe['manipulator_serial_number'],
                ),
                probes=ephys_probe,
            ))
    

    def _get_ephys_probe(self,probe):
        '''
        generate the ephys probe metadata
        '''
        probe_more_info=getattr(Probes_class,probe['probe_model'])
        ephys_probe=[EphysProbe(
                    name=probe['probe_name'],
                    manufacturer=probe_more_info['manufacturer'],
                    probe_model=probe_more_info['name'],
                    serial_number=probe['probe_serial_number'],
                )]
        return ephys_probe
    
    def _custom_sort_key(self,key):
        if '_' in key:
            date_part, number_part = key.rsplit('_', 1)
            return (date_part, int(number_part))
        else:
            return (key, 0)
        

if __name__ == '__main__':
    generate_rig_metadata(json_file=r'E:\GitHub\CTLUT-metadata-gen\src\CTLUT_metadata_gen\fields_for_generating_rig_metadata.json')
    