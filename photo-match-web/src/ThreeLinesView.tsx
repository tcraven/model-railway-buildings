import { FunctionComponent, ReactElement } from 'react';
import { CssTransform, Dimensions, Rect, ShapeEdgeLine, Vector2D } from './types';
import { Utils } from './Utils';

type ThreeLinesViewProps = {
    containerDimensions: Dimensions
    photoRect: Rect
    cssTransform: CssTransform
    shapeEdgeLines: ShapeEdgeLine[]
    selectedPhotoMatchLineId: number | null
    selectedShapeId: number | null
    selectedEdgeId: number | null
    linesOpacity: number
};

export const ThreeLinesView: FunctionComponent<ThreeLinesViewProps> = (props): ReactElement => {

    const toSvgVector = (v: Vector2D): Vector2D => {
        return {
            x: 0.5 * props.photoRect.width + v.x * 0.5 * props.photoRect.width,
            y: 0.5 * props.photoRect.height - v.y * 0.5 * props.photoRect.height
        };
    };

    const lineStyle = {
        stroke: '#f70',
        strokeWidth: 2
    };
    const matchingLineStyle = {
        stroke: '#ffd6b2',
        strokeWidth: 2
    };
    const selectedLineStyle = {
        stroke: '#fff',
        strokeWidth: 2
    };

    return (
        <svg
            className="pm-three-lines-view"
            width={props.photoRect.width}
            height={props.photoRect.height}
            style={{
                ...Utils.getRectStyle(props.photoRect, props.containerDimensions),
                transform: `translate(${props.cssTransform.x}px, ${-props.cssTransform.y}px) scale(${props.cssTransform.scale})`,
                opacity: props.linesOpacity
            }}
        >
            {props.shapeEdgeLines.map((shapeEdgeLine, index) => {
                const isSelected = (shapeEdgeLine.shapeId === props.selectedShapeId && shapeEdgeLine.edgeId === props.selectedEdgeId);
                const isVisible = (shapeEdgeLine.photoMatchLineId !== -1) || isSelected;
                const isMatching = (shapeEdgeLine.photoMatchLineId === props.selectedPhotoMatchLineId);
                if (!isVisible) {
                    return null;
                }
                let _lineStyle = lineStyle;
                if (isSelected) {
                    _lineStyle = selectedLineStyle;
                }
                else if (isMatching) {
                    _lineStyle = matchingLineStyle;
                }
                const lv0 = toSvgVector(shapeEdgeLine.v0);
                const lv1 = toSvgVector(shapeEdgeLine.v1);
                return (
                    <g key={index}>
                        <line
                            style={_lineStyle}
                            x1={lv0.x}
                            y1={lv0.y}
                            x2={lv1.x}
                            y2={lv1.y}
                        />
                    </g>
                );
            })}
        </svg>
    );
};
