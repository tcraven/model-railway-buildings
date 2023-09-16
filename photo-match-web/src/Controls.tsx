import { FunctionComponent, ReactElement } from 'react';
import { ControlMode } from './types';

type ControlsProps = {
    controlMode: string;
    setControlMode: (controlMode: string) => void;
};

export const Controls: FunctionComponent<ControlsProps> = (props): ReactElement => {
    return (
        <div className="pm-controls">
            <button
                className="pm-button"
                onClick={() => {
                    props.setControlMode(
                        (props.controlMode === ControlMode.ORBIT_3D) ?
                            ControlMode.PAN_ZOOM_2D : ControlMode.ORBIT_3D
                    );
                }}
            >
                {props.controlMode}
            </button>
        </div>
    );
};
