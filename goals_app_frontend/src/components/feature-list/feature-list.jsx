import React from "react";


export default class FeatureList extends React.Component {
    render() {
        return (
            <ul className={this.props.className}>
                {this.props.children}
            </ul>
        )
    }
}
