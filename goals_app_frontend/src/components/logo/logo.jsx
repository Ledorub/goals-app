import React from "react";
import classNames from "classnames";

export default class Logo extends React.Component {
    render() {
        const classes = classNames('logo', this.props.className)
        return <img src={this.props.src} alt="logo" className={classes} />
    }
}