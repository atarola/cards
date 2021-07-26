import React from 'react'
import { useSelector } from 'react-redux'
import get from 'lodash.get';
import map from 'lodash.map';

import { Tableu } from './tableu';

export function Application() {
    const status = useSelector((state) => state.status);
    var page;

    switch(status.state) {
        case "SleepAction":
            page = (<div />);
            break;
        default:
            page = (<Tableu />);
    }

    return (
        <div>
            { page }
            <hr />
            <pre>
                { JSON.stringify(status, null, 5) }
            </pre>
        </div>
    )
}
