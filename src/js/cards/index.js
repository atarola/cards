import React from 'react'
import ReactDOM from 'react-dom'
import { Provider } from 'react-redux'

import { Application } from './components/application';
import { store } from './store'
import './websocket';

ReactDOM.render(
    <Provider store={store}>
        <Application />
    </Provider>,
    document.getElementById('container')
);
