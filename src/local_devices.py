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
    Coupling,
    Lamp,
    LightEmittingDiode
)
from aind_data_schema_models.harp_types import HarpDeviceType
from aind_data_schema_models.modalities import Modality
from aind_data_schema_models.organizations import Organization,_New_Scale_Technologies
from aind_data_schema_models.units import FrequencyUnit, PowerUnit, SizeUnit

class Probes_class():
    '''Probe models'''
    MI_ULED_PROBE = {"name":"Michigan uLED Probe (Version 1)"}
    MP_PHOTONIC_V1 = {"name":"MPI Photonic Probe (Version 1)"}
    NP_OPTO_DEMONSTRATOR = {"name":"Neuropixels Opto (Demonstrator)"}
    NP_UHD_FIXED = {"name":"Neuropixels UHD (Fixed)"}
    NP_UHD_SWITCHABLE = {"name":"Neuropixels UHD (Switchable)"}
    NP1 = {"name":"Neuropixels 1.0"}
    NP2_SINGLE_SHANK = {"name":"Neuropixels 2.0 (Single Shank)","manufacturer":Organization.IMEC}
    NP2_MULTI_SHANK = {"name":"Neuropixels 2.0 (Multi Shank)","manufacturer":Organization.IMEC}
    NP2_QUAD_BASE = {"name":"Neuropixels 2.0 (Quad Base)","manufacturer":Organization.IMEC}


class Cameras_class():
    '''Camera models'''
    BFS_U3_120S4C = {
            'detector_type': 'Camera',
            'data_interface': 'USB',
            'manufacturer': Organization.FLIR,
            'model': 'Blackfly S BFS-U3-120S4C',
            'max_frame_rate': 31,
            'sensor_width':4000,
            'sensor_height':3000,
            'sensor_format':"1/1.7",
            'sensor_format_unit':"inches",
            'chroma':"Color",
        }

    BFS_U3_04S2M = {
            "detector_type":"Camera",
            "data_interface":"USB",
            "model":"Blackfly S BFS-U3-04S2M",
            "manufacturer":Organization.FLIR,
            "max_frame_rate":522,
            "sensor_width":720,
            "sensor_height":540,
            "sensor_format":"1/2.9",
            "sensor_format_unit":"inches",
            "chroma":"Monochrome",
        }
    # Camera(**BFS_U3_120S4C)
    # Camera(**BFS_U3_04S2M)
    
class Lens_class():
    '''Lens models'''
    stick_lens = {
            'name': 'Probe Lens',
            'model': 'InfiniProbe S-25',
            'manufacturer': Organization.EDMUND_OPTICS,
        }
    #Lens(**stick_lens)
    side_camera_lens = {
            'name': 'Fujinon CF16ZA-1S 16mm 23MP 1.1" f/1.8 - f/16 C-Mount Lens',
            'model': 'CF16ZA-1S',
            'manufacturer': Organization.FUJINON,
            'focal_length': 16,
            'focal_length_unit': SizeUnit.MM,
        }
    
    bottom_camera_lens = {

            'name': 'Kowa LM25HC C-Mount 25mm Fixed Lens',
            'model': 'LM25HC',
            'manufacturer': Organization.OTHER,
            'focal_length': 25,
            'focal_length_unit': SizeUnit.MM,
        }
    
    body_camera_lens = {
            'name': 'Kowa Lens LM12HC F1.4 f12.5mm',
            'model': 'LM12HC',
            'manufacturer': Organization.OTHER,
            'focal_length': 12.5,
            'focal_length_unit': SizeUnit.MM,
        }

class Filter_class():
    '''Filter models'''

    # used for Fujinon CF16ZA-1S
    LP715_37 = {
        'name': 'LP715-37.5',
        'device_type': 'Filter',
        'filter_type': FilterType.LONGPASS,
        'manufacturer': Organization.OTHER,
        'diameter': 37.5,
        'size_unit': SizeUnit.MM,
        'cut_on_wavelength': int(715),
        'description': 'manufacturer: Midwest Optical Systems. Inc.'
    }
    #Filter(**LP715_37)

    # used for Kowa LM25HC and LM12HC
    M35 = { 
        'name': 'IR (UV/VIS Cut) M35.5 x 0.50 High Performance Machine Vision Filter',
        'device_type': 'Filter',
        'filter_type': FilterType.MULTIBAND,
        'manufacturer': Organization.EDMUND_OPTICS,
        'diameter': 35.5,
        'size_unit': SizeUnit.MM,
        'description': 'Blocking Wavelength Range (nm):200-750, 1000-1200'
    } 



class Mouse_platform_class():
    '''Mouse platform models'''
    tube={
        "name":"Tube", 
        "diameter":3.0,
        "diameter_unit":SizeUnit.CM,
    }
    #Tube(**tube)

