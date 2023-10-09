import { FunctionComponent, ReactElement } from 'react';
import { CssTransform, Dimensions, Rect, Vector2D } from './types';
import { Utils } from './Utils';
import { useData } from './DataContext';

type LinesViewProps = {
    containerDimensions: Dimensions,
    photoRect: Rect,
    cssTransform: CssTransform
};

export const LinesView: FunctionComponent<LinesViewProps> = (props): ReactElement => {

    const { data, dispatch } = useData();
    const scene = Utils.getScene(data);
    const photo = Utils.getPhoto(scene);
    const linesOpacity = photo._uiData.linesOpacity;
    const lines = photo.lines;

    const toSvgVector = (v: Vector2D): Vector2D => {
        return {
            x: 0.5 * props.photoRect.width + v.x * 0.5 * props.photoRect.width,
            y: 0.5 * props.photoRect.height - v.y * 0.5 * props.photoRect.height
        };
    };

    const lineStyle = {
        stroke: '#07f',
        strokeWidth: 2
    };
    const nodeStyle = {
        stroke: '#07f',
        strokeWidth: '2',
        fill: '#fff'
    };
    const nodeRadius = 4;

    return (
        <svg
            className="pm-lines-view"
            width={props.photoRect.width}
            height={props.photoRect.height}
            style={{
                ...Utils.getRectStyle(props.photoRect, props.containerDimensions),
                transform: `translate(${props.cssTransform.x}px, ${-props.cssTransform.y}px) scale(${props.cssTransform.scale})`,
                opacity: linesOpacity
            }}
        >
            {lines.map((line, index) => {
                const lv0 = toSvgVector(line.v0);
                const lv1 = toSvgVector(line.v1);
                return (
                    <g key={index}>
                        <line
                            style={lineStyle}
                            x1={lv0.x}
                            y1={lv0.y}
                            x2={lv1.x}
                            y2={lv1.y}
                        />
                        <circle
                            cx={lv0.x}
                            cy={lv0.y}
                            r={nodeRadius}
                            style={nodeStyle}
                        />
                        <circle
                            cx={lv1.x}
                            cy={lv1.y}
                            r={nodeRadius}
                            style={nodeStyle}
                        />
                    </g>
                );
            })}
        </svg>
    );
};
