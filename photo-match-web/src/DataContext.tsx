import { FunctionComponent, PropsWithChildren, ReactElement, useCallback, useEffect, useRef } from 'react';
import { createContext, Dispatch, useContext, useReducer } from 'react';
import { throttle } from 'throttle-debounce';
import { Data, ViewTransform } from './types';
import { getPhoto, getScene } from './utils';

type InitAction = {
    action: 'init'
    data: Data
};

type SetPhotoIdAction = {
    action: 'setPhotoId'
    photoId: number
};

type SetViewTransformAction = {
    action: 'setViewTransform'
    viewTransform: ViewTransform
};

type SetControlModeAction = {
    action: 'setControlMode'
    controlMode: string
};

type SetPhotoOpacityAction = {
    action: 'setPhotoOpacity'
    photoOpacity: number
};

type SetLinesOpacityAction = {
    action: 'setLinesOpacity'
    linesOpacity: number
};

type SetModelOpacityAction = {
    action: 'setModelOpacity'
    modelOpacity: number
};

type DataAction = 
    InitAction |
    SetPhotoIdAction |
    SetViewTransformAction |
    SetControlModeAction |
    SetPhotoOpacityAction |
    SetLinesOpacityAction |
    SetModelOpacityAction;

type DataAndDispatch = {
    data: Data
    dispatch: Dispatch<DataAction>
};

const emptyData = (): Data => {
    return {
        _metadata: {
            version: -1,
            isReady: false
        },
        _uiData: {
            sceneId: -1
        },
        scenes: []
    };
};

const DataContext = createContext<DataAndDispatch>({
    data: emptyData(),
    dispatch: (action: DataAction): void => {}
});

type DataProviderProps = PropsWithChildren<{}>;

export const DataProvider: FunctionComponent<DataProviderProps> = (props): ReactElement => {

    const [ data, dispatch ] = useReducer(
        dataReducer,
        emptyData()
    );

    const dataAndDispatch = {
        data: data,
        dispatch: dispatch
    };

    const sleep = async (ms: number) => {
        return new Promise(resolve => setTimeout(resolve, ms));
    };

    // Load initial data on mount
    useEffect(() => {
        const fetchData = async () => {
            // TO DO: Remove
            await sleep(1000);

            let resp = await fetch('http://localhost:5007/data', {
                method: 'GET'
            });
            let data = await resp.json();

            dispatch({
                action: 'init',
                data: data
            });
        };

        fetchData();
    },
    []);

    // When data changes, and the data is ready, and this isn't the
    // initial data (first time being ready), then save the data
    const saveData = useCallback(
        throttle(2000, async (data: Data) => {
            const bodyStr = JSON.stringify(data);
            // console.log('saveData', bodyStr);
            await fetch('http://localhost:5007/data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: bodyStr
            });
            // console.log('ZZZ fetch finished');
        }),
        []
    );
    const isFirstReady = useRef(true);
    useEffect(() => {
        if (!data._metadata.isReady) {
            return;
        }
        if (isFirstReady.current) {
            isFirstReady.current = false;
            return;
        }
        saveData(data);
    },
    [ data, saveData ]);

    return (
        <DataContext.Provider value={dataAndDispatch}>
            {props.children}
        </DataContext.Provider>
    );
};

export const useData = (): DataAndDispatch => {
    return useContext(DataContext);
};

const getNextId = (items: { id: number }[]): number => {
    if (items.length === 0) {
        return 0;
    }
    return Math.max(...items.map(t => t.id)) + 1;
};

const setPhotoId = (data: Data, action: SetPhotoIdAction): Data => {
    const newData = { ...data };
    newData._metadata.version += 1;
    const scene = getScene(newData);
    if (!scene) {
        throw Error();
    }
    scene._uiData.photoId = action.photoId;
    return newData;
};

const _getNewData = (data: Data): Data => {
    const newData = { ...data };
    newData._metadata.version += 1;
    return newData;
};

const _getPhoto = (newData: Data) => {
    const scene = getScene(newData);
    return getPhoto(scene);
};

const setViewTransform = (data: Data, action: SetViewTransformAction): Data => {
    const newData = _getNewData(data);
    const photo = _getPhoto(newData);
    photo._uiData.viewTransform = action.viewTransform;
    return newData;
};

const setControlMode = (data: Data, action: SetControlModeAction): Data => {
    const newData = _getNewData(data);
    const photo = _getPhoto(newData);
    photo._uiData.controlMode = action.controlMode;
    return newData;
};

const setPhotoOpacity = (data: Data, action: SetPhotoOpacityAction): Data => {
    const newData = _getNewData(data);
    const photo = _getPhoto(newData);
    photo._uiData.photoOpacity = action.photoOpacity;
    return newData;
};

const setLinesOpacity = (data: Data, action: SetLinesOpacityAction): Data => {
    const newData = _getNewData(data);
    const photo = _getPhoto(newData);
    photo._uiData.linesOpacity = action.linesOpacity;
    return newData;
};

const setModelOpacity = (data: Data, action: SetModelOpacityAction): Data => {
    const newData = _getNewData(data);
    const photo = _getPhoto(newData);
    photo._uiData.modelOpacity = action.modelOpacity;
    return newData;
};

const dataReducer = (data: Data, action: DataAction): Data => {
    switch (action.action) {
        case 'init':
            return {
                ...action.data,
                _metadata: {
                    ...action.data._metadata,
                    isReady: true
                }
            };
        
        case 'setPhotoId':
            return setPhotoId(data, action);
        
        case 'setViewTransform':
            return setViewTransform(data, action);
        
        case 'setControlMode':
            return setControlMode(data, action);
        
        case 'setPhotoOpacity':
            return setPhotoOpacity(data, action);
            
        case 'setLinesOpacity':
            return setLinesOpacity(data, action);

        case 'setModelOpacity':
            return setModelOpacity(data, action);
        
        default: {
            throw Error('Unknown action');
        }
    }
};
