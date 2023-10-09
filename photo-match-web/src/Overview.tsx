import { FunctionComponent, ReactElement } from 'react';
import { Dimensions, Rect } from './types';
import { Utils } from './Utils';

type OverviewProps = {
    dimensions: Dimensions,
    photoRect: Rect,
    viewRect: Rect,
    photoImageUrl: string
};

export const Overview: FunctionComponent<OverviewProps> = (props): ReactElement => {
    return (
        <div
            className="pm-overview"
            style={{
                ...Utils.getDimensionsStyle(props.dimensions)
            }}
        >
            <img
                className="pm-photo"
                src={props.photoImageUrl}
                alt=""
                style={{
                    ...Utils.getRectStyle(props.photoRect, props.dimensions)
                }}
            />
            <div
                className="pm-view"
                style={{
                    ...Utils.getRectStyle(props.viewRect, props.dimensions)
                }}
            />
        </div>
    );
};
