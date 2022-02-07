import React from "react";
import classNames from "classnames";


export default class ButtonAnchor extends React.Component {
    render() {
        return (
            <a className={classNames("button-anchor", {
                'button-anchor_image': this.props.backgroundImage
            })}
               href=""
               style={{"background-image": `url(${this.props.backgroundImage})`}}>
                {this.props.children}
            </a>
        )
    }
}