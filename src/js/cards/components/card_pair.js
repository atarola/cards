import React from 'react'

import { Card } from './card';

export function CardPair(props) {
    var first = { face: null, suit: null };
    var second = { face: null, suit: null };

    if (props.cards) {
        [first, second] = props.cards;
    }

    return (
        <div className="card-pair">
            <Card face={first.face} suit={first.suit} />
            <Card face={second.face} suit={second.suit} />
        </div>
    );
}
