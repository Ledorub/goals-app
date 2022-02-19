import React from "react";
import classNames from "classnames";
import {NavLink} from "react-router-dom";


export default class ButtonAnchor extends React.Component {
    render() {
        return (
            <NavLink
                to={this.props.href}
                className={classNames(
                    "button-anchor",
                    this.props.className,
                    {
                        'button-anchor_image': this.props.backgroundImage,
                    }
                )}
                style={{backgroundImage: `url(${this.props.backgroundImage})`}}
            >
                {this.props.children}
            </NavLink>
        )
    }
}