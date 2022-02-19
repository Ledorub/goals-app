import React from "react";
import Logo from "../logo/logo";
import classNames from "classnames";

export default class Navbar extends React.Component {
    render() {
        const actionButton = this.props.actionButton || false
        const hasLogo = !!this.props.logoSrc

        return (
            <header className="main-header">
                {hasLogo &&
                    <div className="main-header__logo-container">
                        <Logo src={this.props.logoSrc} />
                    </div>
                }
                <div className="main-header__actions-container">
                    {actionButton &&
                        React.cloneElement(
                            actionButton,
                            {
                                className: classNames(actionButton.props.className, 'main-header__action-item')
                            }
                        )
                    }
                    {this.props.children &&
                        <nav className="main-header__nav">
                            <ul className="main-header__nav-items">
                                {React.Children.map(
                                    this.props.children,
                                    (child, idx) => {
                                        return (
                                            <li
                                                key={idx}
                                                className="main-header__action-item main-header__nav-item">
                                                {child}
                                            </li>
                                        )
                                    }
                                )}
                            </ul>
                        </nav>
                    }
                </div>
            </header>
        )
    }
}