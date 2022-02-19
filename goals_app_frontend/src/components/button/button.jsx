import React from "react";
import classNames from "classnames";
import {callHandlers} from "../../utils";


export default class Button extends React.Component {
    constructor(props) {
        super(props);
        this.handleClick = this.handleClick.bind(this)
    }

    handleClick(event) {
        callHandlers(this.props.onClick, event)
    }

    render() {
        return (
            <button
                type={this.props.type}
                className={classNames(
                    'button button_accented',
                    this.props.className
                )}
                onClick={this.handleClick}>
                {this.props.children}
            </button>
        )
    }
}