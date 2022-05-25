import React from "react";


export default class FeatureDescription extends React.Component {
    render() {
        return <p className={this.props.className}>{this.props.children}</p>
    }
}
