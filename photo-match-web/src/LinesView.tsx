import { FunctionComponent, ReactElement } from 'react';
import { CssTransform, Dimensions, DrawNewLineInfo, Rect, Vector2D } from './types';
import { Utils } from './Utils';
import { useData } from './DataContext';

type LinesViewProps = {
    containerDimensions: Dimensions,
    photoRect: Rect,
    cssTransform: CssTransform,
    drawNewLineInfo: DrawNewLineInfo | null
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

    let nlv0 = null;
    let nlv1 = null;
    if (props.drawNewLineInfo !== null) {
        nlv0 = toSvgVector(props.drawNewLineInfo.v0);
        nlv1 = toSvgVector(props.drawNewLineInfo.v1);
    }

    const lineStyle = {
        stroke: '#07f',
        strokeWidth: 2
    };
    const nodeStyle = {
        stroke: '#07f',
        strokeWidth: 2,
        fill: '#fff'
    };
    const nodeRadius = 4;

    const selectedLineStyle = {
        stroke: '#fff',
        strokeWidth: 2
    };
    const selectedNodeStyle = {
        stroke: '#fff',
        strokeWidth: 2,
        fill: '#000'
    };
    const selectedNodeRadius = 4;

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
                const isSelected = (photo._uiData.lineId === line.id);
                return (
                    <SvgLine
                        key={index}
                        v0={lv0}
                        v1={lv1}
                        lineStyle={isSelected ? selectedLineStyle : lineStyle}
                        nodeStyle={isSelected ? selectedNodeStyle : nodeStyle}
                        nodeRadius={isSelected ? selectedNodeRadius : nodeRadius}                            
                    />
                );
            })}

            {nlv0 !== null && nlv1 !== null &&
                <SvgLine
                    v0={nlv0}
                    v1={nlv1}
                    lineStyle={lineStyle}
                    nodeStyle={nodeStyle}
                    nodeRadius={nodeRadius}                            
                />
            }
        </svg>
    );
};

type SvgLineProps = {
    v0: Vector2D
    v1: Vector2D
    lineStyle: any
    nodeStyle: any
    nodeRadius: number
};

const SvgLine: FunctionComponent<SvgLineProps> = (props): ReactElement => {
    return (
        <g>
            <line
                style={props.lineStyle}
                x1={props.v0.x}
                y1={props.v0.y}
                x2={props.v1.x}
                y2={props.v1.y}
            />
            <circle
                cx={props.v0.x}
                cy={props.v0.y}
                r={props.nodeRadius}
                style={props.nodeStyle}
            />
            <circle
                cx={props.v1.x}
                cy={props.v1.y}
                r={props.nodeRadius}
                style={props.nodeStyle}
            />
        </g>
    );
};
