import React from "react";


export default class FeatureItem extends React.Component {
    render() {
        return (
            <li className={this.props.className}>
                {this.props.children}
            </li>
        )
    }
}
