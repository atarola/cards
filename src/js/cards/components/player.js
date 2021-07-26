import React from 'react'
import { useSelector } from 'react-redux'
import get from 'lodash.get';

import { CardPair } from './card_pair';
import { Buttons } from './buttons';

export function Player(props) {
    const status = useSelector((state) => state.status);
    var cards = get(status, `players.${props.userid}.cards`, null);

    return (
        <div className="player-spot">
            <div>{ (props.userid == "dealer") ? "Dealer" : "Player" }</div>
            <CardPair cards={cards} />
            <Buttons userid={props.userid} />
        </div>
    );
}
