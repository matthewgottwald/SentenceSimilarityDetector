import React, { PureComponent } from "react";

/**
 * Header component
 */
class Header extends PureComponent {
    /**
     * @return {JSX.Element} Header with two non-functional buttons
     */
    render() {
        return (
            <div className="ui grid" id="header">
                <div className="five wide column">
                    <div id="logo-div" className="header-logo">
                        <img 
                            alt="The Co-operators logo"
                            id="header-logo"
                            src="https://www.cooperators.ca/en/-/media/Corporate-Site/Cooperators-logo-blue-2x.png?la=en&hash=0AAA8210FFD40BA8BE6BC2666037F8D0DC3FA899"
                        />
                    </div>
                </div>
                <div className="six wide column">
                    <div id="title">Document Compare</div>
                </div>
                <div className="five wide column" id="headerButtonsColumn">
                    <button id="goToUploadPageButton" className="ui blue button headerButton">Upload Files</button>
                    <button id="logoutButton" className="ui blue button headerButton">Logout</button>
                </div>
            </div>
        )
    }
}

export default Header;
