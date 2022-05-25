import React from "react";
import Logo from "../logo/logo";
import classNames from "classnames";

export default class AppHeader extends React.Component {
    render() {
        const actionButton = this.props.actionButton || false
        const hasLogo = !!this.props.logoSrc

        return (
            <header className="app-header">
                {hasLogo &&
                    <div className="app-header__logo-container">
                        <Logo src={this.props.logoSrc} />
                    </div>
                }
                <div className="app-header__actions-container">
                    {actionButton &&
                        React.cloneElement(
                            actionButton,
                            {
                                className: classNames(actionButton.props.className, 'app-header__action-item')
                            }
                        )
                    }
                    {this.props.children &&
                        <nav className="app-header__nav">
                            <ul className="app-header__nav-items">
                                {React.Children.map(
                                    this.props.children,
                                    (child, idx) => {
                                        return (
                                            <li
                                                key={idx}
                                                className="app-header__action-item app-header__nav-item">
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