import React from 'react'
import ReactDOM from 'react-dom'
import {BrowserRouter} from 'react-router-dom'

import './index.css'
import Switch from './components/switch/switch'
import TaskList from "./components/task-list/task-list";
import PopUp from "./components/pop-up/pop-up";
import SignUpForm from "./components/sign-up-form/sign-up-form";


class App extends React.Component {

}

class Page extends React.Component {
    render() {
        return (
            <div className="page"></div>
        )
    }
}

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
    <BrowserRouter>
        <PopUp>
            <SignUpForm />
        </PopUp>
    </BrowserRouter>,
    document.querySelector('#root')
)