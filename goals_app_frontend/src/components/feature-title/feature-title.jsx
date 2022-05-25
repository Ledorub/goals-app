import React from "react";


export default class FeatureTitle extends React.Component {
    render() {
        return <h2 className={this.props.className}>{this.props.children}</h2>
    }
}
