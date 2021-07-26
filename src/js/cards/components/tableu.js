import React from 'react'
import { useSelector } from 'react-redux'
import get from 'lodash.get';
import map from 'lodash.map';

import { Player } from './player';

export function Tableu() {
    const status = useSelector((state) => state.status);

    var players = map(status.players, (value, key) => {
        if (key != "dealer") {
            return (
                <Player key={key} userid={key} />
            );
        }
    });

    return (
        <div>
            <Player key="dealer" userid="dealer" />
            { players }
        </div>
    )
}
