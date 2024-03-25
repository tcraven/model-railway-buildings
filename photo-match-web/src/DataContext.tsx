import { FunctionComponent, PropsWithChildren, ReactElement, useCallback, useEffect, useRef } from 'react';
import { createContext, Dispatch, useContext, useReducer } from 'react';
import { throttle } from 'throttle-debounce';
import { CameraOrbitTransform, CameraTransform, Data, LineEndpoint, Vector2D, ViewTransform } from './types';
import { Utils } from './Utils';

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

type SetCameraTransformAction = {
    action: 'setCameraTransform'
    cameraTransform: CameraTransform
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

type SetLineEndpointPositionAction = {
    action: 'setLineEndpointPosition'
    lineEndpoint: LineEndpoint
    position: Vector2D
}

type SetLineIdAction = {
    action: 'setLineId'
    lineId: number | null
}

type SetShapeEdgeIdsAction = {
    action: 'setShapeEdgeIds'
    shapeId: number | null
    edgeId: number | null
};

type LinkPhotoMatchLineAndShapeEdgeAction = {
    action: 'linkPhotoMatchLineAndShapeEdge'
    lineId: number
    shapeId: number
    edgeId: number
};

type AddPhotoMatchLineAction = {
    action: 'addPhotoMatchLine'
    v0: Vector2D
    v1: Vector2D
};

type DeletePhotoMatchLineAction = {
    action: 'deletePhotoMatchLine'
    lineId: number
};

type SetShapeModeAction = {
    action: 'setShapeMode'
    shapeMode: string
};

type SetCameraOrbitTransformAction = {
    action: 'setCameraOrbitTransform'
    cameraTransform: CameraTransform
    cameraOrbitTransform: CameraOrbitTransform
};

type SetSceneIdAction = {
    action: 'setSceneId'
    sceneId: number
};

type DataAction = 
    InitAction |
    SetPhotoIdAction |
    SetViewTransformAction |
    SetCameraTransformAction |
    SetControlModeAction |
    SetPhotoOpacityAction |
    SetLinesOpacityAction |
    SetModelOpacityAction |
    SetLineEndpointPositionAction |
    SetLineIdAction |
    SetShapeEdgeIdsAction |
    LinkPhotoMatchLineAndShapeEdgeAction |
    AddPhotoMatchLineAction |
    DeletePhotoMatchLineAction |
    SetShapeModeAction |
    SetCameraOrbitTransformAction |
    SetSceneIdAction;

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
            await fetch('http://localhost:5007/data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: bodyStr
            });
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

// const getNextId = (items: { id: number }[]): number => {
//     if (items.length === 0) {
//         return 0;
//     }
//     return Math.max(...items.map(t => t.id)) + 1;
// };

const setPhotoId = (data: Data, action: SetPhotoIdAction): Data => {
    const newData = { ...data };
    newData._metadata.version += 1;
    const scene = Utils.getScene(newData);
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
    const scene = Utils.getScene(newData);
    return Utils.getPhoto(scene);
};

const setViewTransform = (data: Data, action: SetViewTransformAction): Data => {
    const newData = _getNewData(data);
    const photo = _getPhoto(newData);
    photo._uiData.viewTransform = action.viewTransform;
    return newData;
};

