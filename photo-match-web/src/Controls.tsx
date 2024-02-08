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
import { Utils } from './Utils';
import Tooltip from '@mui/material/Tooltip';
import IconButton from '@mui/material/IconButton';
import AddLinkIcon from '@mui/icons-material/AddLink';
import LinkOffIcon from '@mui/icons-material/LinkOff';
import DeleteIcon from '@mui/icons-material/Delete';
import VideocamIcon from '@mui/icons-material/Videocam';
import Button from '@mui/material/Button';

type ControlsProps = {
    deleteEdge: () => void
    linkEdge: () => void
    unlinkEdge: () => void
    optimizeCameraTransform: () => void
};

export const Controls: FunctionComponent<ControlsProps> = (props): ReactElement => {
    const { data, dispatch } = useData();
    const scene = Utils.getScene(data);
    const photo = Utils.getPhoto(scene);
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
                        <PmTooltip text="2D Pan and Zoom">
                            <PanToolIcon />
                        </PmTooltip>
                    </ToggleButton>
                    <ToggleButton value={ControlMode.EDIT_LINES}>
                        <PmTooltip text="Edit Photo Match Lines">
                            <EditIcon />
                        </PmTooltip>
                    </ToggleButton>
                    <ToggleButton value={ControlMode.ORBIT_3D}>
                        <PmTooltip text="3D Orbit, Pan and Zoom">
                            <ThreeDRotationIcon />
                        </PmTooltip>
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
                    tooltipText="Photo Opacity"
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
                    tooltipText="Lines and Edges Opacity"
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
                    tooltipText="3D Shape Opacity"
                />

                <Stack
                    direction="row"
                    spacing={1}
                >

                    <PmTooltip text="Delete selected Photo Match Line">
                        {/* <IconButton>
                            <DeleteIcon />
                        </IconButton> */}
                        <Button
                            variant="outlined"
                            startIcon={<DeleteIcon />}
                            onClick={props.deleteEdge}
                        >
                            Delete
                        </Button>
                    </PmTooltip>

                    <PmTooltip text="Link selected Photo Match Line and 3D Shape Edge">
                        {/* <IconButton>
                            <AddLinkIcon />
                        </IconButton> */}
                        <Button
                            variant="outlined"
                            startIcon={<AddLinkIcon />}
                            onClick={props.linkEdge}
                        >
                            Link
                        </Button>
                    </PmTooltip>

                    <PmTooltip text="Unlink selected Photo Match Line from its 3D Shape Edge">
                        {/* <IconButton>
                            <LinkOffIcon />
                        </IconButton> */}
                        <Button
                            variant="outlined"
                            startIcon={<LinkOffIcon />}
                            onClick={props.unlinkEdge}
                        >
                            Unlink
                        </Button>
                    </PmTooltip>

                    <PmTooltip text="Optimize 3D Camera Transform">
                        {/* <IconButton>
                            <VideocamIcon />
                        </IconButton> */}
                        <Button
                            variant="contained"
                            startIcon={<VideocamIcon />}
                            onClick={props.optimizeCameraTransform}
                        >
                            Optimize
                        </Button>
                    </PmTooltip>

                </Stack>

                {/* <div></div> */}

            </Stack>
        </div>
    );
};

type OpacitySliderProps = {
    icon: ReactElement
    opacity: number
    onOpacityChange: (newOpacity: number) => void
    tooltipText: string
};

const OpacitySlider: FunctionComponent<OpacitySliderProps> = (props): ReactElement => {
    return (
        <Stack
            direction="row"
            spacing={2}
            className="pm-slider-component"
        >
            <PmTooltip text={props.tooltipText}>
                <div className="pm-slider-icon">
                    {props.icon}
                </div>
            </PmTooltip>
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

type PmTooltipProps = {
    children: ReactElement<any, any>
    text: string
};

const PmTooltip: FunctionComponent<PmTooltipProps> = (props): ReactElement => {
    return (
        <Tooltip
            title={
                <span className="pm-tooltip-text">{props.text}</span>
            }
            arrow
        >
            {props.children}
        </Tooltip>
    );
};
