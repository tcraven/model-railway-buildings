import { FunctionComponent, ReactElement } from 'react';
import { PhotoImage } from './types';
import { getRectStyle } from './utils';


type PhotoListProps = {
    photoImages: PhotoImage[],
    photoIndex: number,
    setPhotoIndex: (photoIndex: number) => void;
};

export const PhotoList: FunctionComponent<PhotoListProps> = (props): ReactElement => {
    return (
        <div className="pm-photo-list">
            {props.photoImages.map((photoImage, index) => {
                let className = 'pm-photo-image';
                if (index === props.photoIndex) {
                    className += ' pm-photo-image-selected';
                }
                return (
                    <div
                        className="pm-photo-image-container"
                        key={index}
                        onClick={() => {
                            props.setPhotoIndex(index);
                        }}
                    >
                        <img
                            className={className}
                            src={photoImage.url}
                            alt=""
                        />
                    </div>
                );
            })}
        </div>
    );
};
