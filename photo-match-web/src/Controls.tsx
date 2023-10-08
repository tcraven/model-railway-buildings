import { FunctionComponent, ReactElement } from 'react';
import { CameraMode, ControlMode } from './types';
import CropFreeIcon from '@mui/icons-material/CropFree';
import HomeIcon from '@mui/icons-material/Home';
import PanToolIcon from '@mui/icons-material/PanTool';
import EditIcon from '@mui/icons-material/Edit';
import PhotoIcon from '@mui/icons-material/Photo';
import Slider from '@mui/material/Slider';
import Stack from '@mui/material/Stack';
import ThreeDRotationIcon from '@mui/icons-material/ThreeDRotation';
import ThreeSixtyIcon from '@mui/icons-material/ThreeSixty';
import TimelineIcon from '@mui/icons-material/Timeline';
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
import { useData } from './DataContext';
import { getPhoto, getScene } from './utils';

type ControlsProps = {
    cameraMode: string;
    setCameraMode: (cameraMode: string) => void;
};

export const Controls: FunctionComponent<ControlsProps> = (props): ReactElement => {
    const { data, dispatch } = useData();
    const scene = getScene(data);
    const photo = getPhoto(scene);
    const controlMode = photo._uiData.controlMode;
    const photoOpacity = photo._uiData.photoOpacity;
    const linesOpacity = photo._uiData.linesOpacity;
    const modelOpacity = photo._uiData.modelOpacity;
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
                    value={controlMode}
                    exclusive
                    color="primary"
                    onChange={(event, newControlMode) => {
                        if (!newControlMode) {
                            return;
                        }
                        dispatch({
                            action: 'setControlMode',
                            controlMode: newControlMode
                        });
                    }}
                >
                    <ToggleButton value={ControlMode.PAN_ZOOM_2D}>
                        <PanToolIcon />
                    </ToggleButton>
                    <ToggleButton value={ControlMode.EDIT_LINES}>
                        <EditIcon />
                    </ToggleButton>
                    <ToggleButton value={ControlMode.ORBIT_3D}>
                        <ThreeDRotationIcon />
                    </ToggleButton>
                </ToggleButtonGroup>

                <OpacitySlider
                    icon={<PhotoIcon />}
                    opacity={photoOpacity}
                    onOpacityChange={(newOpacity: number) => {
                        dispatch({
                            action: 'setPhotoOpacity',
                            photoOpacity: newOpacity
                        });
                    }}
                />                

                <OpacitySlider
                    icon={<TimelineIcon />}
                    opacity={linesOpacity}
                    onOpacityChange={(newOpacity: number) => {
                        dispatch({
                            action: 'setLinesOpacity',
                            linesOpacity: newOpacity
                        });
                    }}
                />

                <OpacitySlider
                    icon={<HomeIcon />}
                    opacity={modelOpacity}
                    onOpacityChange={(newOpacity: number) => {
                        dispatch({
                            action: 'setModelOpacity',
                            modelOpacity: newOpacity
                        });
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
    opacity: number,
    onOpacityChange: (newOpacity: number) => void
};

const OpacitySlider: FunctionComponent<OpacitySliderProps> = (props): ReactElement => {
    return (
        <Stack
            direction="row"
            spacing={2}
            className="pm-slider-component"
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
