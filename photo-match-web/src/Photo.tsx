import { FunctionComponent, ReactElement } from 'react';
import { Dimensions, Rect } from './types';
import { getRectStyle } from './utils';


type PhotoProps = {
    containerDimensions: Dimensions,
    boundary: Rect
};

export const Photo: FunctionComponent<PhotoProps> = (props): ReactElement => {
    return (
        <img
            className="pm-photo-img"
            src="photo-1.jpg"
            alt=""
            style={{
                ...getRectStyle(props.boundary, props.containerDimensions)
            }}
        />
    );
};
