import React from "react";


export default class Header {
    render() {
        return <h1 className="header">{this.props.children}</h1>
    }
}
