from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration as LaunchConfig
from launch.actions import DeclareLaunchArgument as LaunchArg
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory

camera_params = {
    'debug': False,
    'compute_brightness': False,
    'dump_node_map': False,
    # set parameters defined in firefly_dl.cfg    
    'pixel_format': 'Mono8', # Mono8, BGR8
    'gain_auto': 'Continuous',
    'exposure_auto': 'Continuous',
    # 'balance_white_auto': 'Continuous', # If BGR8 selected uncomment this line{}
    'always_publish': False,
    'frame_rate_auto': 'Off',
    'frame_rate': 10.0,
    'frame_rate_enable': True,
    'trigger_mode': 'Off',
    'chunk_mode_active': True,
    'chunk_selector_frame_id': 'FrameID',
    'chunk_enable_frame_id': True,
    'chunk_selector_exposure_time': 'ExposureTime',
    'chunk_enable_exposure_time': True,
    'chunk_selector_gain': 'Gain',
    'chunk_enable_gain': True,
    'chunk_selector_timestamp': 'Timestamp',
    'chunk_enable_timestamp': True,
    }

def generate_launch_description():
    """launch firefly camera node."""
    flir_dir = get_package_share_directory('flir_spinnaker_ros2')
    config_dir = flir_dir + '/config/'
    name_arg = LaunchArg('camera_name', default_value='firefly_dl',
                         description='camera name')
    serial_arg = LaunchArg('serial', default_value="'21304524'",
                         description='serial number')
    print([LaunchConfig('serial'),'_'])
    node = Node(package='flir_spinnaker_ros2',
                executable='camera_driver_node',
                output='screen',
                name=[LaunchConfig('camera_name')],
                parameters=[camera_params,
                        {'parameter_file': config_dir + 'firefly_dl.cfg',
                         'serial_number': [LaunchConfig('serial')],
                         'camerainfo_url': 'file://'+config_dir + 'firefly_dl.yaml',
                        }],
                remappings=[('~/control', '/exposure_control/control'),],
    )
    return LaunchDescription([name_arg, serial_arg, node])
