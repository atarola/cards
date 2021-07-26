import React from 'react'
import { useSelector } from 'react-redux'
import get from 'lodash.get';

import { validate } from '../websocket';

export function Buttons(props) {
    const userid = useSelector((state) => state.userid);
    const status = useSelector((state) => state.status);

    const verified = get(status, `players.${props.userid}.verified`, false);
    const score = get(status, `players.${props.userid}.value`, 0);

    if (status.state != "VerifyAction" || props.userid != userid) {
        return null;
    }

    var result = (score > status.dealerScore) ? "won" : "loss";

    return (
        <div className="button-row">
            <span className={result}>{result}</span>
            <button className="accept"
                    disabled={verified}
                    onClick={() => validate()}>Ok</button>
        </div>
    );
}