const setCameraTransform = (data: Data, action: SetCameraTransformAction): Data => {
    const newData = _getNewData(data);
    const photo = _getPhoto(newData);
    photo._uiData.cameraTransform = action.cameraTransform;
    photo._uiData.cameraOrbitTransform = null;
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

const setLineEndpointPosition = (data: Data, action: SetLineEndpointPositionAction): Data => {
    const newData = _getNewData(data);
    const photo = _getPhoto(newData);
    const line = photo.lines.find(l => l.id === action.lineEndpoint.id);
    if (line === undefined) {
        throw new Error(`Photo match line not found for ID: ${action.lineEndpoint.id}`);
    }
    if (action.lineEndpoint.endpointIndex === 0) {
        line.v0 = action.position;
    }
    if (action.lineEndpoint.endpointIndex === 1) {
        line.v1 = action.position;
    }
    return newData;
};

const setLineId = (data: Data, action: SetLineIdAction): Data => {
    const newData = _getNewData(data);
    const photo = _getPhoto(newData);
    photo._uiData.lineId = action.lineId;
    return newData;
};

const setShapeEdgeIds = (data: Data, action: SetShapeEdgeIdsAction): Data => {
    const newData = _getNewData(data);
    const photo = _getPhoto(newData);
    photo._uiData.selectedShapeId = action.shapeId;
    photo._uiData.selectedEdgeId = action.edgeId;
    return newData;
};

const linkPhotoMatchLineAndShapeEdge = (data: Data, action: LinkPhotoMatchLineAndShapeEdgeAction): Data => {
    const newData = _getNewData(data);
    const photo = _getPhoto(newData);
    // TO DO: Get line by ID, not index directly! (deleted lines then added new ones so IDs don't match indexes any more)
    // const line = photo.lines[action.lineId];
    const line = photo.lines.find(l => l.id === action.lineId);
    if (line === undefined) {
        throw new Error(`Photo match line not found for ID: ${action.lineId}`);
    }
    line.matchingShapeId = action.shapeId;
    line.matchingEdgeId = action.edgeId;
    return newData;
};

const addPhotoMatchLine = (data: Data, action: AddPhotoMatchLineAction): Data => {
    const newData = _getNewData(data);
    const photo = _getPhoto(newData);

    let nextLineId = 0;
    if (photo.lines.length > 0) {
        const lastLine = photo.lines[photo.lines.length - 1];
        nextLineId = lastLine.id + 1;
    }
    photo.lines.push({
        id: nextLineId,
        v0: action.v0,
        v1: action.v1,
        matchingShapeId: -1,
        matchingEdgeId: -1
    });
    return newData;
};

const deletePhotoMatchLine = (data: Data, action: DeletePhotoMatchLineAction): Data => {
    const newData = _getNewData(data);
    const photo = _getPhoto(newData);
    photo.lines = photo.lines.filter(l => l.id !== action.lineId);
    return newData;
};

const setShapeMode = (data: Data, action: SetShapeModeAction): Data => {
    const newData = _getNewData(data);
    const photo = _getPhoto(newData);
    photo._uiData.shapeMode = action.shapeMode;
    return newData;
};

const setCameraOrbitTransform = (data: Data, action: SetCameraOrbitTransformAction): Data => {
    const newData = _getNewData(data);
    const photo = _getPhoto(newData);
    photo._uiData.cameraTransform = action.cameraTransform;
    photo._uiData.cameraOrbitTransform = action.cameraOrbitTransform;
    return newData;
};

const setSceneId = (data: Data, action: SetSceneIdAction): Data => {
    const newData = _getNewData(data);
    data._uiData.sceneId = action.sceneId;
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
        
        case 'setCameraTransform':
            return setCameraTransform(data, action);
        
        case 'setControlMode':
            return setControlMode(data, action);
        
        case 'setPhotoOpacity':
            return setPhotoOpacity(data, action);
            
        case 'setLinesOpacity':
            return setLinesOpacity(data, action);

        case 'setModelOpacity':
            return setModelOpacity(data, action);
        
        case 'setLineEndpointPosition':
            return setLineEndpointPosition(data, action);
        
        case 'setLineId':
            return setLineId(data, action);
        
        case 'setShapeEdgeIds':
            return setShapeEdgeIds(data, action);
        
        case 'linkPhotoMatchLineAndShapeEdge':
            return linkPhotoMatchLineAndShapeEdge(data, action);
        
        case 'addPhotoMatchLine':
            return addPhotoMatchLine(data, action);
        
        case 'deletePhotoMatchLine':
            return deletePhotoMatchLine(data, action);

        case 'setShapeMode':
            return setShapeMode(data, action);
        
        case 'setCameraOrbitTransform':
            return setCameraOrbitTransform(data, action);
        
        case 'setSceneId':
            return setSceneId(data, action);
        
        default: {
            throw Error('Unknown action');
        }
    }
};