class Motorstage_class:
    '''Motorized stage models'''
    newscale={
        "name":"Newscale stage",
        "travel":15,
        "travel_unit":SizeUnit.MM,
        "manufacturer":Organization.NEW_SCALE_TECHNOLOGIES,
    }
    # MotorizedStage(**newscale)

class Solenoid_valve_class:
    '''Solenoid valve models'''
    solenoid_valve={
        "name":"Solenoid Valve",
        "manufacturer":Organization.OTHER,
        "device_type":"Solenoid Valve"
    }
    # Device(**solenoid_valve)

class Lickspout_class:
    '''Lickspout models'''
    lickspout_left={
        "name":"Lick spout Left",
        "side":SpoutSide.LEFT,
        "spout_diameter":1.2,
        "spout_diameter_unit":SizeUnit.MM,
        "spout_position":RelativePosition(
                device_position_transformations=[
                    Translation3dTransform(translation=[0, 0, 0]),
                    Rotation3dTransform(rotation=[1, 0, 0, 0, 1, 0, 0, 0, 1])
                ],
                device_origin='None',  
                device_axes=[
                    Axis(name=AxisName.X, direction="Left"),
                    Axis(name=AxisName.Y, direction="Forward"),
                    Axis(name=AxisName.Z, direction="Down")
                ]
        ),
        "solenoid_valve":Device(**Solenoid_valve_class.solenoid_valve),
    }

    lickspout_right={
        "name":"Lick spout Right",
        "side":SpoutSide.RIGHT,
        "spout_diameter":1.2,
        "spout_diameter_unit":SizeUnit.MM,
        "spout_position":RelativePosition(
                device_position_transformations=[
                    Translation3dTransform(translation=[0, 0, 0]),
                    Rotation3dTransform(rotation=[1, 0, 0, 0, 1, 0, 0, 0, 1])
                ],
                device_origin='None',  
                device_axes=[
                    Axis(name=AxisName.X, direction="Left"),
                    Axis(name=AxisName.Y, direction="Forward"),
                    Axis(name=AxisName.Z, direction="Down")
                ]
        ),
        "solenoid_valve":Device(**Solenoid_valve_class.solenoid_valve),
    }

    #RewardSpout(**lickspout_left)
    #RewardSpout(**lickspout_right)

class Light_sources_laser_class():
    Oxxius_Lasers_473_1={
        "name":"Oxxius Laser 473-1",
        "device_type":"Laser",
        "manufacturer":Organization.OXXIUS,
        "wavelength":473,
        "wavelength_unit":SizeUnit.NM,
        "model": "L6CC-CSB-2422",
        "serial_number": "LNC-00771",
        "coupling":Coupling.SMF
    }


    Oxxius_Lasers_473_2={
        "name":"Oxxius Laser 473-2",
        "device_type":"Laser",
        "manufacturer":Organization.OXXIUS,
        "wavelength":473,
        "wavelength_unit":SizeUnit.NM,
        "model": "L6CC-CSB-2422",
        "serial_number": "LNC-00771",
        "coupling":Coupling.SMF
    }

    Oxxius_Lasers_561_1={
        "name":"Oxxius Laser 561-1",
        "device_type":"Laser",
        "manufacturer":Organization.OXXIUS,
        "wavelength":473,
        "wavelength_unit":SizeUnit.NM,
        "model": "L6CC-CSB-2422",
        "serial_number": "LNC-00771",
        "coupling":Coupling.SMF
    }

    Oxxius_Lasers_561_2={
        "name":"Oxxius Laser 561-2",
        "device_type":"Laser",
        "manufacturer":Organization.OXXIUS,
        "wavelength":473,
        "wavelength_unit":SizeUnit.NM,
        "model": "L6CC-CSB-2422",
        "serial_number": "LNC-00771",
        "coupling":Coupling.SMF
    }
    

    Oxxius_Lasers_638_1={
        "name":"Oxxius Laser 638-1",
        "device_type":"Laser",
        "manufacturer":Organization.OXXIUS,
        "wavelength":473,
        "wavelength_unit":SizeUnit.NM,
        "model": "L6CC-CSB-2422",
        "serial_number": "LNC-00771",
        "coupling":Coupling.SMF
    }

    Oxxius_Lasers_638_2={
        "name":"Oxxius Laser 638-2",
        "device_type":"Laser",
        "manufacturer":Organization.OXXIUS,
        "wavelength":473,
        "wavelength_unit":SizeUnit.NM,
        "model": "L6CC-CSB-2422",
        "serial_number": "LNC-00771",
        "coupling":Coupling.SMF
    }

    # used in 323_EPHYS1
    coherent_red={
        "name":"Coherent red",
        "device_type":"Laser",
        "manufacturer":Organization.COHERENT_SCIENTIFIC,
        "wavelength":640,
        "wavelength_unit":SizeUnit.NM,
        "serial_number": "M171024016",
        "coupling":Coupling.SMF
    }
    #Laser(**Oxxius_Lasers_473_1)

