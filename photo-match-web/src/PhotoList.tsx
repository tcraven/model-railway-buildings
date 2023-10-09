import { FunctionComponent, ReactElement } from 'react';
import { useData } from './DataContext';
import { Utils } from './Utils';

export const PhotoList: FunctionComponent = (): ReactElement => {
    const { data, dispatch } = useData();
    const scene = Utils.getScene(data);
    const photoId = Utils.getPhotoId(scene);
    return (
        <div className="pm-photo-list">
            {scene.photos.map((photo) => {
                let className = 'pm-photo-image';
                if (photo.id === photoId) {
                    className += ' pm-photo-image-selected';
                }
                return (
                    <div
                        className="pm-photo-image-container"
                        key={photo.id}
                        onClick={() => {
                            dispatch({
                                action: 'setPhotoId',
                                photoId: photo.id
                            });
                        }}
                    >
                        <img
                            className={className}
                            src={Utils.getFileUrl(photo.filename)}
                            alt=""
                        />
                    </div>
                );
            })}
        </div>
    );
};
