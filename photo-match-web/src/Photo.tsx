import { FunctionComponent, ReactElement } from 'react';
import { Dimensions, Rect } from './types';
import { getRectStyle } from './utils';


type PhotoProps = {
    containerDimensions: Dimensions,
    boundary: Rect,
    opacity: number,
    imageUrl: string
};

export const Photo: FunctionComponent<PhotoProps> = (props): ReactElement => {
    return (
        <img
            className="pm-photo-img"
            src={props.imageUrl}
            alt=""
            style={{
                ...getRectStyle(props.boundary, props.containerDimensions),
                opacity: props.opacity
            }}
        />
    );
};
