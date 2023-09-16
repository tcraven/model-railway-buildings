import { FunctionComponent, ReactElement } from 'react';
import { Rect } from './types';

type LinesProps = {
    boundary: Rect;
};

export const Lines: FunctionComponent<LinesProps> = (props): ReactElement => {
    return (
        <div
            className="pm-lines"
            style={{}}
        >
            Lines
        </div>
    );
};
