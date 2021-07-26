import React from 'react'

export function Card(props) {
    var src, alt;

    if (props.face && props.suit) {
        src = `/static/${props.face}_${props.suit}_white.png`;
        alt = `${props.face} of ${props.suit}`;
    } else {
        src = `/static/back_black_basic_white.png`;
        alt = `card back`;
    }

    return (
        <img className="card" src={src} alt={alt} />
    );
}
