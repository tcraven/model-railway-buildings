import { FunctionComponent, ReactElement } from 'react';
import { CameraMode, ControlMode } from './types';
import HomeIcon from '@mui/icons-material/Home';
import PanToolIcon from '@mui/icons-material/PanTool';
import PhotoIcon from '@mui/icons-material/Photo';
import Slider from '@mui/material/Slider';
import Stack from '@mui/material/Stack';
import ThreeDRotationIcon from '@mui/icons-material/ThreeDRotation';
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';

import ThreeSixtyIcon from '@mui/icons-material/ThreeSixty';
import CropFreeIcon from '@mui/icons-material/CropFree';

type ControlsProps = {
    controlMode: string;
    setControlMode: (controlMode: string) => void;
    photoOpacity: number;
    setPhotoOpacity: (photoOpacity: number) => void;
    threeViewOpacity: number;
    setThreeViewOpacity: (threeViewOpacity: number) => void;
    cameraMode: string;
    setCameraMode: (cameraMode: string) => void;
};

export const Controls: FunctionComponent<ControlsProps> = (props): ReactElement => {
    return (
        <div
            className="pm-controls"
        >
            <Stack
                className="pm-controls-stack"
                direction="row"
                spacing={3}
            >

                <ToggleButtonGroup
                    size="small"
                    value={props.controlMode}
                    exclusive
                    color="primary"
                    onChange={(event, newControlMode) => {
                        if (!newControlMode) {
                            return;
                        }
                        props.setControlMode(newControlMode);
                    }}
                >
                    <ToggleButton value={ControlMode.PAN_ZOOM_2D}>
                        <PanToolIcon />
                    </ToggleButton>
                    <ToggleButton value={ControlMode.ORBIT_3D}>
                        <ThreeDRotationIcon />
                    </ToggleButton>
                </ToggleButtonGroup>
    
                <OpacitySlider
                    className="pm-slider-component"
                    icon={<PhotoIcon />}
                    opacity={props.photoOpacity}
                    onOpacityChange={(newOpacity: number) => {
                        props.setPhotoOpacity(newOpacity);
                    }}
                />                

                <OpacitySlider
                    className="pm-slider-component"
                    icon={<HomeIcon />}
                    opacity={props.threeViewOpacity}
                    onOpacityChange={(newOpacity: number) => {
                        props.setThreeViewOpacity(newOpacity);
                    }}
                />

                <ToggleButtonGroup
                    size="small"
                    value={props.cameraMode}
                    exclusive
                    color="primary"
                    onChange={(event, newCameraMode) => {
                        if (!newCameraMode) {
                            return;
                        }
                        props.setCameraMode(newCameraMode);
                    }}
                >
                    <ToggleButton value={CameraMode.FREE}>
                        <CropFreeIcon />
                    </ToggleButton>
                    <ToggleButton value={CameraMode.ORBIT}>
                        <ThreeSixtyIcon />
                    </ToggleButton>
                </ToggleButtonGroup>

                <div></div>

            </Stack>
        </div>
    );
};

type OpacitySliderProps = {
    icon: ReactElement,
    className?: string,
    opacity: number,
    onOpacityChange: (newOpacity: number) => void
};

const OpacitySlider: FunctionComponent<OpacitySliderProps> = (props): ReactElement => {
    return (
        <Stack
            direction="row"
            spacing={2}
            className={props.className}
        >
            <div className="pm-slider-icon">
                {props.icon}
            </div>
            <Slider
                className="pm-slider"
                size="small"
                value={props.opacity}
                onChange={(event, newOpacity) => {
                    props.onOpacityChange(newOpacity as number);
                }}
                step={0.01}
                // marks={true}
                min={0}
                max={1}
            />
        </Stack>
    );
};