class Patch_class():
    Optogenetics_Fiber_1000={
        "model":"Optogenetics-Fiber-1000",
        "core_diameter":1000,
        "numerical_aperture":0.63,
        "manufacturer":Organization.PRIZMATIX,
        "notes":"SMA to FC"
    }

    Optogenetics_Fiber_500={
        "model":"Optogenetics-Fiber-500",
        "core_diameter":500,
        "numerical_aperture":0.63,
        "manufacturer":Organization.PRIZMATIX,
        "notes":"FC to ferrule; ferrule size 1.25mm",
    }
    
class Light_sources_led_class():
    
    IR_LED_850={
        "model":'M850L3',
        "wavelength":850,
        "wavelength_unit":SizeUnit.NM,
        "manufacturer":Organization.THORLABS,
        "notes":"This LED is used for camera illumination"
    }

    IR_LED_810={
        "model":'M810L3',
        "wavelength":810,
        "wavelength_unit":SizeUnit.NM,
        "manufacturer":Organization.THORLABS,
        "notes":"This LED is used for camera illumination"
    }

    Opetogenetics_LED_460={
        "model":'Dual-Optogenetics-LED-Blue',
        "wavelength":460,
        "wavelength_unit":SizeUnit.NM,
        "manufacturer":Organization.PRIZMATIX,
        "notes":"This LED is used for optogenetics"
    }
    #LightEmittingDiode(**)

class Stimulus_devices_class():
    '''Stimulus devices models'''
    speaker={
        "name":"Speaker",
        "manufacturer":Organization.OTHER,
        "model":"Speaker"
    }
    # Speaker(**speaker)

    reward_delivery={
        "device_type":"Reward delivery",
        "stage_type":MotorizedStage(**Motorstage_class.newscale),
        "reward_spouts":[RewardSpout(**Lickspout_class.lickspout_left),RewardSpout(**Lickspout_class.lickspout_right)]
    }
    # RewardDelivery(**reward_delivery)



class daq_class():
    '''Daq models'''
    harp_behavior_board={
        "name":"harp behavior board",
        "manufacturer":Organization.CHAMPALIMAUD,
        "harp_device_type":HarpDeviceType.BEHAVIOR,
        "is_clock_generator":False,
        "data_interface":DataInterface.USB,
    }       

    harp_sound_board={
        "name":"harp sound card",
        "manufacturer":Organization.CHAMPALIMAUD,
        "harp_device_type":HarpDeviceType.SOUND_CARD,
        "is_clock_generator":False,
        "data_interface":DataInterface.USB,
    }   

    harp_clock_board={
        "name":"harp clock synchronization board",
        "manufacturer":Organization.CHAMPALIMAUD,
        "harp_device_type":HarpDeviceType.CLOCK_SYNCHRONIZER,
        "is_clock_generator":True,
        "data_interface":DataInterface.USB,
    }

    harp_input_expander={
        "name":"harp sound amplifier",
        "manufacturer":Organization.CHAMPALIMAUD,
        "harp_device_type":HarpDeviceType.INPUT_EXPANDER,
        "is_clock_generator":False,
        "data_interface":DataInterface.USB,
    }

    harp_lickety_split_left={
        "name":"harp lickety split left",
        "manufacturer":Organization.CHAMPALIMAUD,
        "harp_device_type":HarpDeviceType.LICKETY_SPLIT,
        "is_clock_generator":False,
        "data_interface":DataInterface.USB,
    }

    harp_lickety_split_right={
        "name":"harp lickety split right",
        "manufacturer":Organization.CHAMPALIMAUD,
        "harp_device_type":HarpDeviceType.LICKETY_SPLIT,
        "is_clock_generator":False,
        "data_interface":DataInterface.USB,
    }

    #HarpDevice(**harp_behavior_board)

    neuropixels_basestation={
        "name":"neuropixel basestation",
        "manufacturer":Organization.IMEC,
        "basestation_firmware_version":"2.0168",
        "bsc_firmware_version":"1.02",
        "slot": 5,
    }
    #NeuropixelsBasestation(**neuropixels_basestation)
    
    optogenetics_nidaq_6002={
        "name":"optogenetics nidaq",
        "manufacturer":Organization.NATIONAL_INSTRUMENTS,
        "model":"USB-6002",
        "data_interface":DataInterface.USB,
    }
    #DAQDevice(**optogenetics_nidaq_6002)
