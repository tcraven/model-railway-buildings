import { FunctionComponent, ReactElement } from 'react';
import { CssTransform, Dimensions, Line, Rect, Vector2D } from './types';
import { getRectStyle } from './utils';

type LinesViewProps = {
    containerDimensions: Dimensions,
    photoRect: Rect,
    cssTransform: CssTransform,
    opacity: number
};

export const LinesView: FunctionComponent<LinesViewProps> = (props): ReactElement => {
    
    // // For photo 1
    // const lines: Line[] = [
    //     { id: 0, v0: { x: -0.8388, y: 0.087 }, v1: { x: -0.835, y: 0.35 }, matchingEdgeIndex: -1 },
    //     { id: 1, v0: { x: -0.86, y: 0.4 }, v1: { x: -0.81, y: 0.55 }, matchingEdgeIndex: -1 },
    //     { id: 2, v0: { x: -0.755, y: 0.43 }, v1: { x: -0.795, y: 0.53 }, matchingEdgeIndex: -1 },
    //     { id: 3, v0: { x: -0.722, y: 0 }, v1: { x: -0.722, y: 0.36 }, matchingEdgeIndex: -1 },
    //     { id: 4, v0: { x: -0.7895, y: 0.5602 }, v1: { x: -0.6322, y: 0.542 }, matchingEdgeIndex: -1 },
    //     { id: 5, v0: { x: -0.5989, y: 0.3898 }, v1: { x: -0.5972, y: 0.2389 }, matchingEdgeIndex: -1 },
    //     { id: 6, v0: { x: -0.7223, y: 0.4115 }, v1: { x: -0.6259, y: 0.4385 }, matchingEdgeIndex: -1 },
    //     { id: 7, v0: { x: -0.6041, y: 0.4467 }, v1: { x: -0.443, y: 0.5948 }, matchingEdgeIndex: -1 },
    //     { id: 8, v0: { x: -0.5393, y: 0.5748 }, v1: { x: -0.4616, y: 0.6042 }, matchingEdgeIndex: -1 },
    //     { id: 9, v0: { x: -0.4163, y: 0.596 }, v1: { x: -0.294, y: 0.4514 }, matchingEdgeIndex: -1 },
    //     { id: 10, v0: { x: -0.4198, y: 0.3795 }, v1: { x: 0.0321, y: 0.4694 }, matchingEdgeIndex: -1 },
    //     { id: 11, v0: { x: -0.6223, y: 0.1985 }, v1: { x: -0.4595, y: 0.3507 }, matchingEdgeIndex: -1 },
    //     { id: 12, v0: { x: -0.5964, y: 0.1976 }, v1: { x: -0.1286, y: 0.2399 }, matchingEdgeIndex: -1 },
    //     { id: 13, v0: { x: -0.0986, y: 0.1143 }, v1: { x: -0.1003, y: -0.1295 }, matchingEdgeIndex: -1 },
    //     { id: 14, v0: { x: -0.0926, y: 0.2561 }, v1: { x: 0.0994, y: 0.4613 }, matchingEdgeIndex: -1 },
    //     { id: 15, v0: { x: 0.1345, y: 0.4551 }, v1: { x: 0.2879, y: 0.2623 }, matchingEdgeIndex: -1 },
    //     { id: 16, v0: { x: 0.1172, y: 0.4106 }, v1: { x: 0.2254, y: 0.2703 }, matchingEdgeIndex: -1 }
    // ];

    // For photo 4
    const lines: Line[] = [
        { id: 0, v0: { x: -0.4766, y: 0.5128 }, v1: { x: -0.0627, y: 0.6932 }, matchingEdgeIndex: -1 },
        { id: 1, v0: { x: -0.7202, y: 0.3471 }, v1: { x: -0.1571, y: 0.5704 }, matchingEdgeIndex: -1 },
        { id: 2, v0: { x: -0.1234, y: 0.5899 }, v1: { x: 0.0375, y: 0.7196 }, matchingEdgeIndex: -1 },
        { id: 3, v0: { x: 0.0638, y: 0.7088 }, v1: { x: 0.1837, y: 0.4885 }, matchingEdgeIndex: -1 },
        { id: 4, v0: { x: 0.0404, y: 0.6659 }, v1: { x: 0.1589, y: 0.4573 }, matchingEdgeIndex: -1 },
        { id: 5, v0: { x: -0.702, y: 0.2925 }, v1: { x: -0.6996, y: -0.0603 }, matchingEdgeIndex: -1 },
        { id: 6, v0: { x: -0.145, y: 0.4799 }, v1: { x: -0.1364, y: -0.0471 }, matchingEdgeIndex: -1 },
        { id: 7, v0: { x: 0.1676, y: 0.3712 }, v1: { x: 0.1738, y: 0.0183 }, matchingEdgeIndex: -1 },
        { id: 8, v0: { x: 0.3198, y: 0.1774 }, v1: { x: 0.316, y: 0.3657 }, matchingEdgeIndex: -1 },
        { id: 9, v0: { x: 0.2156, y: 0.4286 }, v1: { x: 0.3446, y: 0.3805 }, matchingEdgeIndex: -1 },
        { id: 10, v0: { x: 0.3309, y: 0.2632 }, v1: { x: 0.5027, y: 0.2203 }, matchingEdgeIndex: -1 },
        { id: 11, v0: { x: 0.3643, y: 0.145 }, v1: { x: 0.5665, y: 0.1158 }, matchingEdgeIndex: -1 },
        { id: 12, v0: { x: -0.6572, y: 0.0217 }, v1: { x: -0.5978, y: 0.1627 }, matchingEdgeIndex: -1 },
        { id: 13, v0: { x: -0.5873, y: 0.1781 }, v1: { x: -0.4863, y: 0.1683 }, matchingEdgeIndex: -1 },
        { id: 14, v0: { x: -0.5852, y: 0.1557 }, v1: { x: -0.5158, y: 0.0351 }, matchingEdgeIndex: -1 },
        { id: 15, v0: { x: -0.6188, y: -0.1451 }, v1: { x: -0.6209, y: -0.0259 }, matchingEdgeIndex: -1 },
        { id: 16, v0: { x: -0.5058, y: 0.0021 }, v1: { x: -0.5042, y: -0.089 }, matchingEdgeIndex: -1 },
        { id: 17, v0: { x: -0.606, y: 0.0534 }, v1: { x: -0.5797, y: 0.1168 }, matchingEdgeIndex: -1 }
    ];
    
    // { id: 4, v0: XXX, v1: XXX, matchingEdgeIndex: -1 },

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
                ...getRectStyle(props.photoRect, props.containerDimensions),
                transform: `translate(${props.cssTransform.x}px, ${-props.cssTransform.y}px) scale(${props.cssTransform.scale})`,
                opacity: props.opacity
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
