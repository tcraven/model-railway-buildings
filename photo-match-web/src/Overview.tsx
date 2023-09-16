import { FunctionComponent, ReactElement } from 'react';
import { Dimensions, Rect } from './types';
import { getDimensionsStyle, getRectStyle } from './utils';

type OverviewProps = {
    dimensions: Dimensions,
    photoRect: Rect,
    viewRect: Rect
};

export const Overview: FunctionComponent<OverviewProps> = (props): ReactElement => {
    return (
        <div
            className="pm-overview"
            style={{
                ...getDimensionsStyle(props.dimensions)
            }}
        >
            <img
                className="pm-photo"
                src="photo-1.jpg"
                alt=""
                style={{
                    ...getRectStyle(props.photoRect, props.dimensions)
                }}
            />
            <div
                className="pm-view"
                style={{
                    ...getRectStyle(props.viewRect, props.dimensions)
                }}
            />
        </div>
    );
};