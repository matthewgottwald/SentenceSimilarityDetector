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
        <div className="five wide column"></div>
        <div className="six wide column">
          <div id="title">Document Compare</div>
        </div>
        <div className="five wide column" id="headerButtonsColumn">
          <button
            id="goToUploadPageButton"
            className="ui blue button headerButton"
          >
            Upload Files
          </button>
          <button id="logoutButton" className="ui blue button headerButton">
            Logout
          </button>
        </div>
      </div>
    );
  }
}

export default Header;
