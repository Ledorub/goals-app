import React from 'react'
import classNames from "classnames";


export default class Switch extends React.Component {
    state = {
        isOn: false
    }

    constructor(props) {
        super(props);

        this.handleClick = this.handleClick.bind(this)
    }

    handleClick() {
        this.setState((state) => ({
            isOn: !state.isOn
        }))
    }

    render() {
        let switchClassNames = classNames(
            'switch',
            {
                'switch-on': this.state.isOn
            }
        )

        return (
            <div className={switchClassNames} onClick={this.handleClick}>
                <div className="switch__options">
                    <SwitchOption name={this.props.leftOption} />
                    <SwitchOption name={this.props.rightOption} />
                </div>
            </div>
        )
    }
}

class SwitchOption extends React.Component {
    render() {
        return <span className="switch__option">{this.props.name}</span>
    }
}