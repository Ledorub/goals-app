import React from "react";


export default class FeatureDescription {
    render() {
        return <p className={this.props.className}>{this.props.children}</p>
    }
}
