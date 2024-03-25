import { FunctionComponent, ReactElement } from 'react';
import { useData } from './DataContext';
import { Utils } from './Utils';
import { PhotoList } from './PhotoList';
import MenuItem from '@mui/material/MenuItem';
import Select, { SelectChangeEvent } from '@mui/material/Select';

export const Sidebar: FunctionComponent = (): ReactElement => {
    const { data, dispatch } = useData();

    const sceneId = data._uiData.sceneId;

    const onSceneChange = (event: SelectChangeEvent) => {
        dispatch({
            action: 'setSceneId',
            sceneId: parseInt(event.target.value)
        });
    };

    return (
        <div>
            <div className="pm-scene-select-container">
                <Select
                    value={sceneId.toString()}
                    onChange={onSceneChange}
                >
                    {data.scenes.map((scene) => {
                        return (
                            <MenuItem
                                key={scene.id}
                                value={scene.id.toString()}
                            >
                                {scene.name}
                            </MenuItem>
                        );
                    })}
                </Select>
            </div>
            <PhotoList />
        </div>
    );
};
