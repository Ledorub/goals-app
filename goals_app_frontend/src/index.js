import React from 'react'
import ReactDOM from 'react-dom'

import './index.css'
import App from "./App";

const tasks = [
    {
        id: 0,
        todo: 'Wash the dishes.',
        is_achieved: false
    },
    {
        id: 1,
        todo: 'Walk the dog.',
        is_achieved: false
    },
    {
        id: 2,
        todo: 'Clean the house.',
        is_achieved: true
    },
    {
        id: 3,
        todo: 'Read the book.',
        is_achieved: false,
        counter: {
            value: 50,
            target: 116
        }
    }
]

ReactDOM.render(
    <App />,
    document.querySelector('#root')
)
